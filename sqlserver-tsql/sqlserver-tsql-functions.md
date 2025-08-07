![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Functions
Functions are reusable routines that accept input parameters, perform an operation, and return a single value (scalar function) or a table (table-valued function).

## Function with Input Parameter
* In SQL Server, you can create functions that accept input parameters, allowing you to pass values to the function and perform operations based on those values.
```sql
-- Function to Get Employee Details by Department Number
CREATE FUNCTION GetEmployeesByDepartment (@DeptID INT)
RETURNS TABLE
AS
RETURN
    SELECT empno, ename, job
    FROM employees.emp
    WHERE deptno = @DeptID;
```
* Execute the function
```sql
-- Use the function to get employee details for department id 30
SELECT * FROM GetEmployeesByDepartment(30);
```
* We create a table-valued function named `GetEmployeesByDepartment` that takes an integer parameter` @DeptID`, representing the department ID.
* The function returns a table that contains the employee ID, employee name, and job title for all employees who work in the department specified by` @DeptID`.
* The `WHERE` clause in the `SELECT` statement filters the employees based on the department ID.
* To use the function, we call it in a `SELECT` statement, passing the desired department ID as an argument.
* In this case, we pass '10' to get the details of employees in department 10.

## Function with Default Parameter Value
* We can assign default values to parameters in stored procedures and functions.
* When a default value is specified for a parameter, you can omit that parameter when calling the procedure or function, and the default value will be used instead.
``` sql
-- Function to Get Employee Details by Department Number with default parameter
CREATE FUNCTION employees.GetEmployeesByDepartmentDefault (@DeptID INT = NULL)
RETURNS TABLE
AS
RETURN
    SELECT empno, ename, job
    FROM employees.emp
    WHERE deptno = ISNULL(@DeptID, deptno);
```
* Execute the function
``` sql
-- Use the function without specifying a department ID
SELECT * FROM employees.GetEmployeesByDepartmentDefault(DEFAULT);
-- Use the function with a specific department ID
SELECT * FROM employees.GetEmployeesByDepartmentDefault(10);
```
* We create a table-valued function named `GetEmployeesByDepartmentDefault` with an  integer parameter `@DeptID`. We assign a default value of `NULL` to `@DeptID`.
* The function returns a table containing the employee ID, employee name, and  job title.
* The `WHERE` clause uses the `ISNULL` function to check if `@DeptID` is `NULL`. If it  is, the condition `dept_id = dept_id` is effectively ignored, and employees  from all departments are returned. If `@DeptID` is not NULL, only employees  from the specified department are returned.
* When calling the function, you can either omit the parameter to get  employees from all departments or provide a specific department ID to get  employees from that department. 

## Return Statement
* In SQL Server, the `RETURN` statement is used in functions to exit the function and return a value to the caller.
* The value returned by the function can be a scalar value or a table, depending on the type of function.
### Scalar Functions
* A scalar function returns a single value (e.g., an integer, a decimal, or a string). In a scalar function, the `RETURN` statement is used to specify the value that should be returned.
```sql
CREATE FUNCTION employees.GetEmployeeCount()
RETURNS INT
AS
BEGIN
    DECLARE @Count INT;

    -- Count the number of employees
    SELECT @Count = COUNT(*) FROM employees.emp;

    -- Return the count
    RETURN @Count;
END
-- Use the function
SELECT employees.GetEmployeeCount() AS EmployeeCount;
```
### Table-Valued Functions
* A table-valued function returns a table. In a table-valued function, the `RETURN` statement is used to return a table variable or to conclude a `RETURN` clause that contains a `SELECT` statement.
* Inline Table-Valued Function, the `RETURN` statement directly contains a `SELECT` statement that produces the result set.
```sql
CREATE FUNCTION employees.GetEmployeesByDepartment(@DeptID INT)
RETURNS TABLE
AS
RETURN (
    SELECT ename, job FROM employees.emp WHERE deptno = @DeptID
)
-- Use the function
SELECT * FROM employees.GetEmployeesByDepartment(20);
```
* In this example, the `GetEmployeesByDepartment` function returns a table containing the names and job titles of employees in a specified department.
* In a multi-statement table-valued function, the `RETURN` statement is used to return a declared table variable.
```sql
CREATE FUNCTION employees.GetAllEmployees()
RETURNS @EmployeeTable TABLE (ename VARCHAR(100), job VARCHAR(100))
AS
BEGIN
    -- Insert data into the table variable
    INSERT INTO @EmployeeTable (ename, job)
    SELECT ename, job FROM emp;
    
    -- Return the table variable
    RETURN;
END
-- Use the function
SELECT * FROM employees.GetAllEmployees();
```
### Key Points
* In scalar functions, the `RETURN` statement specifies the single value to be returned.
* In table-valued functions, the `RETURN` statement is used to return a result set or a table variable.
* The `RETURN` statement immediately exits the function and returns control to the caller.

## Execute the Function with Begin and End
```sql
-- Execute the Function with Begin and End:
BEGIN
    -- Execute a scalar function and store the result in a variable
    DECLARE @TotalEmployees INT;
    SET @TotalEmployees = employees.GetEmployeeCount();
    PRINT 'Total number of employees: ' + CAST(@TotalEmployees AS VARCHAR);
END

-- Executing a Table-Valued Function with Begin and End
BEGIN
    -- Execute a table-valued function and use the result set directly
    SELECT * FROM employees.GetEmployeesByDepartment(10);

    -- Alternatively, store the result set in a table variable for further processing
    DECLARE @EmployeeDetails TABLE (emp_name VARCHAR(100), job_title VARCHAR(100));
    INSERT INTO @EmployeeDetails
    SELECT * FROM employees.GetEmployeesByDepartment(10);

    SELECT * FROM @EmployeeDetails;
END
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
