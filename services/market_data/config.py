import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    ibkr_host: str = field(default_factory=lambda: os.environ.get("IBKR_HOST", "127.0.0.1"))
    ibkr_port: int = field(default_factory=lambda: int(os.environ.get("IBKR_PORT", "4002")))
    ibkr_client_id: int = field(default_factory=lambda: int(os.environ.get("IBKR_CLIENT_ID", "16")))
    redis_host: str = field(default_factory=lambda: os.environ.get("REDIS_HOST", "localhost"))
    redis_port: int = field(default_factory=lambda: int(os.environ.get("REDIS_PORT", "6379")))
    symbol: str = field(default_factory=lambda: os.environ.get("SYMBOL", "AAPL"))
