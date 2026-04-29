import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

rh_file = "data/raw/Donnees_RH.xlsx"
sport_file = "data/raw/Donnees_Sportive.xlsx"

df_rh = pd.read_excel(rh_file)
df_sport = pd.read_excel(sport_file)

df_rh.columns = df_rh.columns.str.lower().str.replace(" ", "_")
df_sport.columns = df_sport.columns.str.lower().str.replace(" ", "_")

df_rh.to_sql("rh_raw", engine, if_exists="replace", index=False)
df_sport.to_sql("sport_raw", engine, if_exists="replace", index=False)

print("✅ Données chargées dans PostgreSQL")