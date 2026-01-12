import os
from llm_engine import LLMEngine

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class RestoreRecoveryAssistant:
    def __init__(self):
        self.engine = LLMEngine()

    def generate_playbook(self, scenario, have_rman_backups, target_datetime=None, table_name=None, row_info=None):
        
        playbook_md = self.engine.recovery_strategy(
                scenario=scenario, 
                have_rman_backups=have_rman_backups,
                target_datetime=target_datetime,
                table_name=table_name,
                row_info=row_info
            )
        
        output_filename = f"restore_playbook_{scenario.replace(' ', '_').lower()}.md"
        output_path = os.path.join(REPORTS_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(playbook_md)

        print(f"[SUCCESS] Playbook saved to {output_path}")
        return playbook_md



if __name__ == "__main__":
    assistant = RestoreRecoveryAssistant()
    assistant.generate_playbook(
        scenario="Récupération point-in-time (PITR)",
        have_rman_backups="Oui",
        target_datetime="2026-01-15 14:00:00")