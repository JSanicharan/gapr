from datetime import datetime

import redis

from libs.models import Bar


def stream_fields_to_bar(fields: dict[str, str]) -> Bar:
    return Bar(
        timestamp=datetime.fromisoformat(fields["timestamp"]),
        open=float(fields["open"]),
        high=float(fields["high"]),
        low=float(fields["low"]),
        close=float(fields["close"]),
        volume=float(fields["volume"]),
    )


class RedisConsumer:
    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def read_all_bars(self, stream_name: str) -> list[Bar]:
        entries = self.client.xrange(stream_name, "-", "+")
        return [stream_fields_to_bar(fields) for _, fields in entries]
