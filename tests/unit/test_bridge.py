import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from unittest.mock import Mock, patch
from app.bridge.air import AirPlatform
from app.bridge.sea import SeaPlatform
from app.bridge.surface import SurfacePlatform
from app.bridge.controller import DroneController


class TestBridgePattern(unittest.TestCase):
    def test_air_platform_methods(self):
        """Test AirPlatform methods"""
        platform = AirPlatform()
        
        with patch('builtins.print') as mock_print:
            self.assertTrue(platform.takeoff())
            mock_print.assert_called_with("AirPlatform: Taking off vertically")
            
            self.assertTrue(platform.move_to((100, 200)))
            mock_print.assert_called_with("AirPlatform: Flying to (100, 200)")
            
            self.assertTrue(platform.land())
            mock_print.assert_called_with("AirPlatform: Landing vertically")

    def test_sea_platform_methods(self):
        """Test SeaPlatform methods"""
        platform = SeaPlatform()
        
        with patch('builtins.print') as mock_print:
            self.assertTrue(platform.takeoff())
            mock_print.assert_called_with("SeaPlatform: Launching from water surface")
            
            self.assertTrue(platform.move_to((50, 75)))
            mock_print.assert_called_with("SeaPlatform: Sailing to (50, 75)")

    def test_surface_platform_methods(self):
        """Test SurfacePlatform methods"""
        platform = SurfacePlatform()
        
        with patch('builtins.print') as mock_print:
            self.assertTrue(platform.takeoff())
            mock_print.assert_called_with("SurfacePlatform: Starting ground movement")
            
            self.assertTrue(platform.move_to((200, 300)))
            mock_print.assert_called_with("SurfacePlatform: Moving to (200, 300)")

    def test_controller_delegation(self):
        """Test DroneController delegates to platform"""
        mock_platform = Mock()
        mock_platform.move_to.return_value = True
        mock_platform.takeoff.return_value = True
        
        controller = DroneController(mock_platform)
        
        self.assertTrue(controller.move_to((100, 200)))
        mock_platform.move_to.assert_called_with((100, 200))
        
        self.assertTrue(controller.takeoff())
        mock_platform.takeoff.assert_called()

    def test_controller_goto_with_retries(self):
        """Test goto method with retry logic"""
        mock_platform = Mock()
        mock_platform.move_to.side_effect = [False, False, True]  # Third attempt succeeds
        
        controller = DroneController(mock_platform)
        
        with patch('builtins.print') as mock_print:
            result = controller.goto((100, 200), retries=3)
            
            self.assertTrue(result)
            self.assertEqual(mock_platform.move_to.call_count, 3)
            mock_print.assert_called_with("Attempt 2 failed, retrying...")


if __name__ == '__main__':
    unittest.main()