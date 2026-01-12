# RMAN Playbooks — Full Restore / PITR / Table-Level Recovery

## 1. Contexte / Objectif

Ce document décrit les scénarios courants de restauration Oracle et fournit un guide pratique pour chaque cas.
Objectif : permettre une récupération **rapide, fiable et sécurisée** en cas de crash ou de perte de données.

---

# 2. Points clés

### Principaux scénarios de restauration

* **Restauration complète** après crash
* **Récupération point-in-time (PITR)**
* **Restauration d’une table spécifique**
* **Récupération de lignes spécifiques** (PITR au niveau data)

### Conditions essentielles

* Backups valides et accessibles
* Stratégie de restauration documentée
* Étapes incluant validation → restauration → tests post-recovery

---

# 3. Bonnes pratiques

### ✔ Préparation & Validation

* Vérifier la disponibilité et l’intégrité des backups.
* Réaliser les restaurations en environnement de test avant la production, lorsque possible.

### ✔ Documentation & Process

* Documenter toutes les étapes avec les commandes exactes.
* Prévoir un plan de communication pour les interruptions impacts.

### ✔ Automatisation & Sécurité

* Automatiser les procédures via scripts RMAN pour réduire les erreurs humaines.
* Vérifier les permissions, catalogues, et fichiers de contrôle utilisés.

---

# 4. Exemples Oracle SQL / RMAN

## 4.1 Restauration complète

```rman
RESTORE DATABASE;
RECOVER DATABASE;
```

---

## 4.2 Restauration Point-In-Time (PITR)

```rman
RUN {
    SET UNTIL TIME "TO_DATE('2025-12-01 14:00:00', 'YYYY-MM-DD HH24:MI:SS')";
    RESTORE DATABASE;
    RECOVER DATABASE;
}
```

---

## 4.3 Restauration d’une table spécifique

```rman
RECOVER TABLE SCOTT.EMP
    UNTIL TIME '2025-12-01 14:00';
```

---

# 5. Pièges à éviter

* Restaurer sans vérifier quel est le **dernier backup valide**.
* Oublier les **tablespaces**, fichiers de contrôle ou archives nécessaires.
* Ne pas prévenir les utilisateurs (faisabilité / interruption).
* Négliger les **tests post-restauration** (vérification de cohérence).

---

# 6. Quand utiliser ces procédures ?

* Après un **crash complet** ou une **corruption grave**.
* Pour récupérer une table ou des lignes supprimées accidentellement.
* Lors de tests réguliers de stratégie de backup ou sessions de formation DBA.
* Pour vérifier la conformité et l’efficacité des procédures RMAN.

---

# 7. Résumé essentiel

Les playbooks de restauration RMAN assurent que toutes les situations de perte de données peuvent être traitées efficacement et en toute sécurité.
Une procédure fiable repose sur :

* une documentation complète,
* des tests réguliers,
* des backups vérifiés,
* une exécution maîtrisée des scénarios.

---


