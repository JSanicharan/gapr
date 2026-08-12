import redis

from libs.models import FVG


def fvg_to_stream_fields(fvg: FVG) -> dict[str, str]:
    return {
        "direction": fvg.direction.value,
        "top": str(fvg.top),
        "bottom": str(fvg.bottom),
        "timestamp": fvg.timestamp.isoformat(),
    }


class FVGPublisher:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        stream_name: str = "signals:fvg:AAPL",
    ) -> None:
        self.stream_name = stream_name
        self.client = redis.Redis(host=host, port=port)

    def publish_fvg(self, fvg: FVG) -> None:
        fields = fvg_to_stream_fields(fvg)
        self.client.xadd(self.stream_name, fields)
