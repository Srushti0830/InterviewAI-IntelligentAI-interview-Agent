from pydantic import BaseModel
from typing import List, Optional


class QuestionRequest(BaseModel):
    candidate: dict


class AnswerPayload(BaseModel):
    questionId: int
    answer: str


class InterviewSubmission(BaseModel):
    candidate: dict
    questions: List[dict]
    answers: List[AnswerPayload]


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    status: str
    overall_score: Optional[int] = None
    recommendation: Optional[str] = None
