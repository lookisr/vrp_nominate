from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Nomination, Nominee, Vote
from app.schemas.nominee import NomineeWithVotesResponse
from app.schemas.result import NominationResultResponse, ResultsSummaryResponse


async def get_results_by_nomination(
    session: AsyncSession, nomination_id: int
) -> NominationResultResponse | None:
    """Эта функция получает результаты по конкретной номинации, отсортированные по убыванию голосов."""

    # Получаем номинацию
    result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
    nomination = result.scalar_one_or_none()
    if not nomination:
        return None

    # Подзапрос для подсчёта голосов
    vote_count_subquery = (
        select(func.count(Vote.id).label("vote_count"))
        .where(Vote.nominee_id == Nominee.id)
        .scalar_subquery()
    )

    # Получаем номинантов с количеством голосов, отсортированных по убыванию
    result = await session.execute(
        select(
            Nominee,
            func.coalesce(vote_count_subquery, 0).label("vote_count"),
        )
        .where(Nominee.nomination_id == nomination_id)
        .order_by(func.coalesce(vote_count_subquery, 0).desc(), Nominee.created_at)
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

    return NominationResultResponse(
        nomination_id=nomination.id,
        nomination_title=nomination.title,
        nominees=nominees_with_votes,
    )


async def get_all_results(session: AsyncSession) -> ResultsSummaryResponse:
    """Эта функция получает результаты по всем номинациям."""

    # Получаем все номинации из БД
    result = await session.execute(select(Nomination).order_by(Nomination.created_at))
    nominations = result.scalars().all()
    results = []

    for nomination in nominations:
        result = await get_results_by_nomination(session, nomination.id)
        if result:
            results.append(result)

    return ResultsSummaryResponse(nominations=results)

