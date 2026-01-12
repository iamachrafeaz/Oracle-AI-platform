# Playbook de Restauration & Récupération Oracle

## 1. Introduction
Récupération point‑in‑time (PITR) pour la base Oracle en utilisant les sauvegardes RMAN disponibles afin d’atteindre la date/heure cible **2026‑01‑11 16:13:00**. La table et la ligne spécifiques ne sont pas définies; la restauration porte donc sur l’ensemble de la base.

## 2. Étapes détaillées
1. **Préparer l’environnement**  
   - Vérifier que la base de données est arrêtée.  
   - Vérifier la cohérence des fichiers de contrôle et de la configuration RMAN.  
2. **Connecter RMAN**  
   - Se connecter en tant que `sysdba` sur le serveur cible.  
3. **Réinitialiser l’historique de récupération**  
   - Exécuter `RESTORE DATABASE` jusqu’à la cible, puis `RECOVER DATABASE`.  
4. **Vérifier les fichiers de contrôle**  
   - S’assurer que le fichier de contrôle pointe vers la dernière image de contrôle disponible.  
5. **Appliquer la récupération**  
   - Restaurer les blocs modifiés jusqu’à la cible.  
6. **Redémarrer la base**  
   - Utiliser `STARTUP MOUNT` puis `RECOVER DATABASE` si nécessaire, suivi de `STARTUP OPEN`.  
7. **Valider la restauration**  
   - Vérifier l’intégrité des tablespaces et des fichiers de données.  

## 3. Commandes RMAN
```sql
-- Connexion RMAN
rman target /

-- Étape 1 : Vérifier l’état de la base
STARTUP MOUNT;
SHOW DATABASE STATUS;

-- Étape 2 : Réinitialiser la base à la cible
RESTORE DATABASE;
RECOVER DATABASE UNTIL TIME '2026-01-11 16:13:00';

-- Étape 3 : Vérifier la cohérence
RECOVER DATABASE UNTIL TIME '2026-01-11 16:13:00' SKIP UNRECOVERABLE;

-- Étape 4 : Redémarrer la base
STARTUP OPEN;
```

## 4. Points de validation
- **Validation de l’historique RMAN** : `LIST BACKUP SUMMARY;` pour confirmer que les sauvegardes couvrent la cible.  
- **Vérification de la cohérence** : `SQL> SELECT * FROM v$database;` pour s’assurer que le statut est `OPEN`.  
- **Test d’intégrité** : `ANALYZE TABLE <table> VALIDATE STRUCTURE CASCADE;` (si une table est identifiée).  
- **Logs RMAN** : Examiner le fichier de log RMAN pour les erreurs ou avertissements.  
- **Sauvegarde de la base restaurée** : Faire une nouvelle sauvegarde complète après la restauration pour éviter de répéter la procédure.

## 5. Estimation du temps
| Étape | Durée approximative |
|-------|---------------------|
| Préparer l’environnement | 10 min |
| Connecter RMAN | 2 min |
| Restorer & récupérer | 30–60 min (selon taille et I/O) |
| Vérification et validation | 15 min |
| **Total** | **57–87 min** |

---