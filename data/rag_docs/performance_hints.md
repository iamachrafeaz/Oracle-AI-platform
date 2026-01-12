
# Oracle Performance — SQL Hints (FULL, INDEX, USE_NL, etc.)

## Overview

Oracle SQL hints allow influencing the Cost-Based Optimizer (CBO).
They should be used **only when statistics are correct** and the generated plan does not align with functional or business constraints.

---

# 1. Categories of Hints

### 🔹 Access Path Hints

Define how Oracle accesses data:
**FULL, INDEX, INDEX_DESC, INDEX_FFS**

### 🔹 Join Operation Hints

Define the join algorithm:
**USE_NL, USE_HASH, USE_MERGE**

### 🔹 Join Order Hints

Define the table access order:
**LEADING, ORDERED**

### 🔹 Parallelization Hints

Control execution parallelism:
**PARALLEL, PQ_DISTRIBUTE**

### 🔹 Optimization Goal Hints

Set the optimizer target:
**ALL_ROWS, FIRST_ROWS**

---

# 2. Access Path Hints

## 2.1 FULL(table)

Forces a full table scan even if an index exists.

### When to use:

* Table is small
* > 15% of rows must be scanned
* Index has poor selectivity

```sql
SELECT /*+ FULL(emp) */
       *
FROM   employees emp
WHERE  department_id = 10;
```

---

## 2.2 INDEX(table column/index)

Forces the use of a specified index.

```sql
SELECT /*+ INDEX(emp idx_emp_dept) */
       *
FROM   employees emp
WHERE  department_id = 10;
```

---

# 3. Join Operation Hints

## 3.1 USE_NL

Forces a **Nested Loop Join**.

### Best when:

* Outer table returns few rows
* Inner table is indexed

```sql
SELECT /*+ USE_NL(e d) */
       *
FROM   employees e
JOIN   departments d ON e.dept_id = d.id;
```

---

## 3.2 USE_HASH

Forces a **Hash Join**.

### Best when:

* Large datasets
* No useful index
* Equijoins

```sql
SELECT /*+ USE_HASH(e d) */
       *
FROM   employees e
JOIN   departments d ON e.dept_id = d.id;
```

---

# 4. Join Order Hints

## 4.1 LEADING(table1 table2)

Forces the join order.

```sql
SELECT /*+ LEADING(o c) */
       *
FROM   orders o
JOIN   customers c ON o.cust_id = c.id;
```

---

## 4.2 ORDERED

Forces the join order based on the **FROM clause**.

```sql
SELECT /*+ ORDERED */
       *
FROM   orders o
JOIN   customers c ON o.cust_id = c.id;
```

---

# 5. Parallelization Hints

## PARALLEL(table, degree)

Requests parallel execution.

```sql
SELECT /*+ PARALLEL(sales, 8) */
       *
FROM   sales;
```

 **Warning:**
Parallel execution can *reduce* performance if CPU is saturated.

---

# 6. When *Not* to Use Hints

Avoid hints when:

* Statistics are outdated
* Queries evolve frequently
* Hints hide poor SQL design
* An index is missing (create it instead)

---

# 7. RAG — Useful Troubleshooting Patterns

| Symptom                              | Likely Fix / Hint                     |
| ------------------------------------ | ------------------------------------- |
| Unexpected **TABLE ACCESS FULL**     | Propose `INDEX` hint                  |
| Nested loops too slow                | Propose `USE_HASH`                    |
| Wrong join order / bad driving table | Propose `LEADING`                     |
| Poor parallel plan                   | Propose adjusting/removing `PARALLEL` |

---

