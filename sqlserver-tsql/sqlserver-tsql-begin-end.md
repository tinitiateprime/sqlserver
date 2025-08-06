![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# BEGIN...END
* In T-SQL, `BEGIN` and `END` are used to define a block of one or more statements as a single unit.
* This is essential when you need to group multiple operations under control-of-flow constructs, transactions, or within stored routines.

## Example 1: Adding two variables
We are declaring and initializing variables, performing a simple addition operation, and then printing and selecting the result. 
### Declaration
* @num1 is declared as an integer and initialized to 1.
* @num2 is declared as an integer without an initial value.
* @res is declared as an integer to store the result of the addition.
### Setting Variable Values:
* @num2 is set to 20 using the SET statement.
### Performing Addition:
* The sum of @num1 and @num2 is calculated and stored in @res.
### Printing Results:
* The script prints the string 'Sum of Num1 and Num2'.
* It then prints 'Sum: ' followed by the sum, which is cast to a varchar for concatenation with the string.
* The sum is also printed directly as an integer.
* Finally, the SELECT statement is used to display the result in the query result window.
```sql
BEGIN
    DECLARE @num1 INT = 1;  -- Variable = container
    DECLARE @num2 INT;
    DECLARE @res INT;
    
    SET @num2 = 20;

    SET @res = @num1 + @num2;
    PRINT 'Sum of Num1 and Num2';
    PRINT  'Sum: ' + CAST(@res AS VARCHAR);
    PRINT  @res;
    SELECT @res;
END;
```

## Example 1: Reassigning a variable and performing arithmetic
We are declaring and initializing variables, reassigning, performing a simple addition operation, and then printing the result. 
### Declaration
* @data1 is declared as an integer and initialized to 1.
* @data2 is declared as an integer without an initial value.
### Setting Variable Values:
* @data2 is set to 10 using the SET statement, and its value is printed, which will be 10.
### Reassigning Variable Values:
* @data2 is then reassigned to 20, and its new value is printed, which will be 20.
### Performing Arithmetic and Printing Results:
* The script prints the result of adding 10 to @data2, which will be 30.
* It then prints the value of @data2 again, which remains 20, demonstrating that the addition in the previous step did not change the value of @data2.
```sql 
BEGIN
    DECLARE @data1 INT = 1; -- variable declare and initialize
    DECLARE @data2 INT;     -- variable declare
    
    SET @data2 = 10;  -- variable initialize
    PRINT @data2;  -- 10

    SET @data2 = 20;  -- variable re-assign
    PRINT @data2;  -- 20

    PRINT @data2+10; -- 30
    PRINT @data2;    -- 20
END;
```

## Common Use Cases
* **Control-of-Flow** - Group statements under IF…ELSE or WHILE so they execute together.
* **Transactions** - Mark the start and end of an explicit transaction.
* **Stored Procedures & Triggers** - Enclose the body of a stored procedure, trigger, or script section.

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
