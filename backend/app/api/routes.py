import json
import os
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.utils.fallback_content import build_fallback_evaluation, build_fallback_questions
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.answer import Answer
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.question import Question
from app.models.report import Report
from app.prompts.evaluationPrompt import build_evaluation_prompt
from app.prompts.questionPrompt import build_question_prompt
from app.schemas.interview import AnswerPayload, InterviewSubmission, QuestionRequest

router = APIRouter()


@router.post("/generate-questions")
def generate_questions(payload: QuestionRequest, db: Session = Depends(get_db)):
    candidate = payload.candidate
    if not candidate.get("name") or not candidate.get("role"):
        raise HTTPException(status_code=400, detail="Candidate name and role are required")

    role = candidate.get("role", "").strip().lower()
    if "ai engineer" in role:
        questions = build_fallback_questions(candidate)
    else:
        try:
            response = _call_gemini(build_question_prompt(candidate))
            questions = json.loads(response)
        except (json.JSONDecodeError, ValueError, RuntimeError, httpx.HTTPError) as exc:
            questions = build_fallback_questions(candidate)

    if not isinstance(questions, list) or not questions:
        questions = build_fallback_questions(candidate)

    db_candidate = Candidate(
        name=candidate["name"],
        email=candidate["email"],
        role=candidate["role"],
        experience=candidate["experience"],
        skills=candidate["skills"],
        difficulty=candidate["difficulty"],
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    interview = Interview(candidate_id=db_candidate.id, status="in_progress")
    db.add(interview)
    db.commit()
    db.refresh(interview)

    for item in questions:
        db_question = Question(
            interview_id=interview.id,
            question_text=item["question"],
            category=item.get("category"),
            difficulty=item.get("difficulty"),
        )
        db.add(db_question)
    db.commit()

    return {"candidateId": db_candidate.id, "interviewId": interview.id, "questions": questions}


@router.post("/submit-interview")
def submit_interview(payload: InterviewSubmission, db: Session = Depends(get_db)):
    if not payload.questions or not payload.answers:
        raise HTTPException(status_code=400, detail="Questions and answers are required")

    candidate = payload.candidate
    interview = db.query(Interview).filter(Interview.id == payload.questions[0].get("interviewId", 0)).first() if payload.questions else None

    if interview is None:
        interview = Interview(candidate_id=1, status="completed")
        db.add(interview)
        db.commit()
        db.refresh(interview)

    candidate_record = db.query(Candidate).filter(Candidate.id == candidate.get("id", 0)).first()
    if candidate_record is None:
        candidate_record = Candidate(
            name=candidate.get("name", "Unknown"),
            email=candidate.get("email", "unknown@example.com"),
            role=candidate.get("role", "Unknown"),
            experience=candidate.get("experience", "Unknown"),
            skills=candidate.get("skills", "Unknown"),
            difficulty=candidate.get("difficulty", "Unknown"),
        )
        db.add(candidate_record)
        db.commit()
        db.refresh(candidate_record)
        interview.candidate_id = candidate_record.id

    db_questions = db.query(Question).filter(Question.interview_id == interview.id).all()
    if not db_questions:
        for item in payload.questions:
            question = Question(interview_id=interview.id, question_text=item.get("question", ""))
            db.add(question)
        db.commit()
        db_questions = db.query(Question).filter(Question.interview_id == interview.id).all()

    answers_by_question = {answer.questionId: answer.answer for answer in payload.answers}

    for question in db_questions:
        if str(question.id) in answers_by_question:
            answer_text = answers_by_question[str(question.id)]
        elif question.id in answers_by_question:
            answer_text = answers_by_question[question.id]
        else:
            answer_text = ""
        db.add(Answer(question_id=question.id, answer_text=answer_text))

    db.commit()

    try:
        evaluation = _call_gemini(build_evaluation_prompt(candidate, payload.questions, payload.answers))
        evaluation_data = json.loads(evaluation)
    except (json.JSONDecodeError, ValueError, RuntimeError, httpx.HTTPError) as exc:
        evaluation_data = build_fallback_evaluation(candidate, payload.questions, payload.answers)

    interview.status = "completed"
    interview.overall_score = evaluation_data.get("overallScore")
    interview.recommendation = evaluation_data.get("recommendation")
    db.add(interview)

    report = Report(
        interview_id=interview.id,
        technical_skills=evaluation_data.get("technicalSkills"),
        communication=evaluation_data.get("communication"),
        confidence=evaluation_data.get("confidence"),
        problem_solving=evaluation_data.get("problemSolving"),
        strengths=json.dumps(evaluation_data.get("strengths", [])),
        weaknesses=json.dumps(evaluation_data.get("weaknesses", [])),
        recommendation=evaluation_data.get("recommendation"),
        feedback_json=json.dumps(evaluation_data.get("questionEvaluation", [])),
    )
    db.add(report)
    db.commit()
    db.refresh(interview)

    return {"interviewId": interview.id, "report": evaluation_data}


@router.get("/report/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "interviewId": report.interview_id,
        "technicalSkills": report.technical_skills,
        "communication": report.communication,
        "confidence": report.confidence,
        "problemSolving": report.problem_solving,
        "strengths": json.loads(report.strengths or "[]"),
        "weaknesses": json.loads(report.weaknesses or "[]"),
        "recommendation": report.recommendation,
        "feedback": json.loads(report.feedback_json or "[]"),
    }


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    interviews = db.query(Interview).order_by(Interview.created_at.desc()).all()
    return [
        {
            "id": interview.id,
            "candidateId": interview.candidate_id,
            "status": interview.status,
            "overallScore": interview.overall_score,
            "recommendation": interview.recommendation,
        }
        for interview in interviews
    ]


def _call_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        raise RuntimeError("Missing GEMINI_API_KEY")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
