import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    redis_host: str = field(default_factory=lambda: os.environ.get("REDIS_HOST", "localhost"))
    redis_port: int = field(default_factory=lambda: int(os.environ.get("REDIS_PORT", "6379")))
    symbol: str = field(default_factory=lambda: os.environ.get("SYMBOL", "AAPL"))
