import os
import random
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine

load_dotenv()
fake = Faker("fr_FR")

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

rh = pd.read_sql("SELECT * FROM rh_raw", engine)
rh["id_salarié"] = rh["id_salarié"].astype(str)

sport_types = [
    "Course à pied",
    "Vélo",
    "Marche",
    "Randonnée",
    "Natation",
    "Escalade",
    "Tennis",
    "Fitness"
]

comments = [
    "",
    "Reprise du sport :)",
    "Super séance",
    "Sortie entre collègues",
    "Bon rythme aujourd'hui",
    "Belle progression",
    "Séance intense",
    "Activité tranquille"
]

start_period = datetime.now() - timedelta(days=365)
end_period = datetime.now()

rows = []
activity_id = 1

for _, employee in rh.iterrows():
    employee_id = employee["id_salarié"]

    # Simulation réaliste : certains salariés peu actifs, d'autres très actifs
    number_of_activities = random.randint(5, 45)

    for _ in range(number_of_activities):
        sport_type = random.choice(sport_types)
        start_date = fake.date_time_between(start_date=start_period, end_date=end_period)

        if sport_type == "Escalade":
            distance_m = None
            duration_s = random.randint(1800, 7200)
        elif sport_type == "Natation":
            distance_m = random.randint(500, 3000)
            duration_s = random.randint(1200, 5400)
        elif sport_type == "Course à pied":
            distance_m = random.randint(3000, 25000)
            duration_s = random.randint(1200, 9000)
        elif sport_type == "Vélo":
            distance_m = random.randint(5000, 80000)
            duration_s = random.randint(1800, 14400)
        elif sport_type == "Marche":
            distance_m = random.randint(1000, 15000)
            duration_s = random.randint(900, 7200)
        elif sport_type == "Randonnée":
            distance_m = random.randint(5000, 30000)
            duration_s = random.randint(3600, 21600)
        else:
            distance_m = random.randint(1000, 10000)
            duration_s = random.randint(1800, 7200)

        end_date = start_date + timedelta(seconds=duration_s)

        rows.append({
            "id": activity_id,
            "id_salarié": employee_id,
            "date_de_début": start_date,
            "type": sport_type,
            "distance_m": distance_m,
            "date_de_fin": end_date,
            "temps_écoulé_s": duration_s,
            "commentaire": random.choice(comments)
        })

        activity_id += 1

sport_history = pd.DataFrame(rows)

sport_history.to_sql("sport_history", engine, if_exists="replace", index=False)

print("✅ Historique sportif simulé généré")
print(f"Nombre de lignes générées : {len(sport_history)}")