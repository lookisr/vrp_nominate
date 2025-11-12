from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class NominationBase(BaseModel):
    """Базовая схема для номинации."""

    title: str
    image_path: str


class NominationCreate(NominationBase):
    """Схема для создания номинации."""

    pass


class NominationResponse(NominationBase):
    """Схема для ответа с номинацией."""

    id: int
    created_at: datetime

    @field_serializer('image_path')
    def serialize_image_path(self, image_path: str) -> str:
        """Преобразует относительный путь в полный URL."""
        if image_path.startswith('/') or image_path.startswith('http'):
            return image_path
        return f"/media/{image_path}"

    model_config = ConfigDict(from_attributes=True)


class NominationListResponse(BaseModel):
    """Схема для списка номинаций."""

    nominations: list[NominationResponse]

