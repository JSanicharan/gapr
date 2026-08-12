from services.historical_fvg.config import Config
from services.historical_fvg.fvg_detector import detect_fvgs
from services.historical_fvg.redis_consumer import RedisConsumer
from services.historical_fvg.redis_publisher import FVGPublisher


def main() -> None:
    config = Config()

    bars_stream = f"market-data:{config.symbol}:15min"
    consumer = RedisConsumer(host=config.redis_host, port=config.redis_port)
    bars = consumer.read_all_bars(bars_stream)

    fvgs = detect_fvgs(bars)

    fvgs_stream = f"signals:fvg:{config.symbol}"
    publisher = FVGPublisher(host=config.redis_host, port=config.redis_port, stream_name=fvgs_stream)
    for fvg in fvgs:
        publisher.publish_fvg(fvg)

    print(f"Read {len(bars)} bars from {bars_stream}")
    print(f"Detected and published {len(fvgs)} FVGs to {fvgs_stream}")


if __name__ == "__main__":
    main()
