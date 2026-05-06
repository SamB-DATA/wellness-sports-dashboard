from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

client = WebClient(token=SLACK_BOT_TOKEN)

message = """
🏃 Nouvelle activité sportive détectée

Employé : Samir Belasri
Sport : Course à pied
Durée : 47 minutes
Distance : 8.4 km

✅ Prime sportive potentiellement attribuée
"""

try:
    response = client.chat_postMessage(
        channel=SLACK_CHANNEL,
        text=message
    )

    print("✅ Message Slack envoyé avec succès")

except SlackApiError as e:
    print(f"❌ Erreur Slack : {e.response['error']}")