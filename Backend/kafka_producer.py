from kafka import KafkaProducer
import json
import time
import random
import pandas as pd

# Load dataset to simulate transactions
df = pd.read_csv("data/creditcard.csv")
transactions = df.drop("Class", axis=1).to_dict(orient="records")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'transactions'

print(f"Sending transactions to topic '{topic_name}'...")

try:
    while True:
        transaction = random.choice(transactions)
        producer.send(topic_name, transaction)
        print(f"Sent transaction: {transaction}")
        time.sleep(1)  # send 1 transaction per second
except KeyboardInterrupt:
    print("Stopped producing transactions.")
finally:
    producer.close()
