def build_evaluation_prompt(candidate: dict, questions: list, answers: list) -> str:
    return f"""
You are a senior hiring manager. Evaluate the interview response.
Return ONLY JSON with the structure:
{{
  "overallScore": 88,
  "recommendation": "Hire",
  "technicalSkills": 90,
  "communication": 84,
  "problemSolving": 86,
  "confidence": 82,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "questionEvaluation": [
    {{"questionId": 1, "score": 9, "feedback": "...", "suggestion": "..."}}
  ]
}}

Candidate details:
- Name: {candidate.get('name')}
- Role: {candidate.get('role')}
- Experience: {candidate.get('experience')}
- Skills: {candidate.get('skills')}
- Difficulty: {candidate.get('difficulty')}

Questions and answers:
{questions}
{answers}

Requirements:
- Score each answer fairly.
- Provide concise and actionable feedback.
- No commentary or extra text.
"""
