![Tinitiate SQLSERVER Training](./sqlserver_tinitiate.png)

# T-SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Variables & Operators

In T-SQL, you can leverage variables and operators effectively to manipulate and retrieve data from tables like emp (employees) and dept (departments). Here’s a step-by-step guide on how to use these features to perform dynamic queries and data manipulation in a SQL Server environment.

## Declaring Variables
Variables in T-SQL are used to store data temporarily. Here's how you might declare variables to use with the emp and dept tables:

```sql
DECLARE @DeptID INT;   -- Variable to store department ID
DECLARE @DeptName VARCHAR(100); -- Variable to store department name
```

## Setting Variable Values
You can set values to these variables directly or from a table:

```sql
-- Set a specific value
SET @DeptID = 10;

-- Set value based on a query
SELECT @DeptName = dept_name FROM dept WHERE dept_id = @DeptID;
```

## Using Variables in Queries
Once variables are set, you can use them in your queries to filter, update, or manipulate data:

```sql
-- Select query using a variable
SELECT emp_name, job_title FROM emp WHERE dept_id = @DeptID;

-- Update query using a variable
UPDATE emp SET dept_id = @DeptID WHERE emp_name LIKE '%John Doe%';
```

## Using Operators
Operators in T-SQL can be used to perform calculations, compare values, or combine conditions. Here are some examples using operators with the emp and dept tables:

### Arithmetic Operators
```sql
-- Calculate an increase in salary
DECLARE @RaiseAmount DECIMAL(10,2);
SET @RaiseAmount = 500.00;

UPDATE emp SET salary = salary + @RaiseAmount WHERE dept_id = @DeptID;
```
### Comparison Operators
```sql
-- Find employees in a specific department and with a salary greater than a certain amount
SELECT emp_name, salary FROM emp WHERE dept_id = @DeptID AND salary > 50000;
```
### Logical Operators
```sql
-- Find employees who are either in a specific department or whose job title is 'Manager'
SELECT emp_name, dept_id, job_title FROM emp WHERE dept_id = @DeptID OR job_title = 'Manager';
```
## Combining Variables and Operators
You can combine variables and operators to make your scripts dynamic and efficient:

```sql
-- Check if a department exists and assign a new employee to it
IF EXISTS (SELECT 1 FROM dept WHERE dept_id = @DeptID)
BEGIN
    INSERT INTO emp (emp_name, job_title, dept_id) VALUES ('Alice Johnson', 'Developer', @DeptID);
END
ELSE
BEGIN
    PRINT 'Department does not exist';
END
```
## Summary
In T-SQL, variables help you write cleaner and more efficient queries by storing data that can be reused multiple times within scripts or batches. Operators allow you to perform a range of logical, arithmetic, and comparison operations that are essential for querying and manipulating data based on dynamic conditions. 

Combining variables and operators, you can create powerful scripts for querying and managing your data in the emp and dept tables effectively.






