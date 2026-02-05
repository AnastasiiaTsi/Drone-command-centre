from app.strategy.base import ReactionStrategy
from typing import Dict

class WaveReactionStrategy(ReactionStrategy):
    def react(self, mission, reading: Dict):
        if reading.get("wave_height", 0) > 2.0:
            print("WaveReaction: High waves detected, stabilizing...")
            if mission.controller:
                mission.controller.adjust_course((1, 1))