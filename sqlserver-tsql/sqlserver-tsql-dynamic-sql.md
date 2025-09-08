![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL Tutorial
&copy; TINITIATE.COM

##### [Back To Contents](./README.md)

# Dynamic SQL
* Dynamic SQL is a technique where you build and execute SQL statements at runtime as a string, rather than writing them as fixed queries.
* It’s useful when query parts (like table names, column names, filters) need to be determined dynamically, often based on parameters or user input.
#### PROS:
Using Dynamic SQL offers benefits such as increased flexibility through the utilization of parameters in query construction, and improved performance due to the generation of a more efficient execution plan.
#### CONS:
Dynamic SQL has several drawbacks, including difficulties in debugging, unreliable error management, susceptibility to SQL injection attacks, and potential security concerns. Additionally, Dynamic SQL can be slower than static SQL since the SQL Server must generate a new execution plan every time at runtime. Furthermore, it requires users to have direct access permissions on all accessed database objects, such as tables and views.

## Create a test table for Dynamic SQL
```sql
-- Create table 'dynsql_test'
CREATE TABLE dynsql_test (
     test_id       INT
    ,test_date     DATE
    ,test_string   VARCHAR(1000)
    ,test_decimal  DECIMAL(10,2)
);
```

## Dynamic SQL using `EXEC`
```sql
-- EXEC Demo Block
DECLARE  @test_id      INT
        ,@test_date    VARCHAR(1000)
        ,@test_string  VARCHAR(1000)
        ,@test_decimal DECIMAL(10,2)
        ,@sql          VARCHAR(3000)

-- Assign values
SET @test_id      = 1
SET @test_date    = 'GETDATE()'
SET @test_string  = 'TEST'
SET @test_decimal = 10.2

-- Build dynamic statement
SET @sql = 'INSERT INTO dynsql_test VALUES( ' +
           CAST(@test_id AS VARCHAR) +' , '+
           CAST(@test_date AS VARCHAR) +' , '+
           ''''+CAST(@test_string AS VARCHAR)+''''+' , '+
           CAST(@test_decimal AS VARCHAR) + ');'
           
-- Print the @sql statement
PRINT @sql

-- Execute dynamic statement
EXEC(@sql)
PRINT 'Rows Affected ' + CAST(@@rowcount AS VARCHAR)
```

## Dynamic SQL using `sp_executesql`
* `sp_executesql` is a system stored procedure in SQL Server that is used to execute dynamic SQL statements or batches of code that are constructed at runtime. It can be used as an alternative to the `EXECUTE` statement, and offers some advantages over it.
* One of the main advantages of `sp_executesql` is that it allows for parameterized queries, which can help to improve performance and security by reducing the risk of SQL injection attacks. It also supports output parameters and return values, which can be useful in certain scenarios.
* To use `sp_executesql`, you specify the SQL statement or batch of code that you want to execute, along with any input parameters and their values. The procedure then compiles and executes the statement or batch using the specified parameters.
* Overall, `sp_executesql` is a powerful tool for executing dynamic SQL in SQL Server, and can be a useful alternative to the EXECUTE statement in certain situations.
```sql
-- EXEC Demo Block
DECLARE  @test_id      INT
        ,@test_date    VARCHAR(1000)
        ,@test_string  VARCHAR(1000)
        ,@test_decimal DECIMAL(10,2)
        ,@sql          NVARCHAR(3000)

-- Assign values
SET @test_id      = 1
SET @test_date    = 'GETDATE()'
SET @test_string  = 'TEST'
SET @test_decimal = 10.2

-- Build dynamic statement
SET @sql = 'INSERT INTO dynsql_test VALUES( ' +
           CAST(@test_id AS VARCHAR) +' , '+
           CAST(@test_date AS VARCHAR) +' , '+
           ''''+CAST(@test_string AS VARCHAR)+''''+' , '+
           CAST(@test_decimal AS VARCHAR) + ');'
           
-- Print the @sql statement
PRINT @sql

-- Execute dynamic statement
EXECUTE sp_executesql @sql;
PRINT 'Rows Affected ' + CAST(@@rowcount AS VARCHAR)
```

## Dynamic SQL with `SELECT` Statement
```sql
BEGIN
  DECLARE @sql          NVARCHAR(3000)  
  SET @sql = 'SELECT * FROM dynsql_test
  WHERE test_id = ' + CAST(1 AS VARCHAR)
  + ' AND test_date >= GETDATE()-2';
  
  EXEC(@sql)
  PRINT 'Rows Affected ' + CAST(@@rowcount AS VARCHAR)
END;
```
## Parameterization and Security
The biggest distinction between EXEC() and sp_executesql is how they handle parameters. This directly impacts security and performance.

EXEC() handles parameters through string concatenation. You build the entire SQL statement as a single string, embedding all values directly. This approach is highly vulnerable to SQL injection attacks, where a malicious user can insert rogue code into a parameter to modify the query's behavior. For example, a user could enter ''; DROP TABLE dynsql_test;-- into an input field, which would get concatenated into your query and execute a dangerous command.

sp_executesql uses true parameterization. You pass the SQL string and the parameters separately. The procedure handles them as distinct data values, not executable code. This prevents SQL injection attacks because the database engine recognizes the parameter's value as data, not as a command to be executed. Always prefer sp_executesql for security.

## Execution Plan Caching
Query plan caching is a major performance consideration for dynamic SQL.

EXEC() creates a new, separate SQL string for every unique combination of parameter values. The query optimizer treats each unique string as a new query and generates a new execution plan every time. This constant recompilation is resource-intensive and can severely degrade performance, especially in high-volume applications.

sp_executesql allows the query optimizer to reuse execution plans. If you execute the same parameterized query string with different parameter values, SQL Server can reuse the previously cached plan, avoiding the need for a new compilation. This significantly improves performance and reduces server overhead.

* Examples with sp_executesql
The following examples demonstrate the power and safety of sp_executesql over the simple EXEC() method.

### Parameterized INSERT
This is the secure and efficient way to insert data using dynamic SQL. The N prefix on the string literal is crucial, as sp_executesql requires a Unicode string (NVARCHAR).

```sql

DECLARE  @test_id      INT = 1
        ,@test_date    DATE = GETDATE()
        ,@test_string  NVARCHAR(1000) = 'TEST'
        ,@test_decimal DECIMAL(10,2) = 10.2
        ,@sql          NVARCHAR(3000)
        ,@params       NVARCHAR(500);

-- Define the parameterized SQL statement
SET @sql = N'INSERT INTO dynsql_test (test_id, test_date, test_string, test_decimal) 
               VALUES (@p_test_id, @p_test_date, @p_test_string, @p_test_decimal);';

-- Define the parameter declarations for sp_executesql
SET @params = N'@p_test_id INT, @p_test_date DATE, @p_test_string NVARCHAR(1000), @p_test_decimal DECIMAL(10,2)';

-- Execute with parameters
EXECUTE sp_executesql @sql, @params,
                      @p_test_id      = @test_id,
                      @p_test_date    = @test_date,
                      @p_test_string  = @test_string,
                      @p_test_decimal = @test_decimal;

PRINT 'Rows Affected ' + CAST(@@rowcount AS VARCHAR);
```

### Parameterized SELECT with WHERE Clause
This is a common, and secure, use case where you need a flexible WHERE clause. It protects against SQL injection and allows for query plan reuse.

```sql

DECLARE @sql        NVARCHAR(MAX);
DECLARE @params     NVARCHAR(500);
DECLARE @deptName   VARCHAR(100) = 'ACCOUNTING';
DECLARE @minSal     DECIMAL(10,2) = 2000.00;

-- SQL with placeholders
SET @sql = N'SELECT e.ename, e.job, e.sal, d.dname
             FROM employees.emp e
             JOIN employees.dept d ON e.deptno = d.deptno
             WHERE d.dname = @p_deptName AND e.sal > @p_minSal;';

-- Parameter definitions
SET @params = N'@p_deptName VARCHAR(100), @p_minSal DECIMAL(10,2)';

-- Execute
EXEC sp_executesql @sql, @params,
                   @p_deptName = @deptName,
                   @p_minSal   = @minSal;
```
##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
