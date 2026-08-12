from datetime import datetime
from unittest.mock import MagicMock, patch

from libs.models import Bar
from services.market_data.redis_publisher import RedisPublisher, bar_to_stream_fields


def test_bar_to_stream_fields_produces_correct_dict() -> None:
    bar = Bar(
        timestamp=datetime(2024, 1, 1, 9, 30),
        open=100.5,
        high=105.0,
        low=99.0,
        close=103.25,
        volume=15000.0,
    )
    result = bar_to_stream_fields(bar)
    assert result == {
        "timestamp": "2024-01-01T09:30:00",
        "open": "100.5",
        "high": "105.0",
        "low": "99.0",
        "close": "103.25",
        "volume": "15000.0",
    }


def test_publish_bar_calls_xadd_with_correct_stream_and_fields() -> None:
    with patch("services.market_data.redis_publisher.redis.Redis") as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client

        publisher = RedisPublisher(stream_name="market-data:AAPL:15min")
        bar = Bar(
            timestamp=datetime(2024, 1, 1, 9, 30),
            open=100.5,
            high=105.0,
            low=99.0,
            close=103.25,
            volume=15000.0,
        )
        publisher.publish_bar(bar)

        mock_client.xadd.assert_called_once_with(
            "market-data:AAPL:15min",
            {
                "timestamp": "2024-01-01T09:30:00",
                "open": "100.5",
                "high": "105.0",
                "low": "99.0",
                "close": "103.25",
                "volume": "15000.0",
            },
        )
