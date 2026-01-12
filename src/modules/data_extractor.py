import os
import json
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

load_dotenv()

DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASSWORD")
DB_HOST = os.getenv("ORACLE_HOST")
DB_PORT = os.getenv("ORACLE_PORT")
DB_SERVICE = os.getenv("ORACLE_SERVICE")

# Dossier de sortie CSV/JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
os.makedirs(DATA_DIR, exist_ok=True)

# Fichier JSON simulant AUD$ si la table est vide
AUDIT_JSON_FILE = os.path.join(DATA_DIR, "synthetic_audits.json")

# CRÉER LE ENGINE SQLALCHEMY
engine = create_engine(
    f'oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}'
)

# EXTRACTION D'UNE TABLE/VUE
def extract_table(query, output_name, fallback_json=None):
    try:
        df = pd.read_sql(query, engine)
        if df.empty and fallback_json:
            with open(fallback_json, "r") as f:
                df = pd.DataFrame(json.load(f))
        if df.empty:
            print(f"[WARNING] {output_name} est vide !")
        # Export CSV
        df.to_csv(os.path.join(DATA_DIR, f"{output_name}.csv"), index=False)
        # Export JSON
        df.to_json(os.path.join(DATA_DIR, f"{output_name}.json"), orient="records", indent=2)
        print(f"[INFO] {output_name} extrait avec succès, {len(df)} lignes.")
    except Exception as e:
        print(f"[ERROR] Extraction {output_name} a échoué : {e}")


# TEST DE CONNEXION 
def test_connection():
    try:
        with engine.connect() as conn:
            # On encapsule la string dans text()
            query = text("SELECT sysdate FROM dual")
            result = conn.execute(query)
            
            print("[INFO] Connexion OK, sysdate =", result.fetchone()[0])
    except Exception as e:
        print("[ERROR] Connexion échouée :", e)

if __name__ == "__main__":
    print(test_connection())
    