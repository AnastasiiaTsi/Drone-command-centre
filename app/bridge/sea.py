from app.bridge.base import MovementImplementor
from typing import Tuple


class SeaPlatform(MovementImplementor):
    def __init__(self, protocol: str = "NMEA-0183") -> None:
        self.protocol = protocol

    def takeoff(self) -> bool:
        print("SeaPlatform: Launching from water surface")
        return True
    
    def land(self) -> bool:
        print("SeaPlatform: Landing on water surface")
        return True
    
    def move_to(self, coord: Tuple[float, float]) -> bool:
        print(f"SeaPlatform: Sailing to {coord}")
        return True
    
    def adjust_course(self, vector: Tuple[float, float]) -> bool:
        print(f"SeaPlatform: Adjusting course by {vector}")
        return True
    
    def hold_position(self) -> bool:
        print("SeaPlatform: Anchoring in position")
        return True
    
    def set_mode(self, mode: str) -> bool:
        print(f"SeaPlatform: Setting mode to {mode}")
        return True
    
    def broadcast(self, message: str) -> bool:
        print(f"SeaPlatform: Broadcasting '{message}' to swarm")
        return True