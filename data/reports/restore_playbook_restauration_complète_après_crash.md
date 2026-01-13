# Playbook de Restauration & Récupération Oracle

## 1. Introduction
Ce playbook décrit les étapes pour restaurer une base de données Oracle à l’état complet après un crash, en utilisant les backups RMAN disponibles. Il s’applique lorsque la date/heure cible (PITR), la table spécifique et la ligne spécifique ne sont pas nécessaires ou non disponibles.

## 2. Étapes détaillées
1. **Préparer l’environnement de restauration**  
   1.1. Vérifier l’état du serveur Oracle et du stockage.  
   1.2. Créer un répertoire de destination temporaire (`$ORACLE_HOME/backup_restore`).  
2. **Démarrer une session RMAN**  
   2.1. Connexion à la cible (`target sys/password`).  
   2.2. Connexion à l’archive destination (`archivelog destination sys/password`).  
3. **Restaurer la base de données complète**  
   3.1. Restaurer les fichiers de contrôle, les fichiers de données et les logs de redo.  
4. **Récupérer les fichiers**  
   4.1. Exécuter la récupération complète (ou récupération des fichiers de redo).  
5. **Redémarrer la base de données**  
   5.1. Mettre la base en mode `MOUNT`.  
   5.2. Mettre la base en mode `OPEN`.  
6. **Vérifier l’intégrité et le bon fonctionnement**  
   6.1. Vérifier les journaux d’alerte et les rapports RMAN.  
   6.2. Exécuter des requêtes de test pour s’assurer que la base est opérationnelle.  
7. **Nettoyer les ressources temporaires**  
   7.1. Supprimer ou archiver les fichiers de restauration temporaires.  

## 3. Commandes RMAN
```sql
-- 1. Préparer l'environnement
!mkdir -p $ORACLE_HOME/backup_restore
!chmod 700 $ORACLE_HOME/backup_restore

-- 2. Connexion RMAN
rman target sys/your_password @target_connect
rman target sys/your_password archivelog destination sys/your_password

-- 3. Restaurer la base complète
RESTORE DATABASE;
-- (Optionnel) Restaurer les fichiers de contrôle
-- RESTORE CONTROLFILE FROM BACKUP CONTROLFILE;

-- 4. Récupérer les fichiers
RECOVER DATABASE;

-- 5. Redémarrer la base
ALTER DATABASE MOUNT;
ALTER DATABASE OPEN;

-- 6. Vérifier l’état
ARCHIVE LOG LIST;
```

## 4. Points de validation
- **État de la base** : `SELECT status FROM v$instance;` doit afficher `OPEN`.
- **Fichiers de redo** : Aucun journal d’erreur `ORA-` dans `alert.log`.
- **Tablespaces** : `SELECT tablespace_name, status FROM dba_tablespaces;` doit indiquer `OPEN`.
- **Consistance** : Vérifier la consistance d’une table critique (ex. `SELECT COUNT(*) FROM <table>;`).
- **Performance** : Mesurer le temps de réponse d’une requête de test.

## 5. Estimation du temps
| Tâche | Durée approximative |
|-------|---------------------|
| Préparer l’environnement | 5 min |
| Connexion RMAN | 2 min |
| Restaurer la base | 30‑60 min (selon taille) |
| Récupération | 15‑30 min |
| Redémarrage | 5 min |
| Validation | 10 min |
| Nettoyage | 5 min |
| **Total** | **≈ 1h à 1h30** |

---