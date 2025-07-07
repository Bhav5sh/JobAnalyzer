import streamlit as st
from resume_parser import parse_resume
# from job_matcher import predict_job_roles
from sklearn.preprocessing import LabelEncoder
from llm_predictor import predict_job_roles_llm
import joblib
import pandas as pd
from skill_gap import calculate_skill_gap
from course_recommender import recommend_courses_dynamic
from ats_checker import calculate_ats_score
from career_advisor import generate_career_advice

st.set_page_config(page_title="Smart Career Predictor", layout="centered")
st.title("📄 Resume Analyzer ")
st.write("Upload your resume to extract text and basic info.")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file:
    resume_text, entities = parse_resume(uploaded_file)

    if resume_text:
        st.success("✅ Resume text extracted successfully!")
        st.subheader("📜 Extracted Resume Text")
        st.text_area("", resume_text, height=300)

        st.subheader("🧠 Detected Information")
        st.markdown(f"**Skills**: {', '.join(entities['skills']) or 'N/A'}")
        st.markdown(f"**Education**: {', '.join(entities['education']) or 'N/A'}")
        st.markdown(f"**Experience**: {', '.join(entities['experience']) or 'N/A'}")

        # ✅ Save entities in session
        st.session_state.resume_text = resume_text
        st.session_state.entities = entities
    else:
        st.error("❌ Failed to extract from the uploaded file.")

    # Load the salary model once
    salary_model = joblib.load("model/salary_model.pkl")

    # Use session state
    resume_text = st.session_state.get("resume_text", "")
    entities = st.session_state.get("entities", {"skills": []})

    # Predict job roles using Gemini
    if st.button("🤖 Predict Job Roles (AI-powered)"):
        if resume_text:
            with st.spinner("Analyzing your resume using Gemini AI..."):
                roles_output = predict_job_roles_llm(resume_text)
                st.subheader("🎯 AI-Suggested Job Roles")
                st.markdown(roles_output)

                # Save in session
                st.session_state.predicted_job_role = roles_output.split("\n")[0].split(".")[-1].strip()
        else:
            st.warning("⚠️ Please upload a resume first.")

    # Get job role from session or fallback
    predicted_job_role = st.session_state.get("predicted_job_role", "Data Analyst")

    st.subheader("💼 Salary Prediction")

    # Editable job role
    job_role = st.text_input("Predicted Job Role (editable)", value=predicted_job_role)

    # Experience input
    experience = st.slider("Years of Experience", 0, 15, 2)

    # ✅ Now this is safe
    skills_count = len(entities["skills"])

    if st.button("💰 Predict Salary"):
        X_input = pd.DataFrame([[job_role, experience, skills_count]],
                            columns=["job_role", "experience", "skills_count"])
        salary = salary_model.predict(X_input)[0]
        st.success(f"💸 Estimated Salary: ₹{int(salary):,} per year")


    st.subheader("🧠 Skill Gap Checker")

    present, missing = calculate_skill_gap(job_role, entities["skills"])

    st.markdown("✅ **Skills You Have:**")
    st.write(present if present else "None matched")

    st.markdown("❌ **Skills You Need to Learn:**")
    st.write(missing if missing else "No major skill gap found 🎉")


    st.subheader("🎓 Course Recommendations (Live from YouTube)")

    courses = recommend_courses_dynamic(missing)

    if courses:
        for skill, videos in courses.items():
            st.markdown(f"**📘 Learn {skill.capitalize()}:**")
            for course in videos:
                st.markdown(f"- [{course['title']}]({course['link']})")
    else:
        st.info("No course recommendations found.")


    st.subheader("📊 ATS Score Checker")

    ats = calculate_ats_score(resume_text, job_role, entities["skills"])
    st.metric(label="📈 ATS Score", value=f"{ats['total_score']}/100")

    with st.expander("📂 Section Coverage"):
        st.write(f"Sections Present: {ats['present_sections']}")
        st.write(f"Section Score: {ats['section_score']:.2f}/30")

    with st.expander("🔑 Skill Relevance"):
        st.write(f"Matched Skills: {ats['matched_skills']}")
        st.write(f"Skill Match Score: {ats['skill_score']:.2f}/50")

    with st.expander("📄 Formatting Quality"):
        st.write(f"Formatting Score: {ats['format_score']:.2f}/20")



    st.subheader("🧭 Career Advice Summary")

    if st.button("🧠 Generate Career Advice"):
        with st.spinner("Analyzing and generating advice..."):
            advice = generate_career_advice(
                resume_text=resume_text,
                job_role=job_role,
                matched_skills=ats["matched_skills"],
                missing_skills=missing,
                ats_score=ats["total_score"]
            )
            st.success("✅ Here's your personalized guidance:")
            st.markdown(advice)

