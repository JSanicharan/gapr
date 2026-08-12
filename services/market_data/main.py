from ib_async import IB, Stock

from services.market_data.config import Config
from services.market_data.converters import convert_bar_data_list
from services.market_data.redis_publisher import RedisPublisher


def main() -> None:
    config = Config()

    ib = IB()
    ib.connect(config.ibkr_host, config.ibkr_port, config.ibkr_client_id)
    ib.reqMarketDataType(3)

    contract = Stock(config.symbol, "SMART", "USD")
    bar_data_list = ib.reqHistoricalData(contract, "", "3 D", "15 mins", "TRADES", False)

    bars = convert_bar_data_list(bar_data_list)

    stream_name = f"market-data:{config.symbol}:15min"
    publisher = RedisPublisher(host=config.redis_host, port=config.redis_port, stream_name=stream_name)
    for bar in bars:
        publisher.publish_bar(bar)

    print(f"Published {len(bars)} bars to stream {stream_name}")

    ib.disconnect()


if __name__ == "__main__":
    main()
