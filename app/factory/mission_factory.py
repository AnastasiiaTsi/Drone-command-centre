from app.drones.exploration import ExplorationDrone
from app.drones.agriculture import AgricultureDrone
from app.drones.rescue import RescueDrone
from app.environments.air import AirEnvironment
from app.environments.sea import SeaEnvironment
from app.environments.surface import SurfaceEnvironment
from app.bridge.air import AirPlatform
from app.bridge.sea import SeaPlatform
from app.bridge.surface import SurfacePlatform
from app.bridge.controller import DroneController
from app.strategy.wind_reaction import WindReaction
from app.strategy.wave_reaction import WaveReaction
from app.strategy.crack_reaction import CrackReaction
from app.cor.adjust_altitude_handler import AdjustAltitudeHandler
from app.cor.emergency_land_handler import EmergencyLandHandler
from app.engines.electric import ElectricEngine
from app.config.mission_config import MissionConfig

class MissionFactory:
    @staticmethod
    def create_from_config(config: MissionConfig):
        # 1. Створення середовища
        if config.environment_type == "air":
            env = AirEnvironment(wind_speed=config.behavior_params.get("wind_speed", 10.0))
        elif config.environment_type == "sea":
            env = SeaEnvironment(wave_height=config.behavior_params.get("wave_height", 1.0))
        else:
            env = SurfaceEnvironment()
        
        # 2. Створення платформи (Bridge)
        if config.platform_type == "air":
            platform = AirPlatform()
        elif config.platform_type == "sea":
            platform = SeaPlatform()
        else:
            platform = SurfacePlatform()
            
        controller = DroneController(platform)
        
        # 3. Створення дрона
        if config.mission_type == "exploration":
            drone = ExplorationDrone(name=config.mission_id, engine=ElectricEngine(), config={})
        elif config.mission_type == "rescue":
            drone = RescueDrone(name=config.mission_id, engine=ElectricEngine(), config={})
        else:
            drone = AgricultureDrone(name=config.mission_id, engine=ElectricEngine(), config={})
            
        drone.environment = env
        drone.set_controller(controller)
        
        # 4. Вибір стратегії
        strategy = WindReaction() if config.environment_type == "air" else WaveReaction()
        drone.set_strategy(strategy)
        
        # 5. Ланцюжок відповідальності (CoR)
        cor = AdjustAltitudeHandler()
        cor.set_next(EmergencyLandHandler())
        
        return drone, env, controller, strategy, cor