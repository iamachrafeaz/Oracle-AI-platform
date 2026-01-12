# **Oracle Performance — Automatic Tuning, SQL Plan Baselines & Adaptive Plans**

## **Overview**

Ce document présente les fonctionnalités clés d’optimisation avancée dans Oracle Database. Ces mécanismes permettent d'améliorer les performances SQL, de stabiliser les plans d’exécution et d’éviter les régressions après mise à jour de statistiques ou changement de charge.

L’objectif est d’expliquer :

* ce que fait chaque technologie,
* quand et pourquoi l’utiliser,
* leurs limites,
* les risques à éviter en production.

---

# **1. Automatic SQL Tuning**

Oracle propose une tâche automatique nommée **SYS_AUTO_SQL_TUNING_TASK**, exécutée généralement chaque nuit dans la fenêtre de maintenance. Elle analyse les requêtes coûteuses et génère des recommandations telles que :

### 🔹 **SQL Profiling**

Analyse approfondie des prédicats, cardinalités et sélectivités → produit un **SQL Profile** qui corrige les estimations de l’optimiseur *sans imposer un plan*.

### 🔹 **Index Recommendations**

Propose la création ou modification d’index basés sur le workload réel.

### 🔹 **Structure de requête**

Réécritures SQL internes ou suggestions de changements.

### 🔹 **Plan Validation**

Le moteur teste automatiquement les plans proposés avant de les valider.

####  Activer l’acceptation automatique des SQL Profiles

```sql
EXEC DBMS_SQLTUNE.SET_TUNING_TASK_PARAMETER(
    task_name  => 'SYS_AUTO_SQL_TUNING_TASK',
    parameter  => 'ACCEPT_SQL_PROFILES',
    value      => 'TRUE'
);
```

---

# **2. SQL Profiles**

Un **SQL Profile** corrige les estimations de l'optimiseur pour une requête donnée.
Il *n’impose pas un plan précis* mais améliore la qualité des décisions du CBO.

###  Utilité :

* Corrections de cardinalités erronées
* Problèmes ponctuels d’estimation
* Requêtes complexes mal interprétées par le CBO

###  Avantages :

* Flexible, non invasif
* Peut résoudre des problèmes sans changer l'application

###  Limite :

* Ne protège pas contre un changement complet de plan.

---

# **3. SQL Plan Baselines**

Les **baselines** sont des mécanismes de **plan stability**.
Elles garantissent que l’optimiseur n’utilise **que des plans connus et validés**, même si les statistiques changent.

###  Idéal pour :

* éviter les régressions après purge/regénération de stats,
* garantir des performances prévisibles en production.

###  Lister les baselines

```sql
SELECT sql_handle, plan_name, enabled, accepted
FROM   dba_sql_plan_baselines;
```

###  Fonctionnement :

* Oracle maintient un ensemble de **plans acceptés** (trusted)
* Si un nouveau plan apparaît, il doit être **validé** avant d'être accepté
* L’optimiseur reste stable, même en cas d’upgrade Oracle ou changement de stats

###  Mythe :

> Une baseline **n’améliore pas** les performances.
> Elle **stabilise** le comportement — ce qui évite les mauvaises surprises.

---

# **4. Adaptive Query Optimization (Adaptive Plans)**

Introduits dans Oracle 12c, les **Adaptive Plans** permettent au moteur de :

### 1. Ajuster les stratégies de jointure en temps réel

Exemple : passer d’un nested loop à un hash join si le nombre réel de lignes diffère de l’estimation.

### 2. Corriger dynamiquement certaines cardinalités

###  Vérifier si un plan adaptatif a été utilisé :

```sql
SELECT *
FROM   v$sql_plan
WHERE  sql_id = '&SQLID'
AND    is_adaptive = 'YES';
```

###  Cas d’usage :

* tables avec distribution skewée
* requêtes avec mauvais histogrammes
* workloads fluctuants

###  Limites :

* Ne règle pas automatiquement tous les problèmes de cardinalité
* Peut masquer des problèmes de statistiques incorrectes

---

# **5. Best Practices**

### ✔ Activer et surveiller Automatic Tuning sur les bases critiques

### ✔ Ne pas accepter automatiquement les SQL Profiles sans validation préalable

(surtout en production)

### ✔ Utiliser les baselines lorsque :

* les plans changent trop souvent,
* une mise à jour de statistiques provoque des régressions,
* un upgrade Oracle est planifié.

### ✔ Analyser régulièrement les Adaptive Plans pour comprendre :

* pourquoi Oracle change de stratégie,
* lorsque des cardinalités sont mal estimées.

### ✔ Garder un historique AWR suffisamment long

→ indispensable pour diagnostiquer les plans problématiques.

---

# **6. Common Pitfalls (À éviter absolument)**

❌ **Accepter des SQL Profiles sans test**
→ peut dégrader les performances globales.

❌ **Compter uniquement sur les Adaptive Plans**
→ ne remplace pas une bonne gestion des statistiques.

❌ **Croire qu’une SQL Plan Baseline améliore la performance**
→ elle la stabilise seulement.

❌ **Ignorer les changements de workload**
→ un bon plan aujourd’hui peut devenir mauvais demain.

---

# **7. When to Use These Mechanisms?**

### ✔ Après une régression suite à :

* mise à jour de statistiques,
* nettoyage de stats,
* migration / upgrade Oracle,
* changement d’infrastructure.

### ✔ Dans un environnement où les plans changent fréquemment

### ✔ Sur les systèmes critiques demandant des performances stables

### ✔ Pour diagnostiquer les requêtes les plus coûteuses du top SQL

---

# **8. Executive Summary**

L’optimisation automatique Oracle repose sur quatre piliers complémentaires :

| Mécanisme                | Rôle                    | But                              |
| ------------------------ | ----------------------- | -------------------------------- |
| **Automatic SQL Tuning** | Analyse quotidienne     | Propose des améliorations        |
| **SQL Profiles**         | Corrige les estimations | Améliore le plan CBO             |
| **SQL Plan Baselines**   | Stabilise les plans     | Empêche les régressions          |
| **Adaptive Plans**       | Ajuste en temps réel    | Répare les cardinalités erronées |

 Ensemble, ces technologies :

* améliorent les performances SQL,
* protègent contre les régressions,
* renforcent la fiabilité et la prévisibilité du moteur d’optimisation Oracle.

---

Si tu veux, je te génère aussi **performance_hints.md**, **performance_rewrite.md**, ou un **master document** regroupant tout le tuning Oracle.
