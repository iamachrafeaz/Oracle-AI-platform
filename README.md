# Plateforme Oracle IA – Supervision, Sécurité et Optimisation Intelligente

**Réalisé par : Achraf EL AZZOUZI & Mehdi LAGHRISSI**

---

## 1. Présentation du projet

Cette plateforme est une application web développée en **Python + Streamlit**, destinée aux **DBA Oracle**, visant à centraliser :

- la **supervision**
- l’**audit de sécurité**
- l’**optimisation des performances**
- la **gestion des sauvegardes et restaurations**

L’analyse est enrichie par une **IA (LLM)** qui génère automatiquement :

- des scores,
- des diagnostics,
- des recommandations exploitables.

---

## 2. Modules Fonctionnels (vue synthétique)

- **Dashboard global** : état général (sécurité, performance, sauvegardes)
- **Audit de sécurité Oracle** : utilisateurs, rôles, privilèges, risques
- **Optimisation des performances** : requêtes lentes et recommandations SQL
- **Stratégie de sauvegarde intelligente** : RPO / RTO / budget
- **Assistant de restauration** : playbooks de reprise (PITR, crash, tables)
- **Chatbot IA Oracle** : interface conversationnelle orientée DBA

---

## 3. Architecture (résumé)

- Base de données **Oracle 19c**
- Extraction via **SQLAlchemy + oracledb**
- Données stockées en **JSON / CSV**
- IA utilisée comme **moteur d’analyse central**
- Application Streamlit comme interface unifiée

---

## 4. Environnement Oracle (Docker)

### Image utilisée

```text
oracle/database:19.3.0-ee
```

### Configuration recommandée (obligatoire)

```bash
docker run -d \
  --name oracle19 \
  --privileged \
  -m 6g \
  -p 1521:1521 \
  -p 5500:5500 \
  -v oracle_data:/opt/oracle/oradata \
  -e ORACLE_SID=ORCLCDB \
  -e ORACLE_PDB=ORCLPDB1 \
  -e ORACLE_PWD=oracle \
  oracle/database:19.3.0-ee
```

### Pourquoi ces réglages

| Élément        | Raison                  |
| -------------- | ----------------------- |
| `--privileged` | évite ORA-00800 / VKTM  |
| `-m 6g`        | évite l’OOM Killer      |
| `ORCLCDB`      | CDB racine              |
| `ORCLPDB1`     | PDB applicative         |
| volume Docker  | persistance des données |

---

## 5. CDB vs PDB (point clé)

👉 **Les utilisateurs applicatifs doivent être créés dans le PDB**, pas dans le CDB.

```sql
SHOW CON_NAME;
-- doit être ORCLPDB1
```

Si nécessaire :

```sql
ALTER SESSION SET CONTAINER = ORCLPDB1;
```

---

## 6. Création de l’utilisateur applicatif

### Création

```sql
CREATE USER oracle_ai IDENTIFIED BY oracle_ai_pwd;
GRANT CREATE SESSION TO oracle_ai;
```

### Droits nécessaires (lecture & analyse)

```sql
GRANT SELECT ANY DICTIONARY TO oracle_ai;
GRANT SELECT_CATALOG_ROLE TO oracle_ai;

GRANT SELECT ON V_$SQL TO oracle_ai;
GRANT SELECT ON V_$SQLSTATS TO oracle_ai;
GRANT SELECT ON V_$SQL_PLAN TO oracle_ai;
GRANT SELECT ON V_$SYSTEM_EVENT TO oracle_ai;
GRANT SELECT ON UNIFIED_AUDIT_TRAIL TO oracle_ai;
```

⚠️ Les vues `V$` sont en réalité des synonymes vers `V_$`.

---

## 7. Connexion depuis l’application Python

### Driver utilisé

- `oracledb` (driver officiel Oracle)
- intégré à SQLAlchemy

### URL de connexion

```python
oracle+oracledb://oracle_ai:oracle_ai_pwd@localhost:1521/?service_name=ORCLPDB1
```

---

## 8. Point d’attention SQLAlchemy

Les requêtes doivent être encapsulées avec `text()` :

```python
from sqlalchemy import text

conn.execute(text("SELECT sysdate FROM dual"))
```

---

## 9. Valeur ajoutée du projet

- Centralisation complète des décisions DBA
- Réduction des tâches manuelles répétitives
- Analyse intelligente et contextualisée
- Base solide pour une évolution vers **AIOps / SOC / Cloud**

---

## 10. Conclusion

La Plateforme Oracle IA démontre comment l’IA peut transformer la gestion des bases Oracle en un processus **proactif, intelligent et assisté**, tout en restant **compatible avec les pratiques DBA classiques**.
Elle constitue une fondation robuste pour des systèmes de supervision modernes et évolutifs.
