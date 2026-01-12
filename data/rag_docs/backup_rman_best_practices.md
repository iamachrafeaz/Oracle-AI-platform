# RMAN Strategies — Frequency, Retention, Best Practices

## 1. Contexte / Objectif

Ce document présente les bonnes pratiques de sauvegarde Oracle avec **RMAN**.
Objectifs principaux :

* Garantir la disponibilité des données
* Respecter les exigences **RPO/RTO**
* Optimiser l’efficacité et la fiabilité des sauvegardes

---

# 2. Points clés

* RMAN permet des sauvegardes **complètes**, **incrémentales**, et **différentielles**.
* La **fréquence** dépend du volume de transactions et des besoins métiers (RPO).
* La **rétention** définit combien de sauvegardes conserver et pendant combien de temps.
* Les backups peuvent être stockés **localement ou à distance** (disk, tape, cloud).
* Les vérifications régulières (**VALIDATE**, **RESTORE TEST**) garantissent l’intégrité.

---

# 3. Bonnes pratiques

### ✔ Frequency & Backup Strategy

* Planifier :

  * **1 backup complet hebdomadaire**
  * **1 backup incrémental quotidien**
* Adapter la fréquence en fonction des SLA et du RPO.

### ✔ Retention & Compliance

* Définir une **rétention alignée sur la criticité** et les obligations légales.
* Mettre en place une rotation automatique des sauvegardes.

### ✔ Security & Integrity

* Chiffrer les sauvegardes pour protéger les données sensibles.
* Vérifier régulièrement les backups :

  * `VALIDATE`
  * tests de restauration (restore/recover) en environnement isolé.

### ✔ Architecture & Automation

* Utiliser un **RMAN catalog** pour centraliser et pérenniser l’historique.
* Automatiser l’exécution des sauvegardes et la purge.

---

# 4. Exemples RMAN

### Backup complet

```rman
BACKUP DATABASE;
```

### Backup incrémental niveau 1

```rman
BACKUP INCREMENTAL LEVEL 1 DATABASE;
```

### Configuration de la rétention

```rman
CONFIGURE RETENTION POLICY TO REDUNDANCY 2;
```

### Validation d’un backup

```rman
VALIDATE BACKUPSET 1;
```

---

# 5. Pièges à éviter

* Ne pas vérifier la cohérence des sauvegardes.
* Stocker des backups sur disque sans rotation → saturation et perte de rétention.
* Planifier les backups en pleine charge métier.
* Oublier le chiffrement pour des données sensibles.

---

# 6. Quand utiliser RMAN ?

* Pour les **sauvegardes régulières** en production (RPO/RTO).
* Avant une opération critique (upgrade, patch, migration).
* Pour prévenir la perte ou la corruption des données.
* Pour répondre aux exigences **audit** et **conformité**.

---

# 7. Résumé essentiel

RMAN permet de gérer efficacement les sauvegardes Oracle.
Une stratégie combinant :

* backups complets + incrémentaux,
* vérifications régulières,
* rétention adaptée,
* chiffrement,
* tests de restauration

garantit la **sécurité**, **disponibilité**, et **intégrité** des données.

---

