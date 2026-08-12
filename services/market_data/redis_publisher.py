import redis

from libs.models import Bar


def bar_to_stream_fields(bar: Bar) -> dict[str, str]:
    return {
        "timestamp": bar.timestamp.isoformat(),
        "open": str(bar.open),
        "high": str(bar.high),
        "low": str(bar.low),
        "close": str(bar.close),
        "volume": str(bar.volume),
    }


class RedisPublisher:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        stream_name: str = "market-data:AAPL:15min",
    ) -> None:
        self.stream_name = stream_name
        self.client = redis.Redis(host=host, port=port)

    def publish_bar(self, bar: Bar) -> None:
        fields = bar_to_stream_fields(bar)
        self.client.xadd(self.stream_name, fields)
