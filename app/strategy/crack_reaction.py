from app.strategy.base import ReactionStrategy
from typing import Dict

class CrackReactionStrategy(ReactionStrategy):
    def react(self, mission, reading: Dict):
        # Реагуємо, якщо виявлено тріщину або дефект
        if reading.get("crack_detected", False):
            print("CrackReaction: Surface defect found! Initiating detailed scan...")
            if mission.controller:
                # Зупиняємось для детального аналізу
                mission.controller.hold()
                # Тут можна додати логіку фотографування або маркування