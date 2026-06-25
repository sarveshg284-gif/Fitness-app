import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import os

import parser
import skill
import score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening & Job Recommendation System")

# ---------------- LOAD MODEL ----------------
MODEL_PATH = "models/role_prediction.pkl"

if os.path.exists(MODEL_PATH):
    model = pickle.load(open(MODEL_PATH, "rb"))
else:
    st.error("❌ Model not found. Run train.py first.")
    st.stop()

# ---------------- SKILL LIST ----------------
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

# ---------------- UPLOAD FILE ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF/DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file:

    # Extract text
    text = parser.extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    with st.expander("View Resume Text"):
        st.write(text[:5000])

    # Extract skills
    skills = skill.extract_skills(text)

    st.subheader("🧠 Extracted Skills")

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No skills found")

    # ATS Score
    ats_score = score.calculate_ats_score(skills, text)

    st.subheader("📊 ATS Score")
    st.progress(ats_score / 100)
    st.metric("Score", f"{ats_score}%")

    # Feature vector for ML model
    feature_vector = [
        1 if s in skills else 0 for s in skill_list
    ]

    # Prediction
    prediction = model.predict([feature_vector])[0]

    st.subheader("🎯 Predicted Job Role")
    st.success(prediction)

    # Recommendations
    recommendations = {
        "Data Scientist": ["ML Engineer", "AI Engineer", "Data Scientist"],
        "Data Analyst": ["Business Analyst", "Data Analyst", "Reporting Analyst"],
        "Data Engineer": ["Data Engineer", "Big Data Engineer", "Cloud Engineer"],
        "AI Engineer": ["AI Engineer", "NLP Engineer", "Deep Learning Engineer"]
    }

    st.subheader("💼 Recommended Jobs")

    for job in recommendations.get(prediction, []):
        st.write("✅", job)

    # Skill chart
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

    # Missing skills
    missing = [s for s in skill_list if s not in skills]

    st.subheader("⚠️ Missing Skills")

    if missing:
        st.warning(", ".join(missing[:10]))

    # Download report
    report = f"""
ATS SCORE: {ats_score}

PREDICTED ROLE: {prediction}

SKILLS FOUND:
{', '.join(skills)}

MISSING SKILLS:
{', '.join(missing)}
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="resume_report.txt"
    )
