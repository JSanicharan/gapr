from dataclasses import dataclass
from datetime import datetime

from libs.models.fvg import Direction


@dataclass(frozen=True)
class TradeIntent:
    symbol: str
    direction: Direction
    fvg_top: float
    fvg_bottom: float
    entry_price: float
    entry_timestamp: datetime
    fvg_timestamp: datetime
