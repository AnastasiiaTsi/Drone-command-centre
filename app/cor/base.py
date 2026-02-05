from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):
    def __init__(self):
        self._next_handler: Optional['Handler'] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request) -> bool:
        pass
    
    def _handle_next(self, request) -> bool:
        if self._next_handler:
            return self._next_handler.handle(request)
        return False