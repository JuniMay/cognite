
from abc import abstractmethod
from typing import Any 

class Generator:
    
    @abstractmethod
    def generate(self, text: str) -> Any:
        raise NotImplementedError