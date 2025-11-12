from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Nominee, Vote
from app.schemas.vote import VoteResponse
from app.services.nominee_service import get_nominee_by_id
from app.services.settings_service import is_voting_open


async def create_vote(session: AsyncSession, nominee_id: int) -> VoteResponse:
    """Эта функция создаёт голос за номинанта."""

    # Проверяем, открыто ли голосование
    voting_open = await is_voting_open(session)
    if not voting_open:
        return VoteResponse(
            success=False,
            message="Голосование закрыто",
            nominee_name="",
            vote_count=0,
        )

    # Проверяем существование номинанта
    nominee = await get_nominee_by_id(session, nominee_id)
    if not nominee:
        return VoteResponse(
            success=False,
            message="Номинант не найден",
            nominee_name="",
            vote_count=0,
        )

    # Создаём голос
    vote = Vote(nominee_id=nominee_id)
    session.add(vote)
    await session.commit()
    await session.refresh(vote)

    # Подсчитываем общее количество голосов
    result = await session.execute(
        select(func.count(Vote.id)).where(Vote.nominee_id == nominee_id)
    )
    vote_count = result.scalar() or 0

    return VoteResponse(
        success=True,
        message="Голос успешно учтён",
        nominee_name=nominee.name,
        vote_count=vote_count,
    )

