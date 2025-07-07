from job_skills_map import job_skills_map

def calculate_skill_gap(predicted_role, user_skills):
    required_skills = job_skills_map.get(predicted_role, [])
    user_skills_lower = [s.lower() for s in user_skills]

    present = list(set(skill for skill in required_skills if skill in user_skills_lower))
    missing = list(set(skill for skill in required_skills if skill not in user_skills_lower))

    return present, missing
