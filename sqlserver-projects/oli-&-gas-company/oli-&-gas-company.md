![SQL Server Tinitiate Image](../../sqlserver-sql/sqlserver.png)

# SQL Server Tutorial

&copy; TINITIATE.COM

# Oil & Gas Company Data Model
This model spans upstream (regions, fields, wells, drilling), midstream (pipelines and flows), and downstream/commercial (facilities, products, inventory, shipments, contracts, invoices, payments), plus cross-cutting maintenance.  
- **Region → Field → Well** form the exploration/production hierarchy.  
- **DrillingOperation** captures well activity timelines.  
- **Production** stores daily well outputs (oil, gas, water) as a partitioned time-series.  
- **Pipeline / PipelineFlow** model midstream transport and volumes (partitioned).  
- **Facility / Product / Inventory / Shipment** manage refined products and movements.  
- **Customer / SalesContract / Invoice / Payment** cover commercial agreements and cashflow (invoices are partitioned).  
- **AssetMaintenance** records O&M events across wells, pipelines, and facilities.

## Region
* **RegionID**: Surrogate key (PK).  
* **Name, Country**: Geographic grouping (e.g., Basin, State/Country).

## Field
* **FieldID**: Surrogate key (PK).  
* **RegionID**: FK → `Region(RegionID)`.  
* **Name, DiscoveryDate, Status**: Field identity and lifecycle.

## Well
* **WellID**: Surrogate key (PK).  
* **FieldID**: FK → `Field(FieldID)`.  
* **Name, WellType (Oil/Gas/Injector), SpudDate, Status**: Well metadata.

## DrillingOperation
* **OperationID**: Surrogate key (PK).  
* **WellID**: FK → `Well(WellID)`.  
* **StartDate, EndDate, RigName, Status**: Drilling timeline.  
* **IX_Drill_WellDate**: Speeds queries by well and recent start dates.

## Production (Partitioned)
* **ProductionID, ProductionDate**: Composite PK; partitioned by `ProductionDate` (e.g., `PS_OilGasYear`).  
* **WellID**: FK → `Well(WellID)`.  
* **Oil_bbl, Gas_mcf, Water_bbl**: Daily volumes.  
* **CreatedAt/By**: Audit columns.  
* **IX_Prod_WellDate**: Fast lookups by well and date.

## Pipeline
* **PipelineID**: Surrogate key (PK).  
* **Name, FromFacility, ToFacility**: Endpoint IDs (facility references).  
* **CapacityBbl**: Rated capacity.  
* **CreatedAt**: Audit column.

## PipelineFlow (Partitioned)
* **FlowID, FlowDate**: Composite PK; partitioned by `FlowDate`.  
* **PipelineID**: FK → `Pipeline(PipelineID)`.  
* **Volume_bbl**: Daily transported volume.  
* **CreatedAt**: Audit column.  
* **IX_PFlow_PipeDate**: Pipeline/date queries.

## Facility
* **FacilityID**: Surrogate key (PK).  
* **Name, FacilityType (Refinery/Terminal/Storage), Location**: Downstream nodes.  
* **CreatedAt**: Audit column.

## Product
* **ProductID**: Surrogate key (PK).  
* **Name**: Refined product (e.g., Gasoline, Diesel).  
* **APIGravity, SulfurPct**: Quality specs.

## Inventory
* **InventoryID**: Surrogate key (PK).  
* **FacilityID**: FK → `Facility(FacilityID)`.  
* **ProductID**: FK → `Product(ProductID)`.  
* **SnapshotDate, Quantity_bbl, CreatedAt**: Stock position by day.  
* **IX_Inv_FacDate**: Facility/date lookups.

## Shipment (Partitioned)
* **ShipmentID, ShipDate**: Composite PK; partitioned by `ShipDate`.  
* **FromFacility**: FK → `Facility(FacilityID)`.  
* **ToCustomer**: FK → `Customer(CustomerID)`.  
* **ProductID**: FK → `Product(ProductID)`.  
* **Volume_bbl, RatePerBbl, CreatedAt**: Movement and pricing.  
* **IX_Shp_FromDate**: Facility/date queries.

## Customer
* **CustomerID**: Surrogate key (PK).  
* **Name**: Buyer (trader, distributor, refinery).  
* **AddressID**: FK → `Address(AddressID)` if address table exists.  
* **CreatedAt**: Audit column.

## SalesContract
* **ContractID**: Surrogate key (PK).  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **ProductID**: FK → `Product(ProductID)`.  
* **StartDate, EndDate, VolumeCommit_bbl, PricePerBbl**: Commercial terms.  
* **CreatedAt**: Audit column.

## Invoice (Partitioned)
* **InvoiceID, InvoiceDate**: Composite PK; partitioned by `InvoiceDate`.  
* **CustomerID**: FK → `Customer(CustomerID)`.  
* **AmountDue, Status, CreatedAt**: Billing lifecycle.  
* **IX_Inv_Status**: Filters by status (includes `AmountDue`).

## Payment
* **PaymentID**: Surrogate key (PK).  
* **InvoiceID**: FK → `Invoice(InvoiceID)`.  
* **PaymentDate, AmountPaid, CreatedAt**: Remittance details.

## AssetMaintenance
* **MaintenanceID**: Surrogate key (PK).  
* **AssetType, AssetID**: Logical reference to the maintained asset (well/pipeline/facility).  
* **MaintDate, Description, CostUSD, CreatedAt**: Work log and cost.  
* **IX_AM_Date**: Recent maintenance by date; **IX_AM_Asset (unique)** ensures one record per asset/day.

## DDL Syntax
```sql
-- Create 'oil_n_gas_company' schema
CREATE SCHEMA oil_n_gas_company;

-- Create 'Region' table
CREATE TABLE oil_n_gas_company.Region
(
  RegionID     INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(100) NOT NULL,
  Country      NVARCHAR(50)  NOT NULL
)

-- Create 'Field' table
CREATE TABLE oil_n_gas_company.Field
(
  FieldID      INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  RegionID     INT           NOT NULL
    CONSTRAINT FK_Field_Region FOREIGN KEY REFERENCES oil_n_gas_company.Region(RegionID),
  Name         NVARCHAR(150) NOT NULL,
  DiscoveryDate DATE         NULL,
  Status       NVARCHAR(50)  NOT NULL DEFAULT 'Active'
)

-- Create 'Well' table
CREATE TABLE oil_n_gas_company.Well
(
  WellID       BIGINT        IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FieldID      INT           NOT NULL
    CONSTRAINT FK_Well_Field FOREIGN KEY REFERENCES oil_n_gas_company.Field(FieldID),
  Name         NVARCHAR(150) NOT NULL,
  WellType     NVARCHAR(50)  NULL,  -- e.g. Oil, Gas, Injector
  SpudDate     DATE          NULL,
  Status       NVARCHAR(50)  NOT NULL DEFAULT 'Drilling'
)


-- Create 'DrillingOperation' table
CREATE TABLE oil_n_gas_company.DrillingOperation
(
  OperationID      BIGINT    IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  WellID           BIGINT    NOT NULL
    CONSTRAINT FK_Drill_Well FOREIGN KEY REFERENCES oil_n_gas_company.Well(WellID),
  StartDate        DATETIME2 NOT NULL,
  EndDate          DATETIME2 NULL,
  RigName          NVARCHAR(100) NULL,
  Status           NVARCHAR(50) NOT NULL
)
-- Create an index for 'DrillingOperation' table
CREATE INDEX IX_Drill_WellDate
ON oil_n_gas_company.DrillingOperation(WellID, StartDate DESC);

-- Create 'Production' table
CREATE TABLE oil_n_gas_company.Production
(
  ProductionID     BIGINT     NOT NULL,
  WellID           BIGINT     NOT NULL
    CONSTRAINT FK_Prod_Well FOREIGN KEY REFERENCES oil_n_gas_company.Well(WellID),
  ProductionDate   DATE       NOT NULL,
  Oil_bbl          DECIMAL(18,2) NOT NULL,
  Gas_mcf          DECIMAL(18,2) NOT NULL,
  Water_bbl        DECIMAL(18,2) NOT NULL,
  CreatedAt        DATETIME2  NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy        SYSNAME    NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_Production PRIMARY KEY CLUSTERED (ProductionID, ProductionDate)
    ON PS_OilGasYear(ProductionDate)
)
-- Create an index for 'Production' table
CREATE INDEX IX_Prod_WellDate
ON oil_n_gas_company.Production(WellID, ProductionDate DESC);

-- Create 'Pipeline' table
CREATE TABLE oil_n_gas_company.Pipeline
(
  PipelineID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name          NVARCHAR(150) NOT NULL,
  FromFacility  INT           NOT NULL,
  ToFacility    INT           NOT NULL,
  CapacityBbl   DECIMAL(18,2) NOT NULL,
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)

-- Create 'PipelineFlow' table
CREATE TABLE oil_n_gas_company.PipelineFlow
(
  FlowID          BIGINT      NOT NULL,
  PipelineID      INT         NOT NULL
    CONSTRAINT FK_PFlow_Pipe FOREIGN KEY REFERENCES oil_n_gas_company.Pipeline(PipelineID),
  FlowDate        DATE        NOT NULL,
  Volume_bbl      DECIMAL(18,2) NOT NULL,
  CreatedAt       DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_PipelineFlow PRIMARY KEY CLUSTERED (FlowID, FlowDate)
    ON PS_OilGasYear(FlowDate)
)
-- Create an index for 'PipelineFlow' table
CREATE INDEX IX_PFlow_PipeDate
ON oil_n_gas_company.PipelineFlow(PipelineID, FlowDate DESC);

-- Create 'Facility' table
CREATE TABLE oil_n_gas_company.Facility
(
  FacilityID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(150) NOT NULL,
  FacilityType NVARCHAR(50)  NOT NULL,  -- e.g. Refinery, Terminal
  Location     NVARCHAR(100) NULL,
  CreatedAt    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)

-- Create 'Product' table
CREATE TABLE oil_n_gas_company.Product
(
  ProductID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(100) NOT NULL,   -- e.g. Gasoline, Diesel
  APIGravity   DECIMAL(5,2)  NULL,
  SulfurPct    DECIMAL(5,3)  NULL
)

-- Create 'Inventory' table
CREATE TABLE oil_n_gas_company.Inventory
(
  InventoryID  BIGINT        IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FacilityID   INT           NOT NULL
    CONSTRAINT FK_Inv_Facility FOREIGN KEY REFERENCES oil_n_gas_company.Facility(FacilityID),
  ProductID    INT           NOT NULL
    CONSTRAINT FK_Inv_Product FOREIGN KEY REFERENCES oil_n_gas_company.Product(ProductID),
  SnapshotDate DATE          NOT NULL,
  Quantity_bbl DECIMAL(18,2) NOT NULL,
  CreatedAt    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)
-- Create an index for 'Inventory' table
CREATE INDEX IX_Inv_FacDate
ON oil_n_gas_company.Inventory(FacilityID, SnapshotDate DESC);

-- Create 'Shipment' table
CREATE TABLE oil_n_gas_company.Shipment
(
  ShipmentID    BIGINT       NOT NULL,
  FromFacility  INT          NOT NULL
    CONSTRAINT FK_Shp_FromFac FOREIGN KEY REFERENCES oil_n_gas_company.Facility(FacilityID),
  ToCustomer    INT          NOT NULL
    CONSTRAINT FK_Shp_Cust    REFERENCES oil_n_gas_company.Customer(CustomerID),
  ProductID     INT          NOT NULL
    CONSTRAINT FK_Shp_Product FOREIGN KEY REFERENCES oil_n_gas_company.Product(ProductID),
  ShipDate      DATE         NOT NULL,
  Volume_bbl    DECIMAL(18,2)NOT NULL,
  RatePerBbl    DECIMAL(12,4)NOT NULL,
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_Shipment PRIMARY KEY CLUSTERED (ShipmentID, ShipDate)
    ON PS_OilGasYear(ShipDate)
)
-- Create an index for 'Shipment' table
CREATE INDEX IX_Shp_FromDate
ON oil_n_gas_company.Shipment(FromFacility, ShipDate DESC);

-- Create 'Customer' table
CREATE TABLE oil_n_gas_company.Customer
(
  CustomerID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(150) NOT NULL,
  AddressID    INT           NULL
    CONSTRAINT FK_Cust_Address FOREIGN KEY REFERENCES oil_n_gas_company.Address(AddressID),
  CreatedAt    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)

-- Create 'SalesContract' table
CREATE TABLE oil_n_gas_company.SalesContract
(
  ContractID   BIGINT        IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  CustomerID   INT           NOT NULL
    CONSTRAINT FK_SC_Cust FOREIGN KEY REFERENCES oil_n_gas_company.Customer(CustomerID),
  ProductID    INT           NOT NULL
    CONSTRAINT FK_SC_Product FOREIGN KEY REFERENCES oil_n_gas_company.Product(ProductID),
  StartDate    DATE          NOT NULL,
  EndDate      DATE          NULL,
  VolumeCommit_bbl DECIMAL(18,2) NULL,
  PricePerBbl  DECIMAL(12,4) NULL,
  CreatedAt    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
)

-- Create 'Invoice' table
CREATE TABLE oil_n_gas_company.Invoice
(
  InvoiceID    BIGINT       NOT NULL,
  CustomerID   INT          NOT NULL
    CONSTRAINT FK_Inv_Cust FOREIGN KEY REFERENCES oil_n_gas_company.Customer(CustomerID),
  InvoiceDate  DATE         NOT NULL,
  AmountDue    DECIMAL(18,2)NOT NULL,
  Status       NVARCHAR(20) NOT NULL DEFAULT 'Open',
  CreatedAt    DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT PK_Invoice PRIMARY KEY CLUSTERED (InvoiceID, InvoiceDate)
    ON PS_OilGasYear(InvoiceDate)
)
-- Create an index for 'Invoice' table
CREATE INDEX IX_Inv_Status
ON oil_n_gas_company.Invoice(Status)
INCLUDE (AmountDue);

-- Create 'Payment' table
CREATE TABLE oil_n_gas_company.Payment
(
  PaymentID    BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  InvoiceID    BIGINT       NOT NULL
    CONSTRAINT FK_Pmt_Inv FOREIGN KEY REFERENCES oil_n_gas_company.Invoice(InvoiceID),
  PaymentDate  DATE         NOT NULL,
  AmountPaid   DECIMAL(18,2)NOT NULL,
  CreatedAt    DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME()
)

-- Create 'AssetMaintenance' table
CREATE TABLE oil_n_gas_company.AssetMaintenance
(
  MaintenanceID BIGINT      IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  AssetType     NVARCHAR(50) NOT NULL, -- 'Well','Pipeline','Facility'
  AssetID       BIGINT       NOT NULL,
  MaintDate     DATE         NOT NULL,
  Description   NVARCHAR(255) NULL,
  CostUSD       DECIMAL(18,2) NOT NULL,
  CreatedAt     DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CONSTRAINT IX_AM_Asset UNIQUE (AssetType, AssetID, MaintDate)
)
-- Create an index for 'AssetMaintenance' table
CREATE INDEX IX_AM_Date
ON oil_n_gas_company.AssetMaintenance(MaintDate DESC);
```

## DML Syntax
```sql

```
