import json
import os

from dotenv import load_dotenv
from kafka import KafkaConsumer
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

client = WebClient(token=SLACK_BOT_TOKEN)

consumer = KafkaConsumer(
    "sport-activities",
    bootstrap_servers="localhost:19092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="sport-slack-consumer-live",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("👂 En attente d'activités sportives depuis Redpanda...")

for message in consumer:
    activity = message.value

    salarie = activity.get("salarie", "Un salarié")
    sport = activity.get("sport", "une activité sportive")
    distance_km = activity.get("distance_km")
    duree_min = activity.get("duree_min")

    if distance_km:
        slack_message = (
            f"🏃 Nouvelle activité sportive détectée\n\n"
            f"Employé : {salarie}\n"
            f"Sport : {sport}\n"
            f"Distance : {distance_km} km\n"
            f"Durée : {duree_min} minutes\n\n"
            f"Bravo {salarie} ! 🔥🏅"
        )
    else:
        slack_message = (
            f"🏃 Nouvelle activité sportive détectée\n\n"
            f"Employé : {salarie}\n"
            f"Sport : {sport}\n"
            f"Durée : {duree_min} minutes\n\n"
            f"Bravo {salarie} ! 🔥🏅"
        )

    print("📩 Message reçu depuis Redpanda")
    print(slack_message)

    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=slack_message,
        )
        print("✅ Notification Slack envoyée")
    except SlackApiError as e:
        print(f"❌ Erreur Slack : {e.response['error']}")