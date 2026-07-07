# InterviewAI – Intelligent AI Interview Agent

InterviewAI is a production-ready mock interview platform that lets candidates enter their details, generate AI interview questions, answer them, receive evaluation feedback, and download a polished PDF report.

## Features
- Modern landing page with dark mode support
- Interview setup flow with role, experience, difficulty, and skills
- AI-generated interview questions using Gemini
- One-question-at-a-time interview experience with auto-save
- AI-powered evaluation with scoring and recommendations
- PDF report generation
- SQLite-backed history and report persistence

## Tech Stack
- Frontend: React 18, Vite, TailwindCSS, React Router, Framer Motion, Lucide React, Recharts, jsPDF, Axios
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic, python-dotenv, Google Gemini API

## Project Structure
- frontend/ - Vite React application
- backend/ - FastAPI backend service

## Environment Variables
### Frontend
- VITE_API_URL=http://localhost:8000

### Backend
- GEMINI_API_KEY=YOUR_GEMINI_API_KEY

## Local Development
### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Notes
- The app is designed to run locally without deployment configuration.
- Ensure the backend has a valid Gemini API key to enable AI question generation and evaluation.

# -Intelligent-AI-Interview-Agent

# InterviewAI-Intelligent-AI-Interview-Agent
