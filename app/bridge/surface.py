from app.bridge.base import MovementImplementor
from typing import Tuple


class SurfacePlatform(MovementImplementor):
    def takeoff(self) -> bool:
        print("SurfacePlatform: Starting ground movement")
        return True
    
    def land(self) -> bool:
        print("SurfacePlatform: Stopping ground movement")
        return True
    
    def move_to(self, coord: Tuple[float, float]) -> bool:
        print(f"SurfacePlatform: Moving to {coord}")
        return True
    
    def adjust_course(self, vector: Tuple[float, float]) -> bool:
        print(f"SurfacePlatform: Adjusting course by {vector}")
        return True
    
    def hold_position(self) -> bool:
        print("SurfacePlatform: Holding position")
        return True
    
    def set_mode(self, mode: str) -> bool:
        print(f"SurfacePlatform: Setting mode to {mode}")
        return True
    
    def broadcast(self, message: str) -> bool:
        print(f"SurfacePlatform: Broadcasting '{message}' to swarm")
        return True