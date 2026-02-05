# --- ІМПОРТИ ДРОНІВ (Додано MilitaryDrone) ---
from app.drones.military import MilitaryDrone  # <--- ОЬ ТУТ БУЛО ПРОПУЩЕНО
from app.drones.exploration import ExplorationDrone
from app.drones.agriculture import AgricultureDrone
from app.drones.rescue import RescueDrone
from app.drones.pollution_monitoring import PollutionMonitoringDrone
from app.drones.defects_detection import DefectsDetectionDrone

# --- ІМПОРТИ СЕРЕДОВИЩ ---
from app.environments.air import AirEnvironment
from app.environments.sea import SeaEnvironment
from app.environments.surface import SurfaceEnvironment

# --- ІМПОРТИ BRIDGE ---
from app.bridge.controller import DroneController
from app.bridge.air import AirPlatform
from app.bridge.sea import SeaPlatform
from app.bridge.surface import SurfacePlatform

# --- ІМПОРТИ STRATEGY ---
from app.strategy.wind_reaction import WindReactionStrategy
from app.strategy.wave_reaction import WaveReactionStrategy
from app.strategy.crack_reaction import CrackReactionStrategy

# --- ІМПОРТИ CoR ---
from app.cor.adjust_altitude_handler import AdjustAltitudeHandler
from app.cor.reroute_handler import RerouteHandler
from app.cor.emergency_land_handler import EmergencyLandHandler

# --- ІНШЕ ---
from app.engines.electric import ElectricEngine
from app.config.mission_config import MissionConfig

class MissionFactory:
    @staticmethod
    def create_from_config(config: MissionConfig):
        # --- 1. СТВОРЕННЯ СЕРЕДОВИЩА ---
        if config.environment_type == "air":
            env = AirEnvironment(
                visibility=10000.0,
                temperature=20.0,
                altitude=150.0,
                wind_speed=config.behavior_params.get("wind_speed", 5.0)
            )
        elif config.environment_type == "sea":
            env = SeaEnvironment(
                wave_height=config.behavior_params.get("wave_height", 0.5),
                current_speed=2.0 
            )
        else:
            env = SurfaceEnvironment(
                roughness=config.behavior_params.get("roughness", 0.1)
            )

        # --- 2. СТВОРЕННЯ ПЛАТФОРМИ ---
        if config.platform_type == "air":
            platform = AirPlatform()  # ✅ Виправлено
        elif config.platform_type == "sea":
            platform = SeaPlatform(protocol="NMEA-0183")
        else:
            platform = SurfacePlatform(wheels_type="offroad")

        # --- 3. КОНТРОЛЕР ---
        controller = DroneController(platform)

        # --- 4. СТВОРЕННЯ ДРОНА ---
        # Створюємо спільний двигун для прикладу
        engine = ElectricEngine()
        name = config.mission_id
        # Отримуємо вагу з конфігу або беремо дефолтну
        weight = config.behavior_params.get("weight", 10.0) 
        drone_config = {} # Можна передати додаткові параметри

        if config.mission_type == "military":
            # ВИПРАВЛЕНО: Передаємо правильні аргументи в конструктор
            drone = MilitaryDrone(name, engine, weight, drone_config)
        elif config.mission_type == "agriculture":
            drone = AgricultureDrone(name, engine, weight, drone_config)
        elif config.mission_type == "rescue":
            drone = RescueDrone(name, engine, weight, drone_config)
        elif config.mission_type == "pollution_monitoring":
            drone = PollutionMonitoringDrone(name, engine, weight, drone_config)
        elif config.mission_type == "exploration":
            drone = ExplorationDrone(name, engine, weight, drone_config)
        elif config.mission_type == "defects_detection":
            drone = DefectsDetectionDrone(name, engine, weight, drone_config)
        else:
            drone = ExplorationDrone(name, engine, weight, drone_config)

        # Прив'язуємо середовище та контролер
        drone.environment = env
        drone.set_controller(controller)

        # --- 5. СТРАТЕГІЯ ---
        if config.environment_type == "air":
            strategy = WindReactionStrategy()
        elif config.environment_type == "sea":
            strategy = WaveReactionStrategy()
        else:
            strategy = CrackReactionStrategy()
            
        drone.set_strategy(strategy)

        # --- 6. ЛАНЦЮЖОК ВІДПОВІДАЛЬНОСТІ ---
        h1 = AdjustAltitudeHandler()
        h2 = RerouteHandler()
        h3 = EmergencyLandHandler()

        h1.set_next(h2).set_next(h3)
        
        return drone, env, controller, strategy, h1