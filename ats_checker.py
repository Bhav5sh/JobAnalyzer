from job_skills_map import job_skills_map

def check_section_presence(resume_text):
    score = 0
    sections = ["education", "experience", "skills", "projects", "certifications", "summary"]
    found = [s for s in sections if s.lower() in resume_text.lower()]
    score = len(found) / len(sections) * 30  # 30% weight
    return score, found

def check_skill_match(predicted_role, extracted_skills):
    expected_skills = job_skills_map.get(predicted_role, [])
    matched = [skill for skill in expected_skills if skill.lower() in [s.lower() for s in extracted_skills]]
    match_score = len(matched) / len(expected_skills) * 50 if expected_skills else 0
    return match_score, matched

def check_format_quality(resume_text):
    lines = resume_text.strip().split("\n")
    too_short = len(lines) < 10
    too_long = len(lines) > 100
    if too_short:
        return 5  # very short resume
    elif too_long:
        return 10  # too long resume
    return 20  # good format

def calculate_ats_score(resume_text, predicted_role, extracted_skills):
    section_score, present_sections = check_section_presence(resume_text)
    skill_score, matched_skills = check_skill_match(predicted_role, extracted_skills)
    format_score = check_format_quality(resume_text)

    total = round(section_score + skill_score + format_score, 2)
    return {
        "total_score": total,
        "section_score": section_score,
        "present_sections": present_sections,
        "skill_score": skill_score,
        "matched_skills": matched_skills,
        "format_score": format_score
    }
