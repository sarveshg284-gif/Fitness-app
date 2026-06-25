from kafka import KafkaProducer
import json
import pandas as pd
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

df = pd.read_csv("creditcard.csv")

for _, row in df.iterrows():
    producer.send("transactions", row.to_dict())
    print("Sent transaction")
    time.sleep(1)
