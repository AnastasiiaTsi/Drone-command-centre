import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from app.factory.mission_factory import MissionFactory
from app.config.mission_config import MissionConfig


class TestFactoryPattern(unittest.TestCase):
    def test_create_air_exploration(self):
        """Test factory creates air exploration mission"""
        config = MissionConfig(
            mission_id="test_factory_001",
            mission_type="exploration",
            environment_type="air",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 5.0, "sensors": "standard"}
        )
        
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        # Verify correct types created
        self.assertEqual(drone.__class__.__name__, "ExplorationDrone")
        self.assertEqual(environment.__class__.__name__, "AirEnvironment")
        self.assertEqual(controller.__class__.__name__, "DroneController")
        self.assertEqual(strategy.__class__.__name__, "WindReaction")
        
        # Verify platform
        self.assertEqual(controller._implementor.__class__.__name__, "AirPlatform")

    def test_create_sea_rescue(self):
        """Test factory creates sea rescue mission"""
        config = MissionConfig(
            mission_id="test_factory_002",
            mission_type="rescue",
            environment_type="sea",
            platform_type="sea",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 10.0}
        )
        
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        self.assertEqual(drone.__class__.__name__, "RescueDrone")
        self.assertEqual(environment.__class__.__name__, "SeaEnvironment")
        self.assertEqual(strategy.__class__.__name__, "WaveReaction")
        self.assertEqual(controller._implementor.__class__.__name__, "SeaPlatform")

    def test_create_surface_agriculture(self):
        """Test factory creates surface agriculture mission"""
        config = MissionConfig(
            mission_id="test_factory_003",
            mission_type="agriculture",
            environment_type="surface",
            platform_type="surface",
            mode="swarm",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 8.0}
        )
        
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        self.assertEqual(drone.__class__.__name__, "AgricultureDrone")
        self.assertEqual(environment.__class__.__name__, "SurfaceEnvironment")
        self.assertEqual(strategy.__class__.__name__, "CrackReaction")
        self.assertEqual(controller._implementor.__class__.__name__, "SurfacePlatform")

    def test_invalid_mission_type(self):
        """Test factory handles invalid mission type"""
        config = MissionConfig(
            mission_id="test_factory_004",
            mission_type="invalid_type",
            environment_type="air",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 5.0}
        )
        
        with self.assertRaises(ValueError):
            MissionFactory.create_from_config(config)

    def test_invalid_environment_type(self):
        """Test factory handles invalid environment type"""
        config = MissionConfig(
            mission_id="test_factory_005",
            mission_type="exploration",
            environment_type="invalid_env",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 5.0}
        )
        
        with self.assertRaises(ValueError):
            MissionFactory.create_from_config(config)


if __name__ == '__main__':
    unittest.main()