import redis

from libs.models import TradeIntent


def trade_intent_to_stream_fields(intent: TradeIntent) -> dict[str, str]:
    return {
        "symbol": intent.symbol,
        "direction": intent.direction.value,
        "fvg_top": str(intent.fvg_top),
        "fvg_bottom": str(intent.fvg_bottom),
        "entry_price": str(intent.entry_price),
        "entry_timestamp": intent.entry_timestamp.isoformat(),
        "fvg_timestamp": intent.fvg_timestamp.isoformat(),
    }


class TradeIntentPublisher:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        stream_name: str = "signals:trade-intent:AAPL",
    ) -> None:
        self.stream_name = stream_name
        self.client = redis.Redis(host=host, port=port)

    def publish_trade_intent(self, intent: TradeIntent) -> None:
        fields = trade_intent_to_stream_fields(intent)
        self.client.xadd(self.stream_name, fields)
