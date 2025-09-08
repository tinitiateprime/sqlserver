![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](./README.md)

# Cursors
A cursor is a database object used to process the rows of a result set one at a time. While a cursor is a powerful tool for row-by-row operations, it's generally considered a last resort in T-SQL due to significant performance drawbacks.

## When to Use Cursors
Cursors are a procedural approach in a set-based language. They should be used only when a task cannot be performed in a single, efficient, set-based operation. Common use cases include:

### Hierarchical Traversal: 
Navigating a tree-like structure, such as a management hierarchy, where each step depends on the previous one.

### Administrative Tasks: 
Performing maintenance actions on a series of database objects, like dropping tables with a specific prefix.

### Dynamic SQL: 
Executing a unique, dynamically generated SQL command for each row in a result set.

## When to Avoid Cursors 🚫
The primary reason to avoid cursors is performance. A cursor-based operation is often many times slower than its set-based alternative. This is because cursors:

* Require more memory and CPU overhead.

* Cause excessive logging.

* Prevent the query optimizer from creating efficient plans.

Your examples of decreasing salaries and creating a department summary are perfect illustrations of when not to use a cursor. Both tasks can be performed much more efficiently with a single, set-based query.

## Set-Based Alternatives  
### Set-Based Salary Update
Instead of a cursor, a single UPDATE statement can perform the same salary decrease for all employees at once. This is the correct, highly performant way to manipulate large sets of data.

```sql

UPDATE employees.emp
SET sal = sal * 0.90;
```
### Set-Based Department Summary
Similarly, the department salary summary can be generated using a single SELECT statement with GROUP BY and then directly inserted into the summary table.

```sql
-- Drop the summary table to start fresh
DROP TABLE IF EXISTS employees.dept_summary;

-- Create the summary table
CREATE TABLE employees.dept_summary
(
    deptno INT PRIMARY KEY,
    dname VARCHAR(14),
    employee_count INT,
    total_salary NUMERIC(12,2),
    avg_salary NUMERIC(12,2)
);

-- Insert data from a single, set-based query
INSERT INTO employees.dept_summary
    (deptno, dname, employee_count, total_salary, avg_salary)
SELECT
    d.deptno,
    d.dname,
    COUNT(e.empno),
    SUM(e.sal),
    AVG(e.sal)
FROM
    employees.dept AS d
LEFT JOIN
    employees.emp AS e ON d.deptno = e.deptno
GROUP BY
    d.deptno, d.dname;

-- View the summary
SELECT * FROM employees.dept_summary;
```
## Cursor Options and Performance
While cursors are generally discouraged, understanding their different options is critical for working with existing codebases and for the few scenarios where they're necessary. Cursor options can significantly impact performance, concurrency, and memory usage.

### Cursor Types
There are four main types of cursors, each with a different purpose and performance profile.

* FORWARD_ONLY (Default): The most efficient cursor type. It can only move forward through the result set, one row at a time. It's read-only and uses minimal resources. This is the preferred cursor type when you have to use one.

* STATIC: A STATIC cursor creates a full, temporary copy of the result set in tempdb. This makes it slow to open but guarantees that the data you're working with won't change while the cursor is open. Changes made to the underlying tables are not visible to the cursor.

* KEYSET: The KEYSET cursor creates a copy of the keys (e.g., primary keys) for all the rows in the result set. This allows you to move forward and backward through the rows. Data changes to non-key columns are visible to the cursor, but new rows inserted into the table after the cursor is opened are not.

* DYNAMIC: The least performant and most resource-intensive cursor type. It reflects all data changes (inserts, updates, and deletes) as you move through the result set. This provides the most up-to-date view of the data but at a high cost.

###  Using FORWARD_ONLY for Efficiency
This example demonstrates how to explicitly declare a FORWARD_ONLY cursor for a one-time, sequential task, which is the best-case scenario for cursor usage.

```sql
DECLARE @EmpID INT;
DECLARE @Salary DECIMAL(10, 2);

-- Explicitly declare a FORWARD_ONLY cursor for best performance
DECLARE EmployeeCursor CURSOR FORWARD_ONLY FOR
SELECT empno, sal FROM employees.emp;

OPEN EmployeeCursor;

FETCH NEXT FROM EmployeeCursor INTO @EmpID, @Salary;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT 'Processing employee: ' + CAST(@EmpID AS VARCHAR);
    -- Perform some action that requires row-by-row logic
    FETCH NEXT FROM EmployeeCursor INTO @EmpID, @Salary;
END;

CLOSE EmployeeCursor;
DEALLOCATE EmployeeCursor;
```

### Cursors and Concurrency
Cursors can lead to concurrency issues and deadlocks, especially when they lock resources for an extended period. The READ_ONLY and SCROLL options control how cursors interact with the underlying data.

* READ_ONLY: Prevents updates made through the cursor and is a good practice for performance. It signals to the optimizer that it doesn't need to acquire update locks.

* SCROLL: Allows the cursor to move both forward and backward. This option is required for STATIC, KEYSET, and DYNAMIC cursors.

```sql

-- This cursor is less efficient and prone to concurrency issues
-- due to its SCROLL and UPDATE options.
DECLARE EmployeeCursor CURSOR SCROLL FOR
SELECT empno, ename, sal FROM employees.emp;

```
##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
