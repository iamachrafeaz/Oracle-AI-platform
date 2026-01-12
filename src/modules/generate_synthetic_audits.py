#note : in case no auidt logs are available, generate synthetic usingg this file itss note a module, "needs to be deleted after use"
import pandas as pd
import os
from datetime import datetime, timedelta
import random
import json

# Dossier de sortie
DATA_DIR = os.path.join(os.path.dirname(__file__), "oracle_raw")
os.makedirs(DATA_DIR, exist_ok=True)

# Liste d'utilisateurs simulés
users = ["ORACLE_AI", "ADMIN", "DEV_USER", "APP_USER"]

# Types d'actions
actions = ["LOGIN", "LOGOUT", "CREATE_TABLE", "DROP_TABLE", "GRANT_PRIVILEGE", "ALTER_USER"]

# Générer 15 logs simulés
logs = []
now = datetime.now()
for i in range(15):
    log = {
        "event_timestamp": (now - timedelta(minutes=random.randint(0, 1000))).strftime("%Y-%m-%d %H:%M:%S"),
        "dbusername": random.choice(users),
        "action_name": random.choice(actions),
        "return_code": random.choice([0, 1])  # 0 = succès, 1 = échec
    }
    logs.append(log)

# --- Export CSV ---
csv_file = os.path.join(DATA_DIR, "audit_logs.csv")
df = pd.DataFrame(logs)
df.to_csv(csv_file, index=False)
print(f"[INFO] audit_logs.csv créé avec {len(df)} lignes → {csv_file}")

# --- Export JSON ---
json_file = os.path.join(DATA_DIR, "audit_logs.json")
with open(json_file, "w") as f:
    json.dump(logs, f, indent=2)
print(f"[INFO] audit_logs.json créé avec {len(logs)} lignes → {json_file}")
