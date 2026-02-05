import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from unittest.mock import Mock
from app.environments.air import AirEnvironment
from app.environments.sea import SeaEnvironment
from app.environments.surface import SurfaceEnvironment


class TestEnvironmentPattern(unittest.TestCase):
    def test_air_environment(self):
        """Test air environment functionality"""
        # Використовуємо wind_speed > 15 для активації reaction
        env = AirEnvironment(
            wind_speed=16.0,  # > 15
            visibility=10.0,
            temperature=25.0,
            altitude=100.0
        )
        
        # Test properties
        self.assertEqual(env.wind_speed, 16.0)
        self.assertEqual(env.visibility, 10.0)
        self.assertEqual(env.temperature, 25.0)
        self.assertEqual(env.altitude, 100.0)
        
        # Test sampling
        sample = env.sample()
        self.assertIn("wind_speed", sample)
        self.assertIn("environment_type", sample)
        self.assertEqual(sample["environment_type"], "Air")
        
        # Test effects - тепер requires_reaction має бути True
        effects = env.get_specific_effects()
        self.assertIn("requires_reaction", effects)
        self.assertTrue(effects["requires_reaction"], 
                       f"Expected True for wind_speed={env.wind_speed}, got {effects['requires_reaction']}")
        
        # Test speed calculation
        max_speed = env.calc_max_speed(100.0, 5.0)
        self.assertIsInstance(max_speed, float)
        
        # Test with low wind (не має тригерити reaction)
        env_low = AirEnvironment(
            wind_speed=10.0,  # < 15
            visibility=10.0,
            temperature=25.0,
            altitude=100.0
        )
        effects_low = env_low.get_specific_effects()
        self.assertFalse(effects_low.get("requires_reaction", True),
                        f"Expected False for wind_speed={env_low.wind_speed}")

    def test_sea_environment(self):
        """Test sea environment functionality"""
        env = SeaEnvironment(
            wind_speed=10.0,
            visibility=8.0,
            wave_height=2.0,
            current_speed=1.5
        )
        
        sample = env.sample()
        self.assertEqual(sample["environment_type"], "Sea")
        self.assertIn("wave_height", sample)
        
        effects = env.get_specific_effects()
        self.assertIn("wave_effect", effects)

    def test_surface_environment(self):
        """Test surface environment functionality"""
        env = SurfaceEnvironment(
            wind_speed=5.0,
            visibility=15.0,
            terrain_roughness=3.0,
            obstacle_density=2.0
        )
        
        sample = env.sample()
        self.assertEqual(sample["environment_type"], "Surface")
        
        effects = env.get_specific_effects()
        self.assertIn("terrain_difficulty", effects)

    def test_observer_subscription(self):
        """Test observer pattern in environments"""
        env = AirEnvironment(10.0, 10.0, 20.0, 100.0)
        
        events_received = []
        def callback(event):
            events_received.append(event)
        
        # Subscribe
        env.subscribe(callback)
        
        # Generate event
        env.sample()
        
        # Check callback was called
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0]["type"], "air_reading")

    def test_multiple_subscribers(self):
        """Test multiple subscribers"""
        env = AirEnvironment(10.0, 10.0, 20.0, 100.0)
        
        callbacks_called = []
        def callback1(event):
            callbacks_called.append("callback1")
        
        def callback2(event):
            callbacks_called.append("callback2")
        
        env.subscribe(callback1)
        env.subscribe(callback2)
        
        env.sample()
        
        self.assertEqual(len(callbacks_called), 2)
        self.assertIn("callback1", callbacks_called)
        self.assertIn("callback2", callbacks_called)


if __name__ == '__main__':
    unittest.main()