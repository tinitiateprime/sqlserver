![Tinitiate SQLSERVER Training](./sqlserver_tinitiate.png)

# T-SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)


# Handling Exceptions 
 In SQL Server, exceptions (also known as errors) can occur during the execution of SQL statements. To handle these exceptions, you can use the TRY...CATCH block. Here's how you can use this construct with the emp and dept tables:

Example: Preventing Insertion of Duplicate Employee IDs
Suppose you have an emp table with a primary key on the emp_id column. You want to insert a new employee, but you need to ensure that the employee ID does not already exist in the table.

```sql
BEGIN TRY
    -- Attempt to insert a new employee with an existing emp_id
    INSERT INTO emp (emp_id, emp_name, job_title, dept_id)
    VALUES (1, 'John Doe', 'Software Engineer', 1);
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() = 2627  -- Error number for a duplicate key violation
        BEGIN
            PRINT 'Error: Cannot insert duplicate employee ID.';
        END
    ELSE
        BEGIN
            PRINT 'An unexpected error occurred. Error number: ' + CAST(ERROR_NUMBER() AS VARCHAR);
        END
END CATCH
```

 * We use a TRY...CATCH block to handle exceptions.
 * Inside the TRY block, we attempt to insert a new employee into the emp table.
 * If an error occurs (such as a duplicate key violation), the execution is transferred to the CATCH block.
 * Inside the CATCH block, we check the error number using the ERROR_NUMBER() function.
 * If the error number is 2627 (which corresponds to a duplicate key violation), we print a message indicating that a duplicate employee ID cannot be inserted.
 * If a different error occurs, we print a generic message along with the error number.
 
    By using the TRY...CATCH block, we can gracefully handle errors and provide meaningful feedback to the user or the application. This approach is useful for maintaining  data integrity and ensuring that the database operations are performed correctly.

## USER DEFINED EXCEPTIONS


## throw
* Here's how you can use THROW to enforce that the department exists before adding an employee

```sql
-- Adding a new employee
DECLARE @DeptID INT = 10;  -- An example department ID
DECLARE @EmpID INT = 1;
DECLARE @EmpName VARCHAR(100) = 'John Doe';
DECLARE @JobTitle VARCHAR(100) = 'Developer';
DECLARE @Salary DECIMAL(10,2) = 60000.00;

BEGIN TRY
    IF NOT EXISTS(SELECT 1 FROM dept WHERE dept_id = @DeptID)
    BEGIN
        THROW 50001, 'Department does not exist. Cannot add employee.', 1;
    END

    INSERT INTO emp (emp_id, emp_name, job_title, salary, dept_id)
    VALUES (@EmpID, @EmpName, @JobTitle, @Salary, @DeptID);
END TRY
BEGIN CATCH
    PRINT ERROR_MESSAGE();
END CATCH

```

## raiserror
* Here’s an example using RAISERROR in an update trigger to prevent salary reductions
```sql
-- Creating a trigger to prevent salary reductions
CREATE TRIGGER trg_PreventSalaryReduction
ON emp
AFTER UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN deleted d ON i.emp_id = d.emp_id
        WHERE i.salary < d.salary
    )
    BEGIN
        RAISERROR ('Salary cannot be reduced once set.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;

```


## Custom Exception Creation

The RAISERROR statement enables you to send a custom error message back to the application and control the flow of your T-SQL code by raising an error condition that can be caught in a TRY...CATCH block. It's useful for enforcing business rules or constraints that are not inherently enforced by the SQL Server Database Engine.

```sql
RAISERROR (message_string, severity, state)
```
* message_string: The specific error message or a message ID from sys.messages if using sp_addmessage to store a custom message.
* severity: A number from 0 to 25. Severity levels from 11 to 20 cause the connection to break if the session is in a batch.
* state: An arbitrary integer from 0 to 255 that can be used to indicate a location within the code where the error was raised.

**Example of Custom Error**

Suppose you want to enforce a rule in your database where a "manager" job title must have a salary of at least $50,000. Here’s how you could implement this:

```sql

CREATE PROCEDURE AddEmployee
    @emp_name VARCHAR(100),
    @job_title VARCHAR(100),
    @salary DECIMAL(10, 2)
AS
BEGIN
    IF @job_title = 'Manager' AND @salary < 50000
    BEGIN
        RAISERROR('Managers must have a salary of at least $50,000.', 16, 1);
        RETURN;
    END

    -- Insert statement would go here
    -- INSERT INTO emp (emp_name, job_title, salary) VALUES (@emp_name, @job_title, @salary);
END
```

## Custom Exception Simulation using THROW

THROW is a newer command introduced in SQL Server 2012 that provides a more ANSI-standard way to raise an error. Unlike RAISERROR, THROW always terminates the statement batch, regardless of the severity level.

```sql

THROW [error_number, message, state];
```
* error_number: A custom defined error number. Must be greater than 50000 unless re-throwing in a CATCH block.
message: The error message text.
* state: An integer from 0 to 255.

**Example of Custom Error**
Using the same scenario for enforcing the salary rule for managers:

```sql
CREATE PROCEDURE AddEmployee
    @emp_name VARCHAR(100),
    @job_title VARCHAR(100),
    @salary DECIMAL(10, 2)
AS
BEGIN
    TRY
        BEGIN
            IF @job_title = 'Manager' AND @salary < 50000
            BEGIN
                THROW 51000, 'Managers must have a salary of at least $50,000.', 1;
            END

            -- Insert statement would go here
            -- INSERT INTO emp (emp_name, job_title, salary) VALUES (@emp_name, @job_title, @salary);
        END
    END TRY
    BEGIN CATCH
        -- Catch and handle the error
        PRINT ERROR_MESSAGE();
    END CATCH
END
```

**Key Differences**
* Syntax: THROW has a simpler syntax and does not require a pre-defined error message.
* Error Handling: THROW can be used without parameters inside a CATCH block to rethrow the caught exception, which is not possible with RAISERROR.

These examples demonstrate how to use RAISERROR and THROW to enforce custom business rules in SQL Server, mimicking the behavior of user-defined exceptions in traditional programming languages.

## Error functions
 Error functions are used within a CATCH block to retrieve information about the error that caused the TRY block to transfer control to the CATCH block. These functions  provide details such as the error number, message, severity, state, procedure name, and line number where the error occurred. Here are the most commonly used error 
* functions:

**ERROR_NUMBER()**

 Returns the error number of the error that caused the CATCH block to be  executed.
```sql
SELECT ERROR_NUMBER() AS ErrorNumber;
```

**ERROR_MESSAGE()**

Returns the error message text of the error that caused the CATCH block to be executed.
``` sql
SELECT ERROR_MESSAGE() AS ErrorMessage;
```

**ERROR_SEVERITY()**

Returns the severity level of the error that caused the CATCH block to be executed.
```sql
SELECT ERROR_SEVERITY() AS ErrorSeverity;
```

**ERROR_STATE()**
Returns the state number of the error that caused the CATCH block to be executed.
```sql
SELECT ERROR_STATE() AS ErrorState;
```
**ERROR_PROCEDURE()**

Returns the name of the stored procedure or trigger where the error occurred.
```sql
SELECT ERROR_PROCEDURE() AS ErrorProcedure;
```

**ERROR_LINE()**
Returns the line number within the routine that caused the error.

```sql
SELECT ERROR_LINE() AS ErrorLine;
```
These error functions can only be used within a CATCH block and are very useful for diagnosing and handling errors in SQL Server. They provide detailed information about the error, which can be logged or used to take corrective action.