import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

from utils.parser import extract_text
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening & Job Recommendation System")

# Load model
model = pickle.load(open("models/role_prediction.pkl", "rb"))

skill_list = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "aws",
    "nlp",
    "tensorflow",
    "pytorch",
    "statistics",
    "spark"
]

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file:

    text = extract_text(uploaded_file)

    st.subheader("Resume Preview")

    with st.expander("View Resume Text"):
        st.write(text[:5000])

    skills = extract_skills(text)

    st.subheader("Extracted Skills")

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No skills found")

    ats_score = calculate_ats_score(
    skills,
    text
        )

    st.subheader("ATS Score")

    st.progress(ats_score / 100)
    st.metric("ATS Score", f"{ats_score}%")

    feature_vector = []

    for skill in skill_list:
        if skill in skills:
            feature_vector.append(1)
        else:
            feature_vector.append(0)

    prediction = model.predict([feature_vector])[0]

    st.subheader("Predicted Job Role")

    st.success(prediction)

    recommendations = {
        "Data Scientist": [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist"
        ],
        "Data Analyst": [
            "Business Analyst",
            "Data Analyst",
            "Reporting Analyst"
        ],
        "Data Engineer": [
            "Data Engineer",
            "Big Data Engineer",
            "Cloud Engineer"
        ],
        "AI Engineer": [
            "AI Engineer",
            "NLP Engineer",
            "Deep Learning Engineer"
        ]
    }

    st.subheader("Recommended Jobs")

    jobs = recommendations.get(prediction, [])

    for job in jobs:
        st.write("✅", job)

    chart_data = pd.DataFrame({
        "Skills": skill_list,
        "Available": feature_vector
    })

    fig = px.bar(
        chart_data,
        x="Skills",
        y="Available",
        color="Available",
        title="Skill Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    missing = []

    for skill in skill_list:
        if skill not in skills:
            missing.append(skill)

    st.subheader("Missing Skills")

    st.warning(", ".join(missing[:10]))

    report = f"""
    ATS Score: {ats_score}

    Predicted Role: {prediction}

    Skills:
    {', '.join(skills)}

    Missing Skills:
    {', '.join(missing)}
    """

    st.download_button(
        "Download Report",
        report,
        file_name="resume_report.txt"
    )
