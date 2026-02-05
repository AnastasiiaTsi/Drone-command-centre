from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def start(self) -> bool:
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        pass
    
    @abstractmethod
    def get_power_level(self) -> float:
        pass