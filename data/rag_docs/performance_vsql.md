# **performance_vsql.md**

# Oracle Performance – V$SQLSTAT & Slow SQL Diagnostics

## **1. Contexte / Objectif**

V$SQLSTAT et V$SQL sont les vues dynamiques centrales pour analyser les requêtes consommatrices en Oracle.
Elles exposent des métriques cumulatives permettant d’identifier les SQL responsables de :

* lenteurs,
* forte consommation CPU,
* I/O anormale,
* parsing excessif,
* régressions de plans.

Ce document fournit les patterns essentiels pour diagnostiquer rapidement les requêtes problématiques.

---

## **2. Métriques essentielles dans V$SQLSTAT**

| Metric             | Signification                                 |
| ------------------ | --------------------------------------------- |
| **ELAPSED_TIME**   | Temps total d’exécution (µs)                  |
| **CPU_TIME**       | Temps CPU consommé                            |
| **DISK_READS**     | Blocs lus depuis disque                       |
| **BUFFER_GETS**    | Lectures logiques (pressure sur buffer cache) |
| **ROWS_PROCESSED** | Lignes manipulées                             |
| **EXECUTIONS**     | Nombre total d’exécutions                     |
| **PARSE_CALLS**    | Indicateur de hard parsing                    |

### **Requête — Top 10 SQL les plus lents**

```sql
SELECT sql_id, elapsed_time, cpu_time, disk_reads, buffer_gets,
       executions, parsing_schema_name
FROM   v$sqlstat
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;
```

---

## **3. Identifier une requête lente**

Une requête est considérée lente si elle présente :

### **A. ELAPSED_TIME élevé**

→ Premier indicateur global.

### **B. Ratio BUFFER_GETS / ROWS_PROCESSED anormal**

Un ratio élevé indique :

* mauvaises jointures,
* index manquant,
* filtrage tardif.

### **C. DISK_READS élevés**

→ Trop de Full Scans non souhaités.

### **D. EXECUTIONS fréquentes + coût élevé**

→ Requête inefficace exécutée en boucle.

### **E. PARSE_CALLS > EXECUTIONS**

→ Absence de bind variables → hard parsing → contention dans Shared Pool.

### **Coût moyen par exécution**

```sql
SELECT sql_id,
       elapsed_time / GREATEST(executions,1) AS time_per_exec,
       buffer_gets / GREATEST(executions,1) AS gets_per_exec
FROM   v$sqlstat
ORDER BY time_per_exec DESC;
```

---

## **4. Patterns courants de SQL problématiques**

### **Pattern 1 — High Buffer Gets (logical I/O)**

**Symptômes :**

* Gets élevés
* CPU élevé
* Peu de disk reads (car data déjà en cache)

**Causes probables :**

* index mal choisi
* mauvais join order
* fonctions sur colonnes indexées

---

### **Pattern 2 — High Disk Reads**

**Symptômes :**

* DISK_READS élevés
* elapsed_time élevé

**Causes probables :**

* Full table scan inutile
* index non utilisé / trop peu sélectif
* large table non cacheable

---

### **Pattern 3 — Excessive Parsing**

**Symptômes :**

* PARSE_CALLS >> EXECUTIONS
* temps CPU ou latency aléatoire

**Causes probables :**

* literals → hard parse
* manque de bind variables
* SQL généré dynamiquement

---

## **5. Associer performance et plan d’exécution**

```sql
SELECT s.sql_id, p.plan_hash_value, s.elapsed_time, s.cpu_time,
       p.operation, p.options, p.object_name
FROM   v$sqlstat s
JOIN   v$sql_plan p USING (sql_id)
WHERE  s.sql_id = '&SQLID'
ORDER BY p.id;
```

Utilité :

* identifier la partie précise du plan qui consomme,
* confirmer un mauvais access path (full scan, nested loop mal placé),
* détecter index ignoré.

---

## **6. Détection de régression**

Une régression est suspectée si :

* le **plan_hash_value change**, et
* le **elapsed_time double**, ou
* buffer gets x 3, ou
* disk reads x 4.

Requête simple pour détecter plusieurs plans récents :

```sql
SELECT sql_id, plan_hash_value,
       elapsed_time, executions,
       (elapsed_time / GREATEST(executions,1)) AS avg_time
FROM   v$sql
WHERE  sql_id = '&SQLID'
ORDER BY last_active_time DESC;
```

---

## **7. Résumé essentiel (RAG-friendly)**

* **V$SQLSTAT donne le top SQL problématique** (elapsed_time, CPU, gets).
* **Ratios clés** : gets/rows, elapsed/execution.
* **Symptômes** → buffer gets = problème logique ; disk reads = problème physique.
* **Parsing élevé** = absence de bind.
* **Toujours associer le SQL au plan via V$SQL_PLAN**.
* Les **régressions** se détectent par changement de plan_hash_value.

---

