![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Loops
* Loops are used to execute a block of code repeatedly based on a condition. 

## WHILE Loop
* The `WHILE` loop executes a block of code repeatedly as long as a specified condition is true.
```sql
-- Increase salaries of employees by 10%
DECLARE @EmpID INT;

-- Get the first Employee ID
SELECT @EmpID = MIN(empno) FROM employees.emp;

WHILE @EmpID IS NOT NULL
BEGIN
    -- Increase salaries by 10%
    UPDATE employees.emp SET sal = sal * 1.10 WHERE empno = @EmpID;
    -- Get the next Part ID
    SELECT @EmpID = MIN(empno) FROM employees.emp WHERE empno > @EmpID;
END
```
* In this example, we use a `WHILE` loop to increase the salaries of all employees in the emp table by 10%. The loop continues until there are no more employees to update.

## FOR Loop
* `FOR` loop executes a block of code a specific number of times.
* SQL Server does not have a traditional `FOR` loop like some other programming languages. However, you can achieve similar functionality using a `WHILE` loop with a counter variable.
``` sql
-- Print Names of First 3 Projects
DECLARE @Counter INT = 1;

WHILE @Counter <= 3
BEGIN
    SELECT project_name FROM employees.projects WHERE projectno = @Counter;
    SET @Counter = @Counter + 1;
END
```
* In this example, we use a `WHILE` loop to print the names of the first 3 projects from the projects table. The loop runs as long as the @Counter variable is less than or equal to 3.

## DO WHILE Loop
* SQL Server does not have a built-in `DO WHILE` loop, but you can simulate it using a `WHILE` loop with a `BEGIN...END` block.
```sql
-- Add New Projects Until 10 Projects Exist
DECLARE @Count INT;

SELECT @Count = COUNT(*) FROM employees.projects;

WHILE @Count < 10
BEGIN
    INSERT INTO employees.projects (projectno, project_name, budget) VALUES (@Count+1, 'New Project', 50000.00);
    SELECT @Count = COUNT(*) FROM employees.projects;
END
```
* In this example, we use a `WHILE` loop to simulate a `DO WHILE` loop by continuously adding new projects to the projects table until there are 10 projects. The loop checks the condition at the end of each iteration, ensuring that the code inside the loop is executed at least once.

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
