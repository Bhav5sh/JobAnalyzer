import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_career_advice(resume_text, job_role, matched_skills, missing_skills, ats_score):
    prompt = f"""
You are a career advisor AI.

Below is a candidate's resume and analysis results:
---
Job Role: {job_role}
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}
ATS Score: {ats_score}/100
Resume Text:
\"\"\"
{resume_text}
\"\"\"

Now, write a short and realistic career guidance note (5-6 lines). Include:
- Praise for strengths
- Advice for improvement
- Encouragement and motivation

Avoid anything fake or exaggerated. Be honest but supportive.
"""

    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
