from abc import abstractmethod
from typing import Any

class Provider:
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def provide(self, **kwargs: Any) -> Any:
        raise NotImplementedError
