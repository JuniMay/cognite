from cognite.executor.executor import Executor
from cognite.llms.base import Llm
from cognite.prompts.template import PromptTemplate
from typing import List, Dict, Any

class Emotion(Executor):
    def __init__(self, llm: Llm) -> None:
        super().__init__(llm)
        self.emotion = PromptTemplate('prompts/emotion.yaml')
    
    def __call__(self, user_input: str) -> str:
        prompt = self.emotion(input=user_input)
        answer = self.llm.complete(prompt)
        try:
            answer = int(answer)
        except ValueError:
            answer = -1
        return answer