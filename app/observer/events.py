from dataclasses import dataclass
from typing import Any


@dataclass
class EnvironmentEvent:
    event_type: str
    data: Any
    timestamp: float