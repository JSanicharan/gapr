from ib_async import IB, Stock

from services.market_data.config import Config
from services.market_data.converters import convert_bar_data_list
from services.market_data.redis_publisher import RedisPublisher


def fetch_and_publish(ib: IB, symbol: str, bar_size: str, stream_suffix: str, duration: str = "3 D") -> int:
    config = Config()

    if not ib.isConnected():
        ib.connect(config.ibkr_host, config.ibkr_port, config.ibkr_client_id)
        ib.reqMarketDataType(3)

    contract = Stock(symbol, "SMART", "USD")
    bar_data_list = ib.reqHistoricalData(contract, "", duration, bar_size, "TRADES", False)

    bars = convert_bar_data_list(bar_data_list)

    stream_name = f"market-data:{symbol}:{stream_suffix}"
    publisher = RedisPublisher(host=config.redis_host, port=config.redis_port, stream_name=stream_name)
    publisher.clear_stream()
    for bar in bars:
        publisher.publish_bar(bar)

    print(f"Published {len(bars)} bars to stream {stream_name}")

    return len(bars)


def main() -> None:
    config = Config()

    ib = IB()
    ib.connect(config.ibkr_host, config.ibkr_port, config.ibkr_client_id)
    ib.reqMarketDataType(3)

    published_15min = fetch_and_publish(ib, config.symbol, "15 mins", "15min")
    published_1min = fetch_and_publish(ib, config.symbol, "1 min", "1min")

    ib.disconnect()

    print(f"market-data:{config.symbol}:15min -> {published_15min} bars published")
    print(f"market-data:{config.symbol}:1min -> {published_1min} bars published")


if __name__ == "__main__":
    main()
