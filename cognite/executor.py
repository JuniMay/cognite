from cognite.llms.base import Llm
from cognite import Configuration
from cognite.providers import Provider
from cognite.providers import HistoryProvider
from typing import Dict, Callable, Any
from queue import Queue


class Executor:
    def __init__(self, 
                 llm: Llm, 
                 config_path: str, 
                 providers: Dict[str, Provider],
                 finalizer: Callable[[str], Any]) -> None:

        self.config = Configuration(config_path)
        self.providers = providers

        self.config.initialize()
        self.config.verify()

        self.llm = llm

        self.variable_values = {}

        if not isinstance(self.providers['history'], HistoryProvider):
            raise TypeError('History provider must be of type Provider')

        self.finalizer = finalizer

    def execute(self) -> None:

        queue = Queue()

        for provider_name, degree in self.config.indegree:
            if degree == 0:
                queue.put(provider_name)

        while not queue.empty():
            curr_provider_name = queue.get()

            curr_provider = self.providers[curr_provider_name]

            for variable_name in self.config.connections[
                    curr_provider_name].to:
                self.variable_values[variable_name] = curr_provider.provide(
                    self.variable_values)

                if curr_provider_name == 'user':
                    self.providers['history'].add_user(
                        self.variable_values[variable_name])

                for provider_name in self.config.variable_deps[variable_name]:
                    self.config.indegree[provider_name] -= 1
                    if self.config.indegree[provider_name] == 0:
                        queue.put(provider_name)

        prompt = self.config.format_prompt(self.variable_values)

        if self.config.mode == 'text':
            response = self.llm.complete(prompt)
            self.providers['history'].add_response(response)
            self.finalizer(response)
        else:
            raise NotImplementedError