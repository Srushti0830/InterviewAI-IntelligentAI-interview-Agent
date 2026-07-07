from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    experience = Column(String(255), nullable=False)
    skills = Column(Text, nullable=False)
    difficulty = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
