from datetime import date

from sqlalchemy import select, delete
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.sql import func

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from scheduler.broker import broker
from app.db import async_session_factory
from app.models import Order, OrderReport
from datetime import datetime, timezone


scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",   # каждую минуту
            "args": [],
            "schedule_id": "orders_daily_report",
        }
    ]
)


async def my_sheduled_task() -> str:
    today_utc = datetime.now(timezone.utc).date()

    async with async_session_factory() as session:
        # 1. Получаем все актуальные заказы за сегодня
        stmt_orders = select(Order.id).where(func.date(Order.created_at) == today_utc)
        order_ids = [row async for row in await session.stream_scalars(stmt_orders)]

        # 2. Upsert для каждого заказа
        if order_ids:
            stmt_upsert = insert(OrderReport).values([
                {
                    "report_at": today_utc,
                    "order_id": oid,
                    "count_product": 1,
                }
                for oid in order_ids
            ]).on_conflict_do_update(
                index_elements=["report_at", "order_id"],
                set_={"count_product": 1},
            )
            await session.execute(stmt_upsert)

            # 3. Удаляем отчёты, для которых заказов больше нет
            stmt_delete = (
                delete(OrderReport)
                .where(OrderReport.report_at == today_utc)
                .where(OrderReport.order_id.not_in(order_ids))
            )
            await session.execute(stmt_delete)

        else:
            # если заказов нет — просто чистим отчёты за сегодня
            await session.execute(
                delete(OrderReport).where(OrderReport.report_at == today_utc)
            )

        await session.commit()

    return "ok"
