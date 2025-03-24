![SQL Server Tinitiate Image](sqlserver_tinitiateicon.jpg)




&copy; TINITIATE.COM


##### [Back To Context](./README.md)

# DDL - Data Definition Language
* In SQL Server, DDL (Data Definition Language) encompasses a group of SQL commands that are used to create, modify, and remove the structure of database objects. These objects include tables, indexes, views, schemas, sequences, and more.
* DDL statements are crucial for establishing the database schema, defining relationships between tables, and ensuring data integrity. They serve as the foundation for organizing and managing data within SQL Server databases.

## Primary DDL commands in SQL Server:
### CREATE:
* Used to create new database objects such as tables, indexes, views, schemas, sequences, and other objects.
```sql
-- Use database
USE DATABASE tinitiate;

-- Schema DDL
CREATE SCHEMA emp;
CREATE USER ti WITH PASSWORD = 'Tinitiate!23';
ALTER AUTHORIZATION ON SCHEMA::emp TO ti;

-- Set the schema where you want to create the DB objects
ALTER USER ti WITH DEFAULT_SCHEMA = emp;

-- DDL Create Command
-- Create dept table
CREATE TABLE emp.dept (
    deptid  int,
    dname   varchar(100)
);

-- Create emp table
CREATE TABLE emp.emp (
    empid    int,
    ename    varchar(100),
    sal      numeric(7,2),
    deptid   int
);

-- Create projects table
CREATE TABLE emp.projects (
    ProjectID      int,
    ProjectName    varchar(100),
    ProjectBudget  numeric(12,2)
);

-- Create empprojects table
CREATE TABLE emp.EmpProjects (
    EP_ID       int,
    EmpID       int,
    ProjectID   int,
    StartDate   date,
    EndDate     date
);
```

### ALTER:
* Modifies the structure of existing database objects, such as adding or dropping columns from a table.
```sql
-- Alter table "emp": Add a new column called "hire_date" of type DATE.
ALTER TABLE emp.emp ADD hire_date DATE;
-- To change back to previous
ALTER TABLE emp.emp DROP COLUMN hire_date;

-- Alter table "projects":
-- Change the data type of the column "ProjectBudget" to DECIMAL(12,2).
ALTER TABLE emp.projects ALTER COLUMN ProjectBudget DECIMAL(12,2);
-- To change back to previous
ALTER TABLE emp.projects ALTER COLUMN ProjectBudget NUMERIC(12,2);

-- Alter table "EmpProjects": Drop the column "EndDate".
ALTER TABLE emp.EmpProjects DROP COLUMN EndDate;
-- To change back to previous
ALTER TABLE emp.EmpProjects ADD EndDate DATE;
```

### DROP:
* Deletes existing database objects, such as tables, indexes, or views.
```sql
-- To drop dept table in emp schema
DROP TABLE emp.dept;

-- To again create it
CREATE TABLE emp.dept (
    deptid  INT,
    dname   VARCHAR(100)
);
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
