from app.strategy.base import ReactionStrategy
from typing import Dict


class CrackReaction(ReactionStrategy):
    def react(self, mission, reading: Dict):
        if reading.get("terrain_roughness", 0) > 7:
            print("CrackReaction: Rough terrain detected, slowing down")
            mission.speed = max(mission.speed * 0.5, 1.0)