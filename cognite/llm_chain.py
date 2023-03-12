from cognite.llms.base import Llm
from cognite.generator import Generator
from typing import List, Dict
from rich.console import Console
from rich.markdown import Markdown


class PromptTemplate:

    def __init__(self, template: str, variables: List[str]) -> None:
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)


class LlmChain:

    def __init__(self,
                 model: Llm,
                 prompt_template: PromptTemplate,
                 streaming: bool = True,
                 generators: List[Generator] = []) -> None:

        self.model = model
        self.prompt_template = prompt_template
        self.streaming = streaming
        # history will record the prompt arguments in the dict
        self.history: List[Dict[str, str]] = []
        # current entry will be append to history and reset
        # after the response is received
        self.current_history_entry: Dict[str, str] = {}

        self.generators = generators

    def format_prompt(self, **kwargs) -> str:
        self.current_history_entry = kwargs

        if 'user_input' not in kwargs:
            raise ValueError("user_input must be provided")

        if 'history' in self.prompt_template.variables:
            history = "====="
            for entry in self.history:
                for field, content in entry.items():
                    history += f"{field}: {content}"

                history += "====="

            kwargs['history'] = history

        # print(kwargs)

        return self.prompt_template.format(**kwargs)

    def interact(self, user_input, **kwargs) -> str:
        kwargs['user_input'] = user_input
        prompt = self.format_prompt(**kwargs)

        response = self.model.complete(prompt)

        self.current_history_entry['response'] = response
        self.history.append(self.current_history_entry)
        
        if len(self.history) >= 10:
            self.history.pop(0)
        
        self.current_history_entry = {}

        for generator in self.generators:
            _ = generator.generate(response)

        return response


class Repl:

    def __init__(self, llm_chain: LlmChain) -> None:
        self.llm_chain = llm_chain
        self.console = Console()
        self.incremental_text = ""

        self.llm_chain.model.manager = self.markdown_manager

    def markdown_manager(self, text: str) -> None:
        # self.console.print(text, end="")
        pass

    def run(self) -> None:
        while True:
            kwargs = {}

            for variable in self.llm_chain.prompt_template.variables:
                if variable == 'history':
                    continue
                kwargs[variable] = input(f"{variable}: ")
                response = self.llm_chain.interact(**kwargs)
                self.console.print(Markdown(response))
