import pandas as pd
import os

from llm_engine import LLMEngine
from data_extractor import extract_table
from queries import get_queries
from chatbot import CHATBOTENGINE 

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class AnomalyDetector:
    def __init__(self):
        self.engine = LLMEngine()
        self.chatbot = CHATBOTENGINE()
        
    def load_audit_logs(self):
        try:
            extract_table(get_queries("audit_logs").get("query"), "audit_logs")
            logs = pd.read_csv(os.path.join(DATA_DIR, "audit_logs.csv"))
            return logs
        except Exception as e:
            print(f"[ERROR] Could not load audit logs: {e}")
            return None

    def analyze_logs(self, top_n = 10, is_chatbot=False):
        logs = self.load_audit_logs()
        if logs is None:
            return
        
        if is_chatbot==False:
            return self.anomaly_page_results(logs.head(top_n))
        else :
            return self.chat_results(logs.head(top_n))
    
    def anomaly_page_results(self, selected_log):
        all_reports = []
    
        for idx, row in selected_log.iterrows():
            log_text = (
                    f"Timestamp: {row.get('event_timestamp', '')}, "
                    f"User: {row.get('userid', '')}, "
                    f"Host: {row.get('userhost', '')}, "
                    f"Action: {row.get('ACTION#', '')}, "
                    f"Object: {row.get('obj$name', '')}, "
                    f"Privilege: {row.get('priv$used', '')}, "
                    f"SQL: {row.get('sqltext', '')}, "
                    f"Comment: {row.get('comment$text', '')}, "
                    f"Return code: {row.get('comment_text', '')}, "
            )

            if not log_text:
                print(f"[WARNING] Empty log text at index {idx}")
                continue

            print(f"[INFO] Analyzing audit log index {idx}...")

            # Call LLM with the user prompt filled with log text as plain text
            analysis = self.engine.detect_anomaly(
                log_text=log_text
            )

            all_reports.append(analysis)

            # Save each report as individual markdown file
            output_path = os.path.join(REPORTS_DIR, f"anomaly_report_{idx}.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(analysis)
            print(f"[SUCCESS] Anomaly reports saved to {REPORTS_DIR}")
            return all_reports
    
    def chat_results(self,selected_log):
        all_logs = []
    
        for idx, row in selected_log.iterrows():
            log_text = (
                    f"Timestamp: {row.get('event_timestamp', '')}, "
                    f"User: {row.get('userid', '')}, "
                    f"Host: {row.get('userhost', '')}, "
                    f"Action: {row.get('ACTION#', '')}, "
                    f"Object: {row.get('obj$name', '')}, "
                    f"Privilege: {row.get('priv$used', '')}, "
                    f"SQL: {row.get('sqltext', '')}, "
                    f"Comment: {row.get('comment$text', '')}, "
                    f"Return code: {row.get('comment_text', '')}, "
            )

            if not log_text:
                print(f"[WARNING] Empty log text at index {idx}")
                continue

            all_logs.append(log_text)
        
        return self.chatbot.detect_anomaly(
            log_text=" ".join(all_logs)
        )
        
          
        
if __name__ == "__main__":
    print(get_queries("audit_logs"))
