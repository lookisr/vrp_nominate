from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class NomineeBase(BaseModel):
    """Базовая схема для номинанта."""

    name: str
    image_path: str


class NomineeCreate(NomineeBase):
    """Схема для создания номинанта."""

    nomination_id: int


class NomineeResponse(NomineeBase):
    """Схема для ответа с номинантом."""

    id: int
    nomination_id: int
    created_at: datetime

    @field_serializer('image_path')
    def serialize_image_path(self, image_path: str) -> str:
        """Преобразует относительный путь в полный URL."""
        if image_path.startswith('/') or image_path.startswith('http'):
            return image_path
        return f"/media/{image_path}"

    model_config = ConfigDict(from_attributes=True)


class NomineeWithVotesResponse(NomineeResponse):
    """Схема для номинанта с количеством голосов."""

    vote_count: int


class NomineeListResponse(BaseModel):
    """Схема для списка номинантов."""

    nominees: list[NomineeWithVotesResponse]

