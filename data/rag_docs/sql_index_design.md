### *Conception des Index Oracle : Composite, Bitmap, Partitioning*

---

## **Tags**

Oracle, Index, Performance, SQL Tuning, Composite Index, Bitmap Index, Partitioning, DBA, B-tree, Cardinality, Selectivity

---

## **1. Objectif du document**

Ce document présente les meilleures pratiques de conception des index dans Oracle Database, incluant les index B-tree, composites, bitmap et ceux utilisés dans les environnements partitionnés.
Il vise à fournir des modèles, diagnostics et anti-patterns pour optimiser les performances des requêtes et réduire les coûts de maintenance.

---

## **2. Résumé rapide (TL;DR)**

* Les **index B-tree** conviennent aux colonnes très sélectives.
* Les **index composites** nécessitent un ordre logique basé sur les filtres (égalité → ordinale).
* Les **index bitmap** sont utiles en BI mais dangereux en OLTP.
* Le **partitionnement** influence le choix entre index **locaux** et **globaux**.
* Toujours vérifier la **sélectivité** et les **plans d’exécution réels**.
* Éviter la sur-indexation : impact lourd sur insert/update/delete.

---

## **3. Concepts clés**

### **Index B-tree**

Structure classique utilisée pour les recherches rapides sur colonnes sélectives.

### **Index composite**

Index contenant plusieurs colonnes. L'ordre dépend des filtres utilisés dans les requêtes.

### **Index bitmap**

Index basé sur des vecteurs de bits, idéal pour les colonnes de faible cardinalité (BI, entrepôts de données).

### **Index local vs global (partitionnés)**

* **Local** : une partition d’index par partition de table.
* **Global** : une seule structure couvrant toutes les partitions.

### **Sélectivité**

Proportion de lignes filtres par une valeur. Plus elle est élevée → meilleure performance B-tree.

### **Cardinalité**

Nombre de valeurs distinctes. Faible cardinalité → bitmap.

---

## **4. Quand utiliser quel type d’index**

### **Index composite**

* WHERE multi-colonnes courants.
* Joins complexes.
* Requêtes avec filtres d’égalité + ranges.
* Ex : `WHERE status = 'A' AND created_at BETWEEN ...`

### **Index bitmap**

* Systèmes décisionnels (DWH, BI).
* Colonnes catégorielles (gender, region, type).
* Colonnes faiblement variables (LOW cardinality).
* Tables rarement modifiées.

### **Index partitionnés**

* **Locaux** : maintenance simplifiée, opérations partitionnelles rapides.
* **Globaux** : requis pour couvrir des requêtes transversales.

---

## **5. Bonnes pratiques essentielles**

* Dans un **index composite**, mettre en premier les colonnes d’égalité.
* Éviter les composites inutiles → vérifier plans SQL.
* Vérifier la **sélectivité** avant de créer un index.
* Utiliser **bitmap** uniquement en BI.
* Préférer des **index locaux** sur tables partitionnées.
* Analyser les plans via `DBMS_XPLAN.DISPLAY_CURSOR`.
* Actualiser les statistiques avec `DBMS_STATS`.
* Tester l’impact d’un index dans un environnement non-prod avant déploiement.

---

## **6. Pièges à éviter (Anti-patterns)**

* Sur-indexation → augmente le coût des DML.
* Index bitmap sur OLTP (risque de verrous lourds).
* Ajouter des colonnes « au cas où ».
* Ne pas mettre à jour les statistiques.
* Ignorer la cardinalité réelle.
* Utiliser un composite alors qu’un simple B-tree suffit.

---

## **7. Exemples SQL**

### **Créer un index composite**

```sql
CREATE INDEX idx_orders_date_status
ON orders(order_date, status);
```

### **Créer un index bitmap**

```sql
CREATE BITMAP INDEX idx_customer_gender
ON customers(gender);
```

### **Lister les index locaux d'une table partitionnée**

```sql
SELECT index_name, locality
FROM dba_part_indexes
WHERE table_name = 'SALES';
```

### **Lire un plan d’exécution**

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

### **Vérifier la sélectivité d'une colonne**

```sql
SELECT column_name, num_distinct, density
FROM dba_tab_col_statistics
WHERE table_name = 'ORDERS';
```

---

## **8. Requêtes de diagnostic**

### **Lister les index d’une table**

```sql
SELECT index_name, uniqueness, status
FROM dba_indexes
WHERE table_name = 'ORDERS';
```

### **Évaluer l’utilisation réelle des index**

```sql
SELECT name, value
FROM v$sysstat
WHERE name LIKE '%index%';
```

### **Taille d’un index**

```sql
SELECT segment_name, bytes/1024/1024 AS mb
FROM dba_segments
WHERE segment_type='INDEX';
```

---

## **9. Checklist d’indexation**

* [ ] La colonne est-elle filtrée dans les requêtes ?
* [ ] La sélectivité est-elle suffisante ?
* [ ] Index composite → ordre correct ?
* [ ] Table OLTP → éviter bitmap.
* [ ] Table partitionnée → local ou global ?
* [ ] Statistiques à jour ?
* [ ] Impact sur DML acceptable ?

---

## **10. Cas d’usage réalistes**

### **OLTP**

* Beaucoup d'inserts/updates.
* B-tree simples privilégiés.
* Éviter bitmap.

### **DWH / BI**

* Colonnes catégorielles.
* Bitmap très performant.
* Tables stables, peu de DML.

### **Tables partitionnées large volume**

* Index locaux recommandés.
* Rebuild plus simple.
* Query pruning optimisé.

### **Applications multi-colonne**

* Index composites efficaces pour les filtres fréquents.

---

## **11. Résumé final**

La conception d’index Oracle dépend de la sélectivité, de la cardinalité, du type de charge (OLTP/BI) et du partitionnement.
Les index composites optimisent les filtres multi-colonnes, les bitmap accélèrent les analyses décisionnelles, et les index locaux sont essentiels pour les grandes tables partitionnées. La qualité des statistiques et la vérification systématique des plans SQL sont indispensables.

---

## **12. Notes complémentaires**

* Recommandé : tester un index dans un environnement isolé avant production.
* Un index n'est utile que si le plan l’utilise réellement.

---

