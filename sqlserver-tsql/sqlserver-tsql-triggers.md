![Tinitiate SQLSERVER Training](images/sqlserver.png)
# SQL SERVER TRIGGERS
In SQL Server, a trigger is a special type of stored procedure that is automatically executed in response to certain events occurring in the database. Triggers can be used to enforce business rules, validate data, and perform other actions when data is inserted, updated, or deleted from a table.

There are two types of triggers in SQL Server:


* **DDL triggers**

DDL triggers fire in response to changes to the database schema, such as creating or altering tables, views, or stored procedur

* * *
* Tables for Trigger demonstration
```sql
-- Test Table for Trigger Demonstration
-- ----------------------------
CREATE TABLE emp (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    job_title VARCHAR(100),
    salary DECIMAL(10, 2),
    dept_id INT
);

-- Create an Audit Table 

CREATE TABLE emp_salary_audit (
    emp_id INT,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2),
    update_date DATETIME DEFAULT GETDATE()
);



```

* **DML triggers**

Data Manipulation Language (DML) triggers in SQL Server are special types of stored procedures that are automatically executed (or fired) in response to certain events on a table or view. These events are primarily INSERT, UPDATE, and DELETE operations. DML triggers are useful for enforcing business rules, auditing, and other data integrity and compliance measures.

DML triggers fire in response to changes to data in a table, such as an insert, update, or delete operation. They can be defined to execute either before or after the data modification operation.


### Types of DML Triggers
There are three main types of DML triggers:

#### AFTER INSERT Triggers (also known as FOR Triggers):

Suppose you have an emp table and you want to track when new employees are added to your system in a log table called emp_audit.

```sql
-- Example table
CREATE TABLE emp (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    job_title VARCHAR(100),
    dept_id INT
);

-- Audit table
CREATE TABLE emp_audit (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    emp_id INT,
    action_type VARCHAR(50),
    action_timestamp DATETIME DEFAULT GETDATE()
);

-- Creating an AFTER INSERT trigger
CREATE TRIGGER trg_emp_after_insert
ON emp
AFTER INSERT
AS
BEGIN
    INSERT INTO emp_audit (emp_id, action_type)
    SELECT emp_id, 'INSERT'
    FROM inserted;
END;
```
This trigger logs every insert operation on the emp table to the emp_audit table, noting the employee ID and the type of action.

#### AFTER UPDATE Trigger
Continuing with the emp table, let's say you want to audit salary changes, noting the old and new values.

```sql

ALTER TABLE emp ADD salary DECIMAL(10, 2);

-- Update audit table to include salary information
ALTER TABLE emp_audit ADD old_salary DECIMAL(10, 2), new_salary DECIMAL(10, 2);

-- Creating an AFTER UPDATE trigger
CREATE TRIGGER trg_emp_after_update
ON emp
AFTER UPDATE
AS
BEGIN
    IF UPDATE(salary) -- Check if the salary was updated
    BEGIN
        INSERT INTO emp_audit (emp_id, action_type, old_salary, new_salary)
        SELECT i.emp_id, 'UPDATE', d.salary, i.salary
        FROM inserted i
        INNER JOIN deleted d ON i.emp_id = d.emp_id;
    END
END;
```

This trigger checks if the salary field was updated and logs the details in the emp_audit table, including old and new salaries.


#### AFTER DELETE Trigger
Suppose you have an emp (employees) table in your database and you want to keep an audit trail of every deletion from this table. Let's start by creating the emp table and an emp_audit table to store the audit trail.

Create the AFTER DELETE Trigger
Now, create an AFTER DELETE trigger that logs the details of the deleted employee records into the emp_audit table.

```sql
-- Creating an AFTER DELETE trigger on the emp table
CREATE TRIGGER trg_emp_after_delete
ON emp
AFTER DELETE
AS
BEGIN
    -- Insert audit log for deleted employees
    INSERT INTO emp_audit (emp_id, emp_name, job_title, dept_id, action_type)
    SELECT emp_id, emp_name, job_title, dept_id, 'DELETE'
    FROM deleted;
END;
```
#### Test the Trigger
To see the trigger in action, insert some data into the emp table, delete some data, and then check the emp_audit table.

```sql
-- Insert sample data
INSERT INTO emp (emp_id, emp_name, job_title, dept_id) VALUES
(1, 'John Doe', 'Software Developer', 101),
(2, 'Jane Smith', 'Project Manager', 102);

-- Delete an employee
DELETE FROM emp WHERE emp_id = 1;

-- Check the audit table
SELECT * FROM emp_audit;

```
In this example, the AFTER DELETE trigger captures the details of deleted records from the emp table and logs them into the emp_audit table. This setup is crucial for maintaining data integrity and traceability in environments where it is important to track changes to data, such as in regulated industries or for security-sensitive applications.

Using AFTER DELETE triggers effectively allows businesses to ensure that actions taken on critical data are logged and that the system adheres to required business rules and regulatory compliance standards.


This trigger checks if the salary field was updated and logs the details in the emp_audit table, including old and new salaries.

##### INSTEAD OF DELETE Trigger
Suppose you want to prevent accidental deletions from the emp table and instead mark employees as inactive.

```sql
-- Add status column to emp table
ALTER TABLE emp ADD status VARCHAR(10) DEFAULT 'Active';

-- Creating an INSTEAD OF DELETE trigger
CREATE TRIGGER trg_emp_instead_of_delete
ON emp
INSTEAD OF DELETE
AS
BEGIN
    UPDATE emp
    SET status = 'Inactive'
    WHERE emp_id IN (SELECT emp_id FROM deleted);
END;
```
This trigger prevents the actual deletion of rows from the emp table. Instead, it sets the status of employees to 'Inactive'.

### Conclusion
DML triggers in SQL Server offer powerful functionality for automatically managing changes to your data. They can enforce business rules, ensure data integrity, perform logging, and much more. However, triggers should be used judiciously as they can introduce complexity and affect performance, especially if not properly managed or if they contain complex or inefficient queries.

### Multiple Triggers

In SQL Server, it's possible to define multiple triggers for the same event on a single table. This means you can have multiple AFTER INSERT, AFTER UPDATE, AFTER DELETE, INSTEAD OF INSERT, INSTEAD OF UPDATE, or INSTEAD OF DELETE triggers defined on one table. However, managing multiple triggers on the same table for the same action can be complex, and there are important considerations and best practices to keep in mind.

SQL Server does not guarantee any specific execution order unless you explicitly specify it using sp_settriggerorder.
Having multiple triggers for the same event can lead to maintenance challenges, especially if the triggers have overlapping functionality or conflicting actions.

**How to Control Trigger Execution Order**

SQL Server allows you to specify the order of first and last triggers when multiple triggers exist for the same statement on a table:

**sp_settriggerorder** - This system stored procedure allows setting the order of triggers to fire first or last. There's no built-in way to specify the order of triggers that are in the middle; their execution order is undefined and may vary.

**Example Usage of sp_settriggerorder**
Suppose you have two AFTER INSERT triggers on the emp table, and you need to ensure that Trigger1 fires before Trigger2.

```sql
-- Assuming Trigger1 and Trigger2 are already created on the emp table
EXEC sp_settriggerorder @triggername= 'Trigger1', @order= 'First', @stmttype = 'INSERT';
EXEC sp_settriggerorder @triggername= 'Trigger2', @order= 'Last', @stmttype = 'INSERT';
```
**Example Scenario with Multiple Triggers**
Let's create a scenario with two AFTER UPDATE triggers on an emp table, where:

* Trigger1: Logs changes to an audit table.
* Trigger2: Checks and enforces some business rules.

* Create the emp and emp_audit Tables
```sql
CREATE TABLE emp (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    salary DECIMAL(10, 2)
);

CREATE TABLE emp_audit (
    audit_id INT IDENTITY PRIMARY KEY,
    emp_id INT,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2),
    audit_time DATETIME DEFAULT GETDATE()
);
```
**Define Triggers**
```sql
-- Trigger1: Audit salary changes
CREATE TRIGGER trg_emp_audit
ON emp
AFTER UPDATE
AS
BEGIN
    IF UPDATE(salary)
    BEGIN
        INSERT INTO emp_audit (emp_id, old_salary, new_salary)
        SELECT d.emp_id, d.salary, i.salary
        FROM deleted d
        JOIN inserted i ON d.emp_id = i.emp_id;
    END
END;
```
-- Trigger2: Ensure salary does not decrease
```sql
CREATE TRIGGER trg_emp_salary_check
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
        RAISERROR ('Salary cannot decrease', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
```
**Test the Triggers**
```sql
-- Insert sample data
INSERT INTO emp (emp_id, emp_name, salary) VALUES (1, 'John Doe', 50000);

-- Attempt to decrease salary
BEGIN TRY
    UPDATE emp SET salary = 49000 WHERE emp_id = 1;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS ErrorMessage;
END CATCH;
--Check the audit table**

SELECT * FROM emp_audit;
```
#### Best Practices and Considerations
* Minimize the number of triggers: To avoid complexity and potential performance impacts, try to minimize the number of triggers on a table. Consider combining logic into fewer triggers if possible.
Use clear naming conventions: This helps in understanding the purpose of each trigger.

* Document trigger logic: Especially when multiple triggers interact with the same data, documentation is key to maintaining and debugging the system.

* Test thoroughly: Ensure that the triggers perform as expected and that they handle edge cases without conflicts.
Using multiple triggers can be powerful, but requires careful management to ensure that they operate efficiently and without unintended side effects.







## Enable / Disable Trigger
If you have a trigger called trg_emp_after_insert on a table named emp and you need to temporarily disable this trigger for performing bulk data operations, you can do so using the SQL Server DISABLE TRIGGER command. Once your operations are complete, you can re-enable the trigger using the ENABLE TRIGGER command.

Here's how to disable and then re-enable this specific trigger:

### Disabling the Trigger
To prevent the trigger from firing during bulk inserts or updates, thereby improving the performance of these operations, you would execute:

```sql
-- Disable the specific trigger on the emp table
DISABLE TRIGGER trg_emp_after_insert ON emp;
```

This command stops trg_emp_after_insert from firing on the emp table. Any insert operations performed on the emp table while the trigger is disabled will not be logged or processed by this trigger.

### Performing Bulk Operations
With the trigger disabled, you can now perform bulk data inserts or updates without the overhead of the trigger execution. For example:

```sql
-- Example of a bulk insert operation
INSERT INTO emp (emp_id, emp_name, job_title, salary, dept_id)
SELECT emp_id, emp_name, job_title, salary, dept_id
FROM another_table;
```

### Re-enabling the Trigger
Once the bulk operations are complete and you want the trigger to start processing data modifications again, you can re-enable it:

```sql
-- Enable the specific trigger on the emp table
ENABLE TRIGGER trg_emp_after_insert ON emp;
```
By re-enabling the trigger, you ensure that any subsequent insert operations on the emp table are again being logged or processed according to the logic defined in trg_emp_after_insert.

#### Why Disable and Enable Triggers?
* Performance: Disabling triggers can significantly enhance performance during bulk data operations because the database does not need to execute the trigger's logic for each row affected.

* Maintenance: Sometimes, it's necessary to disable triggers to perform maintenance tasks, data migration, or cleanup operations that would otherwise be complicated by the triggers' actions.

* Data Loading: For initial data loads into a new system, disabling triggers can prevent unnecessary logging and processing, especially when the data is known to be clean and does not require the additional integrity checks or transformations provided by triggers.

### Considerations
* Data Integrity: When disabling triggers that enforce business rules or data integrity, ensure that the operations performed while the trigger is disabled do not violate these rules. You might need to manually enforce any necessary constraints during bulk operations.

* Dependency: Be aware of other processes or systems that might depend on the actions performed by triggers (e.g., auditing). Make sure that disabling a trigger does not cause issues in other areas of your application or database management processes.

By carefully managing when to enable or disable triggers, you can balance the needs for performance, data integrity, and operational efficiency in your SQL Server databases.