from cognite.providers import Provider
from typing import Any

class HistoryProvider(Provider):
    def __init__(self) -> None:
        super().__init__()
        
        self.history = []
        
    def get_name(self) -> str:
        return 'history'
    
    def provide(self, **kwargs: Any) -> str:
        result = ""
        for key, value in kwargs.items():
            result += f"{key}: {value}"
            
        return result
    
    def add_user(self, user: str) -> None:
        # user goes first
        self.history.append({})
        # TODO: Mutable length of history.
        if len(self.history) > 10:
            self.history.pop(0)
        
        self.history[-1]['user'] = user
        
    def add_response(self, response: str) -> None:
        # response goes second
        self.history[-1]['response'] = response
        
        
        
        

            