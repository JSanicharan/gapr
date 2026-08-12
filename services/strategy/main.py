from services.strategy.config import Config
from services.strategy.redis_consumer import RedisConsumer
from services.strategy.redis_publisher import TradeIntentPublisher
from services.strategy.retracement import find_all_trade_intents


def main() -> None:
    config = Config()

    fvg_stream = f"signals:fvg:{config.symbol}"
    bar_stream = f"market-data:{config.symbol}:1min"

    consumer = RedisConsumer(host=config.redis_host, port=config.redis_port)
    fvgs = consumer.read_all_fvgs(fvg_stream)
    bars = consumer.read_all_bars(bar_stream)

    trade_intents = find_all_trade_intents(fvgs, bars, config.symbol)

    intent_stream = f"signals:trade-intent:{config.symbol}"
    publisher = TradeIntentPublisher(host=config.redis_host, port=config.redis_port, stream_name=intent_stream)
    for intent in trade_intents:
        publisher.publish_trade_intent(intent)

    print(f"Read {len(fvgs)} FVGs from {fvg_stream}")
    print(f"Read {len(bars)} bars from {bar_stream}")
    print(f"Found and published {len(trade_intents)} trade intents to {intent_stream}")


if __name__ == "__main__":
    main()
