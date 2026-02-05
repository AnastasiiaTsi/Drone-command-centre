import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from unittest.mock import Mock, patch
from app.cor.reroute_handler import ReRouteHandler
from app.cor.adjust_altitude_handler import AdjustAltitudeHandler
from app.cor.swarm_reassign_handler import SwarmReassignHandler
from app.cor.emergency_land_handler import EmergencyLandHandler


class TestChainOfResponsibility(unittest.TestCase):
    def test_reroute_handler(self):
        """Test ReRouteHandler handles obstacle events"""
        handler = ReRouteHandler()
        
        with patch('builtins.print') as mock_print:
            result = handler.handle({"type": "obstacle_detected"})
            
            self.assertTrue(result)
            mock_print.assert_called_with("ReRouteHandler: Obstacle detected, finding alternative route")

    def test_adjust_altitude_handler(self):
        """Test AdjustAltitudeHandler handles low visibility"""
        handler = AdjustAltitudeHandler()
        
        with patch('builtins.print') as mock_print:
            result = handler.handle({"type": "low_visibility"})
            
            self.assertTrue(result)
            mock_print.assert_called_with("AdjustAltitudeHandler: Low visibility, adjusting altitude")

    def test_swarm_reassign_handler(self):
        """Test SwarmReassignHandler handles swarm failure"""
        handler = SwarmReassignHandler()
        
        with patch('builtins.print') as mock_print:
            result = handler.handle({"type": "swarm_member_failed"})
            
            self.assertTrue(result)
            mock_print.assert_called_with("SwarmReassignHandler: Swarm member failed, reassigning tasks")

    def test_emergency_land_handler(self):
        """Test EmergencyLandHandler handles critical failure"""
        handler = EmergencyLandHandler()
        
        with patch('builtins.print') as mock_print:
            result = handler.handle({"type": "critical_failure"})
            
            self.assertTrue(result)
            mock_print.assert_called_with("EmergencyLandHandler: Critical failure, initiating emergency landing")

    def test_chain_construction(self):
        """Test building and using a chain"""
        reroute = ReRouteHandler()
        altitude = AdjustAltitudeHandler()
        emergency = EmergencyLandHandler()
        
        # Build chain
        reroute.set_next(altitude).set_next(emergency)
        
        # Test handling
        with patch('builtins.print') as mock_print:
            # Should be handled by reroute
            result = reroute.handle({"type": "obstacle_detected"})
            self.assertTrue(result)
            
            # Should be handled by altitude
            result = reroute.handle({"type": "low_visibility"})
            self.assertTrue(result)
            
            # Should be handled by emergency
            result = reroute.handle({"type": "critical_failure"})
            self.assertTrue(result)
            
            # Should not be handled (falls through)
            result = reroute.handle({"type": "unknown_event"})
            self.assertFalse(result)

    def test_handler_order(self):
        """Test that handlers process in correct order"""
        handler1 = Mock()
        handler1.handle = Mock(return_value=True)
        
        handler2 = Mock()
        handler2.handle = Mock(return_value=False)
        
        # Build simple chain
        from app.cor.base import Handler
        
        class ConcreteHandler(Handler):
            def handle(self, request):
                if request.get("type") == "test":
                    return True
                return self._handle_next(request)
        
        handler = ConcreteHandler()
        handler.set_next(ConcreteHandler())
        
        result = handler.handle({"type": "test"})
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()