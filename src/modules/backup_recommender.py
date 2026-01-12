import os
import json
from llm_engine import LLMEngine
from chatbot import CHATBOTENGINE

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_metrics")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class BackupPlanner:
    def __init__(self):
        self.engine = LLMEngine()
        self.chatbot = CHATBOTENGINE()

    def collect_metrics(self):
       
        # Exemple statique pour démonstration
        metrics = {
            "db_size_gb": 0.6,
            "daily_tx_volume": 0,
            "data_criticality": "élevée"
        }
        return metrics

    def recommend_backup_strategy(self, rpo, rto, budget, is_chatbot=False):
        metrics = self.collect_metrics()

        metrics_text = (
            f"Taille base: {metrics.get('db_size_gb', 'Information non disponible')} GB\n"
            f"Volume transactions journalier: {metrics.get('daily_tx_volume', 'Information non disponible')}\n"
            f"Criticité des données: {metrics.get('data_criticality', 'Information non disponible')}"
        )

        if is_chatbot==False:
            return self.anomaly_page_result(rpo, rto, budget, metrics_text=metrics_text)
        else :
            return self.chatbot.recommend_backup_strategy(rpo, rto, budget, metrics=metrics_text)
    
    def anomaly_page_result(self,rpo, rto, budget, metrics_text):
        # Appel LLM
        response = self.engine.recommend_backup_strategy(
            rpo=rpo,
            rto=rto,
            budget=budget,
            metrics=metrics_text
        )

        # Supposons que la réponse est un JSON valide
        result = json.loads(response)
        return result
        
    
    def save_report(self, strategy, filename="backup_strategy_report.json"):
        output_path = os.path.join(REPORTS_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(strategy, f, indent=2)
        print(f"[SUCCESS] Backup strategy report saved to {output_path}")

