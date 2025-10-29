# API Specification

## Base URLs

**Production:**
```
https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0
```

**Staging (Future):**
```
https://staging.g-track.eu/api/v0
```

**Local Development:**
```
http://localhost:8000/api/v0
```

**API Version:** v0 (pre-release, breaking changes allowed)

## Authentication

**Method:** Bearer Token (JWT from Auth0)

**Header:**
```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Source:**
1. Frontend authenticates user via Auth0 (OAuth 2.0 + OpenID Connect)
2. Auth0 returns JWT token
3. Frontend includes token in all API requests
4. Backend validates JWT signature using Auth0 public key

**Token Format:**
```json
{
  "sub": "auth0|507f1f77bcf86cd799439011",
  "email": "admin@company.cz",
  "company_id": "550e8400-e29b-41d4-a716-446655440000",
  "roles": ["admin"],
  "iat": 1698765432,
  "exp": 1698851832
}
```

**Unauthenticated Request:**
```json
HTTP 401 Unauthorized
{
  "error": "Unauthorized",
  "message": "Missing or invalid token"
}
```

## Pagination

**Method 1: Cursor-based Pagination (Recommended)**

Used for large datasets with frequent updates (drivers, orders).

**Request:**
```http
GET /api/v0/drivers?limit=20&cursor=eyJpZCI6IjU1MGU4...
```

**Response:**
```json
{
  "data": [
    { "id": "uuid-1", "first_name": "Jan", ... },
    { "id": "uuid-2", "first_name": "Petr", ... }
  ],
  "meta": {
    "next_cursor": "eyJpZCI6InV1aWQtMjAifQ==",
    "has_more": true
  }
}
```

**Method 2: Offset-based Pagination**

Used for smaller, stable datasets (users, vehicles).

**Request:**
```http
GET /api/v0/drivers?page=1&per_page=20
```

**Response:**
```json
{
  "current_page": 1,
  "data": [...],
  "first_page_url": "/api/v0/drivers?page=1",
  "last_page": 15,
  "last_page_url": "/api/v0/drivers?page=15",
  "next_page_url": "/api/v0/drivers?page=2",
  "per_page": 20,
  "prev_page_url": null,
  "total": 287
}
```

## Filtering & Sorting

**Filter Parameters:**
```http
GET /api/v0/drivers?status=active&citizenship=CZ&office_id=uuid-123
```

**Sorting:**
```http
GET /api/v0/drivers?sort_by=last_name&sort_order=asc
```

**Search:**
```http
GET /api/v0/drivers?search=Jan+Novak
```

**Multiple Filters:**
```http
GET /api/v0/drivers?status=active,on_leave&document_status=expired
```

## Error Handling

**HTTP Status Codes:**

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST (new resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate entry (e.g., email) |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

**Error Response Format:**
```json
{
  "error": "ValidationError",
  "message": "The given data was invalid.",
  "errors": {
    "email": ["The email field is required."],
    "birth_date": ["The birth date must be a valid date."]
  }
}
```

**Validation Error Example:**
```json
HTTP 422 Unprocessable Entity
{
  "error": "ValidationError",
  "message": "Validation failed for driver creation",
  "errors": {
    "first_name": ["The first name field is required."],
    "email": [
      "The email field is required.",
      "The email must be a valid email address."
    ],
    "contract_from": ["The contract start date must be before end date."]
  }
}
```

**Multi-tenancy Isolation Error:**
```json
HTTP 403 Forbidden
{
  "error": "AccessDenied",
  "message": "You do not have access to this resource (belongs to another company)"
}
```

## Rate Limiting

**Limits by Subscription Tier:**

| Tier | Requests per Minute | Burst Limit |
|------|---------------------|-------------|
| Free Trial | 60 | 100 |
| Starter | 120 | 200 |
| Professional | 180 | 300 |
| Business | 240 | 400 |
| Enterprise | 300 | 500 |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1698765492
```

**Rate Limit Exceeded:**
```json
HTTP 429 Too Many Requests
{
  "error": "RateLimitExceeded",
  "message": "Too many requests. Please try again in 23 seconds.",
  "retry_after": 23
}
```

## API Endpoints - Drivers Module

### List Drivers

**Endpoint:**
```http
GET /api/v0/drivers
```

**Query Parameters:**
- `page` (int) - Page number (default: 1)
- `per_page` (int) - Results per page (default: 20, max: 100)
- `status` (string) - Filter by status: `active`, `on_leave`, `inactive`, `terminated`
- `office_id` (uuid) - Filter by office
- `citizenship` (string) - Filter by citizenship (ISO 3166-1 alpha-2)
- `document_status` (string) - Filter by document readiness: `valid`, `warning`, `expiring_soon`, `expired`, `no_data`
- `search` (string) - Search by name, email, internal_number
- `sort_by` (string) - Sort field: `internal_number`, `last_name`, `hire_date`, `created_at`
- `sort_order` (string) - `asc` or `desc`

**Response:**
```json
{
  "current_page": 1,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "internal_number": "DRV-0001",
      "first_name": "Jan",
      "last_name": "Novák",
      "email": "jan.novak@gmail.com",
      "phone": "+420 777 123 456",
      "citizenship": "CZ",
      "status": "active",
      "hire_date": "2023-05-15",
      "is_ready": true,
      "documents_summary": {
        "total": 14,
        "valid": 12,
        "warning": 1,
        "expiring_soon": 1,
        "expired": 0,
        "no_data": 0
      },
      "created_at": "2023-05-15T10:30:00Z",
      "updated_at": "2025-10-27T14:22:00Z"
    }
  ],
  "total": 287,
  "per_page": 20,
  "last_page": 15
}
```

### Get Single Driver

**Endpoint:**
```http
GET /api/v0/drivers/{id}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "company_id": "c7e8f9a0-1234-5678-9abc-def012345678",
  "office_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "internal_number": "DRV-0001",
  "first_name": "Jan",
  "last_name": "Novák",
  "middle_name": null,
  "birth_date": "1985-03-20",
  "citizenship": "CZ",
  "rodne_cislo": "850320/1234",
  "email": "jan.novak@gmail.com",
  "phone": "+420 777 123 456",
  "registration_address": "Vinohradská 123, 130 00 Praha 3",
  "residence_address": "Vinohradská 123, 130 00 Praha 3",
  "status": "active",
  "hire_date": "2023-05-15",
  "fire_date": null,
  "contract_from": "2023-05-15",
  "contract_to": null,
  "contract_indefinite": true,
  "work_location": "Praha",
  "bank_country": "CZ",
  "bank_account": "123456789/0800",
  "iban": null,
  "swift": null,
  "flags": {
    "pas_souhlas": true,
    "propiska_cz": true
  },
  "is_ready": true,
  "documents": [...],
  "created_at": "2023-05-15T10:30:00Z",
  "updated_at": "2025-10-27T14:22:00Z"
}
```

### Create Driver

**Endpoint:**
```http
POST /api/v0/drivers
```

**Request Body:**
```json
{
  "first_name": "Petr",
  "last_name": "Dvořák",
  "birth_date": "1990-07-12",
  "citizenship": "CZ",
  "rodne_cislo": "900712/3456",
  "email": "petr.dvorak@gmail.com",
  "phone": "+420 777 654 321",
  "registration_address": "Karlova 45, 110 00 Praha 1",
  "status": "active",
  "hire_date": "2025-11-01",
  "contract_from": "2025-11-01",
  "contract_indefinite": true,
  "work_location": "Praha",
  "bank_country": "CZ",
  "bank_account": "987654321/0800",
  "flags": {
    "pas_souhlas": true,
    "propiska_cz": false
  }
}
```

**Response:**
```json
HTTP 201 Created
{
  "id": "7f9a8b6c-5d4e-3f2a-1b0c-9d8e7f6a5b4c",
  "internal_number": "DRV-0288",
  "first_name": "Petr",
  "last_name": "Dvořák",
  ...
  "created_at": "2025-10-29T16:45:00Z"
}
```

### Update Driver

**Endpoint:**
```http
PUT /api/v0/drivers/{id}
```

**Request Body:**
```json
{
  "status": "on_leave",
  "phone": "+420 777 999 888",
  "residence_address": "Nová adresa 123, 160 00 Praha 6"
}
```

**Response:**
```json
HTTP 200 OK
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "internal_number": "DRV-0001",
  "status": "on_leave",
  "phone": "+420 777 999 888",
  "residence_address": "Nová adresa 123, 160 00 Praha 6",
  ...
  "updated_at": "2025-10-29T16:50:00Z"
}
```

### Delete Driver (Soft Delete)

**Endpoint:**
```http
DELETE /api/v0/drivers/{id}
```

**Response:**
```json
HTTP 204 No Content
```

## Documents API

### List Driver Documents

**Endpoint:**
```http
GET /api/v0/drivers/{driver_id}/documents
```

**Response:**
```json
{
  "data": [
    {
      "id": "doc-uuid-1",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "type": "passport",
      "number": "123456789",
      "country": "CZ",
      "valid_from": "2020-05-15",
      "valid_until": "2030-05-14",
      "status": "valid",
      "days_until_expiry": 1658,
      "files": [
        {
          "id": "file-uuid-1",
          "filename": "passport_jan_novak_v2.pdf",
          "version": 2,
          "is_current": true,
          "uploaded_at": "2025-10-27T14:30:00Z"
        }
      ]
    }
  ]
}
```

### Upload Document File

**Endpoint:**
```http
POST /api/v0/documents/{document_id}/files
```

**Request:**
```http
Content-Type: multipart/form-data

file: [binary data]
```

**Response:**
```json
HTTP 201 Created
{
  "id": "file-uuid-2",
  "document_id": "doc-uuid-1",
  "filename": "passport_jan_novak_v3.pdf",
  "original_filename": "scan_2025_10_29.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1048576,
  "version": 3,
  "is_current": true,
  "storage_path": "550e8400.../passport/passport_jan_novak_v3.pdf",
  "uploaded_by": "user-uuid",
  "uploaded_at": "2025-10-29T17:00:00Z"
}
```

### Download Document File

**Endpoint:**
```http
GET /api/v0/files/{file_id}/download
```

**Response:**
```http
HTTP 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="passport_jan_novak_v3.pdf"

[binary PDF data]
```

### List File Versions

**Endpoint:**
```http
GET /api/v0/documents/{document_id}/files/versions
```

**Response:**
```json
{
  "data": [
    {
      "id": "file-uuid-3",
      "version": 3,
      "is_current": true,
      "filename": "passport_jan_novak_v3.pdf",
      "size_bytes": 1048576,
      "uploaded_by": "Jan Admin",
      "uploaded_at": "2025-10-29T17:00:00Z"
    },
    {
      "id": "file-uuid-2",
      "version": 2,
      "is_current": false,
      "filename": "passport_jan_novak_v2.pdf",
      "size_bytes": 987654,
      "uploaded_by": "Petr Manager",
      "uploaded_at": "2024-06-15T10:30:00Z"
    }
  ]
}
```

## Driver Rating API (NEW 🆕)

### Get Current Driver Rating

**NEW FEATURE (October 29, 2025):** Retrieve driver's current performance rating with detailed component breakdown.

**Endpoint:**
```http
GET /api/v0/drivers/{id}/rating
```

**Query Parameters:**
- `period` (string) - Optional rating period (YYYY-MM, default: current month)

**Response:**
```json
HTTP 200 OK
{
  "driver_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_score": 87.50,
  "rating_period": "2025-10",
  "rank_percentile": 85,
  "previous_score": 84.20,
  "score_change": 3.30,
  "components": {
    "document_expiration": {
      "score": 95,
      "weight": 30,
      "contribution": 28.5,
      "details": "12/14 documents valid, 1 expiring soon, 1 expired"
    },
    "penalties_count": {
      "score": 80,
      "weight": 20,
      "contribution": 16.0,
      "details": "2 penalties this period (threshold: 5)"
    },
    "penalties_amount": {
      "score": 90,
      "weight": 20,
      "contribution": 18.0,
      "details": "3,500 CZK in penalties (threshold: 10,000 CZK)"
    },
    "profile_completeness": {
      "score": 100,
      "weight": 10,
      "contribution": 10.0,
      "details": "All required fields filled (20/20)"
    },
    "document_upload_timeliness": {
      "score": 85,
      "weight": 10,
      "contribution": 8.5,
      "details": "Average 5 days upload time (threshold: 7 days)"
    },
    "activity": {
      "score": 70,
      "weight": 10,
      "contribution": 7.0,
      "details": "6 orders completed (threshold: 8 orders/month)"
    }
  },
  "calculated_at": "2025-10-29T18:00:00Z"
}
```

---

### Get Driver Rating History

**Endpoint:**
```http
GET /api/v0/drivers/{id}/rating/history
```

**Query Parameters:**
- `from` (date) - Start date (YYYY-MM-DD, default: 6 months ago)
- `to` (date) - End date (YYYY-MM-DD, default: today)
- `per_page` (int) - Results per page (default: 12, max: 24)

**Response:**
```json
HTTP 200 OK
{
  "data": [
    {
      "rating_period": "2025-10",
      "total_score": 87.50,
      "rank_percentile": 85,
      "score_change": 3.30
    },
    {
      "rating_period": "2025-09",
      "total_score": 84.20,
      "rank_percentile": 78,
      "score_change": -2.10
    }
  ],
  "summary": {
    "highest_score": 89.50,
    "highest_period": "2025-07",
    "lowest_score": 72.80,
    "lowest_period": "2025-03",
    "average_score": 83.45,
    "trend": "improving"
  }
}
```

---

### Update Rating Configuration

**Endpoint:**
```http
PUT /api/v0/companies/{company_id}/rating-config
```

**Permissions:** Admin, HR Manager

**Request Body:**
```json
{
  "metrics": [
    {
      "metric_name": "document_expiration",
      "weight": 35,
      "is_enabled": true,
      "thresholds": {
        "warning_days": 30
      }
    },
    {
      "metric_name": "penalties_count",
      "weight": 15,
      "is_enabled": true,
      "thresholds": {
        "max_count": 3
      }
    }
  ]
}
```

**Response:**
```json
HTTP 200 OK
{
  "message": "Rating configuration updated successfully",
  "updated_metrics": 6,
  "total_weight": 100
}
```

**Validation:**
- Sum of all weights must equal 100
- All weights must be between 0 and 100
- At least 3 metrics must be enabled

---

### Trigger Rating Recalculation

**Endpoint:**
```http
POST /api/v0/drivers/{id}/rating/calculate
```

**Permissions:** Admin, HR Manager

**Request Body:**
```json
{
  "period": "2025-10"
}
```

**Response:**
```json
HTTP 200 OK
{
  "message": "Rating calculated successfully",
  "snapshot_id": "snapshot-uuid",
  "total_score": 87.50,
  "calculated_at": "2025-10-29T18:30:00Z"
}
```

---

## Finance Tracking API (NEW 🆕)

### List Driver Financial Transactions

**EXPANDED FEATURE (October 29, 2025):** Complete financial contour with full CRUD operations.

**Endpoint:**
```http
GET /api/v0/drivers/{id}/finance
```

**Query Parameters:**
- `page` (int) - Page number (default: 1)
- `per_page` (int) - Results per page (default: 20, max: 100)
- `type` (string) - Filter by transaction type
- `status` (string) - Filter by status: `pending`, `approved`, `paid`, `cancelled`
- `from_date` (date) - Start date (YYYY-MM-DD)
- `to_date` (date) - End date (YYYY-MM-DD)
- `period_id` (uuid) - Filter by specific period

**Response:**
```json
HTTP 200 OK
{
  "current_page": 1,
  "data": [
    {
      "id": "fin-uuid-1",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "transaction_type": "base_salary",
      "category": "salary",
      "amount": 45000.00,
      "currency": "CZK",
      "status": "paid",
      "transaction_date": "2025-10-01",
      "payment_date": "2025-10-15",
      "description": "October 2025 base salary",
      "reference": "SAL-2025-10-001",
      "approved_by": "Jan Admin",
      "paid_by": "Petr Accountant",
      "created_at": "2025-10-01T08:00:00Z"
    },
    {
      "id": "fin-uuid-2",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "transaction_type": "penalty",
      "category": "damage_fine",
      "amount": -3500.00,
      "currency": "CZK",
      "status": "disputed",
      "transaction_date": "2025-10-12",
      "description": "Trailer damage at loading dock",
      "reference": "PEN-2025-10-042",
      "created_at": "2025-10-12T14:30:00Z"
    }
  ],
  "summary": {
    "total_earnings": 75000.00,
    "total_deductions": 8500.00,
    "total_penalties": 3500.00,
    "net_amount": 66500.00,
    "currency": "CZK"
  },
  "total": 45,
  "per_page": 20,
  "last_page": 3
}
```

---

### Create Financial Transaction

**Endpoint:**
```http
POST /api/v0/drivers/{id}/finance
```

**Permissions:** Admin, HR Manager, Accountant

**Request Body:**
```json
{
  "transaction_type": "bonus",
  "category": "performance_bonus",
  "amount": 5000.00,
  "currency": "CZK",
  "transaction_date": "2025-10-29",
  "description": "Outstanding performance bonus for Q3 2025",
  "reference": "BONUS-Q3-2025",
  "metadata": {
    "reason": "Perfect documents, zero penalties, 12 orders completed"
  }
}
```

**Response:**
```json
HTTP 201 Created
{
  "id": "fin-uuid-3",
  "driver_id": "550e8400-e29b-41d4-a716-446655440000",
  "transaction_type": "bonus",
  "category": "performance_bonus",
  "amount": 5000.00,
  "currency": "CZK",
  "status": "pending",
  "transaction_date": "2025-10-29",
  "description": "Outstanding performance bonus for Q3 2025",
  "reference": "BONUS-Q3-2025",
  "created_by": "Jan Admin",
  "created_at": "2025-10-29T18:45:00Z"
}
```

---

### Update Financial Transaction

**Endpoint:**
```http
PUT /api/v0/drivers/{id}/finance/{transaction_id}
```

**Permissions:** Admin, HR Manager, Accountant

**Request Body:**
```json
{
  "status": "approved",
  "payment_date": "2025-11-01",
  "description": "Approved - Outstanding Q3 performance"
}
```

**Response:**
```json
HTTP 200 OK
{
  "id": "fin-uuid-3",
  "status": "approved",
  "payment_date": "2025-11-01",
  "approved_by": "Petr Manager",
  "approved_at": "2025-10-29T19:00:00Z",
  "updated_at": "2025-10-29T19:00:00Z"
}
```

---

### Delete Financial Transaction

**Endpoint:**
```http
DELETE /api/v0/drivers/{id}/finance/{transaction_id}
```

**Permissions:** Admin, HR Manager

**Restrictions:**
- Cannot delete transactions with status `paid`
- Cannot delete transactions older than 90 days

**Response:**
```json
HTTP 204 No Content
```

---

### List Driver Penalties

**Endpoint:**
```http
GET /api/v0/drivers/{id}/penalties
```

**Query Parameters:**
- `page` (int) - Page number (default: 1)
- `per_page` (int) - Results per page (default: 20, max: 100)
- `type` (string) - Filter by penalty type
- `status` (string) - Filter by status: `pending`, `accepted`, `disputed`, `resolved`, `cancelled`
- `severity` (string) - Filter by severity: `minor`, `moderate`, `major`, `critical`

**Response:**
```json
HTTP 200 OK
{
  "current_page": 1,
  "data": [
    {
      "id": "pen-uuid-1",
      "finance_id": "fin-uuid-2",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "penalty_type": "damage",
      "severity": "moderate",
      "amount": 3500.00,
      "currency": "CZK",
      "incident_date": "2025-10-12",
      "location": "Praha - Loading Dock ABC",
      "description": "Trailer damage during backing maneuver",
      "status": "disputed",
      "dispute_reason": "Dock was poorly lit, no guidance provided by staff",
      "dispute_submitted_at": "2025-10-13T08:30:00Z",
      "created_at": "2025-10-12T14:30:00Z"
    }
  ],
  "summary": {
    "total_penalties": 8500.00,
    "pending_count": 1,
    "disputed_count": 1,
    "resolved_count": 3
  },
  "total": 5,
  "per_page": 20,
  "last_page": 1
}
```

---

### Create Penalty

**Endpoint:**
```http
POST /api/v0/drivers/{id}/penalties
```

**Permissions:** Admin, HR Manager

**Request Body:**
```json
{
  "penalty_type": "speeding",
  "severity": "minor",
  "amount": 2000.00,
  "currency": "CZK",
  "incident_date": "2025-10-28",
  "location": "D1 highway, km 42",
  "description": "Speeding violation: 95 km/h in 80 km/h zone",
  "evidence": [
    {"type": "photo", "url": "s3://bucket/evidence/speeding_001.jpg"},
    {"type": "police_report", "url": "s3://bucket/evidence/report_001.pdf"}
  ]
}
```

**Response:**
```json
HTTP 201 Created
{
  "id": "pen-uuid-2",
  "finance_id": "fin-uuid-4",
  "driver_id": "550e8400-e29b-41d4-a716-446655440000",
  "penalty_type": "speeding",
  "severity": "minor",
  "amount": 2000.00,
  "currency": "CZK",
  "status": "pending",
  "incident_date": "2025-10-28",
  "location": "D1 highway, km 42",
  "created_by": "Jan Admin",
  "created_at": "2025-10-29T19:15:00Z"
}
```

---

### File Penalty Dispute

**Endpoint:**
```http
PUT /api/v0/drivers/{id}/penalties/{penalty_id}/dispute
```

**Permissions:** Driver (self), Admin, HR Manager

**Request Body:**
```json
{
  "dispute_reason": "The speed camera was malfunctioning according to reports. I was driving at 82 km/h, not 95 km/h.",
  "evidence": [
    {"type": "dashboard_camera", "url": "s3://bucket/evidence/dashcam_20251028.mp4"}
  ]
}
```

**Response:**
```json
HTTP 200 OK
{
  "id": "pen-uuid-2",
  "status": "disputed",
  "dispute_reason": "The speed camera was malfunctioning...",
  "dispute_submitted_at": "2025-10-29T19:30:00Z",
  "message": "Dispute filed successfully. HR Manager will review within 5 business days."
}
```

---

### Resolve Penalty Dispute

**Endpoint:**
```http
PUT /api/v0/drivers/{id}/penalties/{penalty_id}/resolve
```

**Permissions:** Admin, HR Manager

**Request Body:**
```json
{
  "resolution_action": "reduce",
  "new_amount": 1000.00,
  "resolution": "After reviewing dashcam footage, speed was 87 km/h, not 95 km/h. Reduced penalty to 1,000 CZK."
}
```

**Resolution Actions:**
- `keep` - Keep original penalty amount
- `reduce` - Reduce penalty amount (requires `new_amount`)
- `cancel` - Cancel penalty entirely

**Response:**
```json
HTTP 200 OK
{
  "id": "pen-uuid-2",
  "status": "resolved",
  "amount": 1000.00,
  "resolution": "After reviewing dashcam footage...",
  "resolved_by": "Petr Manager",
  "resolved_at": "2025-10-30T10:00:00Z"
}
```

---

### Get Financial Periods

**Endpoint:**
```http
GET /api/v0/drivers/{id}/finance/periods
```

**Query Parameters:**
- `period_type` (string) - Filter by type: `weekly`, `monthly`, `quarterly`
- `status` (string) - Filter by status: `open`, `closed`, `paid`
- `year` (int) - Filter by year (e.g., 2025)

**Response:**
```json
HTTP 200 OK
{
  "data": [
    {
      "id": "period-uuid-1",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "period_type": "monthly",
      "period_start": "2025-10-01",
      "period_end": "2025-10-31",
      "status": "open",
      "total_earnings": 75000.00,
      "total_deductions": 8500.00,
      "net_amount": 66500.00,
      "currency": "CZK",
      "transactions_count": 15
    },
    {
      "id": "period-uuid-2",
      "driver_id": "550e8400-e29b-41d4-a716-446655440000",
      "period_type": "monthly",
      "period_start": "2025-09-01",
      "period_end": "2025-09-30",
      "status": "paid",
      "total_earnings": 68000.00,
      "total_deductions": 5200.00,
      "net_amount": 62800.00,
      "currency": "CZK",
      "closed_at": "2025-10-01T08:00:00Z",
      "paid_at": "2025-10-15T14:00:00Z"
    }
  ]
}
```

---

### Get Financial Aggregates

**Endpoint:**
```http
GET /api/v0/drivers/{id}/finance/aggregates
```

**Query Parameters:**
- `type` (string) - Aggregate type: `mtd`, `ytd`, `lifetime` (default: all)
- `reference_date` (date) - Reference date for calculation (default: today)

**Response:**
```json
HTTP 200 OK
{
  "mtd": {
    "agg_type": "mtd",
    "reference_date": "2025-10-29",
    "total_earnings": 75000.00,
    "total_deductions": 8500.00,
    "total_penalties": 3500.00,
    "penalties_count": 2,
    "avg_monthly_earnings": 75000.00,
    "currency": "CZK"
  },
  "ytd": {
    "agg_type": "ytd",
    "reference_date": "2025-10-29",
    "total_earnings": 724500.00,
    "total_deductions": 62300.00,
    "total_penalties": 28500.00,
    "penalties_count": 12,
    "avg_monthly_earnings": 72450.00,
    "currency": "CZK",
    "metadata": {
      "months_worked": 10,
      "highest_month": {"month": "2025-07", "amount": 85200.00},
      "lowest_month": {"month": "2025-03", "amount": 58100.00}
    }
  },
  "lifetime": {
    "agg_type": "lifetime",
    "reference_date": "2025-10-29",
    "total_earnings": 1824500.00,
    "total_deductions": 142300.00,
    "total_penalties": 78500.00,
    "penalties_count": 28,
    "avg_monthly_earnings": 68721.00,
    "currency": "CZK",
    "metadata": {
      "employment_months": 28,
      "first_transaction": "2023-05-15"
    }
  }
}
```

---

## Future Integrations

**Phase 2 (Q1-Q2 2026):**
- `/api/v0/orders` - Order management endpoints
- `/api/v0/customers` - Customer management endpoints
- `/api/v0/invoices` - Invoice generation and tracking

**Phase 3 (Q2-Q3 2026):**
- `/api/v0/gps/positions` - Real-time GPS tracking
- `/api/v0/analytics/reports` - Financial and operational reports
- WebSocket endpoints via Laravel Reverb for live updates

**Phase 4 (Q3-Q4 2026):**
- `/api/v0/mobile` - Mobile app API endpoints
- `/api/v0/integrations` - Third-party integrations (accounting systems, fuel cards)

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 15 (API Specification)
