from kafka import KafkaConsumer
import json
import pandas as pd
import sqlite3
import joblib
from alerts import send_alert

model = joblib.load("fraud_model.pkl")

conn = sqlite3.connect("fraud.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    prediction INTEGER
)
""")

conn.commit()

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for msg in consumer:
    data = msg.value

    amount = float(data.get("Amount", 0))

    X = pd.DataFrame([data])
    if "Class" in X.columns:
        X = X.drop("Class", axis=1)

    pred = int(model.predict(X)[0])

    cursor.execute(
        "INSERT INTO transactions (amount, prediction) VALUES (?, ?)",
        (amount, pred)
    )

    conn.commit()

    if pred == 1:
        send_alert(amount)
        print("FRAUD DETECTED")
    else:
        print("NORMAL")
