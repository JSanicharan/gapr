from datetime import datetime

from services.historical_fvg.fvg_detector import detect_fvgs
from libs.models import Bar, Direction, FVG


def make_bar(hour: int, open: float, high: float, low: float, close: float, volume: float = 100.0) -> Bar:
    return Bar(
        timestamp=datetime(2024, 1, 1, hour),
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def test_detects_bullish_fvg() -> None:
    bars = [
        make_bar(0, open=9.5, high=10.0, low=9.0, close=9.8),
        make_bar(1, open=10.5, high=12.0, low=10.2, close=11.5),
        make_bar(2, open=11.5, high=13.0, low=11.0, close=12.5),
    ]
    result = detect_fvgs(bars)
    assert result == [
        FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=bars[1].timestamp)
    ]


def test_detects_bearish_fvg() -> None:
    bars = [
        make_bar(0, open=21.0, high=22.0, low=20.0, close=21.5),
        make_bar(1, open=19.5, high=19.8, low=18.5, close=19.0),
        make_bar(2, open=17.5, high=18.0, low=17.0, close=17.8),
    ]
    result = detect_fvgs(bars)
    assert result == [
        FVG(direction=Direction.BEARISH, top=20.0, bottom=18.0, timestamp=bars[1].timestamp)
    ]


def test_no_fvg_when_ranges_overlap() -> None:
    bars = [
        make_bar(0, open=9.5, high=10.0, low=9.0, close=9.8),
        make_bar(1, open=10.0, high=10.5, low=9.5, close=10.2),
        make_bar(2, open=9.8, high=11.0, low=9.5, close=10.5),
    ]
    assert detect_fvgs(bars) == []


def test_detects_multiple_fvgs_across_sequence() -> None:
    bars = [
        make_bar(0, open=9.5, high=10.0, low=9.0, close=9.8),
        make_bar(1, open=10.5, high=12.0, low=10.2, close=11.5),
        make_bar(2, open=11.5, high=13.0, low=11.0, close=12.5),
        make_bar(3, open=12.5, high=13.2, low=12.0, close=12.8),
        make_bar(4, open=9.5, high=9.8, low=8.5, close=9.0),
    ]
    result = detect_fvgs(bars)
    assert result == [
        FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=bars[1].timestamp),
        FVG(direction=Direction.BEARISH, top=11.0, bottom=9.8, timestamp=bars[3].timestamp),
    ]


def test_returns_empty_list_for_short_input() -> None:
    bars = [
        make_bar(0, open=9.5, high=10.0, low=9.0, close=9.8),
        make_bar(1, open=10.5, high=12.0, low=10.2, close=11.5),
    ]
    assert detect_fvgs(bars) == []
