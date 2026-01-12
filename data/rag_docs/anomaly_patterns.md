
# **Patterns généraux de comportements anormaux**

## **Contexte / Objectif**

Ce document décrit les principaux **patterns de comportements anormaux ou suspects** observables dans une base de données Oracle.
L’objectif est de faciliter la **détection d’incidents de sécurité**, de comportements inattendus ou d’anomalies opérationnelles à travers l’analyse des logs, des audits et de l’activité utilisateur.

---

## **Points clés**

Les anomalies peuvent toucher plusieurs catégories :

* **Connexions** : horaires inhabituels, origine anormale, tentatives échouées.
* **Requêtes** : volume élevé, performances dégradées, requêtes atypiques.
* **Privilèges** : escalade inattendue ou utilisation anormale de privilèges sensibles.
* **Modifications DDL** : création, suppression ou altération non autorisée d’objets critiques.

### **Patterns typiques**

* Connexions **en dehors des heures normales**.
* **Tentatives répétées** et rapprochées de login échoué.
* **Escalade de privilèges** ou GRANT inattendu.
* Suppression ou modification de **tables sensibles**.
* Volume inhabituel d’opérations coûteuses (FULL SCAN, massive DELETE, etc.).
* Déviation par rapport au comportement habituel d’un utilisateur.

L’identification repose sur la **corrélation** entre logs d’audit, activité utilisateur et métriques de performance.

---

## **Bonnes pratiques**

* Définir des règles de détection dans **UNIFIED_AUDIT_TRAIL**, `AUD$`, ou le SIEM connecté.
* Construire un **baseline** de comportement normal (heures, fréquence, privilèges utilisés).
* Mettre en place des **alertes automatiques** pour les patterns critiques (connexion anormale, GRANT suspect…).
* Utiliser **RAG + LLM** pour analyser des séquences rares, longues ou difficiles à corréler manuellement.
* Documenter chaque pattern observé, sa **sévérité** et sa **cause possible**.
* Réviser régulièrement les règles selon l’évolution des usages et des applications.

---

## **Exemples Oracle SQL**

### **Connexions hors horaires de bureau**

```sql
SELECT username, logon_time
FROM dba_audit_session
WHERE TO_CHAR(logon_time, 'HH24') NOT BETWEEN 08 AND 18;
```

### **Escalades de privilèges suspectes**

```sql
SELECT username, privilege, action_name, timestamp
FROM unified_audit_trail
WHERE action_name LIKE '%GRANT%'
  AND privilege IN ('DBA', 'ADMIN');
```

### **Suppression d’objets critiques**

```sql
SELECT username, obj_name, obj_type, timestamp
FROM unified_audit_trail
WHERE action_name LIKE '%DROP%'
  AND obj_type = 'TABLE';
```

---

## **Pièges à éviter**

* Confondre anomalies et activités légitimes (**batch**, CRON, maintenance).
* Négliger la mise à jour des patterns selon les nouveaux usages.
* Se contenter d’une analyse **manuelle** → manque de réactivité.
* Ignorer les **petites anomalies répétitives**, souvent signe précurseur d’intrusion.
* Oublier que le contexte métier est essentiel (une anomalie n’est pas toujours une attaque).

---

## **Quand utiliser ces patterns ?**

* Pour la **détection proactive** d’intrusions ou d’activités malveillantes.
* Lors des audits réguliers portant sur les opérations sensibles.
* Pour alimenter un système RAG avec des exemples de comportements **normaux vs suspects**.
* Pour créer des **alertes intelligentes** basées sur LLM, SIEM ou scripts.

---

## **Résumé essentiel**

L’identification des patterns d’anomalies est un élément clé de la sécurité Oracle.
En combinant **audit**, **corrélation des logs**, **baselines comportementales** et **automatisation via RAG/LLM**, il devient possible de détecter rapidement les activités suspectes et de réduire significativement les risques de compromission.

---

