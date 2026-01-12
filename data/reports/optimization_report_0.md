# Oracle Execution Plan Analysis

## 1. Explication simple du plan
| Id | Operation | Explication |
|----|-----------|-------------|
| 0 | SELECT STATEMENT | Point d’entrée, exécution de la requête finale. |
| 1 | VIEW | Résolution de la vue `ALL_SYNONYMS`. |
| 2 | SORT | Tri des résultats intermédiaires. |
| 3 | UNION-ALL | Combinaison de résultats provenant de deux sources sans suppression de doublons. |
| 4 | FILTER | Application des conditions WHERE après le UNION. |
| 5 | PX COORDINATOR | Coordonnateur pour l’exécution parallèle (PX). |
| 6 | PX SEND | Envoi de requêtes à un nœud PX. |
| 7 | PX PARTITION LIST | Gestion de la répartition des partitions pour PX. |
| 8 | EXTENDED DATA LINK | Accès à la table interne `INT$DBA_SYNONYMS`. |
| 9–10 | FILTER | Filtrage supplémentaire dans les sous‑requêtes. |
| 11–13 | NESTED LOOPS | Recherche imbriquée entre les tables `USER$`, `OBJ$`, `USER_EDITIONING$`. |
| 14 | TABLE ACCESS | Lecture de `USER$`. |
| 15 | INDEX | Utilisation de l’index `I_USER1` sur `USER$`. |
| 16 | TABLE ACCESS | Lecture de `OBJ$`. |
| 17 | INDEX | Utilisation de l’index `I_OBJ5` sur `OBJ$`. |
| 18 | INDEX | Utilisation de l’index `I_USER2` sur `OBJ$`/`USER$`. |
| 19 | INDEX | Utilisation de l’index `I_OBJAUTH1` sur `OBJ$`. |
| 20 | FIXED TABLE | Accès à la table interne `X$KZSRO`. |
| 21–24 | TABLE ACCESS / INDEX | Accès et index sur `USER_EDITIONING$` (2 fois). |
| 25 | NESTED LOOPS | Recherche imbriquée supplémentaire (autre niveau de jointure). |
| 26 | INDEX | Utilisation de l’index `I_USER2` (encore). |
| 27 | INDEX | Utilisation de l’index `I_OBJ4` sur `OBJ$`. |
| 28 | VIEW | Résolution de la vue `_ALL_SYNONYMS_TREE`. |
| 29 | CONNECT BY | Requête récursive pour l’arborescence des synonymes. |
| 30–32 | PX COORDINATOR / PX SEND / HASH JOIN | Jointure en hash join distribué entre nœuds PX. |
| 33 | BUFFER | Tamponnement des résultats intermédiaires. |
| 34 | PX RECEIVE | Réception des données sur le nœud principal. |
| 35 | PX SEND | Envoi de résultats intermédiaires. |
| 36 | STATISTICS COLLECTOR | Collecte de statistiques après exécution. |
| 37 | VIEW | Résolution de la vue `VW_SQ_1`. |
| 38 | FILTER | Filtrage supplémentaire après la vue. |
| 39–43 | PX COORDINATOR / PX SEND / PX PARTITION LIST / EXTENDED DATA LINK / FILTER | Gestion parallèle pour d’autres parties de la requête. |
| 44–46 | NESTED LOOPS | Recherche imbriquée pour d’autres tables. |
| 47–57 | TABLE ACCESS / INDEX | Accès à `USER$`, `OBJ$`, `USER_EDITIONING$` avec leurs indices (répétition). |
| 58 | NESTED LOOPS | Recherche imbriquée finale. |
| 59 | INDEX | Utilisation de l’index `I_USER2`. |
| 60 | INDEX | Utilisation de l’index `I_OBJ4`. |
| 61 | PX RECEIVE | Réception finale des données. |
| 62–68 | PX SEND / PX PARTITION LIST / EXTENDED DATA LINK | Envoi et gestion de partitions pour les derniers sous‑ensembles. |

## 2. Les 3 points les plus coûteux
| Opération | Pourquoi c’est coûteux |
|-----------|------------------------|
| NESTED LOOPS (plusieurs niveaux) | Multiplication des liaisons entre tables sans filtres indexés adéquats, entraînant un grand nombre de scans. |
| HASH JOIN distribué (PX) | Nécessité de rassembler de grandes quantités de données sur le nœud coordonnateur, provoquant un goulet d’étranglement. |
| EXTENDED DATA LINK vers `INT$DBA_SYNONYMS` | Accès à des tables internes volumineuses sans index optimisés, générant des scans complets. |

## 3. Optimisations recommandées
1. **Créer ou optimiser les indices** sur les colonnes utilisées dans les jointures (`USER_ID`, `OBJECT_ID`) pour éviter les NESTED LOOPS coûteux.  
2. **Réécrire les requêtes récursives** (`CONNECT BY`) en utilisant des tables temporaires ou des CTE pré‑filtrées pour réduire la charge sur les vues `_ALL_SYNONYMS_TREE`.  
3. **Convertir le HASH JOIN en NESTED LOOPS** ou en MERGE JOIN lorsque le cardinalité est faible, afin de réduire la charge de collecte des données sur le coordonnateur PX.  
4. **Activer la parallélisation intelligente** (`PARALLEL` clause) uniquement sur les opérations réellement volumineuses et limiter le nombre de threads.  
5. **Supprimer ou fusionner les vues redondantes** (`ALL_SYNONYMS`, `VW_SQ_1`) afin de diminuer la profondeur de l’arbre d’exécution.  
6. **Utiliser des partitions physiques** sur les tables `USER$` et `OBJ$` pour permettre une élimination de partition plus efficace.  

## 4. Estimation de l’impact performance
| Optimisation | Gain attendu | Justification |
|--------------|--------------|---------------|
| Optimisation des indices | 30 – 50 % | Réduction des scans de tables complètes, amélioration des NESTED LOOPS. |
| Réécriture des `CONNECT BY` | 20 % | Réduction de la charge sur les vues internes et évite les scans de `INT$DBA_SYNONYMS`. |
| Conversion HASH JOIN → NESTED LOOPS | 10 % | Moins de données transférées sur le coordonnateur, diminuer le goulet d’étranglement. |
| Limitation de la parallélisation | 5 % | Évite le coût de synchronisation et de collecte excessive des données. |
| Fusion des vues redondantes | 15 % | Réduit la profondeur de l’exécution et simplifie le plan. |
| Partitionnement physique | 25 % | Améliore l’élimination de données non pertinentes dès les premières étapes. |

*Note : Les gains sont estimés en fonction de la taille des tables et de la charge actuelle. L’analyse exacte nécessiterait des mesures réelles.*