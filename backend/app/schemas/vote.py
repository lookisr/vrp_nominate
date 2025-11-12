from pydantic import BaseModel


class VoteCreate(BaseModel):
    """Схема для создания голоса."""

    nominee_id: int
    nomination_id: int  # Для проверки - один голос на номинацию


class VoteResponse(BaseModel):
    """Схема для ответа после голосования."""

    success: bool
    message: str
    nominee_name: str
    vote_count: int
    already_voted: bool = False

