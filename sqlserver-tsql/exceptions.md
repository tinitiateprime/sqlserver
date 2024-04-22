![Tinitiate SQLSERVER Training](../images/sqlserver.png)
# SQL SERVER EXCEPTIONS
> (c) Venkata Bhattaram

## Try Catch Block
```
BEGIN TRY
	DECLARE @num INT, @msg varchar(2000)
	---- Divide by zero to generate Error
	SET @num = 5/0
	PRINT 'This will not execute'
END TRY
BEGIN CATCH
	-- PRINT 'Error occured that is'
	-- set @msg=(SELECT ERROR_PROCEDURE()) -- + ' ' + convert(VARCHAR(50),ERROR_NUMBER()) + ' ' + convert(VARCHAR(50),ERROR_LINE()) + ' ' + ERROR_MESSAGE())
	set @msg = (select convert(VARCHAR(50),ERROR_LINE()) +' ' + ERROR_MESSAGE())
	-- OR
	-- Error Number = ERROR_NUMBER() or @@ERROR
	set @msg = (select convert(VARCHAR(50),ERROR_LINE()) +' ' + convert(VARCHAR(50),@@ERROR))
	
	print 'Error ' + @msg;
	-- print ERROR_PROCEDURE()
	--SELECT ERROR_MESSAGE()
	-- print 'Test'

-- Transaction uncommittable
    IF (XACT_STATE()) = -1
      ROLLBACK TRANSACTION
 
-- Transaction committable
    IF (XACT_STATE()) = 1
      COMMIT TRANSACTION

END CATCH
GO 
```

