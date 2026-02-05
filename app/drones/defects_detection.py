from app.drones.base import Drone
from typing import Dict


class DefectsDetectionDrone(Drone):
    def __init__(self, name: str, engine, weight: float, config: Dict) -> None:
        super().__init__(name, engine, weight, config)
        self.detected_defects = []
    
    def get_drone_type(self) -> str:
        return "DefectsDetectionDrone"
    
    def complete_task(self) -> str:
        defects = ["crack", "corrosion", "deformation"]
        detected = [d for d in defects if hash(self.name + d) % 2 == 0]
        self.detected_defects = detected
        return f"Detected defects: {detected}"