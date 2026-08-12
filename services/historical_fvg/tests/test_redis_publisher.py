from datetime import datetime
from unittest.mock import MagicMock, patch

from libs.models import Direction, FVG
from services.historical_fvg.redis_publisher import FVGPublisher, fvg_to_stream_fields


def test_fvg_to_stream_fields_produces_correct_dict() -> None:
    fvg = FVG(
        direction=Direction.BULLISH,
        top=11.0,
        bottom=10.0,
        timestamp=datetime(2024, 1, 1, 9, 30),
    )
    result = fvg_to_stream_fields(fvg)
    assert result == {
        "direction": "bullish",
        "top": "11.0",
        "bottom": "10.0",
        "timestamp": "2024-01-01T09:30:00",
    }


def test_publish_fvg_calls_xadd_with_correct_stream_and_fields() -> None:
    with patch("services.historical_fvg.redis_publisher.redis.Redis") as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client

        publisher = FVGPublisher(stream_name="signals:fvg:AAPL")
        fvg = FVG(
            direction=Direction.BEARISH,
            top=20.0,
            bottom=18.0,
            timestamp=datetime(2024, 1, 1, 9, 30),
        )
        publisher.publish_fvg(fvg)

        mock_client.xadd.assert_called_once_with(
            "signals:fvg:AAPL",
            {
                "direction": "bearish",
                "top": "20.0",
                "bottom": "18.0",
                "timestamp": "2024-01-01T09:30:00",
            },
        )
