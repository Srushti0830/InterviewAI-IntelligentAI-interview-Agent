from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    experience: str
    skills: str
    difficulty: str


class CandidateResponse(CandidateCreate):
    id: int
