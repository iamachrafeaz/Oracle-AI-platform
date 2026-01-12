import pandas as pd
import os
from llm_engine import LLMEngine
from rag_setup import RagModule2
from data_extractor import extract_table
from queries import get_queries
from chatbot import CHATBOTENGINE


# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/oracle_raw")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class QueryOptimizer:
    def __init__(self):
        self.engine = LLMEngine()
        self.rag = RagModule2()
        self.chatbot = CHATBOTENGINE()
        
    def load_performance_data(self):
        try:
            extract_table(get_queries("sqlstat").get("query"), "sqlstat")
            extract_table(get_queries("sql_plan").get("query"), "sql_plan")
        
            stats = pd.read_csv(os.path.join(DATA_DIR, "sqlstat.csv"))
            plans = pd.read_csv(os.path.join(DATA_DIR, "sql_plan.csv"))
            
            return stats, plans
        except Exception as e:
            print(f"[ERROR] Could not load performance data: {e}")
            return None, None
        
    def analyze_slow_queries(self, top_n=3, is_chatbot=False):
        stats, plans = self.load_performance_data()
        if stats is None or plans is None:
            return

        slow_queries = stats.sort_values(by="elapsed_time", ascending=False).head(top_n)
        
        all_analysis = []
         
        for _, row in slow_queries.iterrows():
            sql_id = row['sql_id']
            query_plan = plans[plans['sql_id'] == sql_id].to_dict(orient='records')
            
            print(f"[INFO] Analyzing sql_id: {sql_id}...")
            
            if is_chatbot == False :
                analysis = self.engine.analyze_query(
                    sql_query=f"sql_id: {sql_id}", 
                    plan=self.format_plan_text(query_plan),
                )
                
                all_analysis.append(analysis)
        
                for i in range(len(all_analysis)) :
                    output_path = os.path.join(REPORTS_DIR, "optimization_report_"+str(i)+".md")
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(all_analysis[i])
                    
                print(f"[SUCCESS] Optimization report saved to {output_path}")
                return analysis
            else :
                return self.chatbot.analyze_query(
                    sql_query=f"sql_id: {sql_id}", 
                    plan=self.format_plan_text(query_plan),
                )
                
                
    
    def format_plan_text(self, plan_records):
        lines = []
        lines.append("Execution Plan:\n")
        lines.append("| Id | Operation | Object | Cost | Rows |\n")
        lines.append("----------------------------------------\n")

        for p in plan_records:
            lines.append(
                f"| {p.get('id')} | {p.get('operation')} | "
                f"{p.get('object_name','')} | "
                f"{p.get('cost')} | {p.get('cardinality')} |\n"
            )
        return "".join(lines)
    
