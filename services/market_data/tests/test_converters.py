from datetime import datetime

from ib_async import BarData

from libs.models import Bar
from services.market_data.converters import bar_data_to_bar, convert_bar_data_list


def test_bar_data_to_bar_maps_every_field() -> None:
    bar_data = BarData(
        date=datetime(2024, 1, 1, 9, 30),
        open=100.5,
        high=105.0,
        low=99.0,
        close=103.25,
        volume=15000.0,
    )
    result = bar_data_to_bar(bar_data)
    assert result == Bar(
        timestamp=datetime(2024, 1, 1, 9, 30),
        open=100.5,
        high=105.0,
        low=99.0,
        close=103.25,
        volume=15000.0,
    )


def test_convert_bar_data_list_converts_every_item() -> None:
    bar_data_list = [
        BarData(
            date=datetime(2024, 1, 1, 9, 30),
            open=100.5,
            high=105.0,
            low=99.0,
            close=103.25,
            volume=15000.0,
        ),
        BarData(
            date=datetime(2024, 1, 1, 9, 31),
            open=103.25,
            high=104.0,
            low=102.5,
            close=103.75,
            volume=8200.0,
        ),
    ]
    result = convert_bar_data_list(bar_data_list)
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
