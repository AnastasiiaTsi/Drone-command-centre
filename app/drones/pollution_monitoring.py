from app.drones.base import Drone
from typing import Dict


class PollutionMonitoringDrone(Drone):  
    def __init__(self, name: str, engine, weight: float, config: Dict) -> None:
        super().__init__(name, engine, weight, config)
        self.pollution_data = []
    
    def get_drone_type(self) -> str:
        return "PollutionMonitoringDrone"
    
    def complete_task(self) -> str:
        # Симулюємо збір даних про забруднення
        pollution_levels = {
            "air_quality": 65,  # у відсотках
            "water_quality": 78,
            "soil_contamination": 42,
            "noise_level": 55
        }
        self.pollution_data.append(pollution_levels)
        
        # Аналізуємо рівні
        status = "good"
        if pollution_levels["air_quality"] < 50 or pollution_levels["water_quality"] < 60:
            status = "poor"
        elif pollution_levels["soil_contamination"] > 70:
            status = "critical"
        
        return f"Pollution levels: {pollution_levels}, Status: {status}"
    
    def get_pollution_summary(self) -> Dict:
        if not self.pollution_data:
            return {}
        
        summary = {}
        for key in self.pollution_data[0].keys():
            values = [data[key] for data in self.pollution_data if key in data]
            if values:
                summary[key] = sum(values) / len(values)
        
        return summary