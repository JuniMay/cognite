from cognite.executor.executor import Executor
from cognite.llms.base import Llm, ChatLlm
from typing import List, Dict, Any, Tuple

class ChatGPT(Executor):
    def __init__(self, llm: ChatLlm) -> None:
        if not isinstance(llm, ChatLlm):
            raise TypeError(f"llm must be ChatLlm, not {type(llm)}")
        super().__init__(llm)
        self.history: List[Tuple[str, str]] = []
        self.system_prompt: str = "You are a artificial intelligence named Cognite. Your job is helping users with their problem."
        
    
    def __call__(self, user_input: str) -> str:
        response = self.llm.chat(self.system_prompt, user_input, self.history)
        self.history.append((user_input, response))
        
        return response
        