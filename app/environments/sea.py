from app.environments.base import Environment
from typing import Dict
import random


class SeaEnvironment(Environment):
    def __init__(self, wind_speed: float, visibility: float,
                 wave_height: float, current_speed: float) -> None:
        super().__init__(wind_speed=wind_speed, visibility=visibility)
        self.wave_height: float = wave_height
        self.current_speed: float = current_speed

    def sample(self) -> Dict:
        reading = {
            "wind_speed": self.wind_speed,
            "visibility": self.visibility,
            "wave_height": self.wave_height + random.uniform(-0.5, 0.5),
            "current_speed": self.current_speed + random.uniform(-0.2, 0.2),
            "environment_type": "Sea"
        }
        self.readings = reading
        self.notify_subscribers({"type": "sea_reading", "data": reading})
        return reading

    def calc_max_speed(self, speed: float, drone_weight: float) -> float:
        wave_effect = max(0.1, 1 - self.wave_height * 0.1)
        current_effect = 1 - self.current_speed * 0.05
        return speed * wave_effect * current_effect

    def get_specific_effects(self) -> Dict:
        return {
            "wave_effect": "High" if self.wave_height > 2 else "Low",
            "current_effect": self.current_speed * 0.5,
            "requires_reaction": self.wave_height > 3 or self.current_speed > 2
        }