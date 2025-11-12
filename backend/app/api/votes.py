from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.vote import VoteCreate, VoteResponse
from app.services.vote_service import create_vote
from app.utils.telegram_auth import get_telegram_user_id

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("", response_model=VoteResponse)
async def vote(
    vote_data: VoteCreate,
    session: AsyncSession = Depends(get_session),
    telegram_user_id: int = Depends(get_telegram_user_id),
) -> VoteResponse:
    """
    Этот эндпоинт принимает голос за номинанта.
    
    Требуется заголовок X-Telegram-Init-Data с валидными данными от Telegram WebApp.
    """

    return await create_vote(
        session,
        telegram_user_id=telegram_user_id,
        nominee_id=vote_data.nominee_id,
        nomination_id=vote_data.nomination_id,
    )

