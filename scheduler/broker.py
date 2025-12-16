from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/local",  # важно: /local, без лишнего слэша
    exchange_name="report",
    queue_name="cmd_order",
)
