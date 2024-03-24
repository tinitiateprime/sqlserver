![SQL Server Tinitiate Image](sqlserver_tinitiate.png)

# SQL Server
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# DQL - Date Functions
* Date functions in SQL Server are used to perform various operations on date and timestamp data stored in the database.
* They allow for manipulation, extraction, formatting, and calculation of dates and times.

## Date functions in SQL Server:
### Current Date and time (GETDATE):
* Returns the current date and time.
```sql
-- Retrieve the current date and time
SELECT GETDATE();
```
### Date Part Function (DATEPART):
* Returns a specific component (such as year, month, day) from a date or timestamp.
```sql
-- Retrieve the day of the month from the 'hiredate' column
SELECT DATEPART(DAY, hiredate) FROM employees.emp;
```
### Date Difference Function (DATEDIFF):
* Calculates the difference between a date or timestamp and the current date or timestamp, returning the result as an interval.
```sql
-- Calculate the age of each employee based on their 'hiredate'
SELECT DATEDIFF(YEAR, hiredate, GETDATE()) FROM employees.emp;
```
### Date Addition/Subtraction:
* Adds or subtracts a specified interval (such as days, months) from a date or timestamp.
```sql
-- Add a specific number of days from a date
SELECT DATEADD(DAY, 7, hiredate) FROM employees.emp;

-- Subtract 6 months from the 'hiredate' column in the employees table
SELECT DATEADD(MONTH, -6, hiredate) FROM employees.emp;
```
### Date Formatting (FORMAT):
* Formats a date or timestamp according to a specified format.
```sql
-- Format the 'hiredate' column in a specific date format
SELECT FORMAT(hiredate, 'yyyy-MM-dd') FROM employees.emp;
```
### Weekday Function (DATEPART):
* Returns the day of the week (0 for Sunday, 1 for Monday, etc.) from a date or timestamp.
```sql
-- Retrieve the day of the week (1 for Sunday, 2 for Monday, etc.) from
-- the 'hiredate' column
SELECT DATEPART(WEEKDAY, hiredate) FROM employees.emp;
```
### Date to String (Various formats)
### DateTime to String (Various formats)
### DateTime TimeZone to String (Various formats)
### String to Date (Various formats)
### String to DateTime (Various formats)
### String to DateTime TimeZone (Various formats)




##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
