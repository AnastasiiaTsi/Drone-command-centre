from app.strategy.base import ReactionStrategy
from typing import Dict


class WaveReaction(ReactionStrategy):
    def react(self, mission, reading: Dict):
        if reading.get("wave_height", 0) > 3:
            print("WaveReaction: High waves detected, moving to safer area")
            if mission.controller:
                mission.controller.adjust_course((5, 0))  # 2D вектор