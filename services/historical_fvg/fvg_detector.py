from libs.models import Bar, Direction, FVG


def detect_fvgs(bars: list[Bar]) -> list[FVG]:
    fvgs: list[FVG] = []
    for i in range(len(bars) - 2):
        first = bars[i]
        third = bars[i + 2]
        if first.high < third.low:
            fvgs.append(
                FVG(
                    direction=Direction.BULLISH,
                    top=third.low,
                    bottom=first.high,
                    timestamp=bars[i + 1].timestamp,
                )
            )
        elif first.low > third.high:
            fvgs.append(
                FVG(
                    direction=Direction.BEARISH,
                    top=first.low,
                    bottom=third.high,
                    timestamp=bars[i + 1].timestamp,
                )
            )
    return fvgs
