from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import User, Address, Product, Order


CONNECT_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"


def main() -> None:
    engine = create_engine(CONNECT_URL, echo=True)

    with Session(engine) as session:
        products = [
            Product(name="Laptop", price=1200.0),
            Product(name="Phone", price=800.0),
            Product(name="Tablet", price=500.0),
            Product(name="Headphones", price=150.0),
            Product(name="Monitor", price=300.0),
        ]
        session.add_all(products)
        session.flush()  # чтобы появились id

        users = session.scalars(select(User)).all()
        addresses = session.scalars(select(Address)).all()

        orders: list[Order] = []
        for i in range(5):
            user = users[i % len(users)]
            addr = addresses[i % len(addresses)]
            product = products[i]

            order = Order(
                user_id=user.id,
                address_id=addr.id,
                product_id=product.id,
            )
            orders.append(order)

        session.add_all(orders)
        session.commit()


if __name__ == "__main__":
    main()
