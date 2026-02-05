from app.bridge.base import MovementImplementor
from typing import Tuple


class DroneController:
    def __init__(self, implementor: MovementImplementor):
        self._implementor = implementor
    
    def goto(self, coord: Tuple[float, float], retries: int = 3) -> bool:
        for attempt in range(retries):
            if self._implementor.move_to(coord):
                return True
            print(f"Attempt {attempt + 1} failed, retrying...")
        return False
    
    # Додаємо метод move_to, який просто делегує до _implementor
    def move_to(self, coord: Tuple[float, float]) -> bool:
        return self._implementor.move_to(coord)
    
    def adjust_course(self, vector: Tuple[float, float]) -> bool:
        return self._implementor.adjust_course(vector)
    
    def set_swarm(self) -> bool:
        return self._implementor.set_mode("swarm")
    
    def set_single(self) -> bool:
        return self._implementor.set_mode("single")
    
    def takeoff(self) -> bool:
        return self._implementor.takeoff()
    
    def land(self) -> bool:
        return self._implementor.land()
    
    def hold(self) -> bool:
        return self._implementor.hold_position()
    
    def broadcast(self, message: str) -> bool:
        return self._implementor.broadcast(message)