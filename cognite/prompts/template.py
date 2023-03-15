import yaml
import re

available_modes = ['chat', 'text']

class Variable(object):
    def __init__(self, name: str, description: str = '', required: bool = False, default: str = None):
        """variable in prompt template

        Args:
            name (str): the name of the variable
            description (str, optional): variable decription. Defaults to ''.
            required (bool, optional): whether it's required or not. Defaults to False.
            default (str, optional): if required is False, this is the default value. Defaults to None.
        """
        self.name = name
        self.description = description
    
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

class PromptTemplate(object):
    def __init__(self, file_path: str):
        """read prompt template from file

        Args:
            file_path (str): prompt template file path
        """
        self.file_path = file_path
        self._load_template()
        self._check_valid()
    
    def _load_template(self) -> None:
        """load template from file

        Raises:
            ValueError: mode is not vali
        """
        with open(self.file_path, 'r') as f:
            template = yaml.load(f, Loader=yaml.FullLoader)
        # necessary properties
        self.name = template['name']
        self.mode = template['mode']
        if self.mode not in available_modes:
            raise ValueError(f"Invalid mode: {self.mode}")
        self.prompt = template['prompt']
        
        # optional properties
        self.description = template['description'] if 'description' in template else ''
        self.author = template['author'] if 'author' in template else ''
        self.version = template['version'] if 'version' in template else None
        self.stop = template['stop'] if 'stop' in template else None

        # variables
        self.variables = []
        if 'variables' in template:
            for name, kwargs in template['variables'].items():
                self.variables.append(Variable(name, **kwargs))
        # optimize for get_prompt
        self.variable_names = [variable.name for variable in self.variables]
    
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
    
    def _check_valid(self) -> None:
        """check if the variables and prompt are corresponding

        Raises:
            ValueError: invalid variable or prompt
        """
        # for variable in self.variables:
        #     if not variable.required and not variable.default:
        #         raise ValueError(f"template {self.name} has optinal variable {variable.name} without default value")
        for variable_name in self.variable_names:
            if f'%{variable_name}%' not in self.prompt:
                raise ValueError(f"template {self.name} has variable {variable_name} not in prompt")
        # regex = re.compile(r'%\w+%')
        # for variable_name in regex.findall(self.prompt):
        #     if variable_name[1:-1] not in self.variable_names:
        #         raise ValueError(f"template {self.name} has invalid variable {variable_name} in prompt")
        

    def __call__(self, **kwargs) -> str:
        """get prompt with variables replaced

        Args:
            **kwargs: variables

        Raises:
            ValueError: invalid variable
        Returns:
            str: prompt
        """
        prompt = self.prompt
        for variable in self.variable_names:
            if variable in kwargs:
                prompt = prompt.replace(f'%{variable}%', kwargs[variable])
            else:
                raise ValueError(f"Missing variable: {variable}")
            for name, value in kwargs.items():
                if name not in self.variable_names:
                    # TODO: rewrite this as warning
                    raise ValueError(f"Invalid variable: {name}")
                
        return prompt.strip()

