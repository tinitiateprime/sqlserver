![SQL Server Tinitiate Image](sqlserver_tinitiate.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# DDL - Constraints
* In SQL Server, Data Definition Language (DDL) constraints are also used to enforce rules on the structure of a database table, ensuring data integrity and consistency by enforcing certain conditions on the data being inserted, updated, or deleted in the table.
* These constraints are applied to columns when the table is created or altered.

## Here are the common types of DDL constraints in SQL Server:
### NOT NULL Constraint:
* This constraint ensures that a column cannot contain NULL values.
* It enforces that every row in the table must have a value for that column.
```sql
-- NOT NULL Constraint on empid column in the emp table
ALTER TABLE emp.emp
ALTER COLUMN empid INT NOT NULL;
-- NOT NULL Constraint on EP_ID column in the EmpProjects table
ALTER TABLE emp.EmpProjects
ALTER COLUMN EP_ID INT NOT NULL;
-- NOT NULL Constraint on deptid column in the dept table
ALTER TABLE emp.dept
ALTER COLUMN deptid INT NOT NULL;
-- NOT NULL Constraint on ProjectID column in the projects table
ALTER TABLE emp.projects
ALTER COLUMN ProjectID INT NOT NULL;

-- We can also specify this constraint while table creation; for example
CREATE TABLE staff (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT
);
```

### UNIQUE Constraint:
* This constraint ensures that the values in a column (or a group of columns) are unique across all rows in the table.
```sql
-- UNIQUE Constraint to the empid column in the emp table
ALTER TABLE emp.emp
ADD CONSTRAINT unique_empid UNIQUE (empid);

-- We can also specify this constraint while table creation; for example
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    name VARCHAR(100)
);
```

### CHECK Constraint:
* This constraint specifies a condition that must be satisfied for each row in the table.
* It allows you to define custom rules for data validation.
```sql
-- CHECK Constraint on ProjectBudget column in the projects table
ALTER TABLE emp.projects
ADD CONSTRAINT chk_project_budget CHECK (ProjectBudget > 0);

-- We can also specify this constraint while table creation; for example
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL,
    quantity INT,
    CONSTRAINT chk_price_quantity CHECK (price > 0 AND quantity >= 0)
);
```

### PRIMARY KEY Constraint:
* This constraint uniquely identifies each record in a table and ensures that there are no duplicate values in the specified column(s).
```sql
-- PRIMARY KEY Constraint on deptid column in the dept table
ALTER TABLE emp.dept
ADD CONSTRAINT pk_dept PRIMARY KEY (deptid);

-- PRIMARY KEY Constraint on empid column in the emp table
ALTER TABLE emp.emp 
ADD CONSTRAINT pk_emp PRIMARY KEY (empid);

-- PRIMARY KEY Constraint on projectid column in the projects table
ALTER TABLE emp.projects 
ADD CONSTRAINT pk_projects PRIMARY KEY (ProjectID);

-- PRIMARY KEY Constraint on EP_ID column in the EmpProjects table
ALTER TABLE emp.EmpProjects
ADD CONSTRAINT pk_empprojects PRIMARY KEY (EP_ID);

-- We can also specify this constraint while table creation; for example
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### FOREIGN KEY Constraint:
* This constraint establishes a relationship between two tables.
* It ensures referential integrity by enforcing a link between the data in the foreign key column(s) and the primary key or unique key in another table.
```sql
-- FOREIGN KEY Constraint on deptid column in the emp table referencing the
-- deptid column in the dept table
ALTER TABLE emp.emp
ADD CONSTRAINT fk_deptid FOREIGN KEY (deptid) REFERENCES emp.dept(deptid);

-- FOREIGN KEY Constraints on EmpID and ProjectID columns in the
-- EmpProjects table referencing the respective columns in the
-- emp and projects tables
ALTER TABLE emp.EmpProjects
ADD CONSTRAINT fk_emp_id FOREIGN KEY (EmpID) REFERENCES emp.emp(empid);
ALTER TABLE emp.EmpProjects
ADD CONSTRAINT fk_project_id FOREIGN KEY (ProjectID)
 REFERENCES emp.projects(ProjectID);

-- We can also specify this constraint while table creation; for example
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE
);
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|