# Oracle Performance — Query Rewrite Techniques

## Overview

This document presents SQL rewrite techniques that improve performance **without modifying the database structure**.
These patterns help reduce CPU and I/O costs and guide the optimizer toward better execution plans.

---

# 1. Replace `SELECT *`

### Problem

Unnecessary load, useless projections, network overhead.

### Rewrite

```sql
SELECT id, name, status
FROM users;
```

---

# 2. Replace `OR` with `IN` (or `UNION ALL` in special cases)

### Anti-pattern

```sql
WHERE status = 'A' OR status = 'B';
```

### Rewrite

```sql
WHERE status IN ('A', 'B');
```

---

# 3. Rewrite Functions on Indexed Columns

Functions on indexed columns **prevent the use of indexes**.

### Anti-pattern

```sql
WHERE UPPER(email) = 'TEST@MAIL.COM';
```

### Rewrite Options

#### ✔ Create a functional index

```sql
CREATE INDEX idx_email_up ON users (UPPER(email));
```

#### ✔ Normalize stored data

Store uppercased/lowercased values directly.

---

# 4. Avoid Leading Wildcards

Leading `%` makes the index unusable.

### Anti-pattern

```sql
WHERE name LIKE '%john';
```

### Rewrite

```sql
WHERE name LIKE 'john%';
```

---

# 5. Replace Subqueries with Joins (When Appropriate)

### Anti-pattern

```sql
SELECT *
FROM emp
WHERE dept_id IN (SELECT id FROM dept WHERE active = 'Y');
```

### Rewrite

```sql
SELECT e.*
FROM   emp e
JOIN   dept d ON e.dept_id = d.id
WHERE  d.active = 'Y';
```

---

# 6. Use `EXISTS` Instead of `IN` for Large Sets

```sql
SELECT *
FROM orders o
WHERE EXISTS (
    SELECT 1
    FROM customers c
    WHERE c.id = o.cust_id
);
```

---

# 7. Replace `DISTINCT` with `GROUP BY` When Counting

```sql
SELECT department_id, COUNT(*)
FROM   employees
GROUP BY department_id;
```

---

# 8. Materialization / Inline View Optimization

Force Oracle to materialize an inline view.

```sql
SELECT /*+ MATERIALIZE */ *
FROM (
    SELECT *
    FROM   sales
    WHERE  amount > 1000
);
```

---

# 9. RAG — Useful Rewrite Patterns

* Detect functions on indexed columns
* Convert `OR` conditions → `IN`
* Detect unnecessary `DISTINCT`
* Recommend `JOIN` instead of subqueries
* Warn when wildcard begins with `%`

---


