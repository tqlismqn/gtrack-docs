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
