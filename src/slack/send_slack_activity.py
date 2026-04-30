import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

query = """
SELECT 
    sh.id,
    sh.id_salarié,
    eb.nom,
    eb.prénom,
    sh.type,
    sh.distance_m,
    sh.temps_écoulé_s,
    sh.commentaire
FROM sport_history sh
LEFT JOIN employee_benefits eb
    ON sh.id_salarié = eb.id_salarié
ORDER BY sh.date_de_début DESC
LIMIT 1;
"""

activity = pd.read_sql(query, engine).iloc[0]

distance_km = (
    round(activity["distance_m"] / 1000, 1)
    if pd.notnull(activity["distance_m"])
    else None
)

duration_min = round(activity["temps_écoulé_s"] / 60)

if distance_km:
    message = (
        f"Bravo {activity['prénom']} {activity['nom']} ! "
        f"Tu viens de faire {distance_km} km en {duration_min} min "
        f"en {activity['type']} ! 🔥🏅"
    )
else:
    message = (
        f"Bravo {activity['prénom']} {activity['nom']} ! "
        f"Belle séance de {activity['type']} pendant {duration_min} min ! 🔥🏅"
    )

if activity["commentaire"]:
    message += f" Commentaire : {activity['commentaire']}"

if slack_webhook_url:
    response = requests.post(slack_webhook_url, json={"text": message})
    response.raise_for_status()
    print("✅ Message envoyé dans Slack")
else:
    print("⚠️ Aucun webhook Slack configuré.")
    print("Message simulé :")
    print(message)