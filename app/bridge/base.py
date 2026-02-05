from abc import ABC, abstractmethod
from typing import Tuple


class MovementImplementor(ABC):
    @abstractmethod
    def takeoff(self) -> bool:
        pass
    
    @abstractmethod
    def land(self) -> bool:
        pass
    
    @abstractmethod
    def move_to(self, coord: Tuple[float, float]) -> bool:
        pass
    
    @abstractmethod
    def adjust_course(self, vector: Tuple[float, float]) -> bool:
        pass
    
    @abstractmethod
    def hold_position(self) -> bool:
        pass
    
    @abstractmethod
    def set_mode(self, mode: str) -> bool:
        pass
    
    @abstractmethod
    def broadcast(self, message: str) -> bool:
        pass