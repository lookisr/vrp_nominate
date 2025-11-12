from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.vote import VoteCreate, VoteResponse
from app.services.vote_service import create_vote

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("", response_model=VoteResponse)
async def vote(
    vote_data: VoteCreate, session: AsyncSession = Depends(get_session)
) -> VoteResponse:
    """Этот эндпоинт принимает голос за номинанта."""

    return await create_vote(session, vote_data.nominee_id)

