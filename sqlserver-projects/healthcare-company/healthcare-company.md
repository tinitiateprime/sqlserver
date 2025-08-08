![SQL Server Tinitiate Image](../../sqlserver-sql/sqlserver.png)

# SQL Server Tutorial

&copy; TINITIATE.COM

# Health Care Data Model
This model covers a clinical workflow end-to-end: patients and providers, appointments and medical records, diagnoses/procedures, medications and prescriptions, labs (orders/results), insurance (policies/claims), and payments.  
- **Patient, Address** capture demographics and contact details.  
- **Department, Provider** define the care organization and clinicians.  
- **Appointment** schedules encounters (partitioned by datetime with targeted indexes).  
- **MedicalRecord, Diagnosis, ProcedureRecord** store clinical documentation and coding.  
- **Medication, Prescription** manage medication master data and patient prescriptions.  
- **LabOrder, LabResult** track ordered tests and their outcomes.  
- **InsurancePolicy, Claim, Payment** represent coverage, billing, and remittances.  
Audit columns (`CreatedAt/By`, `UpdatedAt/By`) are included where appropriate; filtered and covering indexes optimize common access paths.

## Patient
* **PatientID**: Surrogate key (PK).  
* **FirstName, LastName, DOB, Gender**: Core demographics.  
* **Phone, Email, AddressID, EmergencyContact**: Contact & next-of-kin.  
* **CreatedAt/By, UpdatedAt/By**: Audit metadata.

## Address
* **AddressID**: Surrogate key (PK).  
* **Street, City, State, ZIP, Country**: Standard address fields.

## Department
* **DepartmentID**: Surrogate key (PK).  
* **Name, Floor, Location**: Organizational unit info.

## Provider
* **ProviderID**: Surrogate key (PK).  
* **FirstName, LastName, NPI_Number (UNIQUE), Specialty**: Clinician identity.  
* **Phone, Email**: Contact.  
* **DepartmentID**: FK → `Department(DepartmentID)`.  
* **CreatedAt/By, UpdatedAt/By**: Audit.

## Appointment (Partitioned)
* **AppointmentID, ApptDateTime**: Composite PK; partitioned on `ApptDateTime` (e.g., `PS_AppointmentYear`).  
* **PatientID**: FK → `Patient(PatientID)`.  
* **ProviderID**: FK → `Provider(ProviderID)`.  
* **ApptType, Status, Location**: Scheduling details.  
* **Created*/Updated***: Audit.  
* **IX_App_PatientDate (filtered)**: Patient + recent dates.  
* **IX_App_ProviderStatus (includes Location)**: Provider + status filtering.

## MedicalRecord
* **RecordID**: Surrogate key (PK).  
* **PatientID**: FK → `Patient(PatientID)`.  
* **RecordDate, RecordType, AuthorID**: Clinical note metadata.  
* **Created*/Updated***: Audit.  
* **IX_MR_PatientDate**: Patient chronological access.

## Diagnosis
* **DiagnosisID**: Surrogate key (PK).  
* **RecordID**: FK → `MedicalRecord(RecordID)`.  
* **ICD10Code, Description, DiagnosedDate**: Coded condition details.

## ProcedureRecord
* **ProcedureID**: Surrogate key (PK).  
* **RecordID**: FK → `MedicalRecord(RecordID)`.  
* **CPTCode, Description, ProcedureDate**: Procedure coding & timing.

## Medication
* **MedicationID**: Surrogate key (PK).  
* **Name, Form, Strength, NDC_Code**: Drug master attributes.

## Prescription
* **PrescriptionID**: Surrogate key (PK).  
* **PatientID**: FK → `Patient(PatientID)`.  
* **ProviderID**: FK → `Provider(ProviderID)`.  
* **MedicationID**: FK → `Medication(MedicationID)`.  
* **Dosage, Frequency, StartDate, EndDate, Instructions**: Prescribing details.  
* **Created*/Updated***: Audit.  
* **IX_Rx_PatientActive (filtered)**: Active prescriptions per patient.

## LabOrder
* **LabOrderID**: Surrogate key (PK).  
* **PatientID**: FK → `Patient(PatientID)`.  
* **ProviderID**: FK → `Provider(ProviderID)`.  
* **OrderDate, Status, SpecimenType**: Order metadata.  
* **Created*/Updated***: Audit.  
* **IX_LO_PatientDate**: Patient orders by date.

## LabResult
* **LabResultID**: Surrogate key (PK).  
* **LabOrderID**: FK → `LabOrder(LabOrderID)`.  
* **TestCode, TestName, ResultValue, Units, ReferenceRange, ResultDate**: Result details.  
* **IX_LR_OrderDate**: Results by order/date.

## InsurancePolicy
* **PolicyID**: Surrogate key (PK).  
* **PatientID**: FK → `Patient(PatientID)`.  
* **InsurerName, PolicyNumber, GroupNumber**: Coverage identifiers.  
* **EffectiveDate, ExpirationDate**: Validity window.  
* **Created*/Updated***: Audit.  
* **IX_IP_PatientActive (filtered)**: Quickly find current policies.

## Claim
* **ClaimID**: Surrogate key (PK).  
* **PolicyID**: FK → `InsurancePolicy(PolicyID)`.  
* **PatientID**: FK → `Patient(PatientID)`.  
* **ProviderID**: FK → `Provider(ProviderID)`.  
* **ClaimDate, TotalCharge, Status**: Billing event details.  
* **Created*/Updated***: Audit.  
* **IX_Clm_DateStatus**: Query by date/status.

## Payment
* **PaymentID**: Surrogate key (PK).  
* **ClaimID**: FK → `Claim(ClaimID)`.  
* **PaymentDate, AmountPaid, PaymentMethod, CheckReference, CreatedAt**: Remittance info.

## DDL Syntax
```sql
-- Create 'healthcare_company' schema
CREATE SCHEMA healthcare_company;

-- Create 'Patient' table
CREATE TABLE dbo.Patient
(
  PatientID         INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FirstName         NVARCHAR(50)  NOT NULL,
  LastName          NVARCHAR(50)  NOT NULL,
  DOB               DATE          NOT NULL,
  Gender            CHAR(1)       NOT NULL,
  Phone             VARCHAR(20)   NULL,
  Email             VARCHAR(100)  NULL,
  AddressID         INT           NULL,
  EmergencyContact  NVARCHAR(100) NULL,
  -- Audit
  CreatedAt         DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy         SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt         DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy         SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'Address' table
CREATE TABLE dbo.Address
(
  AddressID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Street       NVARCHAR(150) NOT NULL,
  City         NVARCHAR(50)  NOT NULL,
  State        NVARCHAR(50)  NOT NULL,
  ZIP          NVARCHAR(15)  NOT NULL,
  Country      NVARCHAR(50)  NOT NULL
)

-- Create 'Department' table
CREATE TABLE dbo.Department
(
  DepartmentID INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name         NVARCHAR(100) NOT NULL,
  Floor        INT           NULL,
  Location     NVARCHAR(100) NULL
);

-- Create 'Provider' table
CREATE TABLE dbo.Provider
(
  ProviderID    INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  FirstName     NVARCHAR(50)  NOT NULL,
  LastName      NVARCHAR(50)  NOT NULL,
  NPI_Number    VARCHAR(20)   NOT NULL UNIQUE,
  Specialty     NVARCHAR(100) NULL,
  Phone         VARCHAR(20)   NULL,
  Email         VARCHAR(100)  NULL,
  DepartmentID  INT           NOT NULL
    CONSTRAINT FK_Provider_Department FOREIGN KEY REFERENCES dbo.Department(DepartmentID),
  CreatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt     DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy     SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)

-- Create 'Appointment' table
CREATE TABLE dbo.Appointment
(
  AppointmentID  BIGINT         NOT NULL,
  PatientID      INT            NOT NULL,
  ProviderID     INT            NOT NULL,
  ApptDateTime   DATETIME2      NOT NULL,
  ApptType       NVARCHAR(50)   NULL,
  Status         NVARCHAR(20)   NULL,
  Location       NVARCHAR(100)  NULL,
  CreatedAt      DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME        NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME        NOT NULL DEFAULT SUSER_SNAME(),
  CONSTRAINT PK_Appointment PRIMARY KEY CLUSTERED (AppointmentID, ApptDateTime)
    ON PS_AppointmentYear(ApptDateTime),
  CONSTRAINT FK_Appt_Patient FOREIGN KEY (PatientID) REFERENCES dbo.Patient(PatientID),
  CONSTRAINT FK_Appt_Provider FOREIGN KEY (ProviderID) REFERENCES dbo.Provider(ProviderID)
)
-- Create an index for 'Appointment' table
CREATE INDEX IX_App_PatientDate
  ON dbo.Appointment(PatientID, ApptDateTime DESC)
  WHERE ApptDateTime >= '2023-01-01';
-- Create an index for 'Appointment' table
CREATE INDEX IX_App_ProviderStatus
  ON dbo.Appointment(ProviderID, Status)
  INCLUDE (Location);

-- Create 'MedicalRecord' table
CREATE TABLE dbo.MedicalRecord
(
  RecordID     BIGINT         IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PatientID    INT            NOT NULL
    CONSTRAINT FK_MR_Patient FOREIGN KEY REFERENCES dbo.Patient(PatientID),
  RecordDate   DATETIME2      NOT NULL,
  RecordType   NVARCHAR(50)   NULL,
  AuthorID     INT            NOT NULL,  -- could be ProviderID or StaffID
  CreatedAt    DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy    SYSNAME        NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt    DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy    SYSNAME        NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'MedicalRecord' table
CREATE INDEX IX_MR_PatientDate
  ON dbo.MedicalRecord(PatientID, RecordDate);

-- Create 'Diagnosis' table
CREATE TABLE dbo.Diagnosis
(
  DiagnosisID   BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  RecordID      BIGINT       NOT NULL
    CONSTRAINT FK_Dx_Record FOREIGN KEY REFERENCES dbo.MedicalRecord(RecordID),
  ICD10Code     VARCHAR(10)  NOT NULL,
  Description   NVARCHAR(255) NULL,
  DiagnosedDate DATE          NOT NULL
)

-- Create 'ProcedureRecord' table
CREATE TABLE dbo.ProcedureRecord
(
  ProcedureID    BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  RecordID       BIGINT       NOT NULL
    CONSTRAINT FK_Proc_Record FOREIGN KEY REFERENCES dbo.MedicalRecord(RecordID),
  CPTCode        VARCHAR(10)  NOT NULL,
  Description    NVARCHAR(255) NULL,
  ProcedureDate  DATE         NOT NULL
)

-- Create 'Medication' table
CREATE TABLE dbo.Medication
(
  MedicationID   INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  Name           NVARCHAR(150) NOT NULL,
  Form           NVARCHAR(50)  NULL,
  Strength       NVARCHAR(50)  NULL,
  NDC_Code       VARCHAR(20)   NULL
)

-- Create 'Prescription' table
CREATE TABLE dbo.Prescription
(
  PrescriptionID INT           IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PatientID      INT           NOT NULL
    CONSTRAINT FK_Rx_Patient FOREIGN KEY REFERENCES dbo.Patient(PatientID),
  ProviderID     INT           NOT NULL
    CONSTRAINT FK_Rx_Provider FOREIGN KEY REFERENCES dbo.Provider(ProviderID),
  MedicationID   INT           NOT NULL
    CONSTRAINT FK_Rx_Med       FOREIGN KEY REFERENCES dbo.Medication(MedicationID),
  Dosage         NVARCHAR(100) NULL,
  Frequency      NVARCHAR(100) NULL,
  StartDate      DATE          NOT NULL,
  EndDate        DATE          NULL,
  Instructions   NVARCHAR(500) NULL,
  CreatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME       NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'Prescription' table
CREATE INDEX IX_Rx_PatientActive
  ON dbo.Prescription(PatientID)
  WHERE EndDate IS NULL;

-- Create 'LabOrder' table
CREATE TABLE dbo.LabOrder
(
  LabOrderID   BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PatientID    INT          NOT NULL
    CONSTRAINT FK_LO_Patient FOREIGN KEY REFERENCES dbo.Patient(PatientID),
  ProviderID   INT          NOT NULL
    CONSTRAINT FK_LO_Prov    FOREIGN KEY REFERENCES dbo.Provider(ProviderID),
  OrderDate    DATETIME2    NOT NULL,
  Status       NVARCHAR(50) NULL,
  SpecimenType NVARCHAR(100)NULL,
  CreatedAt    DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy    SYSNAME      NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt    DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy    SYSNAME      NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'LabOrder' table
CREATE INDEX IX_LO_PatientDate
  ON dbo.LabOrder(PatientID, OrderDate DESC);

-- Create 'LabResult' table
CREATE TABLE dbo.LabResult
(
  LabResultID   BIGINT       IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  LabOrderID    BIGINT       NOT NULL
    CONSTRAINT FK_LR_Order   FOREIGN KEY REFERENCES dbo.LabOrder(LabOrderID),
  TestCode      VARCHAR(20)  NOT NULL,
  TestName      NVARCHAR(100)NOT NULL,
  ResultValue   DECIMAL(18,4)NULL,
  Units         NVARCHAR(50) NULL,
  ReferenceRange NVARCHAR(100) NULL,
  ResultDate    DATETIME2    NOT NULL
)
-- Create an index for 'LabResult' table
CREATE INDEX IX_LR_OrderDate
  ON dbo.LabResult(LabOrderID, ResultDate);

-- Create 'InsurancePolicy' table
CREATE TABLE dbo.InsurancePolicy
(
  PolicyID       BIGINT      IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PatientID      INT         NOT NULL
    CONSTRAINT FK_IP_Patient FOREIGN KEY REFERENCES dbo.Patient(PatientID),
  InsurerName    NVARCHAR(150)NOT NULL,
  PolicyNumber   VARCHAR(50) NOT NULL,
  GroupNumber    VARCHAR(50) NULL,
  EffectiveDate  DATE        NOT NULL,
  ExpirationDate DATE        NULL,
  CreatedAt      DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME     NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME     NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'InsurancePolicy' table
CREATE INDEX IX_IP_PatientActive
  ON dbo.InsurancePolicy(PatientID)
  WHERE ExpirationDate IS NULL OR ExpirationDate >= GETDATE();

-- Create 'Claim' table
CREATE TABLE dbo.Claim
(
  ClaimID        BIGINT      IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  PolicyID       BIGINT      NOT NULL
    CONSTRAINT FK_Clm_Policy FOREIGN KEY REFERENCES dbo.InsurancePolicy(PolicyID),
  PatientID      INT         NOT NULL
    CONSTRAINT FK_Clm_Patient FOREIGN KEY REFERENCES dbo.Patient(PatientID),
  ProviderID     INT         NOT NULL
    CONSTRAINT FK_Clm_Prov    FOREIGN KEY REFERENCES dbo.Provider(ProviderID),
  ClaimDate      DATE        NOT NULL,
  TotalCharge    DECIMAL(18,2)NOT NULL,
  Status         NVARCHAR(50) NULL,
  CreatedAt      DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME     NOT NULL DEFAULT SUSER_SNAME(),
  UpdatedAt      DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  UpdatedBy      SYSNAME     NOT NULL DEFAULT SUSER_SNAME()
)
-- Create an index for 'Claim' table
CREATE INDEX IX_Clm_DateStatus
  ON dbo.Claim(ClaimDate, Status);

-- Create 'Payment' table
CREATE TABLE dbo.Payment
(
  PaymentID      BIGINT      IDENTITY(1,1) PRIMARY KEY CLUSTERED,
  ClaimID        BIGINT      NOT NULL
    CONSTRAINT FK_Pmt_Claim  FOREIGN KEY REFERENCES dbo.Claim(ClaimID),
  PaymentDate    DATE        NOT NULL,
  AmountPaid     DECIMAL(18,2)NOT NULL,
  PaymentMethod  NVARCHAR(50) NULL,
  CheckReference VARCHAR(50) NULL,
  CreatedAt      DATETIME2   NOT NULL DEFAULT SYSUTCDATETIME(),
  CreatedBy      SYSNAME     NOT NULL DEFAULT SUSER_SNAME()
)
```

## DML Syntax
```sql

```
