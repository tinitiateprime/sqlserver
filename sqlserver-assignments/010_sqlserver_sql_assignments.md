# SQLSERVER SQL Assignments

## **ASSIGNMENT** DDL Scenarios on Table
* For the below table Write the SQLs for the tasks below
```sql
CREATE TABLE employees.emp_test
( 
  empno      INT NOT NULL,
  ename      VARCHAR(10),
  job        VARCHAR(9),
  mgr        NUMERIC(4),
  hiredate   DATE,
  sal        NUMERIC(7,2),
  deptno     INT NOT NULL,
  
);

alter table employees.emp_test add constraint pk_empno primary key(empno);

alter table employees.emp_test add constraint fk_deptno foreign key(deptno)
references employees.dept_test(deptno);

```
* Create `employees.salgrade` table
```sql
-- Create table employees.salgrade_test
CREATE TABLE employees.salgrade_test

( 
  grade INT NOT NULL,
  losal INT,
  hisal INT,
  
  -- Primary Key constraint for employees.salgrade_test on grade
  CONSTRAINT pk_grade PRIMARY KEY (grade)
);
```
* Create `employees.projects` table
```sql
-- Create table employees.projects_test
CREATE TABLE employees.projects_test
( 
  projectno           INT NOT NULL,
  budget              NUMERIC(7,2),
  monthly_commission  NUMERIC(7,2),
  project_opt_out    varchar(100)
  
  -- Primary Key constraint for employees.projects_test on projectno
  CONSTRAINT pk_projectno PRIMARY KEY (projectno)
);
```
* Create `employees.emp_projects` table
```sql
-- Create table employees.emp_test_projects
CREATE TABLE employees.emp_test_projects
( 
  emp_projectno  INT NOT NULL,
  empno          INT NOT NULL,
  projectno      INT NOT NULL,
  start_date     DATE,
  end_date       DATE,
  
  -- Primary Key constraint for employees.emp_test_projects on emp_projectno
  CONSTRAINT pk_emp_projectno PRIMARY KEY (emp_projectno),
  
  -- Foreign key constraint for
  -- employees.emp_test_projects.empno referring employees.emp_test.empno
  CONSTRAINT fk_empno FOREIGN KEY (empno) REFERENCES employees.emp_test (empno),
  
  -- Foreign key constraint for
  -- employees.emp_test_projects.projectno referring employees.projects_test.projectno
  CONSTRAINT fk_projectno FOREIGN KEY (projectno)
   REFERENCES employees.projects_test (projectno)
);
```
* Tasks 
    * **Rename Table**, Write alter to rename emp_test to emp_ddl_tester
    * **Add column**, commission NUMERIC(2,2)
    * **Change DataType**, Change datatype of commission to  NUMERIC(7,2),
    * **Add Check Constraint**, Write alter to add check constraint to make sure sal is always >0, show test case with insert and update.
    * Write alter to add check constraint to add list of values for project_opt_out to THREE values ('YES','NO','N/A')
    * **Remove constraint**:
Alter table to remove check constraint on bonus and write test for insert and update
    * **Remove column**, Write alter to remove publicid column
    * **Add Column to PK**, Add column to Primary Key Write alter to add ename column to Primary Key
Drop table emp_ddl_tester
```
Create table employees.dept_test  again


Insert data into employees.dept_test

*  10, 'accounting', 'new york'
*  20, 'research', 'dallas'
*  30, 'sales', 'chicago'
*  40, 'operations', 'boston'

Insert data into employees.emp_test
* 1,'smith', 'clerk', 7902, '1980-12-17', 800, NULL, 20
*  2,'allen', 'salesman', 7698, '1981-02-20', 1600, NULL, 30
*  3,'ward', 'salesman', 7698, '1981-02-22', 1250, NULL, 30
*  4,'jones', 'manager', 7839, '1981-04-02', 2975, NULL, 20
*  5, 'martin', 'salesman', 7698, '1981-09-28', 1250, 1400, 30
*  6,'blake', 'manager', 7839, '1981-05-01', 2850, NULL, 40
*  7, 'newhire', 'clerk', 7782, '1982-01-23', 1300, NULL, 10

insert data into salgrade_test
* 1, 700, 1200
* 2, 1201, 1400
* 3, 1401, 2000
* 4, 2001, 3000
* 5, 3001, 9999

insert data into projects_test
* 1, 10000, 100,'YES'
* 2, 20000, 200,'NO'
* 3, 30000, 300,'YES'

insert data into emp_projects_test
* 1, 7369, 1, '1984-01-01', '1984-12-31'
* 2, 7499, 2, '1984-01-01', '1984-12-31'
* 3, 7521, 3, '1984-01-01', '1984-12-31'
* 4, 7566, 1, '1984-01-01', '1984-12-31'
* 5, 7654, 1, '1984-01-01', '1984-12-31'
* 6, 7698, 2, '1984-01-01', '1984-12-31' 


* List All Employees

* Find Employees Who Earn More Than Their Managers

* Update Commission for All Sales Employees

* Delete Employees Who Have Not Been Assigned to Any Projects

* List Employees with Their Salary Grades

* Find the Total Budget of Projects Each Employee is Working On

* List Projects with Duration Greater than 6 Months

* Identify Employees Eligible for New Projects

* Update Salaries Based on Performance (monthly_commission > 500)

* List Employees Who Have Never Received a Bonus

* Find Employees Working on Multiple Projects

* List the Top 3 Highest Budget Projects for Each Department

* Increase Salary by 1.5 for Employees Who Joined Before 2000

* List Employees and Their Managers

* Employees with No Current Projects

* Calculate Total Annual Salary Expense

* Find Overlapping Projects for Employees

* List Salaries and Adjust for Inflation(1.03)

* Simulate a Salary Transaction with Rollback

