from app.strategy.base import ReactionStrategy
from typing import Dict


class WindReaction(ReactionStrategy):
    def react(self, mission, reading: Dict):
        if reading.get("wind_speed", 0) > 15:
            print("WindReaction: High wind detected, adjusting altitude")
            if mission.controller:
                # Використовуємо 2D вектор (x, y) для сумісності з тестами
                mission.controller.adjust_course((0, 10))
                if hasattr(mission, 'altitude'):
                    mission.altitude += 10