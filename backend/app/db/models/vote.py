from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.nominee import Nominee


class Vote(Base):
    """Эта модель хранит каждый голос за номинанта."""

    __table_args__ = (
        UniqueConstraint('telegram_user_id', 'nominee_id', name='unique_user_vote_per_nominee'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    nominee_id: Mapped[int] = mapped_column(
        ForeignKey("nominee.id", ondelete="CASCADE"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    nominee: Mapped["Nominee"] = relationship(back_populates="votes")

