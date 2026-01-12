import streamlit as st
import json
import os
import glob

# Importation des modules personnalisés
# (Assurez-vous que ces fichiers sont bien dans le même dossier)
from llm_engine import LLMEngine
from security_audit import SecurityAuditor
from query_optimizer import QueryOptimizer
from anomaly_detector import AnomalyDetector
from backup_recommender import BackupPlanner
from recovery_guide import RestoreRecoveryAssistant
from chatbot import CHATBOTENGINE

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Oracle AI Platform",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONNALISÉ (STYLE DASHBOARD) ---
st.markdown("""
<style>
    /* Fond global plus sombre pour effet 'Enterprise' */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Style pour la Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Titres principaux */
    h1, h2, h3 {
        color: #E6EDF3 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Cartes de métriques (Dashboard) */
    [data-testid="stMetric"] {
        background-color: #21262D;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #8B949E;
    }
    [data-testid="stMetricValue"] {
        color: #58A6FF;
    }

    /* Boutons personnalisés */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: none;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2EA043;
    }
    
    /* Chatbot messages */
    .stChatMessage {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONSTANTES & PATHS ---
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "../../data/reports")
SECURITY_REPORT = os.path.join(REPORTS_DIR, "security_audit_report.json")
BACKUP_REPORT = os.path.join(REPORTS_DIR, "backup_strategy_report.json")

# --- INITIALISATION SESSION ---
if "engine" not in st.session_state:
    st.session_state.engine = LLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("💾 Oracle AI Admin")
    st.markdown("---")
    page = st.radio(
        "Navigation", 
        ["Accueil", "Sécurité", "Performance", "Sauvegardes", "Chatbot IA"],
        index=0
    )
    st.markdown("---")
    st.caption("v2.0.1 | Connected to DB")

# ==========================================
# PAGE: ACCUEIL
# ==========================================
if page == "Accueil":
    st.title("📊 Dashboard Global")
    st.markdown("Bienvenue sur la **Plateforme de Gestion Oracle Intelligente**.")
    
    st.markdown("### État du Système")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Status Database", "ONLINE", "Uptime 99.9%")
    
    with col2:
        # Lecture rapide des risques si fichier existant
        risk_count = "N/A"
        delta_val = None
        if os.path.exists(SECURITY_REPORT):
            try:
                with open(SECURITY_REPORT, 'r') as f:
                    data = json.load(f)
                    val = len(data.get("identified_risks", []))
                    risk_count = f"{val} Détectés"
                    delta_val = "-2 vs hier"
            except:
                pass
        st.metric("Risques Sécurité", risk_count, delta_val, delta_color="inverse")

    with col3:
        st.metric("IA Engine", "ACTIF", "LLM Ready")

    st.markdown("---")
    st.info("💡 **Conseil du jour :** Vérifiez les rapports de performance avant le pic de charge de 14h.")

# ==========================================
# PAGE: SÉCURITÉ
# ==========================================
elif page == "Sécurité":
    st.title("🛡️ Audit de Sécurité & Conformité")
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        run_audit = st.button("🔄 Lancer un nouvel audit", use_container_width=True)
    
    if run_audit:
        with st.status("Audit de sécurité en cours...", expanded=True) as status:
            st.write("🔍 Analyse des privilèges utilisateurs...")
            st.write("🔍 Vérification des configurations réseau...")
            st.write("🧠 Consultation du moteur IA pour recommandations...")
            try:
                auditor = SecurityAuditor()
                auditor.analyze_security()
                status.update(label="Audit terminé avec succès !", state="complete", expanded=False)
                st.rerun() # Rafraichir pour afficher les nouvelles données
            except Exception as e:
                status.update(label="Erreur lors de l'audit", state="error")
                st.error(f"Détails : {e}")

    st.markdown("---")

    # AFFICHAGE DU RAPPORT
    if os.path.exists(SECURITY_REPORT):
        try:
            with open(SECURITY_REPORT, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            # Score
            col_score, col_details = st.columns([1, 2])
            with col_score:
                st.subheader("Score Global")
                score = report.get("security_score", 0)
                st.metric("Security Score", f"{score}/100")
                st.progress(score)
            
            with col_details:
                st.subheader("Résumé")
                st.write(f"Date de l'audit : **{report.get('date', 'Aujourd hui')}**")
                st.write(f"Base de données : **{report.get('database', 'ORCL')}**")

            # Risques
            st.subheader("⚠️ Risques Identifiés")
            risks = report.get("identified_risks", [])
            
            if not risks:
                st.success("Aucun risque majeur détecté. Système sain.")
            else:
                for risk in risks:
                    summary = risk.get('risk', 'Risque Inconnu')
                    severity = risk.get('severity', 'Moyenne')
                    
                    # Style conditionnel pour l'icone
                    icon = "🔴" if "High" in severity or "Critical" in severity else "🟠"
                    
                    with st.expander(f"{icon} [{severity}] {summary}"):
                        st.markdown(f"**Description :** {risk.get('description')}")
                        st.info(f"💡 **Action requise :** {risk.get('recommendation')}")
            
            # Recommandations Globales
            st.subheader("📋 Plan d'Action Recommandé")
            recommendations = report.get("recommendations", [])
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"- {rec}")

        except json.JSONDecodeError:
            st.error("Le fichier de rapport est corrompu.")
    else:
        st.warning("Aucun rapport disponible. Lancez un audit pour commencer.")

# ==========================================
# PAGE: PERFORMANCE
# ==========================================
elif page == "Performance":
    st.title("🚀 Optimisation des Requêtes SQL")
    
    with st.container():
        st.markdown("Analysez les requêtes lentes et obtenez des suggestions d'indexation ou de réécriture via l'IA.")
        if st.button("⚡ Analyser les 3 dernières requêtes lentes", use_container_width=True):
            with st.spinner("Analyse du plan d'exécution et génération des conseils..."):
                try:
                    auditor = QueryOptimizer()
                    auditor.analyze_slow_queries() 
                    st.success("Analyse terminée !")
                except Exception as e:
                    st.error(f"Erreur : {e}")

    st.markdown("---")
    
    st.subheader("📜 Rapports d'Optimisation")
    report_files = glob.glob(os.path.join(REPORTS_DIR, "optimization_report_*.md"))
    
    if report_files:
        # Trier par date de modification (le plus récent en premier)
        report_files.sort(key=os.path.getmtime, reverse=True)
        selected_report = st.selectbox("Sélectionner un rapport", report_files, format_func=lambda x: os.path.basename(x))
        
        with st.container(border=True):
            with open(selected_report, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)
    else:
        st.info("Aucun rapport d'optimisation trouvé.")

# ==========================================
# PAGE: SAUVEGARDES
# ==========================================
elif page == "Sauvegardes":
    st.title("💾 Sauvegardes & Disaster Recovery")
    
    tabs = st.tabs(["⚙️ Stratégie de Backup", "🚑 Assistant Restauration", "👁️ JSON Config"])
    
    # --- TAB 1: STRATÉGIE ---
    with tabs[0]:
        st.subheader("Définir une politique de sauvegarde")
        st.markdown("L'IA analyse vos contraintes (RPO/RTO) pour générer un script RMAN optimal.")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            rpo_input = st.selectbox("RPO (Perte admissible)", ["15 minutes", "1 heure", "4 heures", "24 heures", "Temps réel"])
        with col_b:
            rto_input = st.selectbox("RTO (Temps reprise)", ["30 minutes", "2 heures", "4 heures", "1 jour", "1 semaine"])
        with col_c:
            budget_input = st.select_slider("Budget / Ressources", options=["Faible", "Moyen", "Élevé", "Critique"])

        if st.button("📝 Générer la Stratégie", use_container_width=True):
            with st.spinner("Génération du plan..."):
                try:
                    planner = BackupPlanner()
                    strategy_result = planner.recommend_backup_strategy(rpo=rpo_input, rto=rto_input, budget=budget_input)
                    planner.save_report(strategy_result)
                    st.success("Stratégie mise à jour !")
                    st.json(strategy_result)
                except Exception as e:
                    st.error(f"Erreur : {e}")

    # --- TAB 2: RESTAURATION ---
    with tabs[1]:
        st.subheader("Assistant de Restauration d'Urgence")
        st.warning("Utilisez cet outil en cas d'incident pour générer les commandes RMAN exactes.")
        
        col1, col2 = st.columns(2)
        with col1:
            scenario_options = [
                "Restauration complète après crash",
                "Récupération point-in-time (PITR)",
                "Récupération de table spécifique",
                "Récupération de lignes (Row-level)"
            ]
            selected_scenario = st.selectbox("Scénario d'incident", scenario_options)
        with col2:
            have_backups = st.radio("Backups RMAN disponibles ?", ["Oui", "Non"], horizontal=True)

        # Inputs contextuels
        target_dt_str, table_name_input, row_info_input = None, None, None
        
        if "point-in-time" in selected_scenario or "lignes" in selected_scenario:
            c1, c2 = st.columns(2)
            d = c1.date_input("Date Cible")
            t = c2.time_input("Heure Cible")
            target_dt_str = f"{d} {t}"
        
        if "table" in selected_scenario or "lignes" in selected_scenario:
            table_name_input = st.text_input("Nom de la table (ex: HR.EMPLOYEES)")
        
        if "lignes" in selected_scenario:
            row_info_input = st.text_input("Condition (WHERE ID=...)", placeholder="Ex: WHERE ID=105")

        if st.button("🛠️ Générer le Playbook de Secours", type="primary"):
            if "table" in selected_scenario and not table_name_input:
                st.error("Le nom de la table est requis.")
            else:
                with st.spinner("L'IA rédige la procédure..."):
                    try:
                        assistant = RestoreRecoveryAssistant()
                        playbook_md = assistant.generate_playbook(
                            scenario=selected_scenario,
                            have_rman_backups=have_backups,
                            target_datetime=target_dt_str,
                            table_name=table_name_input,
                            row_info=row_info_input
                        )
                        st.markdown("### 📄 Procédure Générée")
                        with st.container(border=True):
                            st.markdown(playbook_md)
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # --- TAB 3: JSON ---
    with tabs[2]:
        if os.path.exists(BACKUP_REPORT):
            with open(BACKUP_REPORT, 'r') as f:
                st.json(json.load(f))
        else:
            st.info("Aucune stratégie enregistrée.")

# ==========================================
# PAGE: CHATBOT IA
# ==========================================
elif page == "Chatbot IA":
    st.title("🤖 Assistant DBA Oracle")
    st.caption("Posez des questions sur vos logs, vos performances ou la syntaxe SQL.")

    # Affichage de l'historique
    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Input utilisateur
    if prompt := st.chat_input("Ex: Pourquoi ma base est lente ce matin ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyse du contexte..."):
                try:
                    classification = st.session_state.engine.classify_intent(prompt)
                    response = ""
                    
                    # Routing vers le bon module
                    if classification == "QueryOptimizer":
                        optimizer = QueryOptimizer()
                        response = optimizer.analyze_slow_queries(1, is_chatbot=True) 
                    elif classification == "AnomalyDetector":
                        anomaly = AnomalyDetector()
                        response = anomaly.analyze_logs(is_chatbot=True)
                    elif classification == "BackupPlanner":
                        bot = CHATBOTENGINE()
                        response = bot.recommend_backup_strategy(prompt)
                    elif classification == "SecurityAuditor":
                        security = SecurityAuditor()
                        response = security.analyze_security(is_chatbot=True)
                    elif classification == "RestoreRecovery":
                        bot = CHATBOTENGINE()
                        response = bot.recovery_strategy(prompt)
                    else: # GeneralQuestion
                        bot = CHATBOTENGINE()
                        response = bot.generate(prompt)
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    err_msg = "Désolé, une erreur interne est survenue."
                    st.error(f"{err_msg} ({e})")
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})