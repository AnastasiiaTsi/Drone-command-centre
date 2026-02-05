from app.drones.base import Drone
from typing import Dict


class MilitaryDrone(Drone):
    def __init__(self, name: str, engine, weight: float, config: Dict) -> None:
        super().__init__(name, engine, weight, config)
        self.weapons_systems = config.get("weapons", ["standard"])
        self.stealth_mode = False
    
    def get_drone_type(self) -> str:
        return "MilitaryDrone"
    
    def complete_task(self) -> str:
        task_type = self.config.get("mission_type", "surveillance")
        
        if task_type == "surveillance":
            return f"Conducted surveillance at {self.config.get('target_area')}"
        elif task_type == "strike":
            return f"Executed precision strike at {self.config.get('target_area')}"
        elif task_type == "reconnaissance":
            return f"Completed reconnaissance mission over {self.config.get('target_area')}"
        else:
            return f"Performed military operation at {self.config.get('target_area')}"
    
    def activate_stealth_mode(self):
        self.stealth_mode = True
        print("MilitaryDrone: Stealth mode activated")
    
    def deactivate_stealth_mode(self):
        self.stealth_mode = False
        print("MilitaryDrone: Stealth mode deactivated")
    
    def perform_payload_action(self):
        """Override for military-specific actions"""
        if self.config.get("require_stealth", False):
            self.activate_stealth_mode()
        
        self.status = "Performing Military Task"
        result = self.complete_task()
        self.mission_data["task_result"] = result
        self.mission_data["stealth_mode"] = self.stealth_mode
        self.mission_data["weapons_used"] = self.weapons_systems
        
        if self.stealth_mode:
            self.deactivate_stealth_mode()