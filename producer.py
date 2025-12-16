import json
import pika


def send_messages() -> None:
    # подключаемся к RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            virtual_host="local",
            credentials=pika.PlainCredentials("guest", "guest"),
        )
    )
    channel = connection.channel()

    # гарантируем наличие очередей
    channel.queue_declare(queue="product", durable=False)
    channel.queue_declare(queue="order", durable=False)

    # 5 продуктов
    products = [
        {"id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0001", "name": "laptop",  "quantity": 10},
        {"id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0002", "name": "mouse",   "quantity": 50},
        {"id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0003", "name": "keyboard","quantity": 30},
        {"id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0004", "name": "monitor", "quantity": 15},
        {"id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0005", "name": "chair",   "quantity": 5},
    ]

    # 3 заказа
    orders = [
        {
            "id": "9c8c1a10-8d6f-4e0b-9b1e-2a5b7d010001",
            "user_id": "u1",
            "product_id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0001",
        },
        {
            "id": "9c8c1a10-8d6f-4e0b-9b1e-2a5b7d010002",
            "user_id": "u2",
            "product_id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0002",
        },
        {
            "id": "9c8c1a10-8d6f-4e0b-9b1e-2a5b7d010003",
            "user_id": "u3",
            "product_id": "5f0a9e3e-5a9b-4a8c-9a2c-1c9c7c0a0003",
        },
    ]

    # отправяем продукты
    for p in products:
        channel.basic_publish(
            exchange="",
            routing_key="product",
            body=json.dumps(p),
        )
        print("sent product:", p)

    # отправляем заказы
    for o in orders:
        channel.basic_publish(
            exchange="",
            routing_key="order",
            body=json.dumps(o),
        )
        print("sent order:", o)

    connection.close()


if __name__ == "__main__":
    send_messages()
