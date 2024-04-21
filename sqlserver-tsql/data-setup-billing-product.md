# Emp-Dept-Sal Data Model
## Products Table
* product_id: A unique identifier for each product. It is the primary key of the table.
* product_name: The name of the product.
* price: The price of the product.
## Customers Table
* customer_id: A unique identifier for each customer. It is the primary key of the table.
* customer_name: The name of the customer.
* contact_info: Contact information for the customer, such as phone number or email address.
## Bill Table
* bill_id: A unique identifier for each bill. It is the primary key of the table.
* customer_id: A foreign key that references the customer_id in the customers table. It indicates which customer the bill is for.
* bill_date: The date when the bill was generated.
* total_amount: The total amount of the bill.
## BillDetails Table
* billdetail_id: A unique identifier for each bill detail entry. It is the primary key of the table.
* bill_id: A foreign key that references the bill_id in the bill table. It indicates which bill this detail belongs to.
* product_id: A foreign key that references the product_id in the products table. It indicates which product is included in the bill.
* quantity: The quantity of the product in the bill.
* line_total: The total amount for this line item (usually calculated as quantity * price of the product).

The products table stores information about the products that can be billed. The customers table stores information about the customers who receive the bills. The bill table stores information about the bills, including which customer the bill is for and the total amount of the bill. The billdetails table stores detailed information about each line item in a bill, including which product is being billed, the quantity, and the total amount for that line item. The relationships between these tables are established through foreign keys, allowing for easy retrieval of related information across the tables.

## DDL Syntax

```sql
-- Create 'products' table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Create 'customers' table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(200)
);

-- Create 'bill' table
CREATE TABLE bill (
    bill_id INT PRIMARY KEY,
    customer_id INT,
    bill_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create 'billdetails' table
CREATE TABLE billdetails (
    billdetail_id INT PRIMARY KEY,
    bill_id INT,
    product_id INT,
    quantity INT NOT NULL,
    line_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (bill_id) REFERENCES bill(bill_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);


```

## DML Syntax

-- Insert records into 'dept'
```sql
-- Insert records into 'products'
INSERT INTO products (product_id, product_name, price) VALUES
(1, 'Laptop', 1000.00),
(2, 'Smartphone', 700.00),
(3, 'Tablet', 500.00),
(4, 'Headphones', 150.00),
(5, 'Keyboard', 50.00),
(6, 'Mouse', 30.00),
(7, 'Monitor', 200.00),
(8, 'Printer', 250.00),
(9, 'Camera', 400.00),
(10, 'External Hard Drive', 100.00);

-- Insert records into 'customers'
INSERT INTO customers (customer_id, customer_name, contact_info) VALUES
(1, 'John Doe', 'john.doe@example.com'),
(2, 'Jane Smith', 'jane.smith@example.com'),
(3, 'Michael Johnson', 'michael.johnson@example.com'),
(4, 'Emily Davis', 'emily.davis@example.com'),
(5, 'David Wilson', 'david.wilson@example.com'),
(6, 'Sarah Taylor', 'sarah.taylor@example.com'),
(7, 'James Brown', 'james.brown@example.com'),
(8, 'Jessica Jones', 'jessica.jones@example.com'),
(9, 'Chris Miller', 'chris.miller@example.com'),
(10, 'Amanda Martinez', 'amanda.martinez@example.com'),
(11, 'Brian Scott', 'brian.scott@example.com'),
(12, 'Laura Green', 'laura.green@example.com'),
(13, 'Daniel White', 'daniel.white@example.com'),
(14, 'Nancy Moore', 'nancy.moore@example.com'),
(15, 'Steven Harris', 'steven.harris@example.com');

-- Insert records into 'bill' and 'billdetails' tables
-- Note: This is just an example, you will need to adjust the bill_id, customer_id, product_id, quantity, and line_total based on your actual data and billing logic.
INSERT INTO bill (bill_id, customer_id, bill_date, total_amount) VALUES
(1, 1, '2023-01-15', 2150.00),
(2, 2, '2023-01-20', 1200.00);

INSERT INTO billdetails (billdetail_id, bill_id, product_id, quantity, line_total) VALUES
(1, 1, 1, 1, 1000.00),
(2, 1, 4, 2, 300.00),
(3, 1, 5, 1, 50.00),
(4, 1, 6, 1, 30.00),
(5, 1, 7, 1, 200.00),
(6, 1, 8, 1, 250.00),
(7, 1, 10, 1, 100.00),
(8, 2, 2, 1, 700.00),
(9, 2, 3, 1, 500.00);


```