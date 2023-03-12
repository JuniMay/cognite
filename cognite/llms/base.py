
from abc import abstractmethod
from typing import List, Optional, List, Tuple

class Llm:

    @abstractmethod
    def complete(self, prompt: str) -> str:
        raise NotImplementedError


class ChatLlm:

    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        user_input: str,
        history: Optional[List[Tuple[str, str]]] = None
    ) -> str:
        raise NotImplementedError


class Embedding:

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        raise NotImplementedError