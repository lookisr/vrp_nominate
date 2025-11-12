"""Add telegram_user_id column manually

Revision ID: fcb4b3f17ee9
Revises: f2b36f810f58
Create Date: 2025-11-12 22:56:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fcb4b3f17ee9"
down_revision: Union[str, None] = "f2b36f810f58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку telegram_user_id
    op.add_column("vote", sa.Column("telegram_user_id", sa.BigInteger(), nullable=True))
    
    # Заполняем существующие записи тестовым значением
    op.execute("UPDATE vote SET telegram_user_id = 123456789 WHERE telegram_user_id IS NULL")
    
    # Делаем колонку NOT NULL
    op.alter_column("vote", "telegram_user_id", nullable=False)
    
    # Добавляем индекс
    op.create_index("ix_vote_telegram_user_id", "vote", ["telegram_user_id"], unique=False)
    
    # Добавляем уникальное ограничение
    op.create_unique_constraint("unique_user_vote_per_nominee", "vote", ["telegram_user_id", "nominee_id"])


def downgrade() -> None:
    op.drop_constraint("unique_user_vote_per_nominee", "vote", type_="unique")
    op.drop_index("ix_vote_telegram_user_id", table_name="vote")
    op.drop_column("vote", "telegram_user_id")

