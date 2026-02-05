import sys
import os
import logging
import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.factory.mission_factory import MissionFactory
from app.config.mission_config import MissionConfig

def create_test_scenarios():
    scenarios = []
    scenarios.append(MissionConfig(
        mission_id="test_flight_001",
        mission_type="exploration",
        environment_type="air",
        platform_type="air",
        mode="single",
        target_area=(100.0, 200.0),
        base_area=(0.0, 0.0),
        thresholds={"wind_speed": 20},
        behavior_params={"wind_speed": 12.0, "weight": 5.0}
    ))
    return scenarios

def run_console_tests():
    logging.basicConfig(level=logging.INFO)
    scenarios = create_test_scenarios()
    for scenario in scenarios:
        print(f"\nExecuting mission: {scenario.mission_id}")
        try:
            drone, env, ctrl, strat, cor = MissionFactory.create_from_config(scenario)
            result = drone.execute_mission()
            print(f"Status: {drone.status}")
        except Exception as e:
            print(f"Mission failed: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Запуск API сервера...")
        uvicorn.run("app.api.server:app", host="127.0.0.1", port=8000, reload=True)
    else:
        run_console_tests()

if __name__ == "__main__":
    main()