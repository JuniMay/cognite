from cognite.executor import Executor
from cognite.llms.base import Llm
from cognite.prompts.template import PromptTemplate
from typing import List, Dict, Any

class Chat(Executor):
    def __init__(self, llm: Llm, max_history: int = 5) -> None:
        super().__init__(llm)
        self.chat_gpt3 = PromptTemplate('prompts/chat_gpt3.yaml')
        self.history = []
        self.max_history = max_history
    
    def __call__(self, user_input: str) -> str:
        history_str = ''
        for usr, rply in self.history:
            history_str += f'User: {usr}\nCognite: {rply}\n'
        prompt = self.chat_gpt3(history=history_str, input=user_input)
        response = self.llm.complete(prompt)
        self.history.append((user_input, response))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        return response