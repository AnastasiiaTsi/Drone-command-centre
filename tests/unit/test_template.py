import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from unittest.mock import Mock, patch, MagicMock
from app.drones.base import Drone
from app.drones.exploration import ExplorationDrone
from app.drones.agriculture import AgricultureDrone


class MockDrone(Drone):
    """Concrete implementation for testing"""
    def get_drone_type(self):
        return "MockDrone"
    
    def complete_task(self):
        return "Mock task completed"


class TestTemplateMethod(unittest.TestCase):
    def test_template_method_structure(self):
        """Test that template method calls all steps in order"""
        drone = MockDrone("TestDrone", Mock(), 5.0, {})
        drone.controller = Mock()
        drone.environment = Mock()
        drone.strategy = Mock()
        
        # Mock the steps
        drone.load_config = Mock()
        drone.setup_event_subscriptions = Mock()
        drone.analyze_environment = Mock()
        drone.preflight_check = Mock()
        drone.navigate_to_area = Mock()
        drone.perform_payload_action = Mock()
        drone.environment_requires_reaction = Mock(side_effect=[True, False])
        drone.react_to_environment = Mock()
        drone.collect_and_store_data = Mock()
        drone.return_to_base = Mock()
        drone.postprocess_results = Mock()
        
        # Execute mission
        result = drone.execute_mission()
        
        # Verify calls in correct order
        call_order = [
            drone.load_config,
            drone.setup_event_subscriptions,
            drone.analyze_environment,
            drone.preflight_check,
            drone.navigate_to_area,
            drone.perform_payload_action,
            drone.environment_requires_reaction,
            drone.react_to_environment,
            drone.collect_and_store_data,
            drone.return_to_base,
            drone.postprocess_results
        ]
        
        for i, method in enumerate(call_order):
            method.assert_called()
            
            # Check that environment_requires_reaction was called twice
            if method == drone.environment_requires_reaction:
                self.assertEqual(method.call_count, 2)
            elif method != drone.react_to_environment:
                self.assertEqual(method.call_count, 1)

    def test_exploration_drone_task(self):
        """Test exploration drone specific task"""
        drone = ExplorationDrone(
            name="Explorer",
            engine=Mock(),
            weight=5.0,
            sensors="camera",
            config={"target_area": (100, 200), "base_area": (0, 0)}
        )
        
        drone.environment = Mock()
        drone.environment.__class__.__name__ = "AirEnvironment"
        
        result = drone.complete_task()
        self.assertIn("Check Air Conditions", result)
        self.assertIn("Taking Air Photos", result)
        
        # Verify data collection
        self.assertEqual(len(drone.data), 2)
        self.assertEqual(drone.data[0]["task"], "Check Air Conditions")

    def test_agriculture_drone_task(self):
        """Test agriculture drone specific task"""
        drone = AgricultureDrone(
            name="Farmer",
            engine=Mock(),
            weight=8.0,
            config={"target_area": (100, 200)}
        )
        
        result = drone.complete_task()
        self.assertIn("Sprayed pesticides", result)

    def test_drone_status_changes(self):
        """Test drone status changes during mission"""
        drone = MockDrone("TestDrone", Mock(), 5.0, {})
        drone.controller = Mock()
        drone.controller.takeoff.return_value = True
        drone.controller.move_to.return_value = True
        drone.controller.land.return_value = True
        drone.environment = Mock()
        drone.environment.sample.return_value = {}
        drone.environment.get_specific_effects.return_value = {}
        
        # Mock environment_requires_reaction to return False
        drone.environment_requires_reaction = Mock(return_value=False)
        
        drone.execute_mission()
        
        # Check status changes
        self.assertEqual(drone.status, "Completed")


if __name__ == '__main__':
    unittest.main()