from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Nominee, Vote
from app.schemas.nominee import NomineeWithVotesResponse


async def get_nominees_by_nomination(
    session: AsyncSession, nomination_id: int
) -> list[NomineeWithVotesResponse]:
    """Эта функция получает список номинантов по номинации с количеством голосов."""

    # Подзапрос для подсчёта голосов
    vote_count_subquery = (
        select(func.count(Vote.id).label("vote_count"))
        .where(Vote.nominee_id == Nominee.id)
        .scalar_subquery()
    )

    result = await session.execute(
        select(
            Nominee,
            func.coalesce(vote_count_subquery, 0).label("vote_count"),
        )
        .where(Nominee.nomination_id == nomination_id)
        .order_by(Nominee.created_at)
    )

    nominees_with_votes = []
    for row in result.all():
        nominee = row[0]
        vote_count = row[1]
        nominee_dict = {
            "id": nominee.id,
            "nomination_id": nominee.nomination_id,
            "name": nominee.name,
            "image_path": nominee.image_path,
            "created_at": nominee.created_at,
            "vote_count": vote_count,
        }
        nominees_with_votes.append(NomineeWithVotesResponse(**nominee_dict))

    return nominees_with_votes


async def get_nominee_by_id(session: AsyncSession, nominee_id: int) -> Nominee | None:
    """Эта функция получает номинанта по ID."""

    result = await session.execute(select(Nominee).where(Nominee.id == nominee_id))
    return result.scalar_one_or_none()

