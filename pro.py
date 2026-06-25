import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from xgboost import XGBClassifier
import os

file_path = "creditcard.csv"

if not os.path.exists(file_path):
    st.error("creditcard.csv NOT FOUND. Please upload it to GitHub repo.")
    st.stop()

df = pd.read_csv(file_path)

st.set_page_config(page_title="XGBoost Fraud Detection", layout="wide")

st.title("💳 Real-Time Fraud Detection using XGBoost (AI Model)")

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("creditcard.csv")
    return df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# Train XGBoost Model
# -----------------------------
@st.cache_resource
def train_model(data):

    X = data.drop("Class", axis=1)
    y = data["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        eval_metric="logloss",
        use_label_encoder=False
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    return model, acc, y_test, y_pred

model, accuracy, y_test, y_pred = train_model(df)

# -----------------------------
# Metrics
# -----------------------------
st.subheader("Model Performance")

c1, c2 = st.columns(2)
c1.metric("Accuracy", f"{accuracy:.4f}")
c2.metric("Dataset Size", df.shape[0])

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

fig = ff.create_annotated_heatmap(
    z=cm,
    x=["Normal", "Fraud"],
    y=["Normal", "Fraud"],
    colorscale="Viridis"
)

st.subheader("Confusion Matrix")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Fraud Distribution
# -----------------------------
fraud = len(df[df["Class"] == 1])
normal = len(df[df["Class"] == 0])

fig2 = px.pie(
    names=["Normal", "Fraud"],
    values=[normal, fraud],
    title="Fraud vs Normal Transactions"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Live Prediction Input
# -----------------------------
st.subheader("🔍 Test Transaction")

input_data = {}

for col in df.columns:
    if col != "Class":
        input_data[col] = st.number_input(col, value=float(df[col].mean()))

if st.button("Predict Fraud"):

    input_df = pd.DataFrame([input_data])

    pred = model.predict(input_df)[0]

    if pred == 1:
        st.error("🚨 FRAUD DETECTED")
    else:
        st.success("✅ NORMAL TRANSACTION")

# -----------------------------
# Classification Report
# -----------------------------
st.subheader("Classification Report")

report = classification_report(y_test, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())
