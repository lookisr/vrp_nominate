from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.nomination import NominationListResponse, NominationResponse
from app.services.nomination_service import get_all_nominations, get_nomination_by_id

router = APIRouter(prefix="/nominations", tags=["nominations"])


@router.get("", response_model=NominationListResponse)
async def list_nominations(session: AsyncSession = Depends(get_session)) -> NominationListResponse:
    """Этот эндпоинт возвращает список всех номинаций."""

    nominations = await get_all_nominations(session)
    return NominationListResponse(nominations=nominations)


@router.get("/{nomination_id}", response_model=NominationResponse)
async def get_nomination(
    nomination_id: int, session: AsyncSession = Depends(get_session)
) -> NominationResponse:
    """Этот эндпоинт возвращает номинацию по ID."""

    nomination = await get_nomination_by_id(session, nomination_id)
    if not nomination:
        raise HTTPException(status_code=404, detail="Номинация не найдена")
    return nomination

