import pandas as pd
import json
import os
from llm_engine import LLMEngine
from data_extractor import extract_table
from queries import get_queries
from chatbot import CHATBOTENGINE

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class SecurityAuditor:
    def __init__(self):
        self.engine = LLMEngine()
        self.chatbot = CHATBOTENGINE()

    def load_security_data(self):
        try:
            extract_table(get_queries("password_profiles").get("query"), "password_profiles")
            extract_table(get_queries("system_privileges").get("query"), "system_privileges")
            extract_table(get_queries("users_roles").get("query"), "users_roles")
        
        
            users_roles = pd.read_csv(os.path.join(DATA_DIR, "users_roles.csv"))
            system_privs = pd.read_csv(os.path.join(DATA_DIR, "system_privileges.csv")).head(300)
            profiles = pd.read_csv(os.path.join(DATA_DIR, "password_profiles.csv"))
            
            return users_roles, system_privs, profiles
        except Exception as e:
            print(f"[ERROR] Failed to load security data: {e}")
            return None, None, None

    def analyze_security(self, is_chatbot=False):
        users_roles, system_privs, profiles = self.load_security_data()
        if users_roles is None:
            return

        users_roles_text = users_roles.to_string(index=False)
        system_privs_text = system_privs.to_string(index=False)
        profiles_text = profiles.to_string(index=False)

        if is_chatbot==False:
            return self.audit_page_resluts(users_roles_text,system_privs_text,profiles_text)
        else:
            return self.chatbot.assess_security(
                users_roles=users_roles_text,
                system_privileges=system_privs_text,
                password_profiles=profiles_text
            )
            
    def audit_page_resluts(self, users_roles_text,system_privs_text,profiles_text):
        analysis = self.engine.assess_security(
            users_roles=users_roles_text,
            system_privileges=system_privs_text,
            password_profiles=profiles_text
        )

        # Validation minimale : au moins 3 risques
        result = json.loads(analysis)
        if len(result.get("identified_risks", [])) < 3:
            print("[WARNING] Moins de 3 risques détectés")

        output_path = os.path.join(REPORTS_DIR, "security_audit_report.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"[SUCCESS] Security audit report saved to {output_path}")
        return result

    def format_users_roles(self, df):
        lines = []
        lines.append("| Username | Role | Account Status |\n")
        lines.append("|----------|------|----------------|\n")
        for _, row in df.iterrows():
            lines.append(f"| {row.get('username', '')} | {row.get('role', '')} | {row.get('account_status', '')} |\n")
        return "".join(lines)

    def format_system_privileges(self, df):
        lines = []
        lines.append("| Grantee | Privilege | Admin Option |\n")
        lines.append("|---------|-----------|--------------|\n")
        for _, row in df.iterrows():
            lines.append(f"| {row.get('grantee', '')} | {row.get('privilege', '')} | {row.get('admin_option', '')} |\n")
        return "".join(lines)
    
    def format_password_profiles(self, df):
        lines = []
        lines.append("| Profile Name | Password Life Time | Password Reuse Max |\n")
        lines.append("|--------------|--------------------|--------------------|\n")
        for _, row in df.iterrows():
            lines.append(f"| {row.get('profile', '')} | {row.get('password_life_time', '')} | {row.get('password_reuse_max', '')} |\n")
        return "".join(lines)
