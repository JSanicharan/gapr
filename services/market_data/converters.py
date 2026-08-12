from ib_async import BarData

from libs.models import Bar


def bar_data_to_bar(bar_data: BarData) -> Bar:
    return Bar(
        timestamp=bar_data.date,
        open=bar_data.open,
        high=bar_data.high,
        low=bar_data.low,
        close=bar_data.close,
        volume=bar_data.volume,
    )


def convert_bar_data_list(bar_data_list: list[BarData]) -> list[Bar]:
    return [bar_data_to_bar(bar_data) for bar_data in bar_data_list]
