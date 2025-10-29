# Database Schema

## Overview

G-Track uses **PostgreSQL 16+** with the following extensions:

- **PostGIS 3.4+** - Geospatial queries (GPS coordinates, route tracking)
- **TimescaleDB 2.13+** - Time-series data (GPS tracking history)
- **pg_trgm** - Full-text search and fuzzy matching

**Key Patterns:**

- **Multi-tenancy:** Every table has `company_id` (mandatory) and `office_id` (optional)
- **UUID Primary Keys:** All tables use UUIDs for security and scalability
- **Dual Identification:** UUID (internal) + Internal Number (human-readable, e.g., DRV-0001)
- **Soft Deletes:** Most tables have `deleted_at` column for audit trail
- **JSONB Metadata:** Flexible data storage for settings, flags, and additional fields
- **Timestamps:** All tables include `created_at` and `updated_at`

---

## Core Tables

### companies (Tenants)

The root entity for multi-tenancy. Each company is a separate tenant with complete data isolation.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `name` | VARCHAR(200) | Company name |
| `country_code` | CHAR(2) | ISO 3166-1 alpha-2 (CZ, PL, DE) |
| `currency` | CHAR(3) | ISO 4217 (CZK, PLN, EUR) |
| `vat_number` | VARCHAR(50) | EU VAT ID (e.g., CZ12345678) |
| `is_vat_payer` | BOOLEAN | Whether company pays VAT |
| `tax_rate` | DECIMAL(4,2) | Default VAT rate (21.00, 23.00) |
| `default_language` | CHAR(2) | ISO 639-1 (en, cs, pl, ru, de) |
| `timezone` | VARCHAR(50) | IANA timezone (Europe/Prague) |
| `subscription_tier` | VARCHAR(20) | free, starter, professional, business, enterprise |
| `trial_ends_at` | TIMESTAMPTZ | End of free trial |
| `bank_accounts` | JSONB | Array of {iban, swift, bank_name} |
| `settings` | JSONB | Company-wide settings |

**Indexes:**

```sql
CREATE INDEX idx_companies_country ON companies(country_code);
```

---

### offices (Sub-tenants)

Companies can have multiple offices (e.g., Praha, Kladno). Used for regional divisions.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Foreign key to companies |
| `name` | VARCHAR(200) | Office name (Praha, Kladno) |
| `country_code` | CHAR(2) | Office country |
| `city` | VARCHAR(100) | Office city |
| `is_headquarters` | BOOLEAN | Main office flag |

**Indexes:**

```sql
CREATE INDEX idx_offices_company ON offices(company_id);
```

---

### users

Application users with Auth0 authentication and RBAC.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Foreign key to companies |
| `office_id` | UUID | Foreign key to offices (optional) |
| `auth0_user_id` | VARCHAR(100) | Auth0 subject ID (unique) |
| `email` | VARCHAR(255) | Unique email |
| `first_name`, `last_name` | VARCHAR(100) | User name |
| `roles` | JSONB | Array of roles: ['admin', 'hr_manager', 'dispatcher'] |
| `preferred_language` | CHAR(2) | User's language preference |
| `theme` | VARCHAR(20) | UI theme (light, dark) |
| `is_active` | BOOLEAN | Account status |
| `last_login_at` | TIMESTAMPTZ | Last login timestamp |

**Indexes:**

```sql
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth0 ON users(auth0_user_id);
```

---

## Drivers Module

### drivers

Core entity storing driver personal and employment information.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `office_id` | UUID | Office assignment (optional) |
| `internal_number` | BIGSERIAL | Auto-increment (DRV-0001, DRV-0002) |
| `first_name`, `last_name`, `middle_name` | VARCHAR | Driver name |
| `birth_date` | DATE | Date of birth |
| `citizenship` | CHAR(2) | Country code |
| `rodne_cislo` | VARCHAR(20) | Czech/Slovak birth number |
| `email` | VARCHAR(255) | Contact email |
| `phone` | VARCHAR(50) | Contact phone |
| `registration_address` | TEXT | Permanent address |
| `residence_address` | TEXT | Temporary address |
| `status` | VARCHAR(20) | active, on_leave, inactive, terminated |
| `hire_date` | DATE | Employment start |
| `fire_date` | DATE | Employment end |
| `contract_from`, `contract_to` | DATE | Contract validity |
| `contract_indefinite` | BOOLEAN | Indefinite contract flag |
| `work_location` | VARCHAR(50) | Praha, Kladno, etc. |
| `bank_country`, `bank_account` | VARCHAR | Banking details (for CZ) |
| `iban`, `swift` | VARCHAR | Banking details (for non-CZ) |
| `flags` | JSONB | {pas_souhlas, propiska_cz, etc.} |

**Indexes:**

```sql
CREATE INDEX idx_drivers_company ON drivers(company_id);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_internal_number ON drivers(internal_number);
```

---

### driver_documents

Stores metadata for 14 document types. Each driver can have multiple documents (one per type).

**Document Types (ENUM):**

```sql
CREATE TYPE document_type AS ENUM (
    'passport',
    'visa_biometrics',
    'residence_permit',
    'work_permit',
    'a1_eu',
    'a1_switzerland',
    'declaration',
    'health_insurance',
    'travel_insurance',
    'drivers_license',
    'adr_certificate',
    'tachograph_card',
    'code_95',
    'medical_examination'
);
```

**Document Status (ENUM):**

```sql
CREATE TYPE document_status AS ENUM (
    'valid',          -- >30 days until expiry (🟢)
    'warning',        -- 15-30 days (🟠)
    'expiring_soon',  -- <15 days (🟡)
    'expired',        -- Past expiry date (🔴)
    'no_data'         -- Not uploaded (⚪)
);
```

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `driver_id` | UUID | Foreign key to drivers |
| `type` | document_type | Document type |
| `number` | VARCHAR(100) | Document number |
| `country` | CHAR(2) | Issuing country |
| `valid_from`, `valid_until` | DATE | Validity period |
| `status` | document_status | Computed status |
| `days_until_expiry` | INT | Computed days left |
| `meta` | JSONB | Additional fields (categories for license, etc.) |

**Indexes:**

```sql
CREATE INDEX idx_driver_documents_driver ON driver_documents(driver_id);
CREATE INDEX idx_driver_documents_type ON driver_documents(type);
CREATE INDEX idx_driver_documents_status ON driver_documents(status);
CREATE INDEX idx_driver_documents_expiry ON driver_documents(valid_until) WHERE valid_until IS NOT NULL;
```

---

### document_files (Versioning)

Stores uploaded document files with automatic versioning. Each document can have multiple versions (latest + history).

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `document_id` | UUID | Foreign key to driver_documents |
| `filename` | VARCHAR(255) | Generated filename |
| `original_filename` | VARCHAR(255) | User's original filename |
| `mime_type` | VARCHAR(100) | File MIME type |
| `size_bytes` | BIGINT | File size |
| `storage_disk` | VARCHAR(20) | s3, local |
| `storage_path` | TEXT | Full S3 path |
| `version` | INT | Auto-increment version number |
| `is_current` | BOOLEAN | Latest version flag |
| `hash_sha256` | VARCHAR(64) | File integrity check |
| `uploaded_by` | UUID | User who uploaded |
| `uploaded_at` | TIMESTAMPTZ | Upload timestamp |

**Indexes:**

```sql
CREATE INDEX idx_document_files_document ON document_files(document_id);
CREATE INDEX idx_document_files_current ON document_files(document_id, is_current) WHERE is_current = true;
```

**S3 Bucket:**
- **Name:** `gtrack-documents-eu-central-1`
- **Region:** eu-central-1 (Frankfurt)
- **Path:** `{company_id}/{driver_id}/{document_type}/{filename}`

---

### driver_transactions (Finance)

Tracks all financial transactions for drivers: salary, fines, bonuses, damages.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `driver_id` | UUID | Foreign key to drivers |
| `order_id` | UUID | Foreign key to orders (optional) |
| `type` | VARCHAR(50) | base_salary, business_trip, bonus, fine, damage |
| `amount` | DECIMAL(10,2) | Positive or negative |
| `currency` | CHAR(3) | CZK, PLN, EUR |
| `description` | TEXT | Transaction details |
| `reference` | VARCHAR(100) | External reference number |
| `transaction_date` | DATE | When transaction occurred |
| `meta` | JSONB | Additional metadata |
| `created_by` | UUID | User who created |

**Indexes:**

```sql
CREATE INDEX idx_driver_transactions_driver ON driver_transactions(driver_id);
CREATE INDEX idx_driver_transactions_company ON driver_transactions(company_id);
CREATE INDEX idx_driver_transactions_date ON driver_transactions(transaction_date);
```

---

## Vehicles Module

### vehicles

Heavy trucks (LKV) and light vehicles (PKV).

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `office_id` | UUID | Office assignment |
| `internal_number` | VARCHAR(20) | VEH-0001, VEH-0002 |
| `type` | VARCHAR(10) | lkv (truck) or pkv (light vehicle) |
| `identifier` | VARCHAR(50) | User-friendly name |
| `make`, `model` | VARCHAR(100) | MAN, Mercedes, Scania, etc. |
| `year` | INT | Manufacturing year |
| `vin` | VARCHAR(50) | Vehicle Identification Number (unique) |
| `plate_number` | VARCHAR(20) | License plate (unique) |
| `fuel_type` | VARCHAR(20) | diesel, petrol, electric, hybrid |
| `euro_class` | VARCHAR(10) | Euro 5, Euro 6 |
| `max_weight_kg` | INT | Maximum load capacity |
| `status` | VARCHAR(20) | active, in_service, inactive, sold |
| `assignment_mode` | VARCHAR(20) | assigned, pool, unassigned (PKV only) |
| `assigned_driver_id` | UUID | For PKV assigned mode |
| `current_odometer_km` | INT | Current mileage |
| `next_service_km` | INT | Service due at this mileage |

**Indexes:**

```sql
CREATE INDEX idx_vehicles_company ON vehicles(company_id);
CREATE INDEX idx_vehicles_type ON vehicles(type);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_plate ON vehicles(plate_number);
```

---

### trailers

Trailers attached to trucks for cargo transport.

**Types:** standard, mega, frigo, van, tautliner

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `internal_number` | VARCHAR(20) | TRL-0001, TRL-0002 |
| `type` | VARCHAR(20) | Trailer type |
| `identifier` | VARCHAR(50) | User-friendly name |
| `make`, `model` | VARCHAR(100) | Manufacturer and model |
| `plate_number` | VARCHAR(20) | License plate (unique) |
| `status` | VARCHAR(20) | active, in_service, inactive |
| `has_refrigeration` | BOOLEAN | Frigo trailer flag |
| `min_temp_celsius`, `max_temp_celsius` | DECIMAL | Temperature range (if frigo) |

---

### transport_units

Combines Driver + Vehicle + Trailer into a ready-to-work unit.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `driver_id` | UUID | Driver |
| `vehicle_id` | UUID | Vehicle (LKV) |
| `trailer_id` | UUID | Trailer (optional) |
| `is_ready` | BOOLEAN | Computed readiness flag |
| `assigned_at` | TIMESTAMPTZ | When unit was formed |
| `unassigned_at` | TIMESTAMPTZ | When unit was disbanded |

**Constraint:**

```sql
UNIQUE (driver_id, vehicle_id, trailer_id, unassigned_at)
```

**Readiness Logic:**

Transport Unit is ready if:
- Driver status = 'active'
- All driver documents are 🟢 valid or 🟡 expiring_soon (no 🔴 expired or ⚪ missing)
- Vehicle status = 'active' and NOT 'in_service'
- Trailer status = 'active' and NOT 'in_service' (if trailer assigned)

---

## Driver Rating & Finance (NEW 🆕)

### driver_score_config (Rating System Configuration)

**NEW FEATURE (October 29, 2025):** Configurable driver rating system with 6 performance metrics.

Stores company-specific configuration for driver rating calculation. Each company can enable/disable metrics and assign custom weights.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `metric_name` | VARCHAR(50) | Metric identifier (document_expiration, penalties_count, etc.) |
| `weight` | DECIMAL(5,2) | Weight percentage (0.00 to 100.00) |
| `is_enabled` | BOOLEAN | Whether metric is active |
| `thresholds` | JSONB | Metric-specific thresholds (e.g., max penalties for 100 score) |
| `created_at` | TIMESTAMPTZ | Configuration creation date |
| `updated_at` | TIMESTAMPTZ | Last weight/threshold change |

**SQL Schema:**

```sql
CREATE TABLE driver_score_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,
    weight DECIMAL(5,2) NOT NULL CHECK (weight >= 0 AND weight <= 100),
    is_enabled BOOLEAN DEFAULT true,
    thresholds JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (company_id, metric_name)
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_score_config_company ON driver_score_config(company_id);
CREATE INDEX idx_driver_score_config_enabled ON driver_score_config(company_id, is_enabled) WHERE is_enabled = true;
```

**Default Metrics:**

```json
{
  "document_expiration": {"weight": 30, "thresholds": {"warning_days": 30}},
  "penalties_count": {"weight": 20, "thresholds": {"max_count": 5}},
  "penalties_amount": {"weight": 20, "thresholds": {"max_amount": 10000}},
  "profile_completeness": {"weight": 10, "thresholds": {"required_fields": 20}},
  "document_upload_timeliness": {"weight": 10, "thresholds": {"avg_days": 7}},
  "activity": {"weight": 10, "thresholds": {"min_orders_per_month": 8}}
}
```

---

### driver_score_snapshots (Rating History)

Monthly snapshots of driver ratings with detailed component breakdown. Used for historical tracking, trend analysis, and performance reports.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `driver_id` | UUID | Foreign key to drivers |
| `total_score` | DECIMAL(5,2) | Overall rating (0.00 to 100.00) |
| `rating_period` | DATE | Month/period for this snapshot (YYYY-MM-01) |
| `components` | JSONB | Detailed breakdown of all metric scores |
| `rank_percentile` | INT | Driver rank percentile (1-100) |
| `previous_score` | DECIMAL(5,2) | Previous period's score (for delta) |
| `created_at` | TIMESTAMPTZ | When snapshot was calculated |

**SQL Schema:**

```sql
CREATE TABLE driver_score_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    total_score DECIMAL(5,2) NOT NULL CHECK (total_score >= 0 AND total_score <= 100),
    rating_period DATE NOT NULL,
    components JSONB NOT NULL,
    rank_percentile INT CHECK (rank_percentile >= 1 AND rank_percentile <= 100),
    previous_score DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (driver_id, rating_period)
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_score_snapshots_driver ON driver_score_snapshots(driver_id);
CREATE INDEX idx_driver_score_snapshots_period ON driver_score_snapshots(rating_period DESC);
CREATE INDEX idx_driver_score_snapshots_score ON driver_score_snapshots(total_score DESC);
```

**Example Snapshot:**

```json
{
  "driver_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_score": 87.50,
  "rating_period": "2025-10-01",
  "components": {
    "document_expiration": {"score": 95, "weight": 30, "contribution": 28.5},
    "penalties_count": {"score": 80, "weight": 20, "contribution": 16.0},
    "penalties_amount": {"score": 90, "weight": 20, "contribution": 18.0},
    "profile_completeness": {"score": 100, "weight": 10, "contribution": 10.0},
    "document_upload_timeliness": {"score": 85, "weight": 10, "contribution": 8.5},
    "activity": {"score": 70, "weight": 10, "contribution": 7.0}
  },
  "rank_percentile": 85,
  "previous_score": 84.20
}
```

---

### driver_score_components (Metric Details)

Detailed records for individual metric calculations. Provides explainability for each component of the driver rating.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `snapshot_id` | UUID | Foreign key to driver_score_snapshots |
| `metric_name` | VARCHAR(50) | Metric identifier |
| `raw_value` | DECIMAL(10,2) | Raw metric value (e.g., 3 expired docs) |
| `normalized_score` | DECIMAL(5,2) | Normalized score (0-100) |
| `weight` | DECIMAL(5,2) | Weight used in calculation |
| `contribution` | DECIMAL(5,2) | Contribution to total score |
| `metadata` | JSONB | Additional context (e.g., which docs expired) |
| `created_at` | TIMESTAMPTZ | Calculation timestamp |

**SQL Schema:**

```sql
CREATE TABLE driver_score_components (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_id UUID NOT NULL REFERENCES driver_score_snapshots(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,
    raw_value DECIMAL(10,2),
    normalized_score DECIMAL(5,2) NOT NULL CHECK (normalized_score >= 0 AND normalized_score <= 100),
    weight DECIMAL(5,2) NOT NULL,
    contribution DECIMAL(5,2) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_score_components_snapshot ON driver_score_components(snapshot_id);
CREATE INDEX idx_driver_score_components_metric ON driver_score_components(metric_name);
```

**Example Component:**

```json
{
  "snapshot_id": "abc-123",
  "metric_name": "document_expiration",
  "raw_value": 1.0,
  "normalized_score": 95.0,
  "weight": 30.0,
  "contribution": 28.5,
  "metadata": {
    "total_documents": 14,
    "valid": 12,
    "expiring_soon": 1,
    "expired": 1,
    "details": "Medical Examination expired 5 days ago"
  }
}
```

---

### driver_finance (Financial Records)

**EXPANDED FEATURE (October 29, 2025):** Complete financial contour for driver salary, bonuses, and deductions.

Central table for all driver financial transactions. Replaces basic `driver_transactions` with full accounting capabilities.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `driver_id` | UUID | Foreign key to drivers |
| `period_id` | UUID | Foreign key to driver_finance_periods |
| `transaction_type` | VARCHAR(50) | base_salary, overtime, bonus, penalty, deduction |
| `category` | VARCHAR(50) | salary, business_trip, performance_bonus, damage_fine |
| `amount` | DECIMAL(10,2) | Transaction amount (positive or negative) |
| `currency` | CHAR(3) | CZK, PLN, EUR |
| `status` | VARCHAR(20) | pending, approved, paid, cancelled |
| `transaction_date` | DATE | When transaction occurred |
| `payment_date` | DATE | When payment was made (if paid) |
| `description` | TEXT | Transaction details |
| `reference` | VARCHAR(100) | External reference (invoice, order ID) |
| `order_id` | UUID | Related order (optional) |
| `approved_by` | UUID | User who approved |
| `approved_at` | TIMESTAMPTZ | Approval timestamp |
| `paid_by` | UUID | User who marked as paid |
| `paid_at` | TIMESTAMPTZ | Payment timestamp |
| `metadata` | JSONB | Additional context |
| `created_by` | UUID | User who created |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update |

**SQL Schema:**

```sql
CREATE TABLE driver_finance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    period_id UUID REFERENCES driver_finance_periods(id),
    transaction_type VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'CZK',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    transaction_date DATE NOT NULL,
    payment_date DATE,
    description TEXT,
    reference VARCHAR(100),
    order_id UUID,
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMPTZ,
    paid_by UUID REFERENCES users(id),
    paid_at TIMESTAMPTZ,
    metadata JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_finance_company ON driver_finance(company_id);
CREATE INDEX idx_driver_finance_driver ON driver_finance(driver_id);
CREATE INDEX idx_driver_finance_period ON driver_finance(period_id);
CREATE INDEX idx_driver_finance_status ON driver_finance(status);
CREATE INDEX idx_driver_finance_date ON driver_finance(transaction_date DESC);
CREATE INDEX idx_driver_finance_type ON driver_finance(transaction_type);
```

---

### driver_penalties (Penalty Management with Disputes)

**NEW FEATURE (October 29, 2025):** Complete penalty tracking with dispute workflow.

Separate table for managing penalties (fines, damages) with dispute resolution process. Extends driver_finance with additional penalty-specific fields.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `finance_id` | UUID | Foreign key to driver_finance |
| `driver_id` | UUID | Foreign key to drivers |
| `company_id` | UUID | Multi-tenancy |
| `penalty_type` | VARCHAR(50) | speeding, accident, damage, late_delivery, other |
| `severity` | VARCHAR(20) | minor, moderate, major, critical |
| `amount` | DECIMAL(10,2) | Penalty amount |
| `currency` | CHAR(3) | CZK, PLN, EUR |
| `incident_date` | DATE | When incident occurred |
| `location` | TEXT | Where incident occurred |
| `description` | TEXT | Detailed incident description |
| `evidence` | JSONB | Array of evidence file URLs/references |
| `status` | VARCHAR(20) | pending, accepted, disputed, resolved, cancelled |
| `dispute_reason` | TEXT | Driver's dispute explanation |
| `dispute_submitted_at` | TIMESTAMPTZ | When dispute was filed |
| `resolution` | TEXT | Final resolution notes |
| `resolved_by` | UUID | User who resolved dispute |
| `resolved_at` | TIMESTAMPTZ | Resolution timestamp |
| `metadata` | JSONB | Additional context |
| `created_by` | UUID | User who created penalty |
| `created_at` | TIMESTAMPTZ | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update |

**SQL Schema:**

```sql
CREATE TABLE driver_penalties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    finance_id UUID NOT NULL REFERENCES driver_finance(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    penalty_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'minor',
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'CZK',
    incident_date DATE NOT NULL,
    location TEXT,
    description TEXT NOT NULL,
    evidence JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    dispute_reason TEXT,
    dispute_submitted_at TIMESTAMPTZ,
    resolution TEXT,
    resolved_by UUID REFERENCES users(id),
    resolved_at TIMESTAMPTZ,
    metadata JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_penalties_company ON driver_penalties(company_id);
CREATE INDEX idx_driver_penalties_driver ON driver_penalties(driver_id);
CREATE INDEX idx_driver_penalties_finance ON driver_penalties(finance_id);
CREATE INDEX idx_driver_penalties_status ON driver_penalties(status);
CREATE INDEX idx_driver_penalties_type ON driver_penalties(penalty_type);
CREATE INDEX idx_driver_penalties_incident_date ON driver_penalties(incident_date DESC);
```

**Dispute Workflow:**

1. **Pending** → Penalty created by HR/Manager
2. **Accepted** → Driver accepts penalty (no dispute)
3. **Disputed** → Driver files dispute with reason
4. **Resolved** → Manager reviews and resolves (keep, reduce, or cancel)
5. **Cancelled** → Penalty removed entirely

---

### driver_finance_periods (Period Aggregations)

Monthly/weekly financial periods for organized reporting and payroll processing.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `driver_id` | UUID | Foreign key to drivers |
| `period_type` | VARCHAR(20) | weekly, monthly, quarterly |
| `period_start` | DATE | Period start date |
| `period_end` | DATE | Period end date |
| `status` | VARCHAR(20) | open, closed, paid |
| `total_earnings` | DECIMAL(10,2) | Sum of positive transactions |
| `total_deductions` | DECIMAL(10,2) | Sum of penalties and deductions |
| `net_amount` | DECIMAL(10,2) | Earnings - Deductions |
| `currency` | CHAR(3) | CZK, PLN, EUR |
| `closed_at` | TIMESTAMPTZ | When period was closed |
| `closed_by` | UUID | User who closed period |
| `created_at` | TIMESTAMPTZ | Period creation |
| `updated_at` | TIMESTAMPTZ | Last update |

**SQL Schema:**

```sql
CREATE TABLE driver_finance_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    period_type VARCHAR(20) NOT NULL DEFAULT 'monthly',
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    total_earnings DECIMAL(10,2) DEFAULT 0,
    total_deductions DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(10,2) DEFAULT 0,
    currency CHAR(3) NOT NULL DEFAULT 'CZK',
    closed_at TIMESTAMPTZ,
    closed_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (company_id, driver_id, period_start, period_end, period_type)
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_finance_periods_company ON driver_finance_periods(company_id);
CREATE INDEX idx_driver_finance_periods_driver ON driver_finance_periods(driver_id);
CREATE INDEX idx_driver_finance_periods_status ON driver_finance_periods(status);
CREATE INDEX idx_driver_finance_periods_dates ON driver_finance_periods(period_start DESC, period_end DESC);
```

---

### driver_finance_agg (Pre-calculated Aggregates)

Pre-calculated financial aggregates for fast reporting and dashboard queries. Denormalized table updated via triggers or scheduled jobs.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `driver_id` | UUID | Foreign key to drivers |
| `agg_type` | VARCHAR(20) | mtd, ytd, lifetime |
| `reference_date` | DATE | Date for which aggregates are calculated |
| `total_earnings` | DECIMAL(10,2) | Cumulative earnings |
| `total_deductions` | DECIMAL(10,2) | Cumulative deductions |
| `total_penalties` | DECIMAL(10,2) | Cumulative penalties |
| `penalties_count` | INT | Number of penalties |
| `avg_monthly_earnings` | DECIMAL(10,2) | Average earnings per month |
| `currency` | CHAR(3) | CZK, PLN, EUR |
| `metadata` | JSONB | Additional breakdowns |
| `calculated_at` | TIMESTAMPTZ | Last calculation timestamp |
| `created_at` | TIMESTAMPTZ | First calculation |
| `updated_at` | TIMESTAMPTZ | Last update |

**SQL Schema:**

```sql
CREATE TABLE driver_finance_agg (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    agg_type VARCHAR(20) NOT NULL,
    reference_date DATE NOT NULL,
    total_earnings DECIMAL(10,2) DEFAULT 0,
    total_deductions DECIMAL(10,2) DEFAULT 0,
    total_penalties DECIMAL(10,2) DEFAULT 0,
    penalties_count INT DEFAULT 0,
    avg_monthly_earnings DECIMAL(10,2) DEFAULT 0,
    currency CHAR(3) NOT NULL DEFAULT 'CZK',
    metadata JSONB,
    calculated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (company_id, driver_id, agg_type, reference_date)
);
```

**Indexes:**

```sql
CREATE INDEX idx_driver_finance_agg_company ON driver_finance_agg(company_id);
CREATE INDEX idx_driver_finance_agg_driver ON driver_finance_agg(driver_id);
CREATE INDEX idx_driver_finance_agg_type ON driver_finance_agg(agg_type);
CREATE INDEX idx_driver_finance_agg_date ON driver_finance_agg(reference_date DESC);
```

**Example Aggregates:**

```json
{
  "driver_id": "550e8400-e29b-41d4-a716-446655440000",
  "agg_type": "ytd",
  "reference_date": "2025-10-29",
  "total_earnings": 324500.00,
  "total_deductions": 12300.00,
  "total_penalties": 8500.00,
  "penalties_count": 5,
  "avg_monthly_earnings": 32450.00,
  "metadata": {
    "months_worked": 10,
    "highest_month": {"month": "2025-07", "amount": 45200.00},
    "lowest_month": {"month": "2025-03", "amount": 28100.00}
  }
}
```

---

## Audit & History

### audit_logs

Complete history of all changes to all entities.

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `company_id` | UUID | Multi-tenancy |
| `auditable_type` | VARCHAR(50) | Entity type (Driver, Vehicle, Order) |
| `auditable_id` | UUID | Entity ID |
| `user_id` | UUID | User who made change |
| `user_email` | VARCHAR(255) | Denormalized for history |
| `action` | VARCHAR(100) | created, updated, deleted, document.uploaded |
| `old_values` | JSONB | Previous state |
| `new_values` | JSONB | New state |
| `ip_address` | INET | Client IP |
| `user_agent` | TEXT | Browser/client info |
| `created_at` | TIMESTAMPTZ | When change occurred |

**Indexes:**

```sql
CREATE INDEX idx_audit_logs_auditable ON audit_logs(auditable_type, auditable_id);
CREATE INDEX idx_audit_logs_company ON audit_logs(company_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at DESC);
```

**Example Audit Log:**

```json
{
  "auditable_type": "Driver",
  "auditable_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_email": "admin@company.cz",
  "action": "document.uploaded",
  "old_values": {"status": "no_data"},
  "new_values": {"status": "valid", "valid_until": "2027-03-15"},
  "created_at": "2025-10-27T14:30:00Z"
}
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 14 (Database Schema)
