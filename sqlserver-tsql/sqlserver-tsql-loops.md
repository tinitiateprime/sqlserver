![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](./README.md)

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

```sql

DECLARE @EmpName VARCHAR(10);
DECLARE @Salary DECIMAL(10, 2);
DECLARE @RunningTotal DECIMAL(10, 2) = 0;

-- Declare a cursor
DECLARE emp_cursor CURSOR FOR
    SELECT ename, sal
    FROM employees.emp
    ORDER BY empno;

-- Open the cursor
OPEN emp_cursor;

-- Fetch the first row
FETCH NEXT FROM emp_cursor INTO @EmpName, @Salary;

-- Loop through all rows
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @RunningTotal = @RunningTotal + @Salary;
    PRINT @EmpName + ' - Salary: ' + CAST(@Salary AS VARCHAR) + ' | Running Total: ' + CAST(@RunningTotal AS VARCHAR);
    
    -- Fetch the next row
    FETCH NEXT FROM emp_cursor INTO @EmpName, @Salary;
END;

-- Close and deallocate the cursor
CLOSE emp_cursor;
DEALLOCATE emp_cursor;
GO

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
DECLARE @EmpID INT = 7521; -- Start with WARD
DECLARE @MgrID INT;
DECLARE @MgrName VARCHAR(10);

-- Find the initial manager for the given employee
SELECT @MgrID = mgr
FROM employees.emp
WHERE empno = @EmpID;

-- Loop until the manager ID is NULL (the top of the hierarchy)
WHILE @MgrID IS NOT NULL
BEGIN
    -- Get the name and next manager in the chain
    SELECT @MgrName = ename, @MgrID = mgr
    FROM employees.emp
    WHERE empno = @MgrID;

    PRINT 'Manager Name: ' + @MgrName;
END;
GO

```sql



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


```sql

-- Step 1: Set up initial variables
DECLARE @DeptNo INT = 10; -- 'ACCOUNTING' department
DECLARE @EmployeeCount INT;
DECLARE @NewEmpID INT;

-- Step 2: Get the initial employee count for the department
SELECT @EmployeeCount = COUNT(*) FROM employees.emp WHERE deptno = @DeptNo;

-- Step 3: Simulate the DO WHILE loop
PRINT 'Starting employees in Accounting: ' + CAST(@EmployeeCount AS VARCHAR);

WHILE @EmployeeCount < 5
BEGIN
    -- This block will execute at least once
    
    -- Find the next available employee ID
    SELECT @NewEmpID = ISNULL(MAX(empno), 7000) + 1 FROM employees.emp;

    -- Insert a new employee into the 'ACCOUNTING' department
    INSERT INTO employees.emp (empno, ename, job, hiredate, sal, deptno)
    VALUES (@NewEmpID, 'NEW HIRE', 'CLERK', GETDATE(), 1000.00, @DeptNo);

    -- Update the employee count for the next loop check
    SELECT @EmployeeCount = COUNT(*) FROM employees.emp WHERE deptno = @DeptNo;
    
    PRINT 'Added new employee. Current count: ' + CAST(@EmployeeCount AS VARCHAR);

    -- The condition (@EmployeeCount < 5) is checked here at the END of the loop
END;

PRINT 'Final employee count in Accounting: ' + CAST(@EmployeeCount AS VARCHAR);

-- You can also view the new employees
SELECT ename, job, deptno
FROM employees.emp
WHERE deptno = @DeptNo;

```
* In this example, we use a `WHILE` loop to simulate a `DO WHILE` loop by continuously adding new projects to the projects table until there are 10 projects. The loop checks the condition at the end of each iteration, ensuring that the code inside the loop is executed at least once.

##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
