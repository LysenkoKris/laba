import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/local")
app = FastStream(broker)


@broker.subscriber("product")
async def subscribe_product(message: dict) -> None:
    print("[product] received:", message)


@broker.subscriber("order")
async def subscribe_order(message: dict) -> None:
    print("[order] received:", message)


async def main() -> None:
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
