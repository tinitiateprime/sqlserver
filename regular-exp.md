# Regular expressions 
* A regular expression, or regex, is a sequence of characters that defines a search pattern for text. Regex is commonly used for a variety of tasks including pattern matching, data validation, data transformation, and querying. It offers a flexible and an efficient way to search, manipulate, and handle complex data operations.

## Types of Regular Expression

### REGEXP_LIKE	
* Returns a Boolean value that indicates whether the text input matches the regex 
  pattern.
 
```sql 
REGEXP_LIKE 
     (
      string_expression,
      pattern_expression [, flags ]
     )

```
#### string_expression
* An expression of a character string.
* Can be a constant, variable, or column of character string.
* Data types: char, nchar, varchar, or nvarchar.

#### pattern_expression
* Regular expression pattern to match. Usually a text literal
* Data types: char, nchar, varchar, or nvarchar. pattern_expression supports a maximum character length of 8,000 bytes. 

#### start
* Specifies the starting position for the search within the search string. Optional. Type is int or bigint.
* The numbering is 1-based, meaning the first character in the expression is 1 and the value must be >= 1. If the start expression is less than 1, returns error. If the start expression is greater than the length of string_expression, the function returns 0. The default is 1.

#### occurrence
* An expression (positive integer) that specifies which occurrence of the pattern expression within the source string to be searched or replaced. Default is 1. Searches at the first character of the string_expression. For a positive integer n, it searches for the nth occurrence beginning with the first character following the first occurrence of the pattern_expression, and so forth.

#### return_option
* Specifies whether to return the beginning or ending position of the matched substring. Use 0 for the beginning, and 1 for the end. The default value is 0. The query returns error for any other value.

#### flag
* One or more characters that specify the modifiers used for searching for matches. Type is varchar or char, with a maximum of 30 characters.


#### group
* Specifies which capture group (subexpression) of a pattern_expression determines the position within string_expression to return. The group is a fragment of pattern enclosed in parentheses and can be nested. The groups are numbered in the order in which their left parentheses appear in pattern. The value is an integer and must be >= 0 and must not be greater than the number of groups in the pattern_expression. The default value is 0, which indicates that the position is based on the string that matches the entire pattern_expression.

#### Examples

* Select all records from the EMPLOYEES table where the first name starts with A and ends with Y

```sql
SELECT * FROM EMPLOYEES WHERE REGEXP_LIKE (FIRST_NAME, '^A.*Y$'); 

```
* Select all records from the ORDERS table where the order date is in February 2020.
```sql
SELECT * FROM ORDERS WHERE REGEXP_LIKE (ORDER_DATE, '2020-02-\d\d'); 
```

* Select all records from the PRODUCTS table where the product name contains at least three consecutive vowels

```sql
SELECT * FROM PRODUCTS WHERE REGEXP_LIKE (PRODUCT_NAME, '[AEIOU]{3,}'); 

```
 
### REGEXP_REPLACE
* Returns a modified source string replaced by a replacement string, where occurrence 
  of the regex pattern found.

```sql 
REGEXP_REPLACE 
     (
      string_expression,
      pattern_expression [, string_replacement [, start [, occurrence [, flags ] ] ] ]
     )
```

#### string_expression
* An expression of a character string.
* Can be a constant, variable, or column of character string.
* Data types: char, nchar, varchar, or nvarchar.

#### pattern_expression
* Regular expression pattern to match. Usually a text literal
* Data types: char, nchar, varchar, or nvarchar. pattern_expression supports a maximum 
  character length of 8,000 bytes. 

#### string_replacement
* String expression that specifies the replacement string for matching substrings and replaces the substrings matched by the pattern. The string_replacement can be of char, varchar, nchar, and nvarchar datatypes. If an empty string (' ') is specified, the function removes all matched patterns and returns the resulting string. The default replacement string is the empty string (' ').

* The string_replacement can contain \n, where n is 1 through 9, to indicate that the source substring matching the n'th parenthesized group (subexpression) of the pattern should be inserted, and it can contain & to indicate that the substring matching the entire pattern should be inserted. Write \ if you need to put a literal backslash in the replacement text.

```sql
REGEXP_REPLACE('123-456-7890', '(\d{3})-(\d{3})-(\d{4})', '(\1) \2-\3')  
```

```sql 
Returns:
Output
(123) 456-7890 
```

* If the provided \n in string_replacement is greater than the number of groups in the pattern_expression, then the function ignores the value.

```sql 
* example:
REGEXP_REPLACE('123-456-7890', '(\d{3})-(\d{3})-(\d{4})', '(\1) (\4)-xxxx')
```

```sql
Returns:
Output

(123) ()-xxxx
```

#### start
* Specify the starting position for the search within the search string. Optional. Type is int or bigint.

* The numbering is 1-based, meaning the first character in the expression is 1 and the value must be >= 1. If the start expression is less than 1, returns error. If the start expression is greater than the length of string_expression, the function returns string_expression. The default is 1.

#### occurrence
* An expression (positive integer) that specifies which occurrence of the pattern expression within the source string to be searched or replaced. Default is 1. Searches at the first character of the string_expression. For a positive integer n, it searches for the nth occurrence beginning with the first character following the first occurrence of the pattern_expression, and so forth.

#### flags
* One or more characters that specify the modifiers used for searching for matches. Type is varchar or char, with a maximum of 30 characters.

* For example, ims. The default is c. If an empty string (' ') is provided, it will be treated as the default value ('c'). Supply c or any other character expressions. If flag contains multiple contradictory characters, then SQL Server uses the last character.

#### Examples
* Replace all occurrences of a or e with X in the product names.

```sql
SELECT REGEXP_REPLACE (PRODUCT_NAME, '[ae]', 'X', 1, 0, 'i') FROM PRODUCTS; 
```
* Replace the first occurrence of cat or dog with pet in the product descriptions

```sql 
SELECT REGEXP_REPLACE (PRODUCT_DESCRIPTION, 'cat|dog', 'pet', 1, 1, 'i') FROM PRODUCTS; 
```
* Replace the last four digits of the phone numbers with asterisks


```sql
SELECT REGEXP_REPLACE (PHONE_NUMBER, '\d{4}$', '****') FROM CUSTOMERS; 
```

### REGEXP_SUBSTR

* Returns one occurrence of a substring of a string that matches the regular expression pattern. If no match is found, it returns NULL.

```sql
REGEXP_SUBSTR 
     (
      string_expression,
      pattern_expression [, start [, occurrence [, flags [, group ] ] ] ] 
     )
```
#### string_expression
* An expression of a character string.
* Can be a constant, variable, or column of character string.
* Data types: char, nchar, varchar, or nvarchar.

#### pattern_expression
* Regular expression pattern to match. Usually a text literal
* Data types: char, nchar, varchar, or nvarchar. pattern_expression supports a maximum character length of 8,000 bytes. 

#### start
* Specify the starting position for the search within the search string. Optional. Type is int or bigint.
* The numbering is 1-based, meaning the first character in the expression is 1 and the value must be >= 1. If the start expression is less than 1, returns error. If the start expression is greater than the length of string_expression, the function returns NULL. The default is 1.

#### occurrence
* An expression (positive integer) that specifies which occurrence of the pattern expression within the source string to be searched or replaced. Default is 1. Searches at the first character of the string_expression. For a positive integer n, it searches for the nth occurrence beginning with the first character following the first occurrence of the pattern_expression, and so forth.

#### flags
* One or more characters that specify the modifiers used for searching for matches. Type is varchar or char, with a maximum of 30 characters.
* For example, ims. The default is c. If an empty string (' ') is provided, it will be treated as the default value ('c'). Supply c or any other character expressions. If flag contains multiple contradictory characters, then SQL Server uses the last character.
* For example, if you specify ic the regex returns case-sensitive matching.
* If the value contains a character other than those listed at Supported flag values, the query returns an error like the following example:

 
#### group
* Specifies which capture group (subexpression) of a pattern_expression determines the position within string_expression to return. The capture group (subexpression) is a fragment of pattern enclosed in parentheses and can be nested. The capture groups are numbered in the order in which their left parentheses appear. The data type of group will be integer and the value must be greater than or equal to 0 and must not be greater than the number of capture groups (subexpressions) in pattern_expression. The default group value is 0, which indicates that the position is based on the string that matches the entire pattern.

#### Examples
* Extract the domain name from an email address.

```sql
SELECT REGEXP_SUBSTR (EMAIL, '@(.+)$', 1, 1, 'i', 1) AS DOMAIN FROM CUSTOMERS; 
```

* Find the first word in a sentence that starts with a vowel.

```sql
SELECT REGEXP_SUBSTR (COMMENT, '\b[aeiou]\w*', 1, 1, 'i') AS WORD FROM FEEDBACK; 
```

* Get the last four digits of a credit card number.

```sql
SELECT REGEXP_SUBSTR (CARD_NUMBER, '\d{4}$') AS LAST_FOUR FROM PAYMENTS; 
```

### REGEXP_INSTR	
* Returns the starting or ending position of the matched substring, depending on the 
  option supplied.

Returns the starting or ending position of the matched substring, depending on the value of the return_option argument.

syntaxsql

Copy
REGEXP_INSTR 
     (
      string_expression,
      pattern_expression 
         [, start [, occurrence [, return_option [, flags [, group ] ] ] ] ]
     )   

#### string_expression
* An expression of a character string.
* Can be a constant, variable, or column of character string.
* Data types: char, nchar, varchar, or nvarchar.

#### pattern_expression
* Regular expression pattern to match. Usually a text literal
* Data types: char, nchar, varchar, or nvarchar. pattern_expression supports a maximum character length of 8,000 bytes. 

#### start
* Specifies the starting position for the search within the search string. Optional. Type is int or bigint.
* The numbering is 1-based, meaning the first character in the expression is 1 and the value must be >= 1. If the start expression is less than 1, returns error. If the start expression is greater than the length of string_expression, the function returns 0. The default is 1.

#### occurrence
* An expression (positive integer) that specifies which occurrence of the pattern expression within the source string to be searched or replaced. Default is 1. Searches at the first character of the string_expression. For a positive integer n, it searches for the nth occurrence beginning with the first character following the first occurrence of the pattern_expression, and so forth.

#### return_option
* Specifies whether to return the beginning or ending position of the matched substring. Use 0 for the beginning, and 1 for the end. The default value is 0. The query returns error for any other value.

#### flag
* One or more characters that specify the modifiers used for searching for matches. Type is varchar or char, with a maximum of 30 characters.
* For example, ims. The default is c. If an empty string (' ') is provided, it will be treated as the default value ('c'). Supply c or any other character expressions. If flag contains multiple contradictory characters, then SQL Server uses the last character.

#### group
* Specifies which capture group (subexpression) of a pattern_expression determines the position within string_expression to return. The group is a fragment of pattern enclosed in parentheses and can be nested. The groups are numbered in the order in which their left parentheses appear in pattern. The value is an integer and must be >= 0 and must not be greater than the number of groups in the pattern_expression. The default value is 0, which indicates that the position is based on the string that matches the entire pattern_expression.

#### Examples
* Find the position of the first substring that contains only digits in the PRODUCT_DESCRIPTION column.

```sql
SELECT REGEXP_INSTR (PRODUCT_DESCRIPTION, '\d+') FROM PRODUCTS; 
```

* Find the position of the third occurrence of the letter a (case-insensitive) in the PRODUCT_NAME column.

```sql
SELECT REGEXP_INSTR (PRODUCT_NAME, 'a', 1, 3, 0, 'i') FROM PRODUCTS;
```
* Find the position of the end of the first substring that starts with t and ends with e (case-sensitive) in the PRODUCT_DESCRIPTION column.

```sql
SELECT REGEXP_INSTR (PRODUCT_DESCRIPTION, 't.*?e', 1, 1, 1) FROM PRODUCTS;
```


### REGEXP_COUNT	
* Returns a count of the number of times that regex pattern occurs in a string.
```sql 
REGEXP_COUNT (
    string_expression,
    pattern_expression [ , start [ , flags ] ]
)     
```

#### string_expression
* An expression of a character string.
* Can be a constant, variable, or column of character string.
* Data types: char, nchar, varchar, or nvarchar.

#### pattern_expression
* Regular expression pattern to match. Usually a text literal
* Data types: char, nchar, varchar, or nvarchar. pattern_expression supports a maximum character length of 8,000 bytes. 

#### Start
* Specify the starting position for the search within the search string. Optional. Type is int or bigint.

* The numbering is 1-based, meaning the first character in the expression is 1 and the value must be >= 1. If the start expression is less than 1, the returned pattern_expression begins at the first character that is specified in string_expression. If the start expression is greater than the length of string_expression, the function returns 0. The default is 1.

* If the start expression is less than 1, the query returns an error.

#### flags
* One or more characters that specify the modifiers used for searching for matches. Type is varchar or char, with a maximum of 30 characters.

* For example, ims. The default is c. If an empty string (' ') is provided, it will be treated as the default value ('c'). Supply c or any other character expressions. If flag contains multiple contradictory characters, then SQL Server uses the last character


* Count how many times the letter a appears in each product name.

```sql 
SELECT PRODUCT_NAME, REGEXP_COUNT(PRODUCT_NAME, 'a') AS A_COUNT FROM PRODUCTS;
```

* Count how many products have a name that ends with ing.

```sql
SELECT COUNT(*) FROM PRODUCTS WHERE REGEXP_COUNT(PRODUCT_NAME, 'ing$') > 0;
```

* Count how many products have a name that contains three consecutive consonants, ignoring case.

```sql
SELECT COUNT(*) FROM PRODUCTS WHERE REGEXP_COUNT(PRODUCT_NAME, '[^aeiou]{3}', 1, 'i') > 0;
```
