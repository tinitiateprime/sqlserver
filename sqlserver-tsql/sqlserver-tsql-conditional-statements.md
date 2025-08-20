![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](./README.md)

# Conditional Statements
* Conditional statements in SQL Server, such as `IF...ELSE`, `CASE`, and `IIF`, are useful for executing different SQL statements based on specific conditions.

## IF...ELSE Statement
* The `IF...ELSE` statement allows you to execute a block of SQL statements if a condition is true, and another block if the condition is false.
```sql
-- Check if a Department Exists
DECLARE @DeptName VARCHAR(100) = 'accounting';

IF EXISTS (SELECT 1 FROM employees.dept WHERE dname = @DeptName)
    BEGIN
        PRINT 'The department exists.';
    END
ELSE
    BEGIN
        PRINT 'The department does not exist.';
    END
```
* In this example, we check if there is a department named 'accounting' in the dept table. If it exists, we print a message indicating that the department exists. Otherwise, we print a message indicating that it does not exist.

## CASE Statement
* The `CASE` statement is used for conditional logic within a SELECT query. It evaluates a list of conditions and returns a result for the first condition that is true.
 ```sql
SELECT 
    ename,
    CASE 
        WHEN sal < 1500 THEN 'Low'
        WHEN sal BETWEEN 1500 AND 3000 THEN 'Medium'
        ELSE 'High'
    END AS SalaryCategory
FROM employees.emp;
```
* In this example, we categorize employees into 'Low', 'Medium', and 'High' salary groups based on their salary in the emp table.

## IIF Function
* The `IIF` function is a shorthand way to write a simple IF...ELSE condition. It takes three arguments: a condition, a true value, and a false value.
```sql
SELECT 
    ename,
    sal,
    IIF(sal > (SELECT AVG(sal) FROM employees.emp), 'Above Average', 'Below Average') AS SalaryStatus
FROM employees.emp;
```
* In this example, we use the `IIF` function to check if each employee's salary is above the average salary in the emp table. The result is a column that indicates whether each employee's salary is 'Above Average' or 'Below Average'.

##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
