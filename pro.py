import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Fraud Detection", layout="wide")

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="refresh")

st.title("💳 REAL-TIME FRAUD DETECTION SYSTEM")

conn = sqlite3.connect("fraud.db")
df = pd.read_sql("SELECT * FROM transactions ORDER BY id DESC", conn)
conn.close()

if df.empty:
    st.warning("Waiting for live transactions...")
    st.stop()

total = len(df)
fraud = len(df[df["prediction"] == 1])
normal = len(df[df["prediction"] == 0])

fraud_rate = round((fraud / total) * 100, 2)

# METRICS
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Transactions", total)
c2.metric("Fraud", fraud)
c3.metric("Normal", normal)
c4.metric("Fraud %", f"{fraud_rate}%")

# LIVE ALERT
latest = df.iloc[0]

if latest["prediction"] == 1:
    st.error("🚨 LIVE FRAUD DETECTED!")
else:
    st.success("System Running Normally")

# CHARTS
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        names=["Fraud", "Normal"],
        values=[fraud, normal],
        title="Fraud Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(
        x=["Fraud", "Normal"],
        y=[fraud, normal],
        title="Transaction Summary"
    )
    st.plotly_chart(fig2, use_container_width=True)

# TABLE
st.subheader("Latest Transactions")
st.dataframe(df.head(20), use_container_width=True)

# DOWNLOAD
csv = df.to_csv(index=False)
st.download_button("Download Report", csv, "fraud_report.csv", "text/csv")
