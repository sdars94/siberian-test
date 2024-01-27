from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.serializers import serialize_invoices
from app.crud.invoices import get_full_info
from app.db.session import get_async_session
from app.schemas.invoices import DataOut

router = APIRouter()


@router.get("/invoices", response_model=DataOut)
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    total_sum_gte: int = 0,
    total_sum_lte: int = None,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Retrieves a list of Invoices with optional filtering parameters.

    Args:

        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        total_sum_gte (int): Total sum greater than or equal to.
        total_sum_lte (int, optional): Total sum less than or equal to.
        session (AsyncSession): Asynchronous session dependency.

    Returns:

        DataOut: Serialized list of invoices.
    """

    data = await get_full_info(
        session,
        skip=skip,
        limit=limit,
        total_sum_gte=total_sum_gte,
        total_sum_lte=total_sum_lte,
    )
    serialized_data = serialize_invoices(data)
    return serialized_data
