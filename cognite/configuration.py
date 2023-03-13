import yaml
import re
from typing import Optional, List, Any, Dict
from queue import Queue
from abc import abstractmethod
from copy import deepcopy


class Variable:
    def __init__(self,
                 name: str,
                 description: str = '',
                 required: bool = False,
                 default: Optional[str] = None):
        """variable in prompt template

        Args:
            name (str): the name of the variable
            description (str, optional): variable decription. Defaults to ''.
            required (bool, optional): whether it's required or not. 
                Defaults to False.
            default (str, optional): if required is False, this is 
                the default value. Defaults to None.
        """
        self.name = name
        self.description = description
        self.required = required
        self.default = default

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class Connection:
    def __init__(self, provider_name: str, kind: str, deps: List[str],
                 to: List[str]) -> None:
        """Connection from provider to prompt variables.
        
        Args:
            provider_name (str): provider name, 
                this is used to lookup a provider.
            kind (str): kind of the connection. `input` if it is 
                transported into a variable; `output` if it 
                receive response and generate contents.
            deps (List[str]): names of variables that the provider depends on.
            to (List[str]): names of variables that 
                the provider will transported to.
             
        """

        #
        self.provider_name = provider_name
        self.kind = kind
        self.deps = deps
        self.to = to

    def __str__(self) -> str:
        return f"{self.provider_name}: {self.kind} {self.deps} -> {self.to}"

class Configuration:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def initialize(self) -> None:
        yaml_file = yaml.load(open(self.file_path, 'r'),
                              Loader=yaml.FullLoader)

        self.name = yaml_file['name'] if 'name' in yaml_file else None
        self.mode = yaml_file['mode']

        self.prompt = yaml_file['prompt']

        self.description = (yaml_file['description']
                            if 'description' in yaml_file else '')
        self.version = yaml_file['version'] if 'version' in yaml_file else None
        self.stop = yaml_file['stop'] if 'stop' in yaml_file else None

        # Variables used to fill the prompt template.
        self.variables = []
        if 'variables' in yaml_file:
            for name, kwargs in yaml_file['variables'].items():
                self.variables.append(Variable(name, **kwargs))

        # variable names are used to verify the prompt template.
        self.variable_names = [v.name for v in self.variables]

        # connections are indexed by provider names
        self.connections: Dict[str, Connection] = {}
        if 'connections' in yaml_file:
            for provider_name, kwargs in yaml_file['connections'].items():
                self.connections[provider_name] = Connection(
                    provider_name, **kwargs)

    def format_prompt(self, **kwargs: Any) -> str:
        """Format the prompt template with variables.
        
        Args:
            **kwargs: variables used to fill the prompt template.
        
        Returns:
            str: formatted prompt.
        """
        return self.prompt.format(**kwargs)

    def verify(self) -> bool:
        """Verify if the configuration if valid
        
        This method checks:
            - if the mode is valid
            - if all the variables are used in the prompt template
            - if every variable have exactly one provider
            - if all the variables have a provider
            - if the dependency graph is a DAG
        
        """

        # TODO: Errors with more information.

        available_modes = ['chat', 'text']

        if self.mode not in available_modes:
            return False

        for variable_name in self.variable_names:
            if f'%{variable_name}%' not in self.prompt:
                return False

        for connection in self.connections.values():
            # connection dependencies should be included in variables.
            for variable_name in connection.deps:
                if (variable_name not in self.variable_names
                        and variable_name != 'response'):
                    return False
            # connection output should be included in variables.
            for variable_name in connection.to:
                if variable_name not in self.variable_names:
                    return False

        # every variable have exactly one provider.
        variable_from = {}
        for connection in self.connections.values():
            for variable_name in connection.to:
                if variable_from.get(variable_name, None) is not None:
                    return False

                variable_from[variable_name] = connection.provider_name

        for variable_name in self.variable_names:
            if variable_from.get(variable_name, None) is None:
                return False

        # index provider name by variable name.
        # records all the provider_name that depends on the variable.
        #
        #                       dep
        #                   +---------> provider_1
        #                   |   dep
        #     variable_1 ---+---------> provider_2
        #                   |   dep
        #                   +---------> provider_3
        #
        # then variable_deps['variable_1'] = [provider_1, provider_2, provider_3]

        self.variable_deps = {}
        for connection in self.connections.values():
            for variable_name in connection.deps:
                if self.variable_deps.get(variable_name, None) is None:
                    self.variable_deps[variable_name] = []

                self.variable_deps[variable_name].append(
                    connection.provider_name)

        # checking DAG

        # get indegree for providers
        # if the dependencie is like:
        #
        #                   to                   dep
        #     provider_1 --------> variable_1 --------> provider_2
        #
        # provider_2 depends on provider_1, indegree of provider_2 increses.
        #
        # Note that there are two connections, so when conn2 is retrieved by
        # the name of provider_2, the name of provider_1 need to be looked up
        # in the `variable_deps` dict.
        #
        #                       to                   dep
        #     +--> provider_1 --------> variable_1 --------> provider_2 ---+
        #     |                                                            |
        #     |          dep                                  to           |
        #     +------------------------ variable_2 <-----------------------+
        #
        # This is not valid because there are cyclic dependencies.

        indegree = {}
        for connection in self.connections.values():
            for variable_name in connection.deps:

                if variable_name == 'response':
                    continue

                provider_name = self.variable_deps[variable_name]
                indegree[provider_name] = indegree.get(provider_name, 0) + 1

        self.indegree = deepcopy(indegree)

        # Topological sort
        # if there's a cycle, the indegree of some provider will never be 0.

        queue = Queue()
        # find all providers with indegree 0
        for provider_name, degree in indegree.items():
            if degree == 0:
                queue.put(provider_name)

        while not queue.empty():
            provider_name = queue.get()
            # get the connection
            connection = self.connections[provider_name]
            for variable_name in connection.to:

                if variable_name == 'response':
                    continue

                for next_provider_name in self.variable_deps[variable_name]:
                    indegree[next_provider_name] -= 1
                    if indegree[next_provider_name] == 0:
                        queue.put(next_provider_name)

        for provider_name, degree in indegree.items():
            if degree != 0:
                return False

        return True


class PromptTemplate:
    def show(self) -> None:
        """show template info
        """
        print(f"Name: {self.name}")
        print(f"Mode: {self.mode}")
        print(f"Description: {self.description}")
        print(f"Author: {self.author}")
        print(f"Version: {self.version}")
        print(f"Stop: {self.stop}")
        print("Variables:")
        for variable in self.variables:
            print(f"\t{variable}")

    def get_prompt(self, **kwargs) -> str:
        """get prompt with variables replaced

        Args:
            **kwargs: variables

        Raises:
            ValueError: invalid variable
        Returns:
            str: prompt
        """
        prompt = self.prompt
        for name, value in kwargs.items():
            if name not in self.variable_names:
                raise ValueError(f"Invalid variable: {name}")
            prompt = prompt.replace(f'%{name}%', value)
        regex = re.compile(r'%\w+%')
        missing_variables = regex.findall(prompt)
        for variable_name in missing_variables:
            variable_name = variable_name[1:-1]
            # TODO: use dict to optimize
            for variable in self.variables:
                if variable.name == variable_name:
                    if variable.default is not None:
                        prompt = prompt.replace(f'%{variable_name}%',
                                                variable.default)
                    else:
                        raise ValueError(f"Missing variable: {variable_name}")
        return prompt.strip()
