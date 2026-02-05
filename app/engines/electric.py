from app.engines.base import Engine


class ElectricEngine(Engine):
    def __init__(self, power_capacity: float = 100.0):
        self.power_capacity = power_capacity
        self.current_power = power_capacity
        self.is_running = False

    def start(self) -> bool:
        if self.current_power > 10:
            self.is_running = True
            return True
        return False

    def stop(self) -> bool:
        self.is_running = False
        return True

    def get_power_level(self) -> float:
        return self.current_power
    
    def consume_power(self, amount: float):
        self.current_power = max(0, self.current_power - amount)