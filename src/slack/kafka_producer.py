import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:19092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

activity = {
    "salarie": "Samir Belasri",
    "sport": "Course à pied",
    "distance_km": 8.4,
    "duree_min": 47
}

producer.send("sport-activities", activity)

producer.flush()

print("✅ Activité envoyée dans Redpanda/Kafka")