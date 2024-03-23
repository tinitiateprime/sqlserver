![SQL Server Tinitiate Image](sqlserver_tinitiate.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# DQL - Set Operations
* Set operations in SQL are used to combine or compare the results of two or more queries.
* These are essential for manipulating and combining data from multiple tables.
* The main set operations include UNION, INTERSECT, and EXCEPT.

## Set Operations in SQL Server:
### UNION:
* The UNION operator is used to combine the results of two or more SELECT statements into a single result set.
* It returns all distinct rows from both result sets. It removes duplicate rows by default.
```sql
-- Retrieve unique department numbers from both the employees
-- and projects tables
SELECT deptno FROM employees.emp
UNION
SELECT projectno AS deptno FROM employees.projects;

-- Retrieve unique employee names and project names from both the employees
-- and projects tables
SELECT ename AS name FROM employees.emp
UNION
SELECT 'Project: ' + CAST(projectno AS VARCHAR) AS name FROM employees.projects;

-- Combine the names of employees, departments, and projects
SELECT ename AS name FROM employees.emp
UNION
SELECT dname AS name FROM employees.dept
UNION
SELECT CAST(projectno AS VARCHAR) AS name FROM employees.projects;

-- UNION ALL: This operator does same as UNION with including duplicate rows
-- Retrieve all department numbers from both the employees
-- and projects tables
SELECT deptno FROM employees.emp
UNION ALL
SELECT projectno AS deptno FROM employees.projects;
```
### INTERSECT:
* The INTERSECT operator is used to retrieve the common rows that appear in the result sets of two or more SELECT statements. It removes duplicate rows by default.
```sql
-- Retrieve grade number that exist in both the employees
-- and projects tables
SELECT grade FROM employees.salgrade
INTERSECT
SELECT projectno AS grade FROM employees.projects;

-- Retrieve employee names that exist in both the employees
-- and projects tables
SELECT ename AS name FROM employees.emp
INTERSECT
SELECT 'Project: ' + CAST(projectno AS VARCHAR) AS name FROM employees.projects;
```
### EXCEPT:
* The EXCEPT operator is used to retrieve the rows that appear in the first result set but not in the result sets of one or more subsequent SELECT statements. It removes duplicate rows by default.
```sql
-- Retrieve empno numbers from the employees table that
-- do not exist in the emp_projects table
SELECT empno FROM employees.emp
EXCEPT
SELECT empno FROM employees.emp_projects;

-- Retrieve employee names from the employees table that
-- do not exist in the projects table
SELECT ename AS name FROM employees.emp
EXCEPT
SELECT 'Project: ' + CAST(projectno AS VARCHAR) AS name FROM employees.projects;
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|