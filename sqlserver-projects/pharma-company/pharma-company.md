![SQL Server Tinitiate Image](../../sqlserver-sql/sqlserver.png)

# SQL Server Tutorial

&copy; TINITIATE.COM

# Pharmaceutical Manufacturing & Distribution Data Model
This data model supports end-to-end pharmaceutical operations: from raw material sourcing and formulation through manufacturing, quality control, inventory management, and distribution.  
- **Address**, **Supplier**, and **RawMaterial** define lookup data for vendors and inputs.  
- **Product** and **Formulation** capture the bill-of-materials for each drug.  
- **ManufacturingBatch** records each production run, using partitioning for large-scale data.  
- **Equipment** and **QualityTest** list assets and QC procedures.  
- **QCResult** logs pass/fail outcomes per batch.  
- **DistributionCenter**, **Inventory**, and **Shipment** manage where and when product moves.  
- **Customer**, **SalesOrder**, and **RegulatorySubmission** track orders, clients, and compliance filings.

## Address Table
* **AddressID**: Surrogate key (PK).  
* **Street**, **City**, **State**, **ZIP**, **Country**: Standard address fields.

## Supplier Table
* **SupplierID**: Surrogate key (PK).  
* **Name**, **ContactName**, **Phone**, **Email**: Vendor details.  
* **AddressID**: FK → Address(AddressID).  
* **CreatedAt/By**, **UpdatedAt/By**: Audit columns.

## RawMaterial Table
* **RawMaterialID**: Surrogate key (PK).  
* **Name**, **CASNumber**: Material identifiers.  
* **SupplierID**: FK → Supplier(SupplierID).  
* **CreatedAt/By**: Audit columns.

## Product Table
* **ProductID**: Surrogate key (PK).  
* **Name**, **Strength**, **Formulation**: Drug characteristics.  
* **CreatedAt/By**, **UpdatedAt/By**: Audit columns.

## Formulation Table
* **ProductID**, **RawMaterialID**: Composite PK & FKs → Product, RawMaterial.  
* **Percentage**: % by weight/volume.  
* **CreatedAt**: Timestamp.

## ManufacturingBatch Table
* **BatchID**, **BatchDate**: Composite PK, partitioned by date.  
* **ProductID**: FK → Product(ProductID).  
* **QuantityUnits**, **Status**: Production metrics.  
* **CreatedAt/By**: Audit.  
* **IX_Batch_ProductDate**: Index for fast lookups.

## Equipment Table
* **EquipmentID**: Surrogate key (PK).  
* **Name**, **Type**, **Location**: Asset details.  
* **CreatedAt**: Timestamp.

## QualityTest Table
* **TestID**: Surrogate key (PK).  
* **Name**, **Method**: QC procedure info.  
* **CreatedAt**: Timestamp.

## QCResult Table
* **ResultID**, **TestDate**: Composite PK, partitioned by date.  
* **BatchID**: FK → ManufacturingBatch(BatchID).  
* **TestID**: FK → QualityTest(TestID).  
* **ResultValue**, **PassFail**: Outcome data.  
* **CreatedAt**: Timestamp.  
* **IX_QC_BatchDate**: Index for batch/date queries.

## DistributionCenter Table
* **CenterID**: Surrogate key (PK).  
* **Name**, **AddressID**: FK → Address(AddressID).  
* **CreatedAt**: Timestamp.

## Inventory Table
* **InventoryID**, **SnapshotDate**: Composite PK, partitioned by date.  
* **CenterID**, **ProductID**: FKs → DistributionCenter, Product.  
* **QuantityUnits**: On-hand stock.  
* **CreatedAt**: Timestamp.  
* **IX_Inv_CenterDate**: Index on center/date.

## Shipment Table
* **ShipmentID**, **ShipmentDate**: Composite PK, partitioned by date.  
* **CenterID**, **CustomerID**: FKs → DistributionCenter, Customer.  
* **QuantityUnits**: Shipped volume.  
* **CreatedAt**: Timestamp.  
* **IX_Ship_CenterDate**: Index on center/date.

## Customer Table
* **CustomerID**: Surrogate key (PK).  
* **Name**, **AddressID**: FK → Address(AddressID).  
* **CreatedAt**: Timestamp.

## SalesOrder Table
* **SalesOrderID**, **OrderDate**: Composite PK, partitioned by date.  
* **CustomerID**: FK → Customer(CustomerID).  
* **TotalUnits**, **TotalAmount**, **Status**: Order details.  
* **CreatedAt**: Timestamp.  
* **IX_SO_CustDate**: Index on customer/date.

## RegulatorySubmission Table
* **SubmissionID**: Surrogate key (PK).  
* **ProductID**: FK → Product(ProductID).  
* **SubmissionDate**, **Agency**, **Status**, **DocumentLink**: Compliance filings.  
* **CreatedAt**: Timestamp.

## DDL Syntax
```sql
-- Create 'pharma_company' schema
CREATE SCHEMA pharma_company;

-- Create 'Address' table
CREATE TABLE pharma_company.Address
(
  AddressID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Street      NVARCHAR(150) NOT NULL,
  City        NVARCHAR(50)  NOT NULL,
  State       NVARCHAR(50)  NOT NULL,
  ZIP         NVARCHAR(15)  NOT NULL,
  Country     NVARCHAR(50)  NOT NULL
);

-- Create 'Supplier' table
CREATE TABLE pharma_company.Supplier
(
  SupplierID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  ContactName   NVARCHAR(100) NULL,
  Phone         VARCHAR(20)   NULL,
  Email         VARCHAR(100)  NULL,
  AddressID     INT           NULL
    CONSTRAINT FK_Supplier_Address FOREIGN KEY REFERENCES pharma_company.Address(AddressID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
);

-- Create 'RawMaterial' table
CREATE TABLE pharma_company.RawMaterial
(
  RawMaterialID INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  CASNumber     VARCHAR(50)   NULL,
  SupplierID    INT           NOT NULL
    CONSTRAINT FK_RawMat_Supplier FOREIGN KEY REFERENCES pharma_company.Supplier(SupplierID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
);

-- Create 'Product' table
CREATE TABLE pharma_company.Product
(
  ProductID     INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(200) NOT NULL,
  Strength      NVARCHAR(50)  NULL,   -- e.g. "500 mg"
  Formulation   NVARCHAR(50)  NULL,   -- e.g. "Tablet", "Capsule"
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
);

-- Create 'Formulation' table
CREATE TABLE pharma_company.Formulation
(
  ProductID     INT           NOT NULL
    CONSTRAINT PK_Formulation PRIMARY KEY CLUSTERED (ProductID, RawMaterialID),
  RawMaterialID INT           NOT NULL
    CONSTRAINT FK_Formulation_RawMat FOREIGN KEY REFERENCES pharma_company.RawMaterial(RawMaterialID),
  Percentage    DECIMAL(5,2)  NOT NULL,  -- % by weight/volume
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- Create 'ManufacturingBatch' table
CREATE TABLE pharma_company.ManufacturingBatch
(
  BatchID       BIGINT       NOT NULL,
  ProductID     INT           NOT NULL
    CONSTRAINT FK_Batch_Product FOREIGN KEY REFERENCES pharma_company.Product(ProductID),
  BatchDate     DATE          NOT NULL,
  QuantityUnits INT           NOT NULL,
  Status        NVARCHAR(20)  NOT NULL,  -- e.g. "Released","Hold"
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_ManufacturingBatch PRIMARY KEY CLUSTERED (BatchID, BatchDate)
    ON PS_PharmaYear(BatchDate)
);

-- Create 'Equipment' table
CREATE TABLE pharma_company.Equipment
(
  EquipmentID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(100) NOT NULL,
  Type          NVARCHAR(50)  NULL,  -- e.g. "Reactor", "Granulator"
  Location      NVARCHAR(100) NULL,
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- Create 'QualityTest' table
CREATE TABLE pharma_company.QualityTest
(
  TestID        INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,  -- e.g. "Dissolution", "Purity"
  Method        NVARCHAR(100) NULL,
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- Create 'QCResult' table
CREATE TABLE pharma_company.QCResult
(
  ResultID      BIGINT       NOT NULL,
  BatchID       BIGINT       NOT NULL
    CONSTRAINT FK_QC_Batch FOREIGN KEY REFERENCES pharma_company.ManufacturingBatch(BatchID),
  TestID        INT          NOT NULL
    CONSTRAINT FK_QC_Test FOREIGN KEY REFERENCES pharma_company.QualityTest(TestID),
  TestDate      DATE         NOT NULL,
  ResultValue   NVARCHAR(100) NULL,
  PassFail      CHAR(1)      NOT NULL,  -- 'P' or 'F'
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_QCResult PRIMARY KEY CLUSTERED (ResultID, TestDate)
    ON PS_PharmaYear(TestDate)
);

-- Create 'DistributionCenter' table
CREATE TABLE pharma_company.DistributionCenter
(
  CenterID      INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  AddressID     INT           NULL
    CONSTRAINT FK_DC_Address FOREIGN KEY REFERENCES pharma_company.Address(AddressID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- Create 'Inventory' table
CREATE TABLE pharma_company.Inventory
(
  InventoryID   BIGINT       NOT NULL,
  CenterID      INT          NOT NULL
    CONSTRAINT FK_Inv_Center FOREIGN KEY REFERENCES pharma_company.DistributionCenter(CenterID),
  ProductID     INT          NOT NULL
    CONSTRAINT FK_Inv_Product FOREIGN KEY REFERENCES pharma_company.Product(ProductID),
  SnapshotDate  DATE         NOT NULL,
  QuantityUnits INT          NOT NULL,
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_Inventory PRIMARY KEY CLUSTERED (InventoryID, SnapshotDate)
    ON PS_PharmaYear(SnapshotDate)
);

-- Create 'Shipment' table
CREATE TABLE pharma_company.Shipment
(
  ShipmentID    BIGINT       NOT NULL,
  CenterID      INT          NOT NULL
    CONSTRAINT FK_Ship_Center FOREIGN KEY REFERENCES pharma_company.DistributionCenter(CenterID),
  CustomerID    INT          NOT NULL
    CONSTRAINT FK_Ship_Cust FOREIGN KEY REFERENCES pharma_company.Customer(CustomerID),
  ShipmentDate  DATE         NOT NULL,
  QuantityUnits INT          NOT NULL,
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_Shipment PRIMARY KEY CLUSTERED (ShipmentID, ShipmentDate)
    ON PS_PharmaYear(ShipmentDate)
);

-- Create 'Customer' table
CREATE TABLE pharma_company.Customer
(
  CustomerID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  AddressID     INT           NULL
    CONSTRAINT FK_Cust_Address FOREIGN KEY REFERENCES pharma_company.Address(AddressID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- Create 'SalesOrder' table
CREATE TABLE pharma_company.SalesOrder
(
  SalesOrderID  BIGINT       NOT NULL,
  CustomerID    INT          NOT NULL
    CONSTRAINT FK_SO_Cust FOREIGN KEY REFERENCES pharma_company.Customer(CustomerID),
  OrderDate     DATE         NOT NULL,
  TotalUnits    INT          NOT NULL,
  TotalAmount   DECIMAL(18,2)NOT NULL,
  Status        NVARCHAR(20) NOT NULL,  -- e.g. "Open","Shipped"
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_SalesOrder PRIMARY KEY CLUSTERED (SalesOrderID, OrderDate)
    ON PS_PharmaYear(OrderDate)
);

-- Create 'RegulatorySubmission' table
CREATE TABLE pharma_company.RegulatorySubmission
(
  SubmissionID  BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  ProductID     INT          NOT NULL
    CONSTRAINT FK_RS_Product FOREIGN KEY REFERENCES pharma_company.Product(ProductID),
  SubmissionDate DATE        NOT NULL,
  Agency        NVARCHAR(100)NOT NULL,  -- e.g. "FDA", "EMA"
  Status        NVARCHAR(50) NOT NULL,  -- e.g. "Pending","Approved"
  DocumentLink  NVARCHAR(255) NULL,
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME()
);
```

## DML Syntax
```sql
-- Insert records for 'Address'
INSERT INTO pharma_company.Address (Street, City, State, ZIP, Country)
VALUES
  ('123 Elm St','Springfield','Illinois','62701','USA'),
  ('456 Oak St','Greenfield','Wisconsin','53220','USA'),
  ('789 Pine Ave','Munich','Bavaria','80331','Germany'),
  ('101 Maple Rd','London','Greater London','SW1A 1AA','UK'),
  ('202 Cedar Blvd','Mumbai','Maharashtra','400001','India'),
  ('303 Birch Ln','Beijing','Beijing','100000','China'),
  ('404 Walnut Dr','Tokyo','Tokyo','100-0001','Japan'),
  ('505 Chestnut Pkwy','São Paulo','São Paulo','01000-000','Brazil'),
  ('606 Aspen Ct','Toronto','Ontario','M5H 2N2','Canada'),
  ('707 Willow Way','Sydney','New South Wales','2000','Australia');

-- Insert records for 'Supplier'
INSERT INTO pharma_company.Supplier (Name, ContactName, Phone, Email, AddressID)
VALUES
  ('Acme Chemicals','John Doe','+1-555-1001','john.doe@acmechem.com',1),
  ('Global Vitamins','Jane Smith','+1-555-1002','jane.smith@globalvit.com',2),
  ('Pharma Suppliers GmbH','Max Müller','+49-89-123456','max.mueller@pharmasup.de',3),
  ('UK Formulations Ltd','Emily Brown','+44-20-7946-0011','emily.brown@ukform.com',4),
  ('India RawMat Co','Ravi Kumar','+91-22-1234-5678','ravi.kumar@indiarawmat.in',5),
  ('Beijing Biochem','Li Wei','+86-10-12345678','li.wei@bjbiochem.cn',6),
  ('Tokyo Materials','Satoshi Tanaka','+81-3-1234-5678','satoshi.tanaka@tokyomat.jp',7),
  ('Brasil Pharma SRL','Carlos Silva','+55-11-91234-5678','carlos.silva@brpharma.br',8),
  ('Maple Leaf Supplies','Sarah Johnson','+1-416-555-0133','sarah.johnson@maplesup.ca',9),
  ('Sydney BioTech','Michael Lee','+61-2-1234-5678','michael.lee@sydbiotech.au',10);

-- Insert records for 'RawMaterial'
INSERT INTO pharma_company.RawMaterial (Name, CASNumber, SupplierID)
VALUES
  ('Paracetamol','103-90-2',1),
  ('Ibuprofen','15687-27-1',1),
  ('Aspirin','50-78-2',2),
  ('Amoxicillin','61336-70-7',2),
  ('Cetirizine','83881-51-0',3),
  ('Loratadine','79794-75-5',3),
  ('Metformin','657-24-9',4),
  ('Glipizide','29094-61-9',4),
  ('Simvastatin','79902-63-9',5),
  ('Atorvastatin','134523-00-5',5),
  ('Omeprazole','73590-58-6',6),
  ('Esomeprazole','119141-89-8',6),
  ('Ciprofloxacin','85721-33-1',7),
  ('Levofloxacin','100986-85-4',7),
  ('Doxycycline','564-25-0',8),
  ('Tetracycline','60-54-8',8),
  ('Clopidogrel','113507-06-2',9),
  ('Warfarin','81-81-2',9),
  ('Metoprolol','37350-58-6',10),
  ('Amlodipine','88150-42-9',10);

-- Insert records for 'Product'
INSERT INTO pharma_company.Product (Name, Strength, Formulation)
VALUES
  ('PainRelief','500 mg','Tablet'),
  ('ColdCure','10 mg','Capsule'),
  ('AllergyAway','5 mg','Tablet'),
  ('SugarControl','500 mg','Tablet'),
  ('CholesterolX','20 mg','Tablet'),
  ('AcidBlock','20 mg','Capsule'),
  ('InfectionStop','250 mg','Capsule'),
  ('HeartCare','10 mg','Tablet'),
  ('GutHealth','40 mg','Tablet'),
  ('BPRegulator','5 mg','Tablet');

-- Insert records for 'Formulation'
INSERT INTO pharma_company.Formulation (ProductID, RawMaterialID, Percentage)
VALUES
  (1,1,60.00),(1,2,40.00),
  (2,3,70.00),(2,4,30.00),
  (3,5,50.00),(3,6,50.00),
  (4,7,80.00),(4,8,20.00),
  (5,9,65.00),(5,10,35.00),
  (6,11,50.00),(6,12,50.00),
  (7,13,55.00),(7,14,45.00),
  (8,17,50.00),(8,18,50.00),
  (9,19,60.00),(9,20,40.00),
  (10,19,50.00),(10,20,50.00);

-- Insert records for 'ManufacturingBatch'
INSERT INTO pharma_company.ManufacturingBatch
(BatchID, ProductID, BatchDate, QuantityUnits, Status)
VALUES
  (1001,1,'2025-07-01',10000,'Released'),
  (1002,2,'2025-07-02',15000,'Released'),
  (1003,3,'2025-07-03',12000,'Hold'),
  (1004,4,'2025-07-04',8000,'Released'),
  (1005,5,'2025-07-05',20000,'Released'),
  (1006,6,'2025-07-06',11000,'Hold'),
  (1007,7,'2025-07-07',9000,'Released'),
  (1008,8,'2025-07-08',13000,'Released'),
  (1009,9,'2025-07-09',14000,'Hold'),
  (1010,10,'2025-07-10',16000,'Released'),
  (1011,1,'2025-07-11',17000,'Released'),
  (1012,2,'2025-07-12',18000,'Hold'),
  (1013,3,'2025-07-13',19000,'Released'),
  (1014,4,'2025-07-14',12500,'Released'),
  (1015,5,'2025-07-15',13500,'Hold'),
  (1016,6,'2025-07-16',14500,'Released'),
  (1017,7,'2025-07-17',15500,'Released'),
  (1018,8,'2025-07-18',16500,'Hold'),
  (1019,9,'2025-07-19',17500,'Released'),
  (1020,10,'2025-07-20',18500,'Released');

-- Insert records for 'Equipment'
INSERT INTO pharma_company.Equipment (Name, Type, Location)
VALUES
  ('Reactor A','Reactor','Plant 1'),
  ('Reactor B','Reactor','Plant 2'),
  ('Mixer A','Mixer','Plant 1'),
  ('Mixer B','Mixer','Plant 2'),
  ('Dryer A','Dryer','Plant 1'),
  ('Filter Unit','Filter','Plant 2'),
  ('Packaging Line','Packaging','Plant 1'),
  ('Conveyor Belt','Conveyor','Plant 2'),
  ('Autoclave','Sterilizer','Plant 1'),
  ('Quality Station','Inspection','Plant 2');

-- Insert records for 'QualityTest'
INSERT INTO pharma_company.QualityTest (Name, Method)
VALUES
  ('Dissolution Test','USP II'),
  ('Purity Test','HPLC'),
  ('Moisture Content','Karl Fischer'),
  ('Particle Size','Laser Diffraction'),
  ('pH Measurement','pH Meter'),
  ('Bioavailability','In Vivo'),
  ('Content Uniformity','UV Spectroscopy'),
  ('Stability Test','ICH Guidelines'),
  ('Sterility Test','Membrane Filtration'),
  ('Endotoxin Test','LAL Assay');

-- Insert records for 'QCResult'
INSERT INTO pharma_company.QCResult
(ResultID, BatchID, TestID, TestDate, ResultValue, PassFail)
VALUES
  (5001,1001,1,'2025-07-02','98%','P'),
  (5002,1002,2,'2025-07-03','99%','P'),
  (5003,1003,3,'2025-07-04','0.1%','P'),
  (5004,1004,4,'2025-07-05','50 µm','P'),
  (5005,1005,5,'2025-07-06','7.1','P'),
  (5006,1006,6,'2025-07-07','80%','P'),
  (5007,1007,7,'2025-07-08','1.2 AU','P'),
  (5008,1008,8,'2025-07-09','Pass','P'),
  (5009,1009,9,'2025-07-10','Sterile','P'),
  (5010,1010,10,'2025-07-11','Negative','P'),
  (5011,1011,1,'2025-07-12','95%','P'),
  (5012,1012,2,'2025-07-13','90%','P'),
  (5013,1013,3,'2025-07-14','0.2%','P'),
  (5014,1014,4,'2025-07-15','55 µm','P'),
  (5015,1015,5,'2025-07-16','7.0','P'),
  (5016,1016,6,'2025-07-17','75%','P'),
  (5017,1017,7,'2025-07-18','1.1 AU','P'),
  (5018,1018,8,'2025-07-19','Fail','F'),
  (5019,1019,9,'2025-07-20','Contaminated','F'),
  (5020,1020,10,'2025-07-21','Positive','P');

-- Insert records for 'DistributionCenter'
INSERT INTO pharma_company.DistributionCenter (Name, AddressID)
VALUES
  ('Central Warehouse',1),
  ('East Hub',2),
  ('West Hub',3),
  ('North Hub',4),
  ('South Hub',5);

-- Insert records for 'Inventory'
INSERT INTO pharma_company.Inventory
(InventoryID, CenterID, ProductID, SnapshotDate, QuantityUnits)
VALUES
  (2001,1,1,'2025-07-06',5000),
  (2002,2,2,'2025-07-07',6000),
  (2003,3,3,'2025-07-08',5500),
  (2004,4,4,'2025-07-09',7000),
  (2005,5,5,'2025-07-10',6500),
  (2006,1,6,'2025-07-11',5200),
  (2007,2,7,'2025-07-12',5800),
  (2008,3,8,'2025-07-13',6200),
  (2009,4,9,'2025-07-14',7100),
  (2010,5,10,'2025-07-15',8000),
  (2011,1,1,'2025-07-16',4500),
  (2012,2,2,'2025-07-17',4900),
  (2013,3,3,'2025-07-18',5300),
  (2014,4,4,'2025-07-19',5800),
  (2015,5,5,'2025-07-20',6300),
  (2016,1,6,'2025-07-21',6700),
  (2017,2,7,'2025-07-22',7200),
  (2018,3,8,'2025-07-23',7600),
  (2019,4,9,'2025-07-24',8100),
  (2020,5,10,'2025-07-25',8500);

-- Insert records for 'Shipment'
INSERT INTO pharma_company.Shipment
(ShipmentID, CenterID, CustomerID, ShipmentDate, QuantityUnits)
VALUES
  (3001,1,1,'2025-07-08',1000),
  (3002,2,2,'2025-07-09',1500),
  (3003,3,3,'2025-07-10',900),
  (3004,4,4,'2025-07-11',1200),
  (3005,5,5,'2025-07-12',1100),
  (3006,1,6,'2025-07-13',1300),
  (3007,2,7,'2025-07-14',1400),
  (3008,3,8,'2025-07-15',1600),
  (3009,4,9,'2025-07-16',1700),
  (3010,5,10,'2025-07-17',1800),
  (3011,1,1,'2025-07-18',1900),
  (3012,2,2,'2025-07-19',2000),
  (3013,3,3,'2025-07-20',2100),
  (3014,4,4,'2025-07-21',2200),
  (3015,5,5,'2025-07-22',2300),
  (3016,1,6,'2025-07-23',2400),
  (3017,2,7,'2025-07-24',2500),
  (3018,3,8,'2025-07-25',2600),
  (3019,4,9,'2025-07-26',2700),
  (3020,5,10,'2025-07-27',2800);

-- Insert records for 'Customer'
INSERT INTO pharma_company.Customer (Name, AddressID)
VALUES
  ('HealthCare Center',1),
  ('Wellness Clinic',2),
  ('City Pharmacy',3),
  ('Global Health Org',4),
  ('MediPlus Hospital',5),
  ('Green Valley Clinic',6),
  ('Sunrise Pharmacy',7),
  ('Downtown Clinic',8),
  ('Lakeside Hospital',9),
  ('Mountainview Clinic',10);

-- Insert records for 'SalesOrder'
INSERT INTO pharma_company.SalesOrder 
(SalesOrderID, CustomerID, OrderDate, TotalUnits, TotalAmount, Status)
VALUES
  (4001,1,'2025-07-05',500,7500.00,'Open'),
  (4002,2,'2025-07-06',600,9000.00,'Shipped'),
  (4003,3,'2025-07-07',700,10500.00,'Completed'),
  (4004,4,'2025-07-08',800,12000.00,'Open'),
  (4005,5,'2025-07-09',900,13500.00,'Shipped'),
  (4006,6,'2025-07-10',1000,15000.00,'Completed'),
  (4007,7,'2025-07-11',1100,16500.00,'Open'),
  (4008,8,'2025-07-12',1200,18000.00,'Shipped'),
  (4009,9,'2025-07-13',1300,19500.00,'Completed'),
  (4010,10,'2025-07-14',1400,21000.00,'Open'),
  (4011,1,'2025-07-15',1500,22500.00,'Shipped'),
  (4012,2,'2025-07-16',1600,24000.00,'Completed'),
  (4013,3,'2025-07-17',1700,25500.00,'Open'),
  (4014,4,'2025-07-18',1800,27000.00,'Shipped'),
  (4015,5,'2025-07-19',1900,28500.00,'Completed'),
  (4016,6,'2025-07-20',2000,30000.00,'Open'),
  (4017,7,'2025-07-21',2100,31500.00,'Shipped'),
  (4018,8,'2025-07-22',2200,33000.00,'Completed'),
  (4019,9,'2025-07-23',2300,34500.00,'Open'),
  (4020,10,'2025-07-24',2400,36000.00,'Shipped');

-- Insert records for 'RegulatorySubmission'
INSERT INTO pharma_company.RegulatorySubmission
(ProductID, SubmissionDate, Agency, Status, DocumentLink)
VALUES
  (1,'2025-06-15','FDA','Pending','/docs/sub_001.pdf'),
  (2,'2025-06-20','EMA','Approved','/docs/sub_002.pdf'),
  (3,'2025-06-22','PMDA','Pending','/docs/sub_003.pdf'),
  (4,'2025-06-25','TGA','Approved','/docs/sub_004.pdf'),
  (5,'2025-06-28','ANVISA','Pending','/docs/sub_005.pdf'),
  (6,'2025-07-01','FDA','Approved','/docs/sub_006.pdf'),
  (7,'2025-07-03','EMA','Pending','/docs/sub_007.pdf'),
  (8,'2025-07-05','PMDA','Approved','/docs/sub_008.pdf'),
  (9,'2025-07-07','TGA','Pending','/docs/sub_009.pdf'),
  (10,'2025-07-09','ANVISA','Approved','/docs/sub_010.pdf');
```
