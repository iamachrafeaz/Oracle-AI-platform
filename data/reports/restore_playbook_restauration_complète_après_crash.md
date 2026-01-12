# Playbook de Restauration & Récupération Oracle

## 1. Introduction
Ce playbook décrit les étapes à suivre pour effectuer une restauration complète d’une base Oracle après un crash, en partant du principe que des sauvegardes RMAN sont disponibles.

## 2. Étapes détaillées
1. **Préparation**  
   - Vérifier l’intégrité des sauvegardes RMAN (`VALIDATE`).  
   - S’assurer que le répertoire de stockage (tape, disque, etc.) est accessible.  
2. **Arrêt de la base**  
   - Mettre la base en mode `MOUNT` ou `STARTUP MOUNT` via SQL*Plus.  
3. **Connexion à RMAN**  
   - `rman target / catalog rman/cat_pwd@catdb` (si un catalog RMAN est utilisé).  
4. **Restauration complète**  
   - `RUN { RESTORE DATABASE; }`  
5. **Récupération**  
   - `RUN { RECOVER DATABASE; }`  
   - Si des logs de redo sont manquants, arrêter la récupération après la dernière sauvegarde disponible.  
6. **Ouverture de la base**  
   - `ALTER DATABASE OPEN RESETLOGS;` (si un restore a changé le nombre de redo logs).  
7. **Vérification**  
   - Consulter les logs RMAN (`SHOW ALL`).  
   - Exécuter des requêtes de test sur des tables critiques.  

## 3. Commandes RMAN
```sql
-- Connexion à la base cible et au catalogue RMAN
rman target / catalog rman_user/rman_pwd@catdb

-- Validation des sauvegardes
RUN {
  VALIDATE DATABASE;
}

-- Restauration complète de la base
RUN {
  RESTORE DATABASE;
}

-- Récupération de la base
RUN {
  RECOVER DATABASE;
}

-- Ouverture de la base en mode RESETLOGS
ALTER DATABASE OPEN RESETLOGS;
```

## 4. Points de validation
- Vérification de l’intégrité des sauvegardes (`VALIDATE`).  
- Confirmation que le catalogue RMAN contient les métadonnées correctes.  
- Vérification du journal RMAN (`SHOW ALL`) pour l’absence d’erreurs critiques.  
- Test de connectivité via SQL*Plus après ouverture.  
- Exécution de requêtes SELECT sur des tables clés pour valider la cohérence des données.

## 5. Estimation du temps
| Étape | Durée approximative |
|-------|---------------------|
| Préparation & validation | 15–30 min |
| Arrêt de la base | 5 min |
| Restauration complète | 45 min–2 h (selon la taille) |
| Récupération | 15–45 min |
| Ouverture & vérifications | 10–20 min |
| **Total** | **1–3 h** |

---