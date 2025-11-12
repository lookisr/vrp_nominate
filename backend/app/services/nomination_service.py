from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Nomination
from app.schemas.nomination import NominationCreate, NominationResponse


async def get_all_nominations(session: AsyncSession) -> list[NominationResponse]:
    """Эта функция получает список всех номинаций."""

    result = await session.execute(select(Nomination).order_by(Nomination.created_at))
    nominations = result.scalars().all()
    return [NominationResponse.model_validate(n) for n in nominations]


async def get_nomination_by_id(session: AsyncSession, nomination_id: int) -> NominationResponse | None:
    """Эта функция получает номинацию по ID."""

    result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
    nomination = result.scalar_one_or_none()
    if nomination:
        return NominationResponse.model_validate(nomination)
    return None

