from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Nominee, Vote
from app.schemas.vote import VoteResponse
from app.services.nominee_service import get_nominee_by_id
from app.services.settings_service import is_voting_open


async def check_user_voted_in_nomination(
    session: AsyncSession, telegram_user_id: int, nomination_id: int
) -> bool:
    """Проверяет, голосовал ли пользователь в этой номинации."""
    
    result = await session.execute(
        select(Vote)
        .join(Nominee)
        .where(Vote.telegram_user_id == telegram_user_id)
        .where(Nominee.nomination_id == nomination_id)
    )
    return result.scalar_one_or_none() is not None


async def create_vote(
    session: AsyncSession, telegram_user_id: int, nominee_id: int, nomination_id: int
) -> VoteResponse:
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
    
    # Проверяем подписку на канал (только если не в режиме разработки)
    from app.core.config import settings
    from app.utils.telegram_auth import check_channel_subscription
    
    if not settings.development_mode and settings.required_channel:
        is_subscribed = await check_channel_subscription(
            telegram_user_id, 
            settings.required_channel, 
            settings.telegram_bot_token
        )
        
        if not is_subscribed:
            return VoteResponse(
                success=False,
                message=f"Для голосования необходимо подписаться на канал {settings.required_channel}",
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

    # Проверяем, не голосовал ли пользователь уже в этой номинации
    already_voted = await check_user_voted_in_nomination(
        session, telegram_user_id, nomination_id
    )
    
    if already_voted:
        # Подсчитываем текущее количество голосов
        result = await session.execute(
            select(func.count(Vote.id)).where(Vote.nominee_id == nominee_id)
        )
        vote_count = result.scalar() or 0
        
        return VoteResponse(
            success=False,
            message="Вы уже проголосовали в этой номинации",
            nominee_name=nominee.name,
            vote_count=vote_count,
            already_voted=True,
        )

    try:
        # Создаём голос
        vote = Vote(telegram_user_id=telegram_user_id, nominee_id=nominee_id)
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
    except IntegrityError:
        await session.rollback()
        # На случай race condition - если два запроса пришли одновременно
        result = await session.execute(
            select(func.count(Vote.id)).where(Vote.nominee_id == nominee_id)
        )
        vote_count = result.scalar() or 0
        
        return VoteResponse(
            success=False,
            message="Вы уже проголосовали в этой номинации",
            nominee_name=nominee.name,
            vote_count=vote_count,
            already_voted=True,
        )

