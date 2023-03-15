from cognite.llms.base import Llm
from cognite.prompts.template import PromptTemplate
from typing import List, Dict, Any


class Executor:
    def __init__(self, llm: Llm, prompt_templates: List[PromptTemplate] = None) -> None:
        self.llm: Llm = llm
        if prompt_templates:
            self.prompt_templates: Dict[str, PromptTemplate] = {prompt.name: prompt for prompt in prompt_templates}
        
    # def __getattribute__(self, __name: str) -> PromptTemplate:
    #     if __name == 'prompt_templates':
    #         return 
    #     if __name in self.prompt_templates.keys():
    #         return self.prompt_templates[__name]
    #     else:
    #         raise AttributeError(f"Executor has no promt nemed {__name}")         
    
    def registered_prompts(self) -> List[PromptTemplate]:
        return self.prompt_templates

    def register_prompt(self, prompt_templates: List[PromptTemplate]) -> None:
        if prompt_templates.isinstance(PromptTemplate):
            if prompt_templates.name in self.prompt_templates.keys():
                raise ValueError(f"Prompt {prompt_templates.name} already registered")
            self.prompt_templates[prompt_templates.name] = prompt_templates
        elif prompt_templates.isinstance(List):
            for prompt in prompt_templates:
                self.register_prompt(prompt)
        else:
            raise TypeError(f"prompt_templates must be PromptTemplate or List[PromptTemplate], not {type(prompt_templates)}")       
    
    def __str__(self) -> str:
        hint = f"Executor with {len(self.prompt_templates)} prompts"
        hint += "\n".join([f"\t{prompt}" for prompt in self.prompt_templates.keys()])
        return hint
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __call__(self, prompt_name: str, **kwargs: Any) -> str:
        raise NotImplementedError
    
    