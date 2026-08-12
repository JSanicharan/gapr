from datetime import datetime, timedelta

from libs.models import Bar, Direction, FVG, TradeIntent
from services.strategy.retracement import find_all_trade_intents, find_retracement


def make_bar(minute: int, high: float, low: float) -> Bar:
    return Bar(
        timestamp=datetime(2024, 1, 1, 9, 30) + timedelta(minutes=minute),
        open=(high + low) / 2,
        high=high,
        low=low,
        close=(high + low) / 2,
        volume=100.0,
    )


def test_bullish_fvg_with_clear_retracement() -> None:
    fvg = FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bars = [
        make_bar(1, high=13.0, low=12.0),
        make_bar(2, high=12.0, low=10.5),
        make_bar(3, high=11.5, low=10.8),
    ]
    result = find_retracement(fvg, bars, "AAPL")
    assert result == TradeIntent(
        symbol="AAPL",
        direction=Direction.BULLISH,
        fvg_top=11.0,
        fvg_bottom=10.0,
        entry_price=11.0,
        entry_timestamp=bars[1].timestamp,
        fvg_timestamp=fvg.timestamp,
    )


def test_bearish_fvg_with_clear_retracement() -> None:
    fvg = FVG(direction=Direction.BEARISH, top=20.0, bottom=18.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bars = [
        make_bar(1, high=17.5, low=16.5),
        make_bar(2, high=19.5, low=19.0),
        make_bar(3, high=18.5, low=18.2),
    ]
    result = find_retracement(fvg, bars, "AAPL")
    assert result == TradeIntent(
        symbol="AAPL",
        direction=Direction.BEARISH,
        fvg_top=20.0,
        fvg_bottom=18.0,
        entry_price=18.0,
        entry_timestamp=bars[1].timestamp,
        fvg_timestamp=fvg.timestamp,
    )


def test_no_retracement_returns_none() -> None:
    fvg = FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bars = [
        make_bar(1, high=13.0, low=12.0),
        make_bar(2, high=14.0, low=13.5),
        make_bar(3, high=15.0, low=14.5),
    ]
    assert find_retracement(fvg, bars, "AAPL") is None


def test_bars_before_fvg_timestamp_are_ignored() -> None:
    fvg = FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bars = [
        Bar(
            timestamp=datetime(2024, 1, 1, 9, 29),
            open=10.5,
            high=11.5,
            low=10.2,
            close=10.5,
            volume=100.0,
        ),
        Bar(
            timestamp=datetime(2024, 1, 1, 9, 30),
            open=10.5,
            high=11.5,
            low=10.2,
            close=10.5,
            volume=100.0,
        ),
        make_bar(1, high=13.0, low=12.0),
        make_bar(2, high=14.0, low=13.5),
    ]
    assert find_retracement(fvg, bars, "AAPL") is None


def test_find_all_trade_intents_mixes_matches_and_non_matches() -> None:
    bullish_fvg = FVG(direction=Direction.BULLISH, top=11.0, bottom=10.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bearish_fvg = FVG(direction=Direction.BEARISH, top=20.0, bottom=18.0, timestamp=datetime(2024, 1, 1, 9, 30))
    no_match_fvg = FVG(direction=Direction.BULLISH, top=5.0, bottom=4.0, timestamp=datetime(2024, 1, 1, 9, 30))
    bars = [
        make_bar(1, high=13.0, low=12.0),
        make_bar(2, high=19.5, low=10.5),
        make_bar(3, high=18.5, low=18.2),
    ]
    result = find_all_trade_intents([bullish_fvg, bearish_fvg, no_match_fvg], bars, "AAPL")
    assert result == [
        TradeIntent(
            symbol="AAPL",
            direction=Direction.BULLISH,
            fvg_top=11.0,
            fvg_bottom=10.0,
            entry_price=11.0,
            entry_timestamp=bars[1].timestamp,
            fvg_timestamp=bullish_fvg.timestamp,
        ),
        TradeIntent(
            symbol="AAPL",
            direction=Direction.BEARISH,
            fvg_top=20.0,
            fvg_bottom=18.0,
            entry_price=18.0,
            entry_timestamp=bars[1].timestamp,
            fvg_timestamp=bearish_fvg.timestamp,
        ),
    ]
