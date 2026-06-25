import streamlit as st
import pandas as pd
import random
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

st.set_page_config(page_title="AI Fraud Detection", layout="wide")

st.title("💳 AI-Based Fraud Detection System (Machine Learning)")

# ----------------------------
# Train model inside app (simple demo version)
# ----------------------------
@st.cache_resource
def train_model():
    # synthetic dataset (for demo on Streamlit Cloud)
    data = pd.DataFrame({
        "Amount": np.random.uniform(10, 5000, 1000),
        "Time": np.random.randint(1, 1000, 1000),
        "OldBalance": np.random.uniform(0, 10000, 1000),
        "NewBalance": np.random.uniform(0, 10000, 1000),
    })

    # fake rule to generate labels (fraud pattern)
    data["Fraud"] = (
        (data["Amount"] > 3000) |
        (data["NewBalance"] > data["OldBalance"] * 1.5)
    ).astype(int)

    X = data.drop("Fraud", axis=1)
    y = data["Fraud"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model

model = train_model()

# ----------------------------
# Session storage
# ----------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ----------------------------
# Generate transaction
# ----------------------------
def generate_transaction():
    return {
        "Amount": round(random.uniform(10, 5000), 2),
        "Time": random.randint(1, 1000),
        "OldBalance": round(random.uniform(1000, 10000), 2),
        "NewBalance": round(random.uniform(0, 15000), 2),
    }

# ----------------------------
# Predict fraud
# ----------------------------
def predict_fraud(tx):
    df = pd.DataFrame([tx])
    return int(model.predict(df)[0])

# ----------------------------
# Buttons
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Generate Transaction"):
        tx = generate_transaction()
        tx["Prediction"] = predict_fraud(tx)
        st.session_state.transactions.append(tx)

with col2:
    if st.button("🔄 Generate 10 Transactions"):
        for _ in range(10):
            tx = generate_transaction()
            tx["Prediction"] = predict_fraud(tx)
            st.session_state.transactions.append(tx)

# ----------------------------
# DataFrame
# ----------------------------
df = pd.DataFrame(st.session_state.transactions)

if df.empty:
    st.warning("Click button to generate transactions")
    st.stop()

# ----------------------------
# Metrics
# ----------------------------
total = len(df)
fraud = len(df[df["Prediction"] == 1])
normal = total - fraud

c1, c2, c3 = st.columns(3)

c1.metric("Total Transactions", total)
c2.metric("Fraud Detected", fraud)
c3.metric("Normal", normal)

# ----------------------------
# Alert
# ----------------------------
latest = df.iloc[-1]

if latest["Prediction"] == 1:
    st.error("🚨 AI DETECTED FRAUD IN LATEST TRANSACTION")
else:
    st.success("AI System Running Normally")

# ----------------------------
# Charts
# ----------------------------
left, right = st.columns(2)

with left:
    fig1 = px.pie(
        names=["Fraud", "Normal"],
        values=[fraud, normal],
        title="Fraud Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

with right:
    fig2 = px.bar(
        x=["Fraud", "Normal"],
        y=[fraud, normal],
        title="Fraud Analysis"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Table
# ----------------------------
st.subheader("Transaction History")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Download
# ----------------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Report",
    csv,
    "fraud_report.csv",
    "text/csv"
)
