import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Connexion PostgreSQL
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

# Paramètres métier
PRIME_RATE = 0.05
MIN_ACTIVITIES_WELLNESS_DAYS = 15
WELLNESS_DAYS_GRANTED = 5

# Chargement des données
rh = pd.read_sql("SELECT * FROM rh_raw", engine)
sport = pd.read_sql("SELECT * FROM sport_history", engine)

# Normalisation IDs
rh["id_salarié"] = rh["id_salarié"].astype(str)
sport["id_salarié"] = sport["id_salarié"].astype(str)

# Nettoyage salaire
rh["salaire_brut"] = pd.to_numeric(rh["salaire_brut"], errors="coerce").fillna(0)

# Détection des moyens de déplacement sportifs
sport_commute_keywords = [
    "marche",
    "running",
    "course",
    "vélo",
    "velo",
    "trottinette"
]

rh["moyen_de_déplacement_clean"] = (
    rh["moyen_de_déplacement"]
    .fillna("")
    .astype(str)
    .str.lower()
)

rh["eligible_prime_sportive"] = rh["moyen_de_déplacement_clean"].apply(
    lambda x: any(keyword in x for keyword in sport_commute_keywords)
)

rh["montant_prime_sportive"] = rh.apply(
    lambda row: row["salaire_brut"] * PRIME_RATE if row["eligible_prime_sportive"] else 0,
    axis=1
)

# Comptage des activités annuelles par salarié
activity_counts = (
    sport.groupby("id_salarié")
    .size()
    .reset_index(name="nombre_activites_annuelles")
)

# Fusion RH + activité sportive
employee_benefits = rh.merge(activity_counts, on="id_salarié", how="left")

employee_benefits["nombre_activites_annuelles"] = (
    employee_benefits["nombre_activites_annuelles"]
    .fillna(0)
    .astype(int)
)

# Éligibilité aux jours bien-être
employee_benefits["eligible_jours_bien_etre"] = (
    employee_benefits["nombre_activites_annuelles"] >= MIN_ACTIVITIES_WELLNESS_DAYS
)

employee_benefits["jours_bien_etre_accordes"] = employee_benefits[
    "eligible_jours_bien_etre"
].apply(lambda is_eligible: WELLNESS_DAYS_GRANTED if is_eligible else 0)

# KPI globaux
kpi_summary = pd.DataFrame([{
    "nombre_salaries": len(employee_benefits),
    "nombre_eligibles_prime": int(employee_benefits["eligible_prime_sportive"].sum()),
    "cout_total_prime": float(employee_benefits["montant_prime_sportive"].sum()),
    "nombre_eligibles_jours_bien_etre": int(employee_benefits["eligible_jours_bien_etre"].sum()),
    "total_jours_bien_etre": int(employee_benefits["jours_bien_etre_accordes"].sum()),
    "prime_rate": PRIME_RATE,
    "min_activities_wellness_days": MIN_ACTIVITIES_WELLNESS_DAYS
}])

# Export vers PostgreSQL
employee_benefits.to_sql("employee_benefits", engine, if_exists="replace", index=False)
kpi_summary.to_sql("kpi_summary", engine, if_exists="replace", index=False)

print("✅ Transformations métier terminées")
print(kpi_summary)