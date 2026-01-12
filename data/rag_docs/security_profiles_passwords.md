# Oracle — Password Policies & Profiles

## 1. Contexte / Objectif

Ce document décrit la gestion des **profils Oracle**, avec un focus sur :

* la sécurité des mots de passe
* la gestion des ressources utilisateurs
* l’homogénéisation des politiques de sécurité

Objectif : **renforcer la sécurité des comptes** et prévenir les accès non autorisés.

---

# 2. Points clés

### Les profils définissent :

* paramètres de mot de passe : durée de validité, complexité, tentatives échouées, verrouillage
* limites de ressources : sessions simultanées, CPU, I/O

### Règles de complexité recommandées :

* longueur minimale
* majuscules, minuscules
* chiffres
* caractères spéciaux

### Importance

* L’application systématique des profils assure une sécurité homogène
* Compatible avec les normes de conformité (ISO 27001, PCI-DSS, etc.)

---

# 3. Bonnes pratiques

### ✔ Sécurité renforcée

* Créer des profils **stricts** pour les comptes DBA et applicatifs sensibles.
* Activer `PASSWORD_VERIFY_FUNCTION` pour la vérification de complexité.

### ✔ Politique de verrouillage

* Configurer `FAILED_LOGIN_ATTEMPTS` (3 à 5 tentatives conseillées).

### ✔ Renouvellement régulier

* Utiliser :

  * `PASSWORD_LIFE_TIME` (validité du mot de passe)
  * `PASSWORD_GRACE_TIME` (délai avant expiration définitive)

### ✔ Supervision

* Surveiller les comptes verrouillés ou expirés via `DBA_USERS`.

---

# 4. Exemples Oracle SQL

## 4.1 Créer un profil sécurisé

```sql
CREATE PROFILE secure_profile
LIMIT
    FAILED_LOGIN_ATTEMPTS 5
    PASSWORD_LIFE_TIME    30
    PASSWORD_GRACE_TIME   5
    PASSWORD_REUSE_MAX    10
    PASSWORD_REUSE_TIME   90
    PASSWORD_VERIFY_FUNCTION verify_function;
```

---

## 4.2 Attribuer un profil à un utilisateur

```sql
ALTER USER finance_user PROFILE secure_profile;
```

---

## 4.3 Lister les utilisateurs et leurs profils

```sql
SELECT username, profile, account_status
FROM   dba_users;
```

---

# 5. Pièges à éviter

* Laisser le profil **DEFAULT** pour tous les utilisateurs.
* Ne pas activer les règles de complexité.
* Oublier de révoquer ou désactiver les comptes obsolètes.
* Ignorer la gestion de l’expiration des mots de passe.

---

# 6. Quand utiliser ces politiques ?

* Pour **tous les comptes en production**, particulièrement ceux avec accès sensible.
* Lors d’audits de sécurité ou de revue des mots de passe.
* Pour répondre aux obligations de conformité (ISO 27001, PCI-DSS).
* Pour limiter les attaques par brute force ou l’utilisation de comptes inactifs.

---

# 7. Résumé essentiel

Les profils Oracle permettent de standardiser et renforcer la sécurité des comptes.
L’application stricte des politiques de mot de passe et des limites de ressources **réduit les risques d’intrusion, d’abus et de compromission**.



