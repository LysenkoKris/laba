from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from app.models import User, Address


CONNECT_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"


def main() -> None:
    engine = create_engine(CONNECT_URL, echo=True)

    with Session(engine) as session:
        stmt = select(User).options(selectinload(User.addresses))
        result = session.scalars(stmt).all()

        for user in result:
            print(f"User: {user.username} ({user.email})")
            for addr in user.addresses:
                print(
                    f"  Address: {addr.street}, {addr.city}, {addr.zip_code}, {addr.country}"
                )


if __name__ == "__main__":
    main()
