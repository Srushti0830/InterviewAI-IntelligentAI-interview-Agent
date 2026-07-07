def build_question_prompt(candidate: dict) -> str:
    return f"""
You are an expert interviewer. Generate exactly five interview questions for a candidate.
Return ONLY JSON as an array of objects with this structure:
[
  {{"id":1,"question":"...","category":"...","difficulty":"..."}}
]

Candidate details:
- Name: {candidate.get('name')}
- Role: {candidate.get('role')}
- Experience: {candidate.get('experience')}
- Skills: {candidate.get('skills')}
- Difficulty: {candidate.get('difficulty')}

Requirements:
- Tailor questions to the role and experience.
- Include practical and technical depth based on difficulty.
- Use concise and professional wording.
- No commentary or extra text.
- If the role is AI Engineer, prefer questions that cover AI fundamentals, machine learning paradigms, prompt engineering, deployment, and AI project experience.
"""
