![SQL Server Tinitiate Image](sqlservericon.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# DQL - Common Table Expressions (CTEs)
* In SQL Server, a Common Table Expression (CTE) is a temporary result set that you can reference within a SELECT, INSERT, UPDATE, or DELETE statement.
* CTEs provide a way to write more readable and maintainable queries by breaking down complex queries into simpler parts.
* CTEs are defined using the `WITH` keyword.

## Creating a CTE
* To create a CTE, you use the `WITH` keyword.
```sql
-- Define a CTE to get employees with job title 'manager'
WITH Managers AS (
    SELECT empno, ename, job, sal
    FROM employees.emp
    WHERE job = 'manager'
)
-- Retrieve employees with job title 'manager' using the CTE
SELECT *
FROM Managers;

-- Define a CTE to count employees in each department
WITH DeptEmployeeCount AS (
    SELECT deptno, COUNT(*) AS num_employees
    FROM employees.emp
    GROUP BY deptno
)
SELECT d.deptno, d.dname, dec.num_employees
FROM employees.dept d
JOIN DeptEmployeeCount dec ON d.deptno = dec.deptno;

-- Define a CTE to calculate the average salary by department
WITH AvgSalary AS (
    SELECT deptno, AVG(sal) AS avg_sal
    FROM employees.emp
    GROUP BY deptno
)
SELECT d.deptno, d.dname, a.avg_sal
FROM employees.dept d
JOIN AvgSalary a ON d.deptno = a.deptno;

-- Define a CTE to list employees and their associated projects
WITH EmployeeProjects AS (
    SELECT e.empno, e.ename, ep.projectno, p.budget
    FROM employees.emp e
    JOIN employees.emp_projects ep ON e.empno = ep.empno
    JOIN employees.projects p ON ep.projectno = p.projectno
)
SELECT empno, ename, projectno, budget
FROM EmployeeProjects;

-- Define a CTE to rank employees by salary within each department
WITH RankedEmployees AS (
    SELECT empno, ename, deptno, sal,
           ROW_NUMBER() OVER (PARTITION BY deptno ORDER BY sal DESC) AS row_num,
           RANK() OVER (PARTITION BY deptno ORDER BY sal DESC) AS rank,
           DENSE_RANK() OVER (PARTITION BY deptno ORDER BY sal DESC) AS dense_rank
    FROM employees.emp
)
SELECT empno, ename, deptno, sal, row_num, rank, dense_rank
FROM RankedEmployees;

-- Define a CTE to calculate running total of salaries within each department
WITH RunningTotal AS (
    SELECT empno, ename, deptno, sal,
           SUM(sal) OVER (PARTITION BY deptno ORDER BY empno ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
    FROM employees.emp e 
)
SELECT empno, ename, deptno, sal, running_total
FROM RunningTotal;
```
## Using Multiple CTEs
* You can define multiple CTEs in a single query, separated by commas.
```sql
-- Define CTEs to calculate total salary and average salary by department
WITH TotalSalary AS (
    SELECT deptno, SUM(sal) AS total_sal
    FROM employees.emp
    GROUP BY deptno
),
AvgSalary AS (
    SELECT deptno, AVG(sal) AS avg_sal
    FROM employees.emp
    GROUP BY deptno
)
-- Retrieve department numbers, total salary, and average salary
SELECT t.deptno, t.total_sal, a.avg_sal
FROM TotalSalary t
JOIN AvgSalary a ON t.deptno = a.deptno;

WITH TotalSalary AS (
    SELECT deptno, SUM(sal) AS total_sal
    FROM employees.emp d 
    GROUP BY deptno
),
TotalBudget AS (
    SELECT e.deptno, SUM(p.budget) AS total_budget
    FROM employees.emp e
    JOIN employees.emp_projects ep ON e.empno = ep.empno
    JOIN employees.projects p ON ep.projectno = p.projectno
    GROUP BY e.deptno
)
-- Retrieve department numbers, total salary, and total project budget
SELECT ts.deptno, ts.total_sal, tb.total_budget
FROM TotalSalary ts
JOIN TotalBudget tb ON ts.deptno = tb.deptno;
```
## Recursive CTEs
* Recursive CTEs are used to perform operations like traversing hierarchical data or generating sequences.
* Recursive CTEs use the RECURSIVE keyword and consist of two parts: an anchor member and a recursive member.
```sql
-- Define a recursive CTE to generate a sequence of numbers
WITH Sequence AS (
    SELECT 1 AS num
    UNION ALL
    SELECT num + 1
    FROM Sequence
    WHERE num < 10
)
SELECT num
FROM Sequence;

-- Define a recursive CTE to find the management hierarchy
WITH EmpHierarchy AS (
    -- Anchor member: select the top-level manager (president)
    SELECT empno, ename, job, mgr
    FROM employees.emp
    WHERE mgr IS NULL
    
    UNION ALL
    
    -- Recursive member: select employees managed by the current level
    SELECT e.empno, e.ename, e.job, e.mgr
    FROM employees.emp e
    INNER JOIN EmpHierarchy eh ON e.mgr = eh.empno
)
-- Retrieve the management hierarchy
SELECT *
FROM EmpHierarchy;
```
## Common Use Cases for CTEs
* Breaking down complex queries into simpler, more manageable parts.
* Improving readability and maintainability of SQL code.
* Recursively traversing hierarchical data.
* Generating sequences or performing iterative calculations.
## Benefits of Using CTEs
* Enhanced code readability and organization.
* Ability to reference the same CTE multiple times in a query.
* Simplified complex queries by breaking them into smaller, logical components.

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
