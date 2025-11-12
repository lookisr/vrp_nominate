from pydantic import BaseModel


class VoteCreate(BaseModel):
    """Схема для создания голоса."""

    nominee_id: int


class VoteResponse(BaseModel):
    """Схема для ответа после голосования."""

    success: bool
    message: str
    nominee_name: str
    vote_count: int

