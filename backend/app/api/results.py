from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.result import NominationResultResponse, ResultsSummaryResponse
from app.services.result_service import get_all_results, get_results_by_nomination

router = APIRouter(prefix="/results", tags=["results"])


@router.get("", response_model=ResultsSummaryResponse)
async def list_all_results(
    session: AsyncSession = Depends(get_session),
) -> ResultsSummaryResponse:
    """Этот эндпоинт возвращает результаты по всем номинациям."""

    return await get_all_results(session)


@router.get("/{nomination_id}", response_model=NominationResultResponse)
async def get_nomination_results(
    nomination_id: int, session: AsyncSession = Depends(get_session)
) -> NominationResultResponse:
    """Этот эндпоинт возвращает результаты по конкретной номинации."""

    result = await get_results_by_nomination(session, nomination_id)
    if not result:
        raise HTTPException(status_code=404, detail="Номинация не найдена")
    return result

