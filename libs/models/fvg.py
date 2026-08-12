from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Direction(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"


@dataclass(frozen=True)
class FVG:
    direction: Direction
    top: float
    bottom: float
    timestamp: datetime
