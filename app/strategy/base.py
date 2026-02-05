from abc import ABC, abstractmethod
from typing import Dict


class ReactionStrategy(ABC):
    @abstractmethod
    def react(self, mission, reading: Dict):
        pass