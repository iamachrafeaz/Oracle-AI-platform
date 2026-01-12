# src/modules/llm_engine.py
import yaml
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROMPTS_PATH = os.path.join(BASE_DIR, "data", "chatbot_prompts.yaml")

# Env
load_dotenv(os.path.join(BASE_DIR, ".env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("[INFO] OPENAI_API_KEY loaded:", bool(OPENAI_API_KEY))

# Groq Client 
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1/",

    api_key=OPENAI_API_KEY
)

# LLM Engine
class CHATBOTENGINE:
    def __init__(self, prompts_path=PROMPTS_PATH):
        with open(prompts_path, "r", encoding="utf-8") as f:
            self.prompts = yaml.safe_load(f)

        self.groq_client = groq_client
        self.ollama_model = "llama3.2:3b"

    # Core generation
    def generate(self, prompt, context=None, retries=3):
        full_prompt = prompt if not context else f"{context}\n\n{prompt}"

        for attempt in range(1, retries + 1):
            try:
                response = self.groq_client.responses.create(
                    input=full_prompt,
                    model="openai/gpt-oss-20b"
                )
                return response.output_text

                
            except Exception as e:
                print(f"[WARN] Tentative {attempt} échouée : {e}")
                time.sleep(1)

        return "Erreur : échec après plusieurs tentatives."

    # Module 4
    def analyze_query(self, sql_query, plan):
        system_instruction = self.prompts["analyze_query"]["system"]
        user_template = self.prompts["analyze_query"]["user"]

        user_prompt = user_template.format(
            sql_query=sql_query, 
            execution_plan=plan
        )

        full_instruction = f"{system_instruction}\n\n{user_prompt}"

        return self.generate(full_instruction)
    
    # Module 5
    def assess_security(self, users_roles, system_privileges, password_profiles):
        system_instruction = self.prompts["analyze_security"]["system"]
        user_template = self.prompts["analyze_security"]["user"]

        user_prompt = user_template.replace("{users_roles}", users_roles) \
                           .replace("{system_privileges}", system_privileges) \
                           .replace("{password_profiles}", password_profiles)


        full_instruction = f"{system_instruction}\n\n{user_prompt}"

        return self.generate(full_instruction)
    
    # Module 6
    def detect_anomaly(self, log_text, context=None):
        system_instruction = self.prompts["analyze_anomaly"]["system"]
        user_template = self.prompts["analyze_anomaly"]["user"]

        user_prompt = user_template.replace("{audit_log}", log_text)

        full_instruction = f"{system_instruction}\n\n{user_prompt}"

        answer = self.generate(full_instruction)
                
        return answer
    
    # Module 7
    def recommend_backup_strategy(self, prompt):
        system_instruction = self.prompts["backup_strategy"]["system"]
        user_template = self.prompts["backup_strategy"]["user"]

        user_prompt = user_template.replace("{demande}", prompt)\

        full_instruction = f"{system_instruction}\n\n{user_prompt}"

        return self.generate(full_instruction)
    
    # Module 8
    def recovery_strategy(self, prompt):
        system_instruction = self.prompts["restore_recovery"]["system"]
        user_template = self.prompts["restore_recovery"]["user"]
        
        user_prompt = user_template.replace("{question}", str(prompt))

        full_instruction = f"{system_instruction}\n\n{user_prompt}"

        return self.generate(full_instruction)
    
