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

##### [Back To Contents](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
