from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Эта база даёт всем моделям имя таблицы автоматически."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        """Эта функция формирует имя таблицы на основе имени модели."""

        return cls.__name__.lower()

