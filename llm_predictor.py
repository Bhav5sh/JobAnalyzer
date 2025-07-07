import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def predict_job_roles_llm(resume_text):
    prompt = f"""
You are an AI career advisor.

Based on the following resume, suggest the top 3 realistic and relevant job roles that match the candidate's skills, experience, and education.

Only suggest real, industry-accepted roles. Avoid fictional or vague titles.

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond in this format:
1. Job Role 1
2. Job Role 2
3. Job Role 3
"""

    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
