import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from app.factory.mission_factory import MissionFactory
from app.config.mission_config import MissionConfig


class TestEndToEndMission(unittest.TestCase):
    def test_exploration_mission_air(self):
        """Test complete exploration mission in air environment"""
        print("\n=== Testing Air Exploration Mission ===")
        
        config = MissionConfig(
            mission_id="test_exp_air_001",
            mission_type="exploration",
            environment_type="air",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={"wind_speed": 20},
            behavior_params={
                "wind_speed": 12.0,
                "visibility": 10.0,
                "temperature": 25.0,
                "altitude": 150.0,
                "weight": 5.0,
                "sensors": "multispectral"
            }
        )
        
        # Create mission
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        # Verify components created
        self.assertIsNotNone(drone)
        self.assertIsNotNone(environment)
        self.assertIsNotNone(controller)
        self.assertIsNotNone(strategy)
        self.assertIsNotNone(cor_chain)
        
        # Execute mission
        result = drone.execute_mission()
        
        # Verify results
        self.assertEqual(drone.status, "Completed")
        self.assertEqual(drone.get_drone_type(), "ExplorationDrone")
        self.assertIn("task_result", result)
        self.assertIn("Check Air Conditions", result["task_result"])
        
        print(f"✓ Mission completed: {drone.status}")
        print(f"✓ Drone type: {drone.get_drone_type()}")
        print(f"✓ Environment: {environment.__class__.__name__}")
        
        return True

    def test_agriculture_mission_surface(self):
        """Test agriculture mission on surface"""
        print("\n=== Testing Surface Agriculture Mission ===")
        
        config = MissionConfig(
            mission_id="test_agri_surface_001",
            mission_type="agriculture",
            environment_type="surface",
            platform_type="surface",
            mode="swarm",
            target_area=(200.0, 300.0),
            base_area=(0.0, 0.0),
            thresholds={"terrain_roughness": 8},
            behavior_params={
                "wind_speed": 5.0,
                "visibility": 15.0,
                "terrain_roughness": 3.0,
                "obstacle_density": 2.0,
                "weight": 8.0
            }
        )
        
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        result = drone.execute_mission()
        
        self.assertEqual(drone.status, "Completed")
        self.assertEqual(drone.get_drone_type(), "AgricultureDrone")
        self.assertIn("Sprayed pesticides", result["task_result"])
        
        print(f"✓ Mission completed: {drone.status}")
        print(f"✓ Task: {result['task_result']}")
        
        return True

    def test_rescue_mission_sea(self):
        """Test rescue mission at sea"""
        print("\n=== Testing Sea Rescue Mission ===")
        
        config = MissionConfig(
            mission_id="test_rescue_sea_001",
            mission_type="rescue",
            environment_type="sea",
            platform_type="sea",
            mode="single",
            target_area=(50.0, 75.0),
            base_area=(10.0, 10.0),
            thresholds={"wave_height": 4},
            behavior_params={
                "wind_speed": 8.0,
                "visibility": 5.0,
                "wave_height": 2.5,
                "current_speed": 1.2,
                "weight": 10.0
            }
        )
        
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        result = drone.execute_mission()
        
        self.assertEqual(drone.status, "Completed")
        self.assertEqual(drone.get_drone_type(), "RescueDrone")
        self.assertIn("rescue operation", result["task_result"].lower())
        
        print(f"✓ Mission completed: {drone.status}")
        print(f"✓ Platform: {controller._implementor.__class__.__name__}")
        
        return True

    def test_cor_chain_functionality(self):
        """Test Chain of Responsibility in mission"""
        print("\n=== Testing CoR Chain ===")
        
        config = MissionConfig(
            mission_id="test_cor_001",
            mission_type="exploration",
            environment_type="air",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={"weight": 5.0}
        )
        
        _, _, _, _, cor_chain = MissionFactory.create_from_config(config)
        
        # Test different events
        events = [
            {"type": "obstacle_detected"},
            {"type": "low_visibility"},
            {"type": "critical_failure"},
            {"type": "unknown_event"}  # Should not be handled
        ]
        
        for event in events:
            result = cor_chain.handle(event)
            if event["type"] != "unknown_event":
                self.assertTrue(result, f"Event {event['type']} should be handled")
            else:
                self.assertFalse(result, "Unknown event should not be handled")
        
        print("✓ All CoR handlers working correctly")
        
        return True

    def test_strategy_activation(self):
        """Test that strategies activate based on environment"""
        print("\n=== Testing Strategy Activation ===")
        
        # Test with high wind (should trigger strategy)
        config = MissionConfig(
            mission_id="test_strategy_001",
            mission_type="exploration",
            environment_type="air",
            platform_type="air",
            mode="single",
            target_area=(100.0, 200.0),
            base_area=(0.0, 0.0),
            thresholds={},
            behavior_params={
                "wind_speed": 18.0,  # High wind
                "visibility": 10.0,
                "temperature": 20.0,
                "altitude": 150.0,
                "weight": 5.0
            }
        )
        
        drone, environment, controller, strategy, _ = MissionFactory.create_from_config(config)
        
        # Verify correct strategy created
        self.assertEqual(strategy.__class__.__name__, "WindReaction")
        
        print(f"✓ Strategy created: {strategy.__class__.__name__}")
        print(f"✓ Wind speed: {environment.wind_speed} (should trigger reaction if > 15)")
        
        return True


def run_all_integration_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("RUNNING INTEGRATION TESTS")
    print("=" * 60)
    
    test_cases = [
        ("Air Exploration", TestEndToEndMission().test_exploration_mission_air),
        ("Surface Agriculture", TestEndToEndMission().test_agriculture_mission_surface),
        ("Sea Rescue", TestEndToEndMission().test_rescue_mission_sea),
        ("CoR Chain", TestEndToEndMission().test_cor_chain_functionality),
        ("Strategy Activation", TestEndToEndMission().test_strategy_activation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in test_cases:
        try:
            if test_func():
                print(f"\n✓ {test_name}: PASSED\n")
                passed += 1
            else:
                print(f"\n✗ {test_name}: FAILED\n")
                failed += 1
        except Exception as e:
            print(f"\n✗ {test_name}: ERROR - {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    # Run as unittest
    unittest.main()
    
    # Or run integration tests manually
    # run_all_integration_tests()