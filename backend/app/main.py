from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.database import Base, engine
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.report import Report
from app.api import routes

app = FastAPI(title="InterviewAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "InterviewAI backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(routes.router)
