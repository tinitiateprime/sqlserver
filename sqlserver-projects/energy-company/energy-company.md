![SQL Server Tinitiate Image](../../sqlserver-sql/sqlserver.png)

# SQL Server Tutorial

&copy; TINITIATE.COM

# Energy Company Data Model
This model covers the end-to-end energy lifecycle: customers and meters, facilities and assets, generation (production), consumption (meter readings), pricing (rate plans), sales, invoicing, payments, and asset maintenance.  
- **Address, Customer** capture contact and identity data.  
- **Department, Facility, AssetType, Asset** define the operational structure and physical equipment.  
- **EnergyProduction** records generation at assets (partitioned).  
- **Meter, MeterReading** track installed meters and periodic consumption (partitioned).  
- **RatePlan, EnergySale, Invoice, Payment** handle commercial processes from pricing to collections (partitioned where time-series).  
- **AssetMaintenance** logs upkeep and costs.  
Time-series tables use date partitioning (e.g., `PS_EnergyYear`) for scale and query performance; selective nonclustered indexes optimize common filters.

## Address
* **AddressID**: Surrogate key (PK).  
* **Street, City, State, ZIP, Country**: Standard address fields.

## Customer
* **CustomerID**: Surrogate key (PK).  
* **FirstName, LastName, Email, Phone**: Customer identity and contact.  
* **AddressID**: FK → `Address(AddressID)`.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.

## Department
* **DepartmentID**: Surrogate key (PK).  
* **Name**: Organizational unit (e.g., Operations, Maintenance).

## Facility
* **FacilityID**: Surrogate key (PK).  
* **Name, Location**: Plant/substation identity.  
* **DepartmentID**: FK → `Department(DepartmentID)`.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.

## AssetType
* **AssetTypeID**: Surrogate key (PK).  
* **Name, Description**: Equipment category (e.g., Turbine, Transformer).

## Asset
* **AssetID**: Surrogate key (PK).  
* **FacilityID**: FK → `Facility(FacilityID)`.  
* **AssetTypeID**: FK → `AssetType(AssetTypeID)`.  
* **Name, CommissionDate, Status, CapacityMW**: Equipment details and capacity.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.  
* **IX_Asset_Status**: Speeds status queries; includes `CommissionDate, CapacityMW`.

## EnergyProduction (Partitioned)
* **ProductionID, ProductionDate**: Composite PK; partitioned by `ProductionDate` (e.g., `PS_EnergyYear`).  
* **AssetID**: FK → `Asset(AssetID)`.  
* **EnergyMWh**: Generated energy for the day/period.  
* **CreatedAt/By**: Audit columns.  
* **IX_EP_AssetDate**: Fast lookups by asset and recent dates.

## Meter
* **MeterID**: Surrogate key (PK).  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **InstallationDate, MeterType, SerialNumber (UNIQUE), Status**: Meter metadata.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.

## MeterReading (Partitioned)
* **ReadingID, ReadDate**: Composite PK; partitioned by `ReadDate`.  
* **MeterID**: FK → `Meter(MeterID)`.  
* **Consumption_kWh**: Period consumption.  
* **CreatedAt/By**: Audit columns.  
* **IX_MR_MeterDate**: Optimizes recent-read queries per meter.

## RatePlan
* **RatePlanID**: Surrogate key (PK).  
* **Name, Description, PricePerkWh**: Tariff definition.  
* **EffectiveDate, ExpirationDate**: Validity window.  
* **IX_RatePlan_Eff**: Efficient plan lookup by effective/expiry dates.

## EnergySale (Partitioned)
* **SaleID, SaleDate**: Composite PK; partitioned by `SaleDate`.  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **RatePlanID**: FK → `RatePlan(RatePlanID)`.  
* **kWhSold, TotalCharge**: Billed energy and amount.  
* **CreatedAt/By**: Audit columns.  
* **IX_ES_CustDate**: Customer history by date.

## Invoice (Partitioned)
* **InvoiceID, InvoiceDate**: Composite PK; partitioned by `InvoiceDate`.  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **SaleID**: FK → `EnergySale(SaleID)`.  
* **DueDate, AmountDue, Status**: Billing lifecycle.  
* **CreatedAt/By**: Audit columns.  
* **IX_Inv_Status**: Filters by status; includes `DueDate, AmountDue`.

## Payment
* **PaymentID**: Surrogate key (PK).  
* **InvoiceID**: FK → `Invoice(InvoiceID)`.  
* **PaymentDate, AmountPaid, PaymentMethod, CheckRef**: Remittance details.  
* **CreatedAt/By**: Audit columns.

## AssetMaintenance
* **MaintenanceID**: Surrogate key (PK).  
* **AssetID**: FK → `Asset(AssetID)`.  
* **MaintenanceDate, Description, CostUSD, PerformedBy**: Work log and cost tracking.  
* **CreatedAt/By, UpdatedAt/By**: Audit columns.  
* **IX_AM_AssetDate**: Recent maintenance per asset.

## DDL Syntax
```sql
-- Create 'energy_company' schema
CREATE SCHEMA energy_company;

-- Create 'Address' table
CREATE TABLE energy_company.Address
(
  AddressID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Street      NVARCHAR(150) NOT NULL,
  City        NVARCHAR(50)  NOT NULL,
  State       NVARCHAR(50)  NOT NULL,
  ZIP         NVARCHAR(15)  NOT NULL,
  Country     NVARCHAR(50)  NOT NULL
);

-- Create 'Customer' table
CREATE TABLE energy_company.Customer
(
  CustomerID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FirstName     NVARCHAR(50)  NOT NULL,
  LastName      NVARCHAR(50)  NOT NULL,
  Email         VARCHAR(100)  NULL,
  Phone         VARCHAR(20)   NULL,
  AddressID     INT           NULL
    CONSTRAINT FK_Cust_Address FOREIGN KEY REFERENCES energy_company.Address(AddressID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'Department' table
CREATE TABLE energy_company.Department
(
  DepartmentID  INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(100) NOT NULL
)

-- Create 'Facility' table
CREATE TABLE energy_company.Facility
(
  FacilityID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  Location      NVARCHAR(100) NULL,
  DepartmentID  INT           NULL
    CONSTRAINT FK_Fac_Department FOREIGN KEY REFERENCES energy_company.Department(DepartmentID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'AssetType' table
CREATE TABLE energy_company.AssetType
(
  AssetTypeID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(100) NOT NULL,
  Description   NVARCHAR(255) NULL
)

-- Create 'Asset' table
CREATE TABLE energy_company.Asset
(
  AssetID         BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FacilityID      INT          NOT NULL
    CONSTRAINT FK_Asset_Facility FOREIGN KEY REFERENCES energy_company.Facility(FacilityID),
  AssetTypeID     INT          NOT NULL
    CONSTRAINT FK_Asset_Type     FOREIGN KEY REFERENCES energy_company.AssetType(AssetTypeID),
  Name            NVARCHAR(150) NOT NULL,
  CommissionDate  DATE         NULL,
  Status          NVARCHAR(50)  NOT NULL DEFAULT 'Active',
  CapacityMW      DECIMAL(10,2) NULL,
  CreatedAt       DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy       SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt       DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy       SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'Asset' table
CREATE INDEX IX_Asset_Status
ON energy_company.Asset(Status)
INCLUDE (CommissionDate, CapacityMW);

-- Create 'EnergyProduction' table
CREATE TABLE energy_company.EnergyProduction
(
  ProductionID     BIGINT       NOT NULL,
  AssetID          BIGINT       NOT NULL
    CONSTRAINT FK_EP_Asset FOREIGN KEY REFERENCES energy_company.Asset(AssetID),
  ProductionDate   DATE         NOT NULL,
  EnergyMWh        DECIMAL(18,4)NOT NULL,
  CreatedAt        DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy        SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
  ,CONSTRAINT PK_EnergyProduction PRIMARY KEY CLUSTERED (ProductionID, ProductionDate)
    ON PS_EnergyYear(ProductionDate)
)
-- Create an index for 'EnergyProduction' table
CREATE INDEX IX_EP_AssetDate
ON energy_company.EnergyProduction(AssetID, ProductionDate DESC);

-- Create 'Meter' table
CREATE TABLE energy_company.Meter
(
  MeterID          BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  CustomerID       INT          NOT NULL
    CONSTRAINT FK_Meter_Cust FOREIGN KEY REFERENCES energy_company.Customer(CustomerID),
  InstallationDate DATE         NOT NULL,
  MeterType        NVARCHAR(50) NULL,
  SerialNumber     VARCHAR(50)  NULL UNIQUE,
  Status           NVARCHAR(50) NOT NULL DEFAULT 'Active',
  CreatedAt        DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy        SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt        DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy        SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'Meter' table
CREATE INDEX IX_QC_BatchDate
ON pharma_company.QCResult(BatchID, TestDate DESC);

-- Create 'MeterReading' table
CREATE TABLE energy_company.MeterReading
(
  ReadingID       BIGINT       NOT NULL,
  MeterID         BIGINT       NOT NULL
    CONSTRAINT FK_MR_Meter FOREIGN KEY REFERENCES energy_company.Meter(MeterID),
  ReadDate        DATE         NOT NULL,
  Consumption_kWh DECIMAL(18,4)NOT NULL,
  CreatedAt       DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy       SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_MeterReading PRIMARY KEY CLUSTERED (ReadingID, ReadDate)
    ON PS_EnergyYear(ReadDate)
)
-- Create an index for 'MeterReading' table
CREATE INDEX IX_MR_MeterDate
ON energy_company.MeterReading(MeterID, ReadDate DESC);

-- Create 'RatePlan' table
CREATE TABLE energy_company.RatePlan
(
  RatePlanID     INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name           NVARCHAR(100) NOT NULL,
  Description    NVARCHAR(255) NULL,
  PricePerkWh    DECIMAL(10,4) NOT NULL,
  EffectiveDate  DATE         NOT NULL,
  ExpirationDate DATE         NULL
)
-- Create an index for 'RatePlan' table
CREATE INDEX IX_RatePlan_Eff
ON energy_company.RatePlan(EffectiveDate, ExpirationDate);

-- Create 'EnergySale' table
CREATE TABLE energy_company.EnergySale
(
  SaleID         BIGINT       NOT NULL,
  CustomerID     INT          NOT NULL
    CONSTRAINT FK_ES_Cust FOREIGN KEY REFERENCES energy_company.Customer(CustomerID),
  RatePlanID     INT          NOT NULL
    CONSTRAINT FK_ES_Rate FOREIGN KEY REFERENCES energy_company.RatePlan(RatePlanID),
  SaleDate       DATE         NOT NULL,
  kWhSold        DECIMAL(18,4)NOT NULL,
  TotalCharge    DECIMAL(18,2)NOT NULL,
  CreatedAt      DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_EnergySale PRIMARY KEY CLUSTERED (SaleID, SaleDate)
    ON PS_EnergyYear(SaleDate)
)
-- Create an index for 'EnergySale' table
CREATE INDEX IX_ES_CustDate
ON energy_company.EnergySale(CustomerID, SaleDate DESC);

-- Create 'Invoice' table
CREATE TABLE energy_company.Invoice
(
  InvoiceID      BIGINT       NOT NULL,
  CustomerID     INT          NOT NULL
    CONSTRAINT FK_Inv_Cust FOREIGN KEY REFERENCES energy_company.Customer(CustomerID),
  SaleID         BIGINT       NOT NULL
    CONSTRAINT FK_Inv_Sale FOREIGN KEY REFERENCES energy_company.EnergySale(SaleID),
  InvoiceDate    DATE         NOT NULL,
  DueDate        DATE         NOT NULL,
  AmountDue      DECIMAL(18,2)NOT NULL,
  Status         NVARCHAR(20) NOT NULL DEFAULT 'Open',
  CreatedAt      DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_Invoice PRIMARY KEY CLUSTERED (InvoiceID, InvoiceDate)
    ON PS_EnergyYear(InvoiceDate)
)
-- Create an index for 'Invoice' table
CREATE INDEX IX_Inv_Status
ON energy_company.Invoice(Status)
INCLUDE (DueDate, AmountDue);

-- Create 'Payment' table
CREATE TABLE energy_company.Payment
(
  PaymentID      BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  InvoiceID      BIGINT       NOT NULL
    CONSTRAINT FK_Pmt_Inv FOREIGN KEY REFERENCES energy_company.Invoice(InvoiceID),
  PaymentDate    DATE         NOT NULL,
  AmountPaid     DECIMAL(18,2)NOT NULL,
  PaymentMethod  NVARCHAR(50) NULL,
  CheckRef       VARCHAR(50)  NULL,
  CreatedAt      DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'AssetMaintenance' table
CREATE TABLE energy_company.AssetMaintenance
(
  MaintenanceID   BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  AssetID         BIGINT       NOT NULL
    CONSTRAINT FK_AM_Asset FOREIGN KEY REFERENCES energy_company.Asset(AssetID),
  MaintenanceDate DATE         NOT NULL,
  Description     NVARCHAR(255) NULL,
  CostUSD         DECIMAL(18,2) NOT NULL,
  PerformedBy     INT          NULL,  -- could FK to a Staff table
  CreatedAt       DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy       SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt       DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy       SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'AssetMaintenance' table
CREATE INDEX IX_AM_AssetDate
ON energy_company.AssetMaintenance(AssetID, MaintenanceDate DESC);
```

## DML Syntax
```sql

```
