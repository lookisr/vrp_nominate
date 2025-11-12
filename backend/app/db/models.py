from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Nomination(Base):
    """Эта модель хранит информацию о номинациях премии."""

    __tablename__ = "nominations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    image_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    nominees = relationship("Nominee", back_populates="nomination", cascade="all, delete-orphan")


class Nominee(Base):
    """Эта модель хранит информацию о номинантах в рамках номинации."""

    __tablename__ = "nominees"

    id = Column(Integer, primary_key=True, index=True)
    nomination_id = Column(Integer, ForeignKey("nominations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    image_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    nomination = relationship("Nomination", back_populates="nominees")
    votes = relationship("Vote", back_populates="nominee", cascade="all, delete-orphan")


class Vote(Base):
    """Эта модель хранит информацию о голосах пользователей."""

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    nominee_id = Column(Integer, ForeignKey("nominees.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    nominee = relationship("Nominee", back_populates="votes")


class Setting(Base):
    """Эта модель хранит настройки приложения (ключ-значение)."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Admin(Base):
    """Эта модель хранит список администраторов по их Telegram ID."""

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

