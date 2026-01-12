# **Privilèges Oracle à risque et bonnes pratiques**

## **Contexte / Objectif**

Ce document décrit les **privilèges sensibles** dans Oracle, fournit des **exemples concrets d’accès à risque**, et propose les **meilleures pratiques pour les corriger**.
L’objectif est de **faciliter l’audit de sécurité** et de réduire la surface d’attaque d’une base Oracle.

---

## **Points clés**

* **Privilèges SYSTEM** : impact global sur la base, peuvent être dangereux.
* **Privilèges OBJECT** : spécifiques à un schéma, souvent surexposés.
* **Privilèges ANY** : les plus critiques (CREATE ANY, DROP ANY, SELECT ANY TABLE).
* **Rôles par défaut** (CONNECT, RESOURCE) : à éviter en production.
* **Excès de privilèges** : augmente le risque de manipulation non autorisée.

---

## **Bonnes pratiques**

* Éviter les privilèges **ANY** sauf nécessité absolue.
* Créer des **rôles dédiés** pour les applications au lieu de GRANT individuels multiples.
* Restreindre l’exposition des objets sensibles (tables de facturation, paiements, RH).
* Vérifier régulièrement les privilèges via `DBA_TAB_PRIVS` et `DBA_SYS_PRIVS`.
* Documenter tous les privilèges accordés en production.
* Révoquer les privilèges temporaires dès que possible.

---

## **Exemples Oracle SQL**

### **Détection des privilèges système à haut risque**

```sql
SELECT * 
FROM dba_sys_privs 
WHERE privilege LIKE '%ANY%';
```

### **Privilège dangereux accordé à un utilisateur**

```sql
GRANT SELECT ANY TABLE TO reporting_user;
-- Correction recommandée :
GRANT SELECT ON sales TO reporting_user;
```

### **Rôle trop permissif**

```sql
GRANT RESOURCE TO app_user;
-- Correction :
CREATE ROLE app_min_role;
GRANT CREATE TABLE, CREATE VIEW TO app_min_role;
GRANT app_min_role TO app_user;
```

### **Lister les privilèges objet accordés à un utilisateur**

```sql
SELECT table_name, privilege 
FROM dba_tab_privs 
WHERE grantee='APP_USER';
```

---

## **Pièges à éviter**

* Utiliser **SELECT ANY TABLE** pour un dépannage temporaire.
* Donner **CREATE ANY PROCEDURE** à un développeur.
* Oublier de **révoquer des privilèges temporaires**.
* Réutiliser un **rôle applicatif** pour plusieurs environnements.

---

## **Quand utiliser ?**

* Lors d’un **audit interne de sécurité**.
* Quand une application **accède trop largement aux données**.
* Après une **migration Oracle** ou un **changement de configuration**.
* Pour **réduire la surface d’attaque** d’un environnement critique.

---

## **Résumé essentiel**

Les privilèges **ANY** et les **rôles génériques** représentent les principales sources de risque dans Oracle.
Une politique stricte basée sur :

* la **granularité des droits**,
* les **rôles dédiés**,
* la **révision régulière des privilèges**,

permet de limiter les accès excessifs ou dangereux tout en maintenant la productivité et la sécurité.

---


