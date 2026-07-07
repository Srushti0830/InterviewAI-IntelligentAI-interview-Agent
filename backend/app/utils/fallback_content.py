import json
from typing import Any, Dict, List


def build_fallback_questions(candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
    role = candidate.get("role", "Software Engineer")
    skills = candidate.get("skills", "general engineering")
    experience = candidate.get("experience", "professional")
    difficulty = candidate.get("difficulty", "Intermediate")
    normalized_role = role.strip().lower()

    if "ai engineer" in normalized_role:
        return [
            {
                "id": 1,
                "question": "What is the difference between Artificial Intelligence, Machine Learning, and Deep Learning?",
                "category": "Fundamentals",
                "difficulty": difficulty,
            },
            {
                "id": 2,
                "question": "Explain the difference between supervised, unsupervised, and reinforcement learning.",
                "category": "Machine Learning",
                "difficulty": difficulty,
            },
            {
                "id": 3,
                "question": "What is Prompt Engineering, and why is it important for Large Language Models (LLMs)?",
                "category": "AI",
                "difficulty": difficulty,
            },
            {
                "id": 4,
                "question": "How would you deploy an AI model to production?",
                "category": "Deployment",
                "difficulty": difficulty,
            },
            {
                "id": 5,
                "question": "Tell us about an AI project you have built and the challenges you faced.",
                "category": "Experience",
                "difficulty": difficulty,
            },
        ]

    return [
        {
            "id": 1,
            "question": f"Describe how you would design a scalable solution for a {role.lower()} role using your experience in {skills}.",
            "category": "Technical",
            "difficulty": difficulty,
        },
        {
            "id": 2,
            "question": f"Walk through a project from {experience} where you solved a meaningful problem and explain your trade-offs.",
            "category": "Experience",
            "difficulty": difficulty,
        },
        {
            "id": 3,
            "question": f"How would you approach debugging a production issue in an application built around {skills}?",
            "category": "Problem Solving",
            "difficulty": difficulty,
        },
        {
            "id": 4,
            "question": "Explain how you would communicate technical decisions to non-technical stakeholders clearly and confidently.",
            "category": "Communication",
            "difficulty": difficulty,
        },
        {
            "id": 5,
            "question": "What would you do to improve your own reliability and growth as a professional in this field?",
            "category": "Growth",
            "difficulty": difficulty,
        },
    ]


def build_fallback_evaluation(candidate: Dict[str, Any], questions: List[Dict[str, Any]], answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    score = 78
    recommendation = "Strong potential"

    if candidate.get("difficulty") == "Advanced":
        score = 82
        recommendation = "Ready for advanced roles"

    return {
        "overallScore": score,
        "recommendation": recommendation,
        "technicalSkills": 80,
        "communication": 77,
        "problemSolving": 79,
        "confidence": 76,
        "strengths": [
            "Clear and structured thinking",
            "Practical engineering approach",
            "Good professional awareness",
        ],
        "weaknesses": [
            "Add more concrete examples",
            "Further deepen technical trade-off discussion",
            "Strengthen confidence in high-pressure scenarios",
        ],
        "questionEvaluation": [
            {
                "questionId": item.get("questionId") or item.get("id"),
                "score": 8,
                "feedback": "The answer showed solid understanding and a practical approach.",
                "suggestion": "Add a more specific example or implementation detail to increase clarity.",
            }
            for item in answers
        ],
    }
