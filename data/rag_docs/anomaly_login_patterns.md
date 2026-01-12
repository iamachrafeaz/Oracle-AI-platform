
# **Connexions inhabituelles & IP / horaire suspect dans Oracle**

## **Contexte / Objectif**

Ce document décrit les **patterns de connexion anormaux** dans Oracle, incluant :

* IP suspectes
* Heures inhabituelles
* Connexions répétées

L’objectif est de **détecter des intrusions** ou des comportements **non conformes**, pour renforcer la sécurité et alimenter la base RAG.

---

## **Points clés**

* Connexions en dehors des **heures business normales**.
* Accès depuis des **adresses IP inhabituelles** ou géographiquement éloignées.
* **Connexions multiples échouées** consécutives.
* Comptes utilisés **simultanément depuis différents sites**.

---

## **Bonnes pratiques**

* Créer des règles pour détecter les **connexions hors plage horaire**.
* Maintenir une **liste blanche d’IP** et surveiller les exceptions.
* Mettre en place des **alertes automatiques** pour tentatives répétées.
* Corréler les logs avec l’**activité métier** pour réduire les faux positifs.

---

## **Exemples Oracle SQL**

### Connexions hors heures normales

```sql
SELECT username, logon_time, host
FROM dba_audit_session
WHERE TO_CHAR(logon_time,'HH24') NOT BETWEEN 08 AND 18;
```

### Tentatives multiples échouées

```sql
SELECT username, COUNT(*) AS failed_attempts
FROM dba_audit_session
WHERE returncode != 0
GROUP BY username
HAVING COUNT(*) > 3;
```

### Connexions depuis IP inhabituelle

```sql
SELECT username, userhost, logon_time
FROM dba_audit_session
WHERE userhost NOT IN ('192.168.0.%','10.0.0.%');
```

---

## **Pièges à éviter**

* Ignorer les **scripts automatisés** qui déclenchent de faux alertes.
* Ne pas tenir compte des **fuseaux horaires** pour les utilisateurs distants.
* Se limiter aux **tentatives échouées** et ignorer les connexions réussies suspectes.

---

## **Quand utiliser ?**

* Pour la **détection d’intrusions réseau** ou d’accès non autorisés.
* Lors de la configuration d’un **monitoring RAG ou LLM** sur la sécurité.
* Pour l’**audit périodique** des activités utilisateur.

---

## **Résumé essentiel**

Surveiller les **patterns de login** permet d’identifier les accès non autorisés et les tentatives d’intrusion.
L’**automatisation** et la **corrélation avec le contexte métier** améliorent la précision de détection et enrichissent la base RAG.

