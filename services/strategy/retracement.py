from libs.models import Bar, Direction, FVG, TradeIntent


def find_retracement(fvg: FVG, bars: list[Bar], symbol: str) -> TradeIntent | None:
    candidates = [bar for bar in bars if bar.timestamp > fvg.timestamp]
    for bar in candidates:
        if bar.low <= fvg.top and bar.high >= fvg.bottom:
            entry_price = fvg.top if fvg.direction == Direction.BULLISH else fvg.bottom
            return TradeIntent(
                symbol=symbol,
                direction=fvg.direction,
                fvg_top=fvg.top,
                fvg_bottom=fvg.bottom,
                entry_price=entry_price,
                entry_timestamp=bar.timestamp,
                fvg_timestamp=fvg.timestamp,
            )
    return None


def find_all_trade_intents(fvgs: list[FVG], bars: list[Bar], symbol: str) -> list[TradeIntent]:
    intents = [find_retracement(fvg, bars, symbol) for fvg in fvgs]
    return [intent for intent in intents if intent is not None]
