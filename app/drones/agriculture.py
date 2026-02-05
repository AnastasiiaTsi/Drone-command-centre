from app.drones.base import Drone
from typing import Dict


class AgricultureDrone(Drone):
    def get_drone_type(self) -> str:
        return "AgricultureDrone"
    
    def complete_task(self) -> str:
        return f"Sprayed pesticides over area {self.config.get('target_area')}"