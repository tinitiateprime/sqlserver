![SQL Server Tinitiate Image](sqlserver_tinitiate.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# DQL Data Setup
* Data Query Language (DQL) is a powerful tool used to retrieve and manipulate data within a database management system.
* Before diving into querying data that is to going into the details of Data Query Language (DQL) commands, it's essential to have a properly structured dataset to work with.
* This preliminary step lays the groundwork for a comprehensive understanding of DQL operations, enabling users to effectively utilize DQL commands to query and manipulate data within a database management system.
* In this tutorial, we'll walk through the process of setting up Employees DQL data, step by step.

## Create tables
* Create dataset under **EMPLOYEES** schema
```sql
-- Switch to the tinitiate database
USE tinitiate;

-- Set the default schema for your user to employees
ALTER USER tiuser WITH DEFAULT_SCHEMA = employees;
```
*  Drop tables if exists
```sql
-- Drop tables from the "employees" schema if any exists
DROP TABLE employees.emp;
DROP TABLE employees.dept;
DROP TABLE employees.salgrade;
DROP TABLE employees.projects;
DROP TABLE employees.emp_projects;
```
* Create `employees.dept` table
```sql
-- Create table employees.dept
CREATE TABLE employees.dept
( 
  deptno INT NOT NULL,
  dname VARCHAR(14),
  loc VARCHAR(13),
  
  -- Primary Key constraint for employees.dept on deptno
  CONSTRAINT pk_dept PRIMARY KEY (deptno)
);
```
* Create `employees.emp` table
```sql
-- Create table employees.emp
CREATE TABLE employees.emp
( 
  empno      INT NOT NULL,
  ename      VARCHAR(10),
  job        VARCHAR(9),
  mgr        NUMERIC(4),
  hiredate   DATE,
  sal        NUMERIC(7,2),
  commission NUMERIC(7,2),
  deptno     INT NOT NULL,
  
  -- Primary Key constraint for employees.emp on empno
  CONSTRAINT pk_empno PRIMARY KEY (empno),
  
  -- Foreign key constraint for
  -- employees.emp.deptno referring employees.dept.deptno
  CONSTRAINT fk_deptno FOREIGN KEY (deptno) REFERENCES employees.dept (deptno)
);
```
* Create `employees.salgrade` table
```sql
-- Create table employees.salgrade
CREATE TABLE employees.salgrade

( 
  grade INT NOT NULL,
  losal INT,
  hisal INT,
  
  -- Primary Key constraint for employees.salgrade on grade
  CONSTRAINT pk_grade PRIMARY KEY (grade)
);
```
* Create `employees.projects` table
```sql
-- Create table employees.projects
CREATE TABLE employees.projects
( 
  projectno           INT NOT NULL,
  budget              NUMERIC(7,2),
  monthly_commission  NUMERIC(7,2),
  
  -- Primary Key constraint for employees.projects on projectno
  CONSTRAINT pk_projectno PRIMARY KEY (projectno)
);
```
* Create `employees.emp_projects` table
```sql
-- Create table employees.emp_projects
CREATE TABLE employees.emp_projects
( 
  emp_projectno  INT NOT NULL,
  empno          INT NOT NULL,
  projectno      INT NOT NULL,
  start_date     DATE,
  end_date       DATE,
  
  -- Primary Key constraint for employees.emp_projects on emp_projectno
  CONSTRAINT pk_emp_projectno PRIMARY KEY (emp_projectno),
  
  -- Foreign key constraint for
  -- employees.emp_projects.empno referring employees.emp.empno
  CONSTRAINT fk_empno FOREIGN KEY (empno) REFERENCES employees.emp (empno),
  
  -- Foreign key constraint for
  -- employees.emp_projects.projectno referring employees.projects.projectno
  CONSTRAINT fk_projectno FOREIGN KEY (projectno)
   REFERENCES employees.projects (projectno)
);
```

## Insert data into the tables
* Inserts for `employees.dept`
```sql
-- Insert data into employees.dept
INSERT INTO employees.dept (deptno, dname, loc)
 VALUES (10, 'accounting', 'new york');
INSERT INTO employees.dept (deptno, dname, loc)
 VALUES (20, 'research', 'dallas');
INSERT INTO employees.dept (deptno, dname, loc)
 VALUES (30, 'sales', 'chicago');
INSERT INTO employees.dept (deptno, dname, loc)
 VALUES (40, 'operations', 'boston');
```
* Inserts for `employees.emp`
```sql
-- Insert data into employees.emp
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7369, 'smith', 'clerk', 7902, '1980-12-17', 800, NULL, 20);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7499, 'allen', 'salesman', 7698, '1981-02-20', 1600, NULL, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7521, 'ward', 'salesman', 7698, '1981-02-22', 1250, NULL, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7566, 'jones', 'manager', 7839, '1981-04-02', 2975, NULL, 20);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7654, 'martin', 'salesman', 7698, '1981-09-28', 1250, 1400, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7698, 'blake', 'manager', 7839, '1981-05-01', 2850, NULL, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7782, 'clark', 'manager', 7839, '1981-06-09', 2450, NULL, 10);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7788, 'scott', 'analyst', 7566, '1982-12-09', 3000, NULL, 20);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7839, 'king', 'president', NULL, '1981-11-17', 5000, NULL, 10);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7844, 'turner', 'salesman', 7698, '1981-09-08', 1500, 0, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7876, 'adams', 'clerk', 7788, '1983-01-12', 1100, NULL, 20);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7900, 'james', 'clerk', 7698, '1981-12-03', 950, NULL, 30);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7902, 'ford', 'analyst', 7566, '1981-12-03', 3000, NULL, 20);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (7934, 'miller', 'clerk', 7782, '1982-01-23', 1300, NULL, 10);
INSERT INTO employees.emp (
    empno, ename, job, mgr, hiredate, sal, commission, deptno)
     VALUES (8000, 'newhire', 'clerk', 7782, '1982-01-23', 1300, NULL, 10);
```
* Inserts for `employees.salgrade`
```sql
-- Insert data into employees.salgrade
INSERT INTO employees.salgrade (grade, losal, hisal) VALUES (1, 700, 1200);
INSERT INTO employees.salgrade (grade, losal, hisal) VALUES (2, 1201, 1400);
INSERT INTO employees.salgrade (grade, losal, hisal) VALUES (3, 1401, 2000);
INSERT INTO employees.salgrade (grade, losal, hisal) VALUES (4, 2001, 3000);
INSERT INTO employees.salgrade (grade, losal, hisal) VALUES (5, 3001, 9999);
```
* Inserts for `employees.projects`
```sql
-- Insert data into employees.projects
INSERT INTO employees.projects (projectno, budget, monthly_commission)
 VALUES (1, 10000, 100);
INSERT INTO employees.projects (projectno, budget, monthly_commission)
 VALUES (2, 20000, 200);
INSERT INTO employees.projects (projectno, budget, monthly_commission)
 VALUES (3, 30000, 300);
```
* Inserts for `employees.emp_projects`
```sql
-- Insert data into employees.emp_projects
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (1, 7369, 1, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (2, 7499, 2, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (3, 7521, 3, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (4, 7566, 1, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (5, 7654, 1, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (6, 7698, 2, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (7, 7782, 2, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (8, 7788, 2, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (9, 7839, 3, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (10, 7844, 3, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (11, 7876, 3, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (12, 7900, 2, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (13, 7902, 1, '1984-01-01', '1984-12-31');
INSERT INTO employees.emp_projects (
    emp_projectno, empno, projectno, start_date, end_date)
     VALUES (14, 7934, 1, '1984-01-01', '1984-12-31');
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|