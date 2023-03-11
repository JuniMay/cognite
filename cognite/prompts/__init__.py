from typing import List


class PromptTemplate:

    def __init__(self, template: str, variables: List[str]) -> None:
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)
