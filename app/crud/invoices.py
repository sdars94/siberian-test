import sys
from typing import Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invoice, InvoiceLine


async def get_full_info(
    session: AsyncSession,
    skip: int,
    limit: int,
    total_sum_gte: int = 0,
    total_sum_lte: int = None,
) -> Sequence[Row]:
    if not total_sum_lte:
        total_sum_lte = sys.maxsize
    lines_subquery = (
        select(
            Invoice.title,
            InvoiceLine.title.label("line_title"),
            InvoiceLine.quantity,
            InvoiceLine.price_per_one,
            (InvoiceLine.quantity * InvoiceLine.price_per_one).label(
                "subtotal_line"
            ),
            (
                InvoiceLine.quantity
                * InvoiceLine.price_per_one
                * (1 - Invoice.discount / 100)
            ).label("total_line"),
        )
        .join(InvoiceLine)
        .alias("lines")
    )
    main_query_cte = (
        select(
            lines_subquery.c.title,
            (
                func.sum(lines_subquery.c.subtotal_line).over(
                    partition_by=lines_subquery.c.title
                )
            ).label("subtotal"),
            (
                func.sum(lines_subquery.c.total_line).over(
                    partition_by=lines_subquery.c.title
                )
            ).label("total"),
            lines_subquery.c.line_title,
            lines_subquery.c.quantity,
            lines_subquery.c.price_per_one,
            lines_subquery.c.subtotal_line,
            lines_subquery.c.total_line,
            (func.sum(lines_subquery.c.total_line).over()).label(
                "invoices_total"
            ),
        )
        .group_by(
            lines_subquery.c.title,
            lines_subquery.c.line_title,
            lines_subquery.c.quantity,
            lines_subquery.c.price_per_one,
            lines_subquery.c.subtotal_line,
            lines_subquery.c.total_line,
        )
        .order_by(lines_subquery.c.title)
    ).cte(name="main")

    filtered_query = (
        select(main_query_cte)
        .where((main_query_cte.c.total.between(total_sum_gte, total_sum_lte)))
        .cte(name="filtered")
    )
    paginated = select(filtered_query).where(
        filtered_query.c.title.in_(
            select(filtered_query.c.title).distinct().offset(skip).limit(limit)
        )
    )

    result = (await session.execute(paginated)).all()
    return result
