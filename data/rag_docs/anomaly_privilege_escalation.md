# **Escalade de privilèges dans Oracle**

## **Contexte / Objectif**

Ce document traite de la **détection des incidents d’escalade de privilèges** dans Oracle.
L’objectif est de **repérer quand un utilisateur obtient plus de droits que prévu**, volontairement ou par erreur, et de documenter les **patterns de détection** pour sécuriser la base.

---

## **Points clés**

* Escalades fréquentes : **GRANT DBA**, **ALTER USER**, création de rôle critique.
* Les utilisateurs normaux **ne doivent pas posséder de privilèges ANY**.
* Les changements inattendus dans les privilèges sont un **indicateur critique de risque**.
* La **corrélation avec les logs de connexion** aide à déterminer si l’action est suspecte.

---

## **Bonnes pratiques**

* Auditer régulièrement `DBA_SYS_PRIVS` et `DBA_ROLE_PRIVS`.
* Créer des **alertes automatiques** pour tout GRANT sur privilèges critiques.
* Documenter chaque changement et le valider via un **workflow de contrôle**.
* Comparer les privilèges **avant et après chaque modification majeure**.
* Limiter la **durée des privilèges temporaires** pour réduire l’exposition.

---

## **Exemples Oracle SQL**

### **Identifier les escalades de privilèges**

```sql
SELECT grantee, privilege, granted_by, timestamp
FROM unified_audit_trail
WHERE privilege IN ('DBA','ADMIN','SELECT ANY TABLE')
ORDER BY timestamp DESC;
```

### **Vérifier les rôles sensibles**

```sql
SELECT grantee, granted_role
FROM dba_role_privs
WHERE granted_role='DBA';
```

### **Corréler avec la connexion de l’utilisateur**

```sql
SELECT username, logon_time, host
FROM dba_audit_session
WHERE username='APP_USER';
```

---

## **Pièges à éviter**

* Supposer que tout **GRANT est légitime** sans contexte.
* Ignorer les **privilèges temporaires** attribués par scripts automatisés.
* Ne pas vérifier **l’activité subséquente** de l’utilisateur après l’escalade.

---

## **Quand utiliser ?**

* Pour la **détection proactive** d’accès non autorisé.
* Lors d’**audits de sécurité périodiques**.
* Pour enrichir la base **RAG avec des exemples d’escalade**.
* Pour créer des **alertes en temps réel** sur les changements critiques de privilèges.

---

## **Résumé essentiel**

L’escalade de privilèges est un **indicateur clé de risque** dans Oracle.
Une **surveillance continue**, combinée à la corrélation avec l’activité des utilisateurs, permet de **prévenir les incidents** et de **réagir rapidement** aux accès non autorisés.

