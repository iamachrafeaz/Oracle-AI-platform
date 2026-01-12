# **Unified Security Audit – Best Practices & Security Log Analysis**

## **Contexte / Objectif**

Ce document présente **Oracle Unified Auditing**, le mécanisme centralisé d’audit permettant de tracer les opérations sensibles dans une base Oracle.
Il synthétise les principes clés, les bonnes pratiques et les exemples SQL essentiels pour sécuriser, analyser et contrôler les activités critiques.

---

## **Points clés**

* **Unified Auditing** centralise tous les mécanismes d’audit Oracle dans un cadre unique.
* Les **politiques d’audit** permettent de cibler précisément les actions à surveiller.
* Les logs sont enregistrés dans la vue **UNIFIED_AUDIT_TRAIL**.
* L’audit peut se baser sur :

  * des actions,
  * des privilèges,
  * des rôles,
  * des conditions dynamiques.
* Une activation correcte permet de détecter les comportements anormaux, frauduleux ou non conformes.

---

## **Bonnes pratiques**

* Activer l'audit pour les **comptes privilégiés** : `SYS`, `SYSTEM`, `DBA`.
* Auditer les **opérations critiques** :

  * `CREATE USER`
  * `DROP TABLE`
  * `GRANT`
  * `ALTER SYSTEM`
* Créer des **AUDIT POLICIES** dédiées pour les applications sensibles.
* Consulter régulièrement **UNIFIED_AUDIT_TRAIL** pour détecter les anomalies.
* Exporter les logs vers un **SIEM** externe : Splunk, ELK, QRadar.
* Éviter les audits trop larges → risque de surcharge des performances.

---

## **Exemples SQL (Oracle)**

### **Créer une politique d’audit pour les actions administratives sensibles**

```sql
CREATE AUDIT POLICY audit_admin_actions
ACTIONS ALTER SYSTEM, CREATE USER, DROP USER;
```

### **Activer cette politique pour SYSDBA**

```sql
AUDIT POLICY audit_admin_actions BY sysdba;
```

### **Consulter les logs d’audit**

```sql
SELECT event_timestamp,
       dbusername,
       action_name,
       return_code
FROM unified_audit_trail
ORDER BY event_timestamp DESC;
```

### **Auditer toutes les connexions échouées**

```sql
CREATE AUDIT POLICY audit_failed_login
WHEN 'SYS_CONTEXT(''USERENV'', ''AUTHENTICATION_METHOD'') IS NOT NULL'
ACTIONS LOGON;
```

---

## **Pièges courants**

* Activer un audit global et non ciblé → **grosse charge** sur la base.
* Oublier de vérifier régulièrement les logs → perte de visibilité.
* Créer une politique sans l’activer → **audit inopérant**.
* Penser que l’audit est un mécanisme de protection →
  👉 il **détecte**, mais **ne bloque pas**.

---

## **Quand utiliser Unified Auditing ?**

* En environnements soumis à conformité :

  * **PCI-DSS**
  * **HIPAA**
  * **ISO 27001**
* En cas d’investigation de comportements suspects.
* Pour tracer les actions d’un compte privilégié.
* Lors de la sécurisation d’opérations administratives sensibles.

---

## **Résumé essentiel**

**Unified Auditing** centralise la traçabilité des actions critiques dans Oracle.
Avec des politiques ciblées et bien configurées, il devient un outil puissant pour surveiller, analyser et renforcer la sécurité de la base tout en permettant une exploitation simple des logs via **UNIFIED_AUDIT_TRAIL**.

---


