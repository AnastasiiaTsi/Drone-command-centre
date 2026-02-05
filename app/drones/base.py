from abc import ABC, abstractmethod
from typing import Any, Dict
from app.engines.base import Engine
from app.bridge.controller import DroneController
from app.strategy.base import ReactionStrategy


class Drone(ABC):
    def __init__(self, name: str, engine: Any, weight: float,
                 config: Dict) -> None:
        self.name: str = name
        self.engine: Engine = engine
        self.weight: float = weight
        self.operational_radius: float = 0.0
        self.environment: Any = None
        self.controller: DroneController = None
        self.strategy: ReactionStrategy = None
        self.altitude: float = 0.0
        self.speed: float = 0.0
        self.status: str = "Idle"
        self.config: Dict = config
        self.mission_data: Dict = {}

    @abstractmethod
    def get_drone_type(self) -> str:
        pass

    @abstractmethod
    def complete_task(self) -> str:
        pass

    def set_controller(self, controller: DroneController):
        self.controller = controller

    def set_strategy(self, strategy: ReactionStrategy):
        self.strategy = strategy

    def execute_mission(self):
        """Template method"""
        self.load_config()
        self.setup_event_subscriptions()
        self.analyze_environment()
        self.preflight_check()
        self.navigate_to_area()
        self.perform_payload_action()
        
        while self.environment_requires_reaction():
            reading = self.environment.sample()
            self.react_to_environment(reading)
        
        self.collect_and_store_data()
        self.return_to_base()
        self.postprocess_results()
        return self.mission_data

    def load_config(self):
        self.mission_data["config_loaded"] = True

    def setup_event_subscriptions(self):
        if self.environment:
            self.environment.subscribe(self.on_environment_event)

    def analyze_environment(self):
        if self.environment:
            self.mission_data["environment_analysis"] = self.environment.get_specific_effects()

    def preflight_check(self):
        self.status = "Preflight"
        self.mission_data["preflight_check"] = "OK"

    def navigate_to_area(self):
        if self.controller:
            self.controller.takeoff()
            target = self.config.get("target_area", (0, 0))
            self.controller.move_to(target)
            self.status = "Navigating"

    def perform_payload_action(self):
        self.status = "Performing Task"
        result = self.complete_task()
        self.mission_data["task_result"] = result

    def environment_requires_reaction(self) -> bool:
        if self.environment:
            effects = self.environment.get_specific_effects()
            return effects.get("requires_reaction", False)
        return False

    def react_to_environment(self, reading: Dict):
        if self.strategy:
            self.strategy.react(self, reading)

    def collect_and_store_data(self):
        self.mission_data["data_collected"] = True

    def return_to_base(self):
        if self.controller:
            base = self.config.get("base_area", (0, 0))
            self.controller.move_to(base)
            self.controller.land()
            self.status = "Returned"

    def postprocess_results(self):
        self.mission_data["postprocessed"] = True
        self.status = "Completed"

    def on_environment_event(self, event):
        self.mission_data.setdefault("events", []).append(event)