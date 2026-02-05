from app.environments.base import Environment
from typing import Dict
import random


class SurfaceEnvironment(Environment):
    def __init__(self, wind_speed: float, visibility: float,
                 terrain_roughness: float, obstacle_density: float) -> None:
        super().__init__(wind_speed=wind_speed, visibility=visibility)
        self.terrain_roughness: float = terrain_roughness
        self.obstacle_density: float = obstacle_density

    def sample(self) -> Dict:
        reading = {
            "wind_speed": self.wind_speed,
            "visibility": self.visibility,
            "terrain_roughness": self.terrain_roughness,
            "obstacle_density": self.obstacle_density,
            "environment_type": "Surface"
        }
        self.readings = reading
        self.notify_subscribers({"type": "surface_reading", "data": reading})
        return reading

    def calc_max_speed(self, speed: float, drone_weight: float) -> float:
        roughness_effect = max(0.3, 1 - self.terrain_roughness * 0.2)
        obstacle_effect = max(0.5, 1 - self.obstacle_density * 0.1)
        return speed * roughness_effect * obstacle_effect

    def get_specific_effects(self) -> Dict:
        return {
            "terrain_difficulty": "High" if self.terrain_roughness > 5 else "Low",
            "obstacle_level": self.obstacle_density,
            "requires_reaction": self.obstacle_density > 7
        }