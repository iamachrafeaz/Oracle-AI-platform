# Oracle — Exemples Concrets de Logs Anormaux

## 1. Contexte / Objectif

Ce document fournit des exemples réels de logs Oracle présentant des anomalies ou comportements suspects.
Objectif : constituer une **base d’entraînement RAG** et aider un LLM à **détecter automatiquement les incidents potentiels**.

---

# 2. Points clés

* Les logs d’audit fournissent les informations essentielles :
  **utilisateur, action, objet, timestamp, SQL_ID, durée**, etc.
* Anomalies typiques :

  * suppression d’objets critiques
  * opérations DDL non planifiées
  * tentatives de connexion multiples échouées
  * requêtes anormalement coûteuses ou répétées
* L’analyse des patterns récurrents permet la détection de comportements malveillants ou accidentels.

---

# 3. Bonnes pratiques

### ✔ Gestion & Historique

* Conserver un historique **suffisant** pour permettre les comparaisons temporelles.
* Utiliser `UNIFIED_AUDIT_TRAIL` ou `AUD$` pour centraliser les logs.

### ✔ Annotation & Classification

* Annoter chaque log par **niveau de sévérité** :
  *normal / suspect / critique*.
* Fournir des exemples variés pour améliorer la robustesse du modèle RAG.

### ✔ Automatisation

* Automatiser l’analyse via scripts ou via un LLM.
* Corréler les logs entre eux (temps, utilisateur, objet, fréquence).

---

# 4. Exemples de logs Oracle

## 4.1 Tentative de suppression d’objet critique

```
USER=FINANCE
ACTION=DROP TABLE
OBJ=PAYMENTS
TIMESTAMP=2025-05-20 10:45
SEVERITY=CRITICAL
```

## 4.2 Connexions échouées répétées

```
USER=APP_USER
ACTION=LOGON FAILED
TIMESTAMP=2025-05-20 22:05
COUNT=6
SEVERITY=SUSPECT
```

## 4.3 Requête longue et coûteuse

```
USER=REPORTING
ACTION=SELECT
SQL_ID=abcd1234
ELAPSED_TIME=125000ms
SEVERITY=SUSPECT
```

---

# 5. Pièges à éviter

* Confondre des logs de **maintenance planifiée** avec des anomalies.
* Ignorer le **contexte métier**, les horaires ou les plages de maintenance.
* Se concentrer uniquement sur les logs récents sans vision historique.

---

# 6. Quand utiliser ?

* Pour entraîner un système RAG ou un LLM à détecter les anomalies Oracle.
* Lors d’audits réguliers pour identifier incidents et dérives passées.
* Pour générer des alertes automatiques en cas de comportements suspects.

---

# 7. Résumé essentiel

Ces exemples illustrent les scénarios les plus fréquents d’anomalies de logs Oracle.
Les collecter, les structurer et les annoter correctement est essentiel pour automatiser la détection et la prévention des incidents.

