from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

df = pd.read_csv("creditcard.csv")

for _, row in df.iterrows():
    data = row.to_dict()

    producer.send("transactions", data)

    print("Sent transaction")

    time.sleep(0.5)   # REAL-TIME SPEED
