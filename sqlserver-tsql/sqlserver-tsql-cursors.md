![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Cursors
* In SQL Server, cursors are used to fetch and process rows from a result set one at a time.
* They are particularly useful when you need to perform row-by-row operations.

## Basic Cursor Usage
```sql
-- Decrease Salaries of All Employees by 10%
DECLARE @EmpID INT;
DECLARE @Salary DECIMAL(10, 2);

-- Declare the cursor
DECLARE EmployeeCursor CURSOR FOR
SELECT empno, sal FROM employees.emp;

-- Open the cursor
OPEN EmployeeCursor;

-- Fetch the first row from the cursor
FETCH NEXT FROM EmployeeCursor INTO @EmpID, @Salary;

-- Loop through all rows
WHILE @@FETCH_STATUS = 0
BEGIN
    -- Decrease the salary by 10%
    UPDATE employees.emp SET sal = @Salary * 0.90 WHERE empno = @EmpID;

    -- Fetch the next row from the cursor
    FETCH NEXT FROM EmployeeCursor INTO @EmpID, @Salary;
END
-- Close and deallocate the cursor
CLOSE EmployeeCursor;
DEALLOCATE EmployeeCursor;
```
* In this example, we use a cursor to iterate through all rows in the employees table and decrease the salaries of each employee by 10%. The cursor fetches each row into variables @EmpID and @Salary, which are then used in an UPDATE statement to modify the salary.

## Cursor with Dynamic SQL
```sql
-- Generate Department Salary Summary
BEGIN
    -- Drop the summary table if it exists
    BEGIN TRY
        EXEC('DROP TABLE employees.dept_summary');
    END TRY
    BEGIN CATCH
    END CATCH;

    -- Create a table to hold per‐department summary
    CREATE TABLE employees.dept_summary
    (
        deptno          INT       PRIMARY KEY,
        dname           VARCHAR(14),
        employee_count  INT,
        total_salary    NUMERIC(12,2),
        avg_salary      NUMERIC(12,2)
    );

    -- Declare variables for cursor processing
    DECLARE 
        @DeptNo     INT,
        @DName      VARCHAR(14),
        @EmpCount   INT,
        @TotalSal   NUMERIC(12,2),
        @AvgSal     NUMERIC(12,2);

    -- Define cursor to iterate all departments
    DECLARE DeptCursor CURSOR FOR
        SELECT deptno, dname
        FROM employees.dept;

    OPEN DeptCursor;

    FETCH NEXT FROM DeptCursor
    INTO @DeptNo, @DName;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Compute headcount, total and average salary per department
        SELECT 
            @EmpCount = COUNT(*),
            @TotalSal = SUM(sal),
            @AvgSal   = AVG(sal)
        FROM employees.emp
        WHERE deptno = @DeptNo;

        -- Insert results into the summary table
        INSERT INTO employees.dept_summary
            (deptno, dname, employee_count, total_salary, avg_salary)
        VALUES
            (
                @DeptNo,
                @DName,
                ISNULL(@EmpCount, 0),
                ISNULL(@TotalSal, 0),
                ISNULL(@AvgSal,   0)
            );

        -- Move to the next department
        FETCH NEXT FROM DeptCursor
        INTO @DeptNo, @DName;
    END

    -- Clean up
    CLOSE DeptCursor;
    DEALLOCATE DeptCursor;
END;
-- View the summary
SELECT * 
FROM employees.dept_summary;
```
* In this example, we use a cursor to iterate through all departments in the dept table and generate salary summary for each department. The cursor fetches the department number into the variable @DeptNo, which is then used to calculate the total amount for the employees salaries and insert a new record into the dept_summary table.

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
