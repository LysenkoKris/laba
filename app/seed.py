from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Address, User

CONNECT_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"


def main() -> None:
    engine = create_engine(CONNECT_URL, echo=True)

    session_local = sessionmaker(bind=engine)

    users_data = [
        {
            "username": "john",
            "email": "john@example.com",
            "street": "Main St 1",
            "city": "London",
            "zip_code": "10001",
            "country": "UK",
        },
        {
            "username": "jane",
            "email": "jane@example.com",
            "street": "High St 5",
            "city": "London",
            "zip_code": "10002",
            "country": "UK",
        },
        {
            "username": "alex",
            "email": "alex@example.com",
            "street": "Elm St 10",
            "city": "Berlin",
            "zip_code": "20001",
            "country": "DE",
        },
        {
            "username": "kate",
            "email": "kate@example.com",
            "street": "Park Ave 3",
            "city": "Paris",
            "zip_code": "30001",
            "country": "FR",
        },
        {
            "username": "mike",
            "email": "mike@example.com",
            "street": "Oak St 7",
            "city": "Rome",
            "zip_code": "40001",
            "country": "IT",
        },
    ]

    with session_local() as session:
        for item in users_data:
            user = User(username=item["username"], email=item["email"])
            address = Address(
                user=user,
                street=item["street"],
                city=item["city"],
                zip_code=item["zip_code"],
                country=item["country"],
            )
            session.add(user)
            session.add(address)

        session.commit()


if __name__ == "__main__":
    main()
