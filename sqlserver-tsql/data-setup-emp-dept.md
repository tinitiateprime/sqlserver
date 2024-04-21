# Emp-Dept-Sal Data Model
## Departments (dept) Table
* dept_id: A unique identifier for each department. It is the primary key of the table.
* dept_name: The name of the department.
* location: The physical location of the department.
# Employees (emp) Table
* emp_id: A unique identifier for each employee. It is the primary key of the table.
* emp_name: The name of the employee.
* job_title: The job title or position of the employee.
* dept_id: A foreign key that references the dept_id in the dept (departments) table. It indicates which department the employee belongs to.
# Salaries (sal) Table
* emp_id: A foreign key that references the emp_id in the emp (employees) table. It indicates which employee the salary record belongs to.
* salary: The amount of salary paid to the employee.
* pay_date: The date on which the salary was paid.
* The combination of emp_id and pay_date forms the primary key of the table, ensuring that each salary record is unique for an employee on a given pay date.

The dept table stores information about the departments within the organization, including their names and locations. The emp table stores information about the employees, including their names, job titles, and the departments they belong to. The sal table stores salary information for each employee, including the amount paid and the date of payment. The relationships between these tables are established through foreign keys, allowing for easy retrieval of related information across the tables.

## DDL Syntax

```sql
-- Create 'dept' table
CREATE TABLE dept (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- Create 'emp' table
CREATE TABLE emp (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES dept(dept_id)
);

-- Create 'sal' table
CREATE TABLE sal (
    emp_id INT,
    salary DECIMAL(10, 2) NOT NULL,
    pay_date DATE NOT NULL,
    PRIMARY KEY (emp_id, pay_date),
    FOREIGN KEY (emp_id) REFERENCES emp(emp_id)
);

```

## DML Syntax

-- Insert records into 'dept'
```sql
-- Insert records into 'dept'
INSERT INTO dept (dept_id, dept_name, location) VALUES
(1, 'Human Resources', 'Building A'),
(2, 'Finance', 'Building B'),
(3, 'IT', 'Building C'),
(4, 'Marketing', 'Building D');

-- Insert records into 'emp'
INSERT INTO emp (emp_id, emp_name, job_title, dept_id) VALUES
(1, 'John Doe', 'HR Manager', 1),
(2, 'Jane Smith', 'Finance Analyst', 2),
(3, 'Michael Johnson', 'IT Specialist', 3),
(4, 'Emily Davis', 'Marketing Coordinator', 4),
(5, 'David Wilson', 'HR Assistant', 1),
(6, 'Sarah Taylor', 'Accountant', 2),
(7, 'James Brown', 'Network Administrator', 3),
(8, 'Jessica Jones', 'Marketing Specialist', 4),
(9, 'Chris Miller', 'Recruiter', 1),
(10, 'Amanda Martinez', 'Financial Planner', 2);

-- Insert records into 'sal'
INSERT INTO sal (emp_id, salary, pay_date) VALUES
(1, 70000.00, '2023-01-15'),
(2, 60000.00, '2023-01-15'),
(3, 65000.00, '2023-01-15'),
(4, 55000.00, '2023-01-15'),
(5, 45000.00, '2023-01-15'),
(6, 50000.00, '2023-01-15'),
(7, 60000.00, '2023-01-15'),
(8, 58000.00, '2023-01-15'),
(9, 42000.00, '2023-01-15'),
(10, 62000.00, '2023-01-15');

```