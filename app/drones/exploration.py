from app.drones.base import Drone
from typing import Dict, List


class ExplorationDrone(Drone):
    def __init__(self, name: str, engine, weight: float, sensors: str, config: Dict) -> None:
        super().__init__(
            name=name,
            engine=engine,
            weight=weight,
            config=config
        )
        self.sensors: str = sensors
        self.operational_radius = 200
        self.data: List = []

    def get_drone_type(self) -> str:
        return "ExplorationDrone"

    def complete_task(self) -> str:
        env_type = self.environment.__class__.__name__

        exploration_types = {
            "AirEnvironment": [
                "Check Air Conditions",
                "Taking Air Photos",
            ],
            "SeaEnvironment": [
                "Measuring Water Conditions",
            ],
            "SurfaceEnvironment":[
                "Collecting Surface Features",
            ]
        }
        tasks = exploration_types.get(env_type, ["general Exploration"])

        for task in tasks:
            self._collect_data(task)

        return f"Completed {tasks}"

    def _collect_data(self, task: str):
        env_data = {
            "task": task,
            "environment_type": self.environment.__class__.__name__,
            "timestamp": "time",
            "sensors": self.sensors
        }
        self.data.append(env_data)