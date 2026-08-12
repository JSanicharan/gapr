from datetime import datetime
from unittest.mock import MagicMock, patch

from libs.models import Bar, Direction, FVG
from services.strategy.redis_consumer import RedisConsumer, stream_fields_to_bar, stream_fields_to_fvg


def test_stream_fields_to_fvg_parses_known_values() -> None:
    fields = {
        "direction": "bullish",
        "top": "11.0",
        "bottom": "10.0",
        "timestamp": "2024-01-01T09:30:00",
    }
    result = stream_fields_to_fvg(fields)
    assert result == FVG(
        direction=Direction.BULLISH,
        top=11.0,
        bottom=10.0,
        timestamp=datetime(2024, 1, 1, 9, 30),
    )


def test_stream_fields_to_bar_parses_known_values() -> None:
    fields = {
        "timestamp": "2024-01-01T09:30:00",
        "open": "100.5",
        "high": "105.0",
        "low": "99.0",
        "close": "103.25",
        "volume": "15000.0",
    }
    result = stream_fields_to_bar(fields)
    assert result == Bar(
        timestamp=datetime(2024, 1, 1, 9, 30),
        open=100.5,
        high=105.0,
        low=99.0,
        close=103.25,
        volume=15000.0,
    )


def test_read_all_fvgs_converts_stream_entries_in_order() -> None:
    with patch("services.strategy.redis_consumer.redis.Redis") as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        mock_client.xrange.return_value = [
            (
                "1-1",
                {
                    "direction": "bullish",
                    "top": "11.0",
                    "bottom": "10.0",
                    "timestamp": "2024-01-01T09:30:00",
                },
            ),
            (
                "2-1",
                {
                    "direction": "bearish",
                    "top": "20.0",
                    "bottom": "18.0",
                    "timestamp": "2024-01-01T09:31:00",
                },
            ),
        ]

        consumer = RedisConsumer()
        result = consumer.read_all_fvgs("signals:fvg:AAPL")

        mock_client.xrange.assert_called_once_with("signals:fvg:AAPL", "-", "+")
        assert result == [
            FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=datetime(2024, 1, 1, 9, 30)),
            FVG(direction=Direction.BEARISH, top=20.0, bottom=18.0, timestamp=datetime(2024, 1, 1, 9, 31)),
        ]


def test_read_all_bars_converts_stream_entries_in_order() -> None:
    with patch("services.strategy.redis_consumer.redis.Redis") as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        mock_client.xrange.return_value = [
            (
                "1-1",
                {
                    "timestamp": "2024-01-01T09:30:00",
                    "open": "100.5",
                    "high": "105.0",
                    "low": "99.0",
                    "close": "103.25",
                    "volume": "15000.0",
                },
            ),
            (
                "2-1",
                {
                    "timestamp": "2024-01-01T09:31:00",
                    "open": "103.25",
                    "high": "104.0",
                    "low": "102.5",
                    "close": "103.75",
                    "volume": "8200.0",
                },
            ),
        ]

        consumer = RedisConsumer()
        result = consumer.read_all_bars("market-data:AAPL:1min")

        mock_client.xrange.assert_called_once_with("market-data:AAPL:1min", "-", "+")
        assert result == [
            Bar(
                timestamp=datetime(2024, 1, 1, 9, 30),
                open=100.5,
                high=105.0,
                low=99.0,
                close=103.25,
                volume=15000.0,
            ),
            Bar(
                timestamp=datetime(2024, 1, 1, 9, 31),
                open=103.25,
                high=104.0,
                low=102.5,
                close=103.75,
                volume=8200.0,
            ),
        ]
