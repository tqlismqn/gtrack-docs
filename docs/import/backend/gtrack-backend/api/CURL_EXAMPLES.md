# G-Track API - cURL Examples

## Notifications, Search & Companies API

All examples use placeholder values. Replace with actual values from your environment.

**Base URL:** `https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0`
**Auth Header:** `Authorization: Bearer YOUR_JWT_TOKEN`

---

## 📬 Notifications API

### 1. Get Notifications (Paginated)

```bash
# Get all notifications (default: 20 per page)
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Get only unread notifications
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications?unread_only=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Filter by category and priority
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications?category=driver&priority=urgent" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Pagination
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications?page=2&per_page=50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "current_page": 1,
  "data": [
    {
      "id": "9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a",
      "type": "document_expired",
      "category": "driver",
      "title": "Document Expired",
      "message": "Driver license for Ivan Ivanov has expired",
      "icon": "🔴",
      "notifiable_type": "App\\Models\\DriverDocument",
      "notifiable_id": "8c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f",
      "action_url": "/drivers/7b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e/documents",
      "action_text": "View Document",
      "priority": "urgent",
      "read_at": null,
      "created_at": "2025-10-27T10:30:00Z"
    }
  ],
  "total": 45,
  "per_page": 20,
  "last_page": 3
}
```

---

### 2. Get Unread Count

```bash
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications/unread-count" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "count": 5,
  "by_category": {
    "driver": 3,
    "vehicle": 0,
    "order": 0,
    "invoice": 0,
    "system": 2
  },
  "by_priority": {
    "low": 0,
    "normal": 2,
    "high": 1,
    "urgent": 2
  }
}
```

---

### 3. Mark Notification as Read

```bash
curl -X POST "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications/9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a/read" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "id": "9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a",
  "read_at": "2025-10-28T11:00:00Z"
}
```

---

### 4. Mark All Notifications as Read

```bash
curl -X POST "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications/mark-all-read" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "marked_read": 5,
  "message": "All notifications marked as read"
}
```

---

### 5. Archive Notification

```bash
curl -X DELETE "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/notifications/9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "message": "Notification archived successfully"
}
```

---

## 🔍 Global Search API

### Search Across All Entities

```bash
# Basic search
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/search?q=Ivan" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Search only drivers
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/search?q=ivan&categories[]=drivers" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"

# Search multiple categories with limit
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/search?q=mesar&categories[]=drivers&categories[]=orders&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "query": "Ivan",
  "results": {
    "drivers": [
      {
        "id": "7b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e",
        "type": "driver",
        "internal_number": "DRV-0001",
        "name": "Ivan Ivanov",
        "status": "active",
        "avatar_url": null,
        "highlight": "Ivan Ivanov",
        "url": "/drivers/7b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e"
      }
    ],
    "vehicles": [],
    "orders": [],
    "invoices": []
  },
  "total_results": 1,
  "search_time_ms": 12
}
```

---

## 🏢 Companies API (Multi-Tenant)

### 1. Get Accessible Companies

```bash
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/companies" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "data": [
    {
      "id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "name": "MESAR Transport s.r.o.",
      "slug": "mesar-transport",
      "logo_url": "https://cdn.g-track.eu/logos/mesar.png",
      "active": true,
      "role": "admin",
      "is_current": true
    }
  ],
  "current_company_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
}
```

---

### 2. Switch Active Company

```bash
curl -X POST "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/companies/switch" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "company_id": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e"
  }'
```

**Response (Success):**
```json
{
  "message": "Company switched successfully",
  "company": {
    "id": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e",
    "name": "G-Track Demo Company",
    "slug": "gtrack-demo"
  }
}
```

**Response (Error - Access Denied):**
```json
{
  "message": "You do not have access to this company",
  "error": "COMPANY_ACCESS_DENIED"
}
```

---

## 👤 User Preferences API

### 1. Get Notification Preferences

```bash
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/user/notification-preferences" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "email": {
    "document_expired": true,
    "document_expiring": true,
    "order_created": false,
    "invoice_paid": false,
    "system": false
  },
  "in_app": {
    "document_expired": true,
    "document_expiring": true,
    "order_created": true,
    "invoice_paid": true,
    "system": true
  },
  "telegram": {
    "document_expired": false,
    "document_expiring": false,
    "order_created": false,
    "invoice_paid": false,
    "system": false
  }
}
```

---

### 2. Update Notification Preferences

```bash
curl -X PUT "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/user/notification-preferences" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "email": {
      "document_expired": true,
      "document_expiring": false
    },
    "telegram": {
      "document_expired": true
    }
  }'
```

**Response:**
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "email": {
      "document_expired": true,
      "document_expiring": false,
      "order_created": false,
      "invoice_paid": false,
      "system": false
    },
    "in_app": {
      "document_expired": true,
      "document_expiring": true,
      "order_created": true,
      "invoice_paid": true,
      "system": true
    },
    "telegram": {
      "document_expired": true,
      "document_expiring": false,
      "order_created": false,
      "invoice_paid": false,
      "system": false
    }
  }
}
```

---

## 🔐 Authentication

All endpoints require a valid JWT token from Auth0.

### Getting a JWT Token

1. **Via Auth0 Dashboard:**
   - Go to Auth0 Dashboard → APIs → Test
   - Copy the generated token

2. **Via Auth0 Authentication API:**
```bash
curl -X POST "https://YOUR_AUTH0_DOMAIN/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "audience": "https://api.g-track.eu",
    "grant_type": "client_credentials"
  }'
```

### Using the Token

Include the JWT token in the `Authorization` header:

```bash
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 📊 Rate Limits

| Endpoint Group | Rate Limit |
|----------------|------------|
| Notifications  | 120 requests/minute |
| Search         | 60 requests/minute |
| Companies      | No limit |
| Company Switch | 10 requests/minute |
| User Preferences | No limit |

When rate limit is exceeded, you'll receive:
```json
{
  "message": "Too Many Attempts."
}
```
HTTP Status: `429 Too Many Requests`

---

## 🧪 Testing Endpoints

### Health Check (No Auth Required)

```bash
curl -X GET "https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/health" \
  -H "Accept: application/json"
```

Expected response:
```json
{
  "status": "ok",
  "version": "0.1.0",
  "database": "connected",
  "timestamp": "2025-10-28T12:00:00Z"
}
```

---

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- UUIDs are in standard format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- All requests must include `Accept: application/json` header
- POST/PUT requests must include `Content-Type: application/json` header
- Multi-tenancy is automatically enforced via JWT `company_id` claim
- All responses use Laravel's standard pagination format for lists
