# **Oracle Performance — Index Usage & Access Paths**

## **Overview**

Ce document présente les patterns d’accès aux données dans Oracle, les cas où le moteur choisit un index ou un Full Table Scan (FTS), et les méthodes d’analyse permettant d’identifier les index absents, inefficaces ou sous-utilisés.

L’objectif est d’aider à :

* diagnostiquer rapidement les problèmes d’indexation,
* optimiser les chemins d’accès SQL,
* améliorer la sélectivité et réduire les I/O inutiles,
* supprimer les index coûteux et non utilisés.

---

# **1. Access Paths in Oracle**

Oracle peut sélectionner plusieurs types de chemins d’accès :

### 🔹 **INDEX UNIQUE SCAN**

Accès direct via clé unique ou contrainte UNIQUE.
→ Très efficace, retourne 0 ou 1 ligne.

### 🔹 **INDEX RANGE SCAN**

Utilisé pour des conditions sélectives.
→ Parcours contrôlé d’une partie de l’index.

### 🔹 **INDEX FULL SCAN**

Parcours complet de l’index **dans l’ordre des clés**.
→ Avantage : tri implicite → évite un SORT ORDER BY.

### 🔹 **INDEX FAST FULL SCAN**

Équivalent d’un full scan mais sur l’index seul.
→ Peut utiliser le parallélisme.
→ Nécessite un index **couvrant** les colonnes du SELECT.

### 🔹 **TABLE ACCESS FULL (FTS)**

Lecture complète de la table.
→ Peut être normal… ou symptôme d’un index manquant.

---

# **2. Detecting Index Usage Problems**

## **Pattern 1 — Full Table Scan on a Selective Column**

Un FTS peut indiquer :

* **statistiques obsolètes**,
* **index manquant**,
* filtre appliqué via une **fonction sur la colonne** (rendant l’index inutilisable).

```sql:disable-run
SELECT /*+ MONITOR */ emp_id, salary
FROM   employees
WHERE  salary = 4500;
```

Analyse du plan :

```sql
EXPLAIN PLAN FOR ...
SELECT * FROM table(dbms_xplan.display);
```

---

## **Pattern 2 — Index Exists but Not Used**

Causes fréquentes :

### ❌ 1. Expressions non indexables

Exemples :

* `UPPER(col) = ...`
* `SUBSTR(col, 2) = ...`
* Calculs sur colonne.

Solution → créer un **function-based index**.

---

### ❌ 2. Mauvais ordre dans un index composite

Index (A, B, C)
Query filtre sur C uniquement → **index inutilisable**.

---

### ❌ 3. Conditions OR non réécrites

Exemple :

```sql
WHERE dept = 10 OR status = 'A'
```

→ Oracle peut abandonner l’index.

Solutions :

* réécrire en `UNION ALL`,
* utiliser `BITMAP INDEX` si data warehouse.

---

# **3. Composite Index Best Practices**

Un index composite doit respecter :

### ✔ Ordre de sélectivité décroissante

La colonne la plus sélective en premier.

### ✔ Ordre cohérent avec les filtres réels

Aligné avec les prédicats récurrents.

### ✔ Utilisé pleinement si les premières colonnes apparaissent dans le WHERE

Anti-pattern :

```text
Index: (A, B, C)
WHERE C = 'x'      → index inutilisable
```

---

# **4. Detecting Unused or Low-Value Indexes**

### **1. Trouver les index non utilisés (oracle ≥ 12c)**

```sql
SELECT index_name, table_name, monitoring, used
FROM   v$object_usage;
```

### **2. Indicateurs d’un mauvais index**

* **leaf_blocks >> distinct_keys** → faible sélectivité
* **clustering_factor élevé** → lectures aléatoires inefficaces
* **index trop large** → surcharge INSERT/UPDATE/DELETE

---

# **5. When Is a Full Table Scan Legit?**

Un FTS n’est pas systématiquement mauvais.

Il est optimal lorsque :

### ✔ La table est petite (≈ < 10k blocks)

### ✔ Le filtre retourne > 10–15% de la table

### ✔ L’index n’est pas couvrant

→ Oracle préfère lire directement la table.

### ✔ Le coût I/O du FTS < coût de l’accès index

---

# **6. Practical RAG Examples (Red / Amber / Green)**

## **Example A — Index Needed (Red)**

**Symptômes :**

* `BUFFER_GETS` très élevés dans `V$SQLSTAT`
* `TABLE ACCESS FULL` dans le plan
* prédicats très sélectifs

**Solution :**

```sql
CREATE INDEX idx_emp_status ON employees(status);
```

---

## **Example B — Useless Index to Drop (Orange → Green)**

**Symptômes :**

* index jamais utilisé (dans `v$object_usage`)
* clustering factor trop élevé
* surcharge importante lors des DML

**Solution :**

```sql
ALTER INDEX idx_old_col UNUSABLE;
DROP INDEX idx_old_col;
```

---

# **7. How Oracle Chooses Between Index & Full Table Scan**

## Oracle privilégie **l’index** quand :

* sélectivité < 5–10%
* faible nombre de lignes retournées
* index **couvrant** toutes les colonnes SELECT
* ordre des colonnes optimal

## Oracle privilégie **le FTS** quand :

* grand volume de lignes matchées
* table petite
* index non sélectif
* statistique incomplètes

---

## **Conclusion**

Ce document fournit un cadre complet pour analyser l’utilisation des index et améliorer les performances SQL Oracle.
Il peut servir de guide dans :

* tuning de requêtes,
* conception ou nettoyage d’index,
* analyse des chemins d’accès Oracle,
* diagnostic de régressions de performance.

---


