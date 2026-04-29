import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

output_dir = "reports/tableau"

tables = {
    "employee_benefits": "employee_benefits.csv",
    "kpi_summary": "kpi_summary.csv",
    "sport_history": "sport_history.csv"
}

for table, filename in tables.items():
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    path = f"{output_dir}/{filename}"
    df.to_csv(path, index=False)
    print(f"✅ Export terminé : {path} ({len(df)} lignes)")