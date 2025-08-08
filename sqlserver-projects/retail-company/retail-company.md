![SQL Server Tinitiate Image](../../sqlserver-sql/sqlserver.png)

# SQL Server Tutorial

&copy; TINITIATE.COM

# Retail Company Data Model
This model supports core retail operations: customers and addresses, catalog (categories, suppliers, products), inventory across warehouses, sales orders with line items, and procurement via purchase orders.  
- **Customer, Address** capture buyer and shipping details.  
- **ProductCategory, Supplier, Product** define the merchandise master.  
- **Warehouse, Inventory** track stock by site and date.  
- **SalesOrder, SalesOrderDetail** handle order capture (partitioned by order date).  
- **PurchaseOrder, PurchaseOrderDetail** manage replenishment from suppliers.  
Targeted nonclustered indexes optimize common filters (category, product/date, customer/date, status).

## Customer
* **CustomerID**: Surrogate key (PK).  
* **FirstName, LastName, Email, Phone**: Customer identity and contact.  
* **AddressID**: FK → `Address(AddressID)` (shipping/billing address).  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.

## Address
* **AddressID**: Surrogate key (PK).  
* **Street, City, State, ZIP, Country**: Standard address fields.

## ProductCategory
* **CategoryID**: Surrogate key (PK).  
* **Name, Description**: Merchandise grouping.

## Supplier
* **SupplierID**: Surrogate key (PK).  
* **Name, ContactName, Phone, Email**: Vendor info.  
* **AddressID**: FK → `Address(AddressID)`.

## Product
* **ProductID**: Surrogate key (PK).  
* **Name**: Product title.  
* **CategoryID**: FK → `ProductCategory(CategoryID)`.  
* **SupplierID**: FK → `Supplier(SupplierID)`.  
* **UnitPrice, UnitsInStock, ReorderLevel, Discontinued**: Item economics & availability.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.  
* **IX_Prod_Category**: Speeds lookups by category.

## Warehouse
* **WarehouseID**: Surrogate key (PK).  
* **Name, Location**: Stocking point metadata.

## Inventory
* **InventoryID**: Surrogate key (PK).  
* **ProductID**: FK → `Product(ProductID)`.  
* **WarehouseID**: FK → `Warehouse(WarehouseID)`.  
* **StockDate, QuantityOnHand, CreatedAt**: Daily on-hand snapshot.  
* **IX_Inv_ProductDate**: Fast recent stock checks per product.

## SalesOrder (Partitioned)
* **SalesOrderID, OrderDate**: Composite PK; partitioned by `OrderDate` (e.g., `PS_SalesYear`).  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **ShipDate, ShipAddressID**: Optional ship info (FK → `Address`).  
* **Status, TotalAmount, Created*/Updated***: Order lifecycle & audit.  
* **IX_SO_CustDate**: Customer order history by date.  
* **IX_SO_Status**: Filter by status; includes `TotalAmount`.

## SalesOrderDetail
* **SalesOrderDetailID**: Surrogate key (PK).  
* **SalesOrderID**: FK → `SalesOrder(SalesOrderID)`.  
* **ProductID**: FK → `Product(ProductID)`.  
* **UnitPrice, Quantity, LineTotal (computed)**: Line economics.  
* **IX_SOD_Product**: Product-level line lookups.

## PurchaseOrder
* **PurchaseOrderID**: Surrogate key (PK).  
* **SupplierID**: FK → `Supplier(SupplierID)`.  
* **OrderDate, ExpectedDate, Status, TotalAmount, CreatedAt/By**: PO lifecycle.  
* **IX_PO_SuppDate**: Supplier history by date.

## PurchaseOrderDetail
* **PurchaseOrderDetailID**: Surrogate key (PK).  
* **PurchaseOrderID**: FK → `PurchaseOrder(PurchaseOrderID)`.  
* **ProductID**: FK → `Product(ProductID)`.  
* **UnitCost, Quantity, LineTotal (computed)**: PO line economics.

## DDL Syntax
```sql
-- Create 'retail_company' schema
CREATE SCHEMA retail_company;

-- Create 'Customer' table
CREATE TABLE retail_company.Customer
(
  CustomerID     INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FirstName      NVARCHAR(50)  NOT NULL,
  LastName       NVARCHAR(50)  NOT NULL,
  Email          VARCHAR(100)  NULL,
  Phone          VARCHAR(20)   NULL,
  AddressID      INT           NULL
    CONSTRAINT FK_Cust_Address FOREIGN KEY REFERENCES retail_company.Address(AddressID),
  CreatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'Address' table
CREATE TABLE retail_company.Address
(
  AddressID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Street       NVARCHAR(150) NOT NULL,
  City         NVARCHAR(50)  NOT NULL,
  State        NVARCHAR(50)  NOT NULL,
  ZIP          NVARCHAR(15)  NOT NULL,
  Country      NVARCHAR(50)  NOT NULL
)

-- Create 'ProductCategory' table
CREATE TABLE retail_company.ProductCategory
(
  CategoryID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(100) NOT NULL,
  Description  NVARCHAR(255) NULL
)

-- Create 'Supplier' table
CREATE TABLE retail_company.Supplier
(
  SupplierID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  ContactName   NVARCHAR(100) NULL,
  Phone         VARCHAR(20)   NULL,
  Email         VARCHAR(100)  NULL,
  AddressID     INT           NULL
    CONSTRAINT FK_Supp_Address FOREIGN KEY REFERENCES retail_company.Address(AddressID)
)

-- Create 'Product' table
CREATE TABLE retail_company.Product
(
  ProductID      INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name           NVARCHAR(200) NOT NULL,
  CategoryID     INT           NOT NULL
    CONSTRAINT FK_Prod_Category FOREIGN KEY REFERENCES retail_company.ProductCategory(CategoryID),
  SupplierID     INT           NOT NULL
    CONSTRAINT FK_Prod_Supplier FOREIGN KEY REFERENCES retail_company.Supplier(SupplierID),
  UnitPrice      DECIMAL(18,2) NOT NULL,
  UnitsInStock   INT           NOT NULL DEFAULT 0,
  ReorderLevel   INT           NOT NULL DEFAULT 0,
  Discontinued   BIT           NOT NULL DEFAULT 0,
  CreatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'Product' table
CREATE INDEX IX_Prod_Category
ON retail_company.Product(CategoryID);

-- Create 'Inventory' table
CREATE TABLE retail_company.Inventory
(
  InventoryID   BIGINT        IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  ProductID     INT           NOT NULL
    CONSTRAINT FK_Inv_Product FOREIGN KEY REFERENCES retail_company.Product(ProductID),
  WarehouseID   INT           NOT NULL
    CONSTRAINT FK_Inv_Warehouse FOREIGN KEY REFERENCES retail_company.Warehouse(WarehouseID),
  StockDate     DATE          NOT NULL,
  QuantityOnHand INT          NOT NULL,
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)
-- Create an index for 'Inventory' table
CREATE INDEX IX_Inv_ProductDate
ON retail_company.Inventory(ProductID, StockDate DESC);

-- Create 'Warehouse' table
CREATE TABLE retail_company.Warehouse
(
  WarehouseID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(100) NOT NULL,
  Location      NVARCHAR(100) NULL
)

-- Create 'SalesOrder' table
CREATE TABLE retail_company.SalesOrder
(
  SalesOrderID   BIGINT        NOT NULL,
  CustomerID     INT           NOT NULL
    CONSTRAINT FK_SO_Customer FOREIGN KEY REFERENCES retail_company.Customer(CustomerID),
  OrderDate      DATE          NOT NULL,
  ShipDate       DATE          NULL,
  ShipAddressID  INT           NULL
    CONSTRAINT FK_SO_ShipAddr FOREIGN KEY REFERENCES retail_company.Address(AddressID),
  Status         NVARCHAR(20)  NOT NULL,
  TotalAmount    DECIMAL(18,2) NOT NULL,
  CreatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_SalesOrder PRIMARY KEY CLUSTERED (SalesOrderID, OrderDate)
    ON PS_SalesYear(OrderDate)
)

-- Create 'SalesOrderDetail' table
CREATE TABLE retail_company.SalesOrderDetail
(
  SalesOrderDetailID BIGINT    IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  SalesOrderID       BIGINT    NOT NULL
    CONSTRAINT FK_SOD_Order FOREIGN KEY REFERENCES retail_company.SalesOrder(SalesOrderID),
  ProductID          INT       NOT NULL
    CONSTRAINT FK_SOD_Product FOREIGN KEY REFERENCES retail_company.Product(ProductID),
  UnitPrice          DECIMAL(18,2) NOT NULL,
  Quantity           INT       NOT NULL,
  LineTotal          AS (UnitPrice * Quantity) PERSISTED
)
-- Create an index for 'SalesOrderDetail' table
CREATE INDEX IX_SOD_Product
ON retail_company.SalesOrderDetail(ProductID);

-- Create 'PurchaseOrder' table
CREATE TABLE retail_company.PurchaseOrder
(
  PurchaseOrderID  BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  SupplierID       INT          NOT NULL
    CONSTRAINT FK_PO_Supplier FOREIGN KEY REFERENCES retail_company.Supplier(SupplierID),
  OrderDate        DATE         NOT NULL,
  ExpectedDate     DATE         NULL,
  Status           NVARCHAR(20) NOT NULL,
  TotalAmount      DECIMAL(18,2)NOT NULL,
  CreatedAt        DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy        SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'PurchaseOrder' table
CREATE INDEX IX_PO_SuppDate
ON retail_company.PurchaseOrder(SupplierID, OrderDate DESC);

-- Create 'PurchaseOrderDetail' table
CREATE TABLE retail_company.PurchaseOrderDetail
(
  PurchaseOrderDetailID BIGINT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PurchaseOrderID       BIGINT NOT NULL
    CONSTRAINT FK_POD_PO FOREIGN KEY REFERENCES retail_company.PurchaseOrder(PurchaseOrderID),
  ProductID             INT    NOT NULL
    CONSTRAINT FK_POD_Product FOREIGN KEY REFERENCES retail_company.Product(ProductID),
  UnitCost              DECIMAL(18,2) NOT NULL,
  Quantity              INT    NOT NULL,
  LineTotal             AS (UnitCost * Quantity) PERSISTED
)
```

## DML Syntax
```sql

```
