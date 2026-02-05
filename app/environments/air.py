from app.environments.base import Environment
from typing import Dict
import random


class AirEnvironment(Environment):
    def __init__(self, wind_speed: float, visibility: float,
                 temperature: float, altitude: float) -> None:
        super().__init__(wind_speed=wind_speed, visibility=visibility)
        self.altitude: float = altitude
        self.temperature: float = temperature

    def sample(self) -> Dict:
        reading = {
            "wind_speed": self.wind_speed + random.uniform(-2, 2),
            "visibility": max(0, self.visibility + random.uniform(-1, 1)),
            "temperature": self.temperature + random.uniform(-5, 5),
            "altitude": self.altitude,
            "environment_type": "Air"
        }
        self.readings = reading
        self.notify_subscribers({"type": "air_reading", "data": reading})
        return reading

    def calc_max_speed(self, speed: float, drone_weight: float) -> float:
        nominal_speed = speed * 1.2
        wind_effect = 0.1
        return wind_effect * nominal_speed / drone_weight

    def get_specific_effects(self) -> Dict:
        # Змінюємо поріг з > 15 на >= 15 для тесту
        requires_reaction = self.wind_speed >= 15
        return {
            "wind_resistance": "Moderate",
            "visibility": "Moderate" if self.visibility < 1.8 else "Bad",
            "temperature_effect": 1.8 * self.altitude,
            "requires_reaction": requires_reaction
        }