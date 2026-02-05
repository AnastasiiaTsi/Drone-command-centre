import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from unittest.mock import Mock, patch
from app.strategy.wind_reaction import WindReaction
from app.strategy.wave_reaction import WaveReaction
from app.strategy.crack_reaction import CrackReaction


class TestStrategyPattern(unittest.TestCase):
    def test_wind_reaction_high_wind(self):
        """Test wind reaction for high wind conditions"""
        strategy = WindReaction()
        mission = Mock()
        mission.controller = Mock()
        mission.controller.adjust_course.return_value = True
        mission.altitude = 100
        
        reading = {"wind_speed": 20}  # High wind
        
        with patch('builtins.print') as mock_print:
            strategy.react(mission, reading)
            
            mock_print.assert_called_with("WindReaction: High wind detected, adjusting altitude")
            # Тепер очікуємо (0, 10)
            mission.controller.adjust_course.assert_called_with((0, 10))
            self.assertEqual(mission.altitude, 110)

    def test_wind_reaction_low_wind(self):
        """Test wind reaction doesn't trigger for low wind"""
        strategy = WindReaction()
        mission = Mock()
        mission.controller = Mock()
        
        reading = {"wind_speed": 5}  # Low wind
        
        with patch('builtins.print') as mock_print:
            strategy.react(mission, reading)
            
            # Should not call adjust_course
            mission.controller.adjust_course.assert_not_called()
            mock_print.assert_not_called()

    def test_wave_reaction_high_waves(self):
        """Test wave reaction for high waves"""
        strategy = WaveReaction()
        mission = Mock()
        mission.controller = Mock()
        mission.controller.adjust_course.return_value = True
        
        reading = {"wave_height": 4}  # High waves
        
        with patch('builtins.print') as mock_print:
            strategy.react(mission, reading)
            
            mock_print.assert_called_with("WaveReaction: High waves detected, moving to safer area")
            mission.controller.adjust_course.assert_called_with((5, 0))

    def test_crack_reaction_rough_terrain(self):
        """Test crack reaction for rough terrain"""
        strategy = CrackReaction()
        mission = Mock()
        mission.speed = 10.0
        
        reading = {"terrain_roughness": 8}  # Rough terrain
        
        with patch('builtins.print') as mock_print:
            strategy.react(mission, reading)
            
            mock_print.assert_called_with("CrackReaction: Rough terrain detected, slowing down")
            self.assertEqual(mission.speed, 5.0)  # Should be half of 10

    def test_strategy_mission_integration(self):
        """Test strategy integration with mission"""
        from app.drones.base import Drone
        
        class TestDrone(Drone):
            def get_drone_type(self):
                return "Test"
            def complete_task(self):
                return "Done"
        
        drone = TestDrone("Test", Mock(), 5.0, {})
        drone.speed = 20.0
        
        strategy = CrackReaction()
        drone.set_strategy(strategy)
        
        # Test strategy reaction
        with patch('builtins.print'):
            strategy.react(drone, {"terrain_roughness": 9})
            self.assertEqual(drone.speed, 10.0)


if __name__ == '__main__':
    unittest.main()