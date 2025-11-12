from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.nomination import Nomination
    from app.db.models.vote import Vote


class Nominee(Base):
    """Эта модель хранит номинанта внутри выбранной номинации."""

    __table_args__ = (UniqueConstraint("nomination_id", "name", name="uq_nominee_nomination_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomination_id: Mapped[int] = mapped_column(
        ForeignKey("nomination.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    nomination: Mapped["Nomination"] = relationship(back_populates="nominees")
    votes: Mapped[list["Vote"]] = relationship(
        back_populates="nominee", cascade="all, delete-orphan", passive_deletes=True
    )

