from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.nominee import NomineeListResponse
from app.services.nominee_service import get_nominees_by_nomination

router = APIRouter(prefix="/nominations", tags=["nominees"])


@router.get("/{nomination_id}/nominees", response_model=NomineeListResponse)
async def list_nominees(
    nomination_id: int, session: AsyncSession = Depends(get_session)
) -> NomineeListResponse:
    """Этот эндпоинт возвращает список номинантов по номинации."""

    nominees = await get_nominees_by_nomination(session, nomination_id)
    return NomineeListResponse(nominees=nominees)

