![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](./README.md)

# VIEWS
* A view is a virtual table based on the result-set of an SQL statement.
* Views contain rows and columns, just like a real table, and the fields in a view are fields from one or more real tables in the database.
* You can use views to simplify complex queries, enhance security by restricting access to underlying tables, and abstract data in a way that users find natural or intuitive.

## Key Characteristics of Views:
* **Simplification of Complex Queries:** Views can encapsulate complex queries with joins, filters, and calculations, presenting a simple interface to the user or application.
* **Data Abstraction:** Users can interact with data without needing to understand details about the underlying table structures.
* **Security:** Views can limit the visibility of certain data within the database, thereby providing a security mechanism to restrict access to sensitive information.
* **Updateability:**  Depending on the SQL Server version and the view’s complexity, some views are updateable, meaning you can perform INSERT, UPDATE, or DELETE operations on the view.

## Creating Views
* Here is how you can create a simple view
```sql
CREATE VIEW vw_EmployeeInfo
AS
SELECT empno, ename, job, deptno
FROM employees.emp
WHERE job LIKE '%Manager%';
```
* This view vw_EmployeeInfo shows a list of employees who are managers.

## Using Views
* Once a view is created, you can use it just like you would use a table.
* Here’s how you can query the view:
```sql
SELECT * FROM vw_EmployeeInfo;
```

## Modifying Views
* To change a view after it has been created, you can use the ALTER VIEW statement:
```sql
ALTER VIEW vw_EmployeeInfo
AS
SELECT empno, ename, job, deptno, sal
FROM employees.emp
WHERE job LIKE '%Manager%' AND sal > 2500;
```
* This modification adds a filter to display managers with salary greater than 2500.

## Dropping Views
* If you no longer need a view, you can remove it using the DROP VIEW statement:
```sql
DROP VIEW vw_EmployeeInfo;
```

## Complex Views
* Complex views in SQL Server that involve joining multiple tables is a common practice to encapsulate complex SQL queries into a simpler form that can be reused.
* This is particularly useful in scenarios where you have normalized databases with data spread across multiple related tables, and you frequently need to aggregate this data for reporting or business logic purposes.
* Here's an example of how to create a complex view in SQL Server that involves multiple joins across several tables. Suppose we have a typical business database with tables for employees (emp), departments (dept), projects (projects), and employee assignments to projects (emp_projects). We'll create a view that provides a comprehensive overview of employee details along with their department names and projects they are working on.
### Scenario:
* You want a view that shows the following for each employee: Employee ID and name, Department name, List of projects they are assigned to.
```sql
CREATE VIEW vw_EmployeeDetails
AS
SELECT 
    e.empno,
    e.ename,
    d.dname,
    STRING_AGG(p.project_name, ', ') WITHIN GROUP (ORDER BY p.project_name)
    AS Projects
FROM 
    employees.emp e
    INNER JOIN employees.dept d ON e.deptno = d.deptno
    LEFT JOIN employees.emp_projects ep ON e.empno = ep.empno
    LEFT JOIN employees.projects p ON ep.projectno = p.projectno
GROUP BY 
    e.empno,
    e.ename,
    d.dname;
```
### Explanation:
* **INNER JOIN** between emp and dept: This join ensures that we only get employees who are assigned to departments. It connects each employee with their respective department.
* **LEFT JOIN** between emp and emp_project, and emp_project to project: These joins are used to gather project information for each employee. The use of LEFT JOIN ensures that employees who are not assigned to any project are also included in the results, with their project information being null.
* **STRING_AGG** function aggregates the project names into a single comma-separated string for each employee. It is a convenient way to list all projects associated with an employee in a single row of the view. The WITHIN GROUP (ORDER BY p.project_name) clause orders the projects by name within each aggregated string.
* **GROUP BY** clause is necessary because the STRING_AGG function is an aggregate function. We group by employee ID, name, and department name to ensure that our aggregate function (STRING_AGG) works across the correct grouping of data.
### Usage:
* To use this view to fetch employee details along with their department and projects:
```sql
SELECT * FROM vw_EmployeeDetails;
```

## Updating Using Simple View
* Here is an example of creating a simple updatable view and using it to update data:
```sql
-- Creating a simple view on the employees table
CREATE VIEW vw_EmployeeBasicInfo AS
SELECT empno, ename, job
FROM employees.emp;

-- Updating data through the view
UPDATE vw_EmployeeBasicInfo
SET job = 'Developer'
WHERE empno = 7788;
```

## Updating Using Complex View
* Here is an Example of a Complex View with an `INSTEAD OF` trigger
* For complex views, you can use `INSTEAD OF` triggers to specify custom actions to take when an insert, update, or delete operation is attempted on the view:
```sql
-- Creating a complex view with a join
CREATE VIEW vw_EmployeeDept AS
SELECT e.empno, e.ename, e.job, d.dname
FROM employees.emp e
JOIN employees.dept d ON e.deptno = d.deptno;

-- Creating an INSTEAD OF UPDATE trigger on the view
CREATE TRIGGER trg_UpdateEmployeeDept ON vw_EmployeeDept
INSTEAD OF UPDATE
AS
BEGIN
    -- Update the emp table based on the view update
    UPDATE employees.emp
    SET ename = INSERTED.ename,
    job = INSERTED.job
    FROM INSERTED
    WHERE emp.empno = INSERTED.empno;
    -- Update logic for dept could also be included if needed
END;

-- Updating data through the view
UPDATE vw_EmployeeDept
SET job = 'analyst'
WHERE empno = 7788;
```
* In this scenario, vw_EmployeeDept includes a join, making it complex and typically not updatable directly.
* The `INSTEAD OF` trigger, `trg_UpdateEmployeeDept`, intercepts update operations on the view and provides the necessary SQL commands to update the underlying emp table accordingly.

##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
