from dataclasses import dataclass
from typing import Dict, Tuple, Any

@dataclass
class MissionConfig:
    mission_id: str
    mission_type: str
    environment_type: str
    platform_type: str
    mode: str
    target_area: Tuple[float, float]
    base_area: Tuple[float, float]
    thresholds: Dict[str, Any]
    behavior_params: Dict[str, Any]