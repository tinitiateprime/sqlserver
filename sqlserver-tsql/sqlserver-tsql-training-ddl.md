![SQL Server Tinitiate Image](../sqlserver-sql/sqlserver.png)

# SQL Server - TSQL
&copy; TINITIATE.COM

##### [Back To Context](./README.md)

# Training DDL
* We will use the below DDL in our TSQL training.
```sql
-- Use tinitiate database
USE tinitiate;

-- Invoice Schema
CREATE SCHEMA invoicing authorization dbo;
ALTER AUTHORIZATION ON SCHEMA::invoicing TO tiuser;

-- Products
CREATE TABLE invoicing.products(
    product_id INT NOT NULL,
    product_category VARCHAR(100),
    product_name VARCHAR(25),
    product_unit_price DECIMAL(12,2));
    
ALTER TABLE invoicing.products ADD CONSTRAINT pk_product_id
PRIMARY KEY(product_id);

-- Invoice
CREATE TABLE invoicing.invoice(
    invoice_id INT NOT NULL,
    invoice_date DATE,
    invoice_total DECIMAL(12,2),
    discount DECIMAL(12,2),
    invoice_price DECIMAL(12,2));
    
ALTER TABLE invoicing.invoice ADD CONSTRAINT pk_invoice_id
PRIMARY KEY(invoice_id);

-- Invoice Details
CREATE TABLE invoicing.invoice_items (
    invoice_item_id INT NOT NULL,
    invoice_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(12,2),
    invoice_item_price DECIMAL(12,2));

ALTER TABLE invoicing.invoice_items ADD CONSTRAINT pk_invoice_item_id
PRIMARY KEY(invoice_item_id);
ALTER TABLE invoicing.invoice_items ADD CONSTRAINT fk_invoice_id
FOREIGN KEY(invoice_id) REFERENCES invoicing.invoice(invoice_id);
ALTER TABLE invoicing.invoice_items ADD CONSTRAINT fk_product_id
FOREIGN KEY(product_id) REFERENCES invoicing.products(product_id);
```

##### [Back To Context](./README.md)
***
| &copy; TINITIATE.COM |
|----------------------|
