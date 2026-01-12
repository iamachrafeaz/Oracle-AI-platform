
# Oracle — EXPLAIN PLAN & Bottleneck Identification

## 1. Contexte / Objectif

Ce document présente des exemples concrets d’**EXPLAIN PLAN** dans Oracle et explique comment identifier les **goulots d’étranglement** dans les requêtes SQL.
Objectif : fournir des patterns pratiques pour comprendre **où une requête dépense le plus de temps** et comment interpréter les opérations coûteuses.

---

# 2. Points clés

* L’opération la **plus coûteuse** apparaît généralement **en bas** du plan.
* `TABLE ACCESS FULL` indique souvent :

  * un manque d’index
  * un filtre peu sélectif
* `SORT ORDER BY` et `HASH JOIN` peuvent devenir dominants selon la volumétrie.
* Les vues **V$SQL_PLAN** et les fonctions **DBMS_XPLAN** donnent des détails avancés.
* Les **estimations de cardinalité** guident le choix du plan par l’optimiseur.

---

# 3. Bonnes pratiques

### ✔ Vérification de la cardinalité

* Comparer l’estimation (`E-Rows`) à la cardinalité réelle (`A-Rows`).
* Activer des **statistiques étendues** si les estimations sont erronées.

### ✔ Détection d’opérations indésirables

* Repérer `TABLE ACCESS FULL` non souhaités.
* Analyser les opérations consommant le plus de temps ou de mémoire.

### ✔ Comparer plan estimé vs exécuté

* Utiliser `DBMS_XPLAN.DISPLAY_CURSOR` pour vérifier le **plan réellement exécuté**.

### ✔ Analyser les pics de coût

* Observer les opérations où les coûts cumulés (`Cost`, `Bytes`, `Cardinality`) augmentent fortement.

---

# 4. Exemples Oracle SQL

## 4.1 Générer un plan simple

```sql
EXPLAIN PLAN FOR
SELECT *
FROM orders
WHERE customer_id = 500;
```

## 4.2 Afficher le plan estimé

```sql
SELECT *
FROM TABLE(DBMS_XPLAN.DISPLAY);
```

## 4.3 Afficher le plan réellement exécuté

```sql
SELECT *
FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('&sql_id', NULL, 'ALLSTATS LAST'));
```

---

# 5. Exemples de bottlenecks typiques

### 🔸 TABLE ACCESS FULL

Sur une table de plusieurs millions de lignes → manque d’index ou prédicats peu sélectifs.

### 🔸 SORT GROUP BY

Surtout si la cardinalité est sous-estimée → risque de temp space spill.

### 🔸 HASH JOIN

Coût mémoire élevé, croissance excessive du hash area.

---

# 6. Pièges à éviter

* Interpréter un coût élevé comme systématiquement mauvais : **contexte important**.
* Lire uniquement les coûts sans examiner la cardinalité.
* Supposer que le premier plan affiché est celui réellement utilisé.
* Ignorer les **paramètres de session** qui peuvent influencer l’optimiseur.

---

# 7. Quand utiliser EXPLAIN PLAN ?

* Diagnostic de requêtes lentes ou imprévisibles.
* Après changement de statistiques ou mise à jour d’index.
* Lors de migrations de version ou refonte applicative.
* Pour valider l’impact d’un tuning avant déploiement en production.

---

# 8. Résumé essentiel

`EXPLAIN PLAN` permet d’identifier les opérations les plus coûteuses d’une requête.
Comprendre les `FULL SCAN`, `JOIN`, `SORT`, et les estimations de cardinalité est essentiel pour éliminer les bottlenecks et guider l’optimisation SQL.


