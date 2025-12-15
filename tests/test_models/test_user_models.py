import pytest
from sqlalchemy import select

from app.models import User, Address, Order, Product


@pytest.mark.asyncio
async def test_create_user_model(session):
    user = User(
        username="model_user",
        email="model@example.com",
        description="Model test",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id is not None
    assert user.username == "model_user"
    assert user.email == "model@example.com"
    assert user.description == "Model test"


@pytest.mark.asyncio
async def test_user_address_relationship(session):
    user = User(
        username="with_address",
        email="addr@example.com",
        description="Has address",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    address = Address(
        user_id=user.id,
        street="Main street",
        city="City",
        zip_code="123456",
        country="Country",
    )
    session.add(address)
    await session.commit()
    await session.refresh(address)

    result = await session.scalars(
        select(Address).where(Address.user_id == user.id)
    )
    addresses = result.all()

    assert len(addresses) == 1
    assert addresses[0].city == "City"
    assert addresses[0].street == "Main street"


@pytest.mark.asyncio
async def test_address_order_relationship(session):
    user = User(
        username="with_order",
        email="order@example.com",
        description="Has order",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    address = Address(
        user_id=user.id,
        street="Main street",
        city="City",
        zip_code="123456",
        country="Country",
    )
    session.add(address)
    await session.commit()
    await session.refresh(address)

    product = Product(
        name="Test product",
        price=9.99,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    order = Order(
        user_id=user.id,
        address_id=address.id,
        product_id=product.id,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    assert order.user_id == user.id
    assert order.address_id == address.id
    assert order.product_id == product.id
