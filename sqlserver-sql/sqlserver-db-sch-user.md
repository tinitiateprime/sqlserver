![SQL Server Tinitiate Image](sqlservericon.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Database, Schema, and User
* In SQL Server, a database serves as a structured collection of data.
* A schema, acts as a logical container for organizing and grouping database objects, such as tables, views, and stored procedures.
* Lastly, a user in SQL Server is an entity that holds access rights to interact with the SQL Server system and its databases.
* To make it even short:
    * SQL Server software is called the instance
    * In an instance we can create multiple databases
    * Each database has logical grouping of database objects called Schema
    * The schema within a database can be accessed by users, which are the individual user logins.
## Database:
* In SQL Server, a database is a structured collection of data that is organized and managed for easy access and retrieval.
* It stores tables, views, stored procedures, and other objects that define the schema and structure of the data.
* Within a SQL Server instance, you can create multiple databases to organize your data.
```sql
-- Create database tinitiate
CREATE DATABASE tinitiate;

-- Alter database tinitiate to set containment
ALTER DATABASE [tinitiate] SET CONTAINMENT = PARTIAL;
-- SQL Server commands are generally case-insensitive
-- We can use uppercase or lowercase or mix of both for commands
-- But for best practice stick to any one format
```
## User:
* In SQL Server, users are individual logins that can access the database objects within a schema.
* These users are granted permissions to interact with specific databases and schemas as per the database administrator's configuration.
```sql
-- Step 1:
-- Use the Database where you want to create the USER
USE tinitiate;

-- Step 2:
-- Enable contained database authentication
EXEC sp_configure 'contained database authentication', 1;

-- Step 3:
-- Reconfigure the database to apply the configuration change
RECONFIGURE;

-- Step 4:
-- Set the database containment to partial to allow contained database users
ALTER DATABASE [tinitiate] SET CONTAINMENT = PARTIAL;

-- Step 5:
-- Create a user named 'tiuser' with the password 'Tinitiate!23'
CREATE USER tiuser WITH PASSWORD = 'Tinitiate!23';
-- Create a user named 'developer' with the password 'Tinitiate!23'
CREATE USER developer WITH PASSWORD = 'Tinitiate!23';
```
## Schema:
* In SQL Server, each database contains a logical grouping of database objects called schemas.
* Schemas provide a way to organize and namespace database objects within a database.
```sql
-- Use the Database where you want to create the SCHEMA
USE tinitiate;

-- Create the schema
CREATE SCHEMA employees AUTHORIZATION dbo;
-- Here schema is created with the authorization set to database owner(dbo).
-- We can create schema without authorization also, 'CREATE SCHEMA employees;'

-- Change the authorization of the schema to tiuser
ALTER AUTHORIZATION ON SCHEMA::employees TO tiuser;
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
