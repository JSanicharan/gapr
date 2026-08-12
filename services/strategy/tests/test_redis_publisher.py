from datetime import datetime
from unittest.mock import MagicMock, patch

from libs.models import Direction, TradeIntent
from services.strategy.redis_publisher import TradeIntentPublisher, trade_intent_to_stream_fields


def test_trade_intent_to_stream_fields_produces_correct_dict() -> None:
    intent = TradeIntent(
        symbol="AAPL",
        direction=Direction.BULLISH,
        fvg_top=11.0,
        fvg_bottom=10.0,
        entry_price=11.0,
        entry_timestamp=datetime(2024, 1, 1, 9, 32),
        fvg_timestamp=datetime(2024, 1, 1, 9, 30),
    )
    result = trade_intent_to_stream_fields(intent)
    assert result == {
        "symbol": "AAPL",
        "direction": "bullish",
        "fvg_top": "11.0",
        "fvg_bottom": "10.0",
        "entry_price": "11.0",
        "entry_timestamp": "2024-01-01T09:32:00",
        "fvg_timestamp": "2024-01-01T09:30:00",
    }


def test_publish_trade_intent_calls_xadd_with_correct_stream_and_fields() -> None:
    with patch("services.strategy.redis_publisher.redis.Redis") as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client

        publisher = TradeIntentPublisher(stream_name="signals:trade-intent:AAPL")
        intent = TradeIntent(
            symbol="AAPL",
            direction=Direction.BEARISH,
            fvg_top=20.0,
            fvg_bottom=18.0,
            entry_price=18.0,
            entry_timestamp=datetime(2024, 1, 1, 9, 32),
            fvg_timestamp=datetime(2024, 1, 1, 9, 30),
        )
        publisher.publish_trade_intent(intent)

        mock_client.xadd.assert_called_once_with(
            "signals:trade-intent:AAPL",
            {
                "symbol": "AAPL",
                "direction": "bearish",
                "fvg_top": "20.0",
                "fvg_bottom": "18.0",
                "entry_price": "18.0",
                "entry_timestamp": "2024-01-01T09:32:00",
                "fvg_timestamp": "2024-01-01T09:30:00",
            },
        )
