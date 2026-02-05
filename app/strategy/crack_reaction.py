from app.strategy.base import ReactionStrategy
from typing import Dict

class CrackReactionStrategy(ReactionStrategy):
    def react(self, mission, reading: Dict):
        if reading.get("crack_detected", False):
            print("CrackReaction: Surface defect found! Initiating detailed scan...")
            if mission.controller:
                mission.controller.hold()