from kafka import KafkaConsumer
import json
import joblib
import pandas as pd

model = joblib.load("fraud_model.pkl")

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in consumer:
    data = msg.value

    X = pd.DataFrame([data]).drop("Class", axis=1, errors='ignore')

    prediction = model.predict(X)

    if prediction[0] == 1:
        print("FRAUD DETECTED")
    else:
        print("Normal Transaction")
