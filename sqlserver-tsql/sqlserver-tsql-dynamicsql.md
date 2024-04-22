![Tinitiate SQLSERVER Training](./sqlserver_tinitiate.png)

# T-SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# SQL Server Dynamic SQL
Dynamic SQL in SQL Server refers to constructing and executing SQL statements dynamically at runtime, rather than at compile time. This allows for greater flexibility in query construction and enables the reuse of SQL code through the use of parameters. 

**PROS:**
Using Dynamic SQL offers benefits such as increased flexibility through the utilization of parameters in query construction, and improved performance due to the generation of a more efficient execution plan.

**CONS:**
Dynamic SQL has several drawbacks, including difficulties in debugging, unreliable error management, susceptibility to SQL injection attacks, and potential security concerns. Additionally, Dynamic SQL can be slower than static SQL since the SQL Server must generate a new execution plan every time at runtime. Furthermore, it requires users to have direct access permissions on all accessed database objects, such as tables and views.

* Test Table for Dynamic SQL
```sql
-- Drop the emp table if it exists
DROP TABLE emp;

-- Create the emp table
CREATE TABLE emp (
    emp_id INT,
    emp_name VARCHAR(100),
    job_title VARCHAR(100),
    dept_id INT
);

```

* Dynamic SQL using EXEC
```sql
-- EXEC Demo Block
DECLARE @emp_id INT,
        @emp_name VARCHAR(100),
        @job_title VARCHAR(100),
        @dept_id INT,
        @sql NVARCHAR(4000);

-- Assign values
SET @emp_id = 1;
SET @emp_name = 'John Doe';
SET @job_title = 'Senior Developer';
SET @dept_id = 10;

-- build dynamic statement
-- Build the dynamic SQL statement for insertion
SET @sql = 'INSERT INTO emp (emp_id, emp_name, job_title, dept_id) VALUES (' +
            CAST(@emp_id AS VARCHAR) + ', ' +
            '''' + @emp_name + ''', ' +
            '''' + @job_title + ''', ' +
            CAST(@dept_id AS VARCHAR) + ');';

-- Print the SQL for debugging
PRINT @sql;

-- Execute the dynamic SQL statement
EXEC(@sql);

-- Inform about rows affected
PRINT 'Rows Affected: ' + CAST(@@ROWCOUNT AS VARCHAR);

```
* sp_executesql is a system stored procedure in SQL Server that is used to execute dynamic SQL statements or batches of code that are constructed at runtime. It can be used as an alternative to the EXECUTE statement, and offers some advantages over it.
* One of the main advantages of sp_executesql is that it allows for parameterized queries, which can help to improve performance and security by reducing the risk of SQL injection attacks. It also supports output parameters and return values, which can be useful in certain scenarios.
* To use sp_executesql, you specify the SQL statement or batch of code that you want to execute, along with any input parameters and their values. The procedure then compiles and executes the statement or batch using the specified parameters.
* Overall, sp_executesql is a powerful tool for executing dynamic SQL in SQL Server, and can be a useful alternative to the EXECUTE statement in certain situations.
```sql
-- EXEC Demo Block
DECLARE @emp_id INT,
        @emp_name VARCHAR(100),
        @job_title VARCHAR(100),
        @dept_id INT,
        @sql NVARCHAR(4000);

-- Assign values
SET @emp_id = 1;
SET @emp_name = 'John Doe';
SET @job_title = 'Senior Developer';
SET @dept_id = 10;

-- build dynamic statement
-- Build and execute a safer dynamic SQL statement
SET @sql = N'INSERT INTO emp (emp_id, emp_name, job_title, dept_id) VALUES (@p_emp_id, @p_emp_name, @p_job_title, @p_dept_id);';

EXEC sp_executesql @sql,
                   N'@p_emp_id INT, @p_emp_name VARCHAR(100), @p_job_title VARCHAR(100), @p_dept_id INT',
                   @p_emp_id = @emp_id, @p_emp_name = @emp_name, @p_job_title = @job_title, @p_dept_id = @dept_id;

PRINT 'Rows Affected: ' + CAST(@@ROWCOUNT AS VARCHAR);

```
* Dynamic SQL with SELECT Statement
```sql
-- Build SQL Select Statement
-- -----------------------------------
CREATE TABLE emp (
    emp_id INT,
    emp_name VARCHAR(100),
    job_title VARCHAR(100),
    salary DECIMAL(10, 2),
    dept_id INT
);

```
Declare Variables for Dynamic SQL
Declare the variables that will hold the dynamic parts of the SQL query:

```sql
DECLARE @SelectCols NVARCHAR(1000) = 'emp_id, emp_name, job_title';
DECLARE @FilterCondition NVARCHAR(1000) = 'salary > 50000';
DECLARE @SQLQuery NVARCHAR(MAX);

--Build the Dynamic SQL Statement
SET @SQLQuery = 'SELECT ' + @SelectCols + ' FROM emp WHERE ' + @FilterCondition;

-- Print the SQL for debugging (optional, remove in production)
PRINT @SQLQuery;

EXEC sp_executesql @SQLQuery;

```