from app.drones.base import Drone
from typing import Dict


class RescueDrone(Drone):
    def get_drone_type(self) -> str:
        return "RescueDrone"
    
    def complete_task(self) -> str:
        return f"Conducted rescue operation at {self.config.get('target_area')}"