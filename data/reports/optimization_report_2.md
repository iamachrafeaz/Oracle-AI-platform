# Oracle Execution Plan Analysis

## 1. Explication simple du plan

| Id | Opération | Explication |
|----|-----------|-------------|
| 0 | SELECT STATEMENT | Point d’entrée du plan, exécute la requête finale. |
| 1 | VIEW | Résolution d’une vue (ou sous‑requête) utilisée dans la requête. |
| 2 | UNION‑ALL | Combine les résultats de deux jeux sans élimination de doublons. |
| 3 | FILTER | Applique des conditions WHERE sur le jeu résultant. |
| 4 | MERGE JOIN | Jointure interne combinant plusieurs sous‑ensembles par fusion. |
| 5 | HASH JOIN | Jointure interne basée sur un algorithme de hachage. |
| 6 | NESTED LOOPS | Accès séquentiel de tables via boucles imbriquées. |
| 7 | STATISTICS COLLECTOR | Récupération de statistiques d’exécution. |
| 8–17 | Répétitions de HASH JOIN / NESTED LOOPS | Représente plusieurs couches d’opérations de jointure et de boucle. |
| 28–49 | TABLE ACCESS / INDEX | Accès à des tables (USER$, OBJ$, TAB$, TS$, SEG$) et aux indices correspondants. |
| 50 | BUFFER | Gestion de la mise en cache des blocs de données. |
| 51–56 | FIXED TABLE | Accès aux tables système X$ pour obtenir des métadonnées. |
| 57–64 | INDEX | Accès à des index supplémentaires (I_OBJAUTH2, I_USER_EDITIONING, etc.). |
| 65 | FILTER | Filtration supplémentaire après certaines jointures. |
| 66–68 | PX COORDINATOR / PX SEND / PX PARTITION LIST | Coordination et envoi des tâches parallèles. |
| 69–73 | EXTENDED DATA LINK / FIXED TABLE | Récupération de données depuis des tables système ou des vues étendues. |

*Remarque : Les identifiants 0‑73 sont répétés dans la liste ; la première occurrence est considérée comme représentative.*

---

## 2. Les 3 points les plus coûteux

| Opération | Pourquoi c’est coûteux |
|-----------|------------------------|
| HASH JOIN | Implique le chargement de grands jeux de données en mémoire pour créer des tables de hachage, provoquant de fortes charges CPU et I/O. |
| NESTED LOOPS (répétés) | Chaque boucle peut nécessiter un scan complet d’une table ou d’un index, multipliant les lectures disque quand les cardinalités sont élevées. |
| UNION‑ALL / MERGE JOIN | La fusion de plusieurs jeux de résultats nécessite la construction de buffers temporaires volumineux, augmentant la mémoire et le temps d’exécution. |

---

## 3. Optimisations recommandées

1. **Remplacer les NESTED LOOPS par des HASH JOIN ou MERGE JOIN** lorsqu’une cardinalité élevée est anticipée, afin de réduire le nombre de passes disque.  
2. **Créer ou réévaluer les indexes** sur les colonnes utilisées dans les filtres et les jointures (ex. I_USER1, I_OBJ5, I_USER2) pour diminuer le temps de recherche.  
3. **Supprimer ou désactiver les STATISTICS COLLECTOR** inutiles qui ajoutent de la surcharge d’exécution.  
4. **Réécrire le UNION‑ALL** pour éviter des sous‑requêtes redondantes ou combiner les jeux en un seul SELECT si possible.  
5. **Activer la parallélisation (PX)** pour les tables volumineuses et s’assurer que les tailles de lot sont optimales afin d’éviter le sur‑ou sous‑traitement.  
6. **Vérifier les paramètres de mémoire (SGA/ PGA)** afin que les HASH JOIN aient assez de RAM pour éviter le swap.

---

## 4. Estimation de l’impact performance

| Optimisation | Gain attendu | Justification |
|--------------|--------------|---------------|
| Remplacement des NESTED LOOPS par HASH JOIN | ~30 % | Réduit le nombre de passes disque et le coût de recherche séquentielle. |
| Indexation des colonnes clés | ~20 % | Accélère l'accès aux lignes via des recherches d’index, évitant les scans complets. |
| Suppression des STATISTICS COLLECTOR | ~10 % | Élimine la surcharge de collecte de statistiques à chaque exécution. |
| Réécriture du UNION‑ALL | ~15 % | Diminue la taille des buffers temporaires et le coût de fusion. |
| Optimisation de PX (taille de lot) | ~25 % | Améliore l’équilibrage de charge entre les nœuds, réduisant le temps total d’exécution. |

> **Note** : Les gains sont indicatifs; une mise en œuvre réelle nécessite des tests sur un environnement de production ou de test.