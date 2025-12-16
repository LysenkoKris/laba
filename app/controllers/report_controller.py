from datetime import date

from litestar import Controller, get
from sqlalchemy import select

from app.db import async_session_factory
from app.models import OrderReport


class ReportController(Controller):
    path = "/report"

    @get()
    async def get_report(self, report_at: date) -> list[dict]:
        async with async_session_factory() as session:
            stmt = select(OrderReport).where(OrderReport.report_at == report_at)
            result = await session.scalars(stmt)
            rows = result.all()

        return [
            {
                "report_at": r.report_at.isoformat(),
                "order_id": str(r.order_id),
                "count_product": r.count_product,
            }
            for r in rows
        ]
