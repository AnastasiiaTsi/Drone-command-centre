from abc import ABC, abstractmethod
from typing import Dict, List, Callable


class Environment(ABC):
    def __init__(self, wind_speed: float = 0.0, visibility: float = 10.0) -> None:
        self.wind_speed: float = wind_speed
        self.visibility: float = visibility
        self.subscribers: List[Callable] = []
        self.readings: Dict = {}

    @abstractmethod
    def sample(self) -> Dict:
        pass

    @abstractmethod
    def calc_max_speed(self, speed: float, drone_weight: float) -> float:
        pass

    @abstractmethod
    def get_specific_effects(self) -> Dict:
        pass

    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)

    def notify_subscribers(self, event: Dict):
        for subscriber in self.subscribers:
            subscriber(event)

    def start(self):
        pass