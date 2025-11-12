from pydantic import BaseModel

from app.schemas.nominee import NomineeWithVotesResponse


class NominationResultResponse(BaseModel):
    """Схема для результатов по номинации."""

    nomination_id: int
    nomination_title: str
    nominees: list[NomineeWithVotesResponse]


class ResultsSummaryResponse(BaseModel):
    """Схема для сводки результатов по всем номинациям."""

    nominations: list[NominationResultResponse]

