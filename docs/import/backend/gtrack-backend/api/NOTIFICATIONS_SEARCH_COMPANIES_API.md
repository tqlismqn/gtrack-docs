# G-Track API Documentation
## Notifications, Global Search & Company Management

**Version:** 0.1.0
**Base URL:** `https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0`
**Authentication:** JWT Bearer Token (Auth0)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Rate Limiting](#rate-limiting)
3. [Notifications API](#notifications-api)
4. [Global Search API](#global-search-api)
5. [Companies API](#companies-api)
6. [User Preferences API](#user-preferences-api)
7. [Error Responses](#error-responses)
8. [WebSocket Events (Future)](#websocket-events-future)

---

## Authentication

All endpoints (except `/health`) require a valid JWT token from Auth0.

### Request Header

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### JWT Claims

The JWT token must include:
- `sub` - Auth0 user ID
- `company_id` - Active company UUID (for multi-tenancy)
- `aud` - Audience: `https://api.g-track.eu`
- `iss` - Issuer: Auth0 domain

### Token Expiration

- Access tokens expire after **24 hours**
- Frontend should refresh tokens before expiration
- Expired tokens return `401 Unauthorized`

---

## Rate Limiting

| Endpoint Group | Rate Limit | HTTP Status on Exceed |
|----------------|------------|----------------------|
| Notifications  | 120 requests/min | 429 Too Many Requests |
| Search         | 60 requests/min | 429 Too Many Requests |
| Company Switch | 10 requests/min | 429 Too Many Requests |
| Other endpoints | No limit | - |

**Rate limit headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
Retry-After: 23
```

---

## Notifications API

### Overview

User notifications for document expirations, order updates, system events, etc.

**Base Path:** `/api/v0/notifications`

---

### 1. Get Notifications

**Endpoint:** `GET /notifications`

**Description:** Retrieve paginated list of user's notifications

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number |
| `per_page` | integer | No | 20 | Items per page (max: 100) |
| `unread_only` | boolean | No | false | Filter unread only |
| `category` | string | No | - | Filter by category: `driver`, `vehicle`, `order`, `invoice`, `system` |
| `priority` | string | No | - | Filter by priority: `low`, `normal`, `high`, `urgent` |

**Example Request:**

```http
GET /api/v0/notifications?unread_only=true&category=driver&priority=urgent
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

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

**Notification Types:**

| Type | Category | Priority | Description |
|------|----------|----------|-------------|
| `document_expired` | driver | urgent | Document has expired |
| `document_expiring_urgent` | driver | high | Document expires in ≤15 days |
| `document_expiring_soon` | driver | normal | Document expires in ≤30 days |
| `document_uploaded` | driver | low | New document uploaded |
| `order_created` | order | normal | New order created |
| `order_assigned` | order | normal | Order assigned to driver |
| `invoice_paid` | invoice | normal | Invoice paid |
| `system_login_new_device` | system | high | Login from new device |

---

### 2. Get Unread Count

**Endpoint:** `GET /notifications/unread-count`

**Description:** Get count of unread notifications grouped by category and priority

**Example Request:**

```http
GET /api/v0/notifications/unread-count
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

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

**Use Case:** Display notification badge count in frontend header

---

### 3. Mark Notification as Read

**Endpoint:** `POST /notifications/{id}/read`

**Description:** Mark a specific notification as read

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Notification ID |

**Example Request:**

```http
POST /api/v0/notifications/9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a/read
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

```json
{
  "id": "9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a",
  "read_at": "2025-10-28T11:00:00Z"
}
```

**Idempotent:** Calling multiple times on already-read notification returns same result

---

### 4. Mark All Notifications as Read

**Endpoint:** `POST /notifications/mark-all-read`

**Description:** Mark all user's notifications as read

**Example Request:**

```http
POST /api/v0/notifications/mark-all-read
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

```json
{
  "marked_read": 5,
  "message": "All notifications marked as read"
}
```

---

### 5. Archive Notification

**Endpoint:** `DELETE /notifications/{id}`

**Description:** Archive a notification (soft delete)

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Notification ID |

**Example Request:**

```http
DELETE /api/v0/notifications/9d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

```json
{
  "message": "Notification archived successfully"
}
```

**Note:** Archived notifications are soft-deleted (can be restored by admin if needed)

---

## Global Search API

### Overview

Full-text search across all entities (drivers, vehicles, orders, invoices).

**Base Path:** `/api/v0/search`

**Search Algorithm:**
- PostgreSQL `ILIKE` (case-insensitive)
- Future: Full-text search with `tsvector` and GIN indexes
- Searches: names, internal numbers, license plates, order numbers, invoice numbers

---

### Global Search

**Endpoint:** `GET /search`

**Description:** Search across all entities with relevance ranking

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | - | Search query (min: 2 chars, max: 255) |
| `categories` | array | No | all | Categories to search: `drivers`, `vehicles`, `orders`, `invoices` |
| `limit` | integer | No | 5 | Max results per category (1-20) |

**Example Request:**

```http
GET /api/v0/search?q=Ivan&categories[]=drivers&categories[]=orders&limit=10
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

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

**Search Fields by Entity:**

| Entity | Searchable Fields |
|--------|------------------|
| Drivers | first_name, last_name, middle_name, email, phone, internal_number |
| Vehicles | license_plate, internal_number, model, vin (future) |
| Orders | order_number, internal_number, customer_name, loading_city (future) |
| Invoices | invoice_number, internal_number, customer_name (future) |

**Performance:**
- Average response time: 10-30ms
- Optimized with database indexes
- Multi-tenancy automatically scoped (only searches current company's data)

---

## Companies API

### Overview

Multi-tenant company management. Users can be members of multiple companies.

**Base Path:** `/api/v0/companies`

---

### 1. Get Accessible Companies

**Endpoint:** `GET /companies`

**Description:** Retrieve list of companies accessible by current user

**Example Request:**

```http
GET /api/v0/companies
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

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
    },
    {
      "id": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e",
      "name": "G-Track Demo Company",
      "slug": "gtrack-demo",
      "logo_url": null,
      "active": true,
      "role": "hr_manager",
      "is_current": false
    }
  ],
  "current_company_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
}
```

**User Roles:**
- `admin` - Full system access
- `hr_manager` - Drivers, documents, comments
- `accountant` - Invoices, payments, financial reports
- `dispatcher` - Orders, transport units, assignments
- `driver` - Self-service (own profile)

---

### 2. Switch Active Company

**Endpoint:** `POST /companies/switch`

**Description:** Switch user's active company context (generates new JWT token)

**Request Body:**

```json
{
  "company_id": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e"
}
```

**Example Request:**

```http
POST /api/v0/companies/switch
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "company_id": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e"
}
```

**Response:** `200 OK`

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

**Future Enhancement:** Return new JWT token with updated `company_id` claim

**Error Responses:**

- `403 Forbidden` - User doesn't have access to company
- `403 Forbidden` - Company is not active
- `404 Not Found` - Company not found

**Security:**
- User can only switch to companies they have access to
- Company membership verified via database
- Rate limited to 10 requests/minute (prevents abuse)

---

## User Preferences API

### Overview

Manage user settings and notification preferences.

**Base Path:** `/api/v0/user`

---

### 1. Get Notification Preferences

**Endpoint:** `GET /user/notification-preferences`

**Description:** Retrieve user's notification preferences for all channels

**Example Request:**

```http
GET /api/v0/user/notification-preferences
Authorization: Bearer YOUR_TOKEN
```

**Response:** `200 OK`

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

**Notification Channels:**
- `email` - Email notifications
- `in_app` - In-app notifications (shown in frontend)
- `telegram` - Telegram bot notifications (future)

**Default Preferences:**
- Email: Only critical (document expired/expiring)
- In-app: All notifications enabled
- Telegram: All disabled (opt-in)

---

### 2. Update Notification Preferences

**Endpoint:** `PUT /user/notification-preferences`

**Description:** Update user's notification preferences (partial update)

**Request Body:**

```json
{
  "email": {
    "document_expired": true,
    "document_expiring": false
  },
  "telegram": {
    "document_expired": true
  }
}
```

**Example Request:**

```http
PUT /api/v0/user/notification-preferences
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "email": {
    "document_expired": true,
    "document_expiring": false
  }
}
```

**Response:** `200 OK`

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
      "document_expired": false,
      "document_expiring": false,
      "order_created": false,
      "invoice_paid": false,
      "system": false
    }
  }
}
```

**Merge Behavior:**
- Only provided fields are updated
- Other preferences remain unchanged
- Missing channels are not modified

---

## Error Responses

### Standard Error Format

All error responses follow this format:

```json
{
  "message": "Human-readable error message",
  "error": "ERROR_CODE",
  "errors": {
    "field_name": ["Validation error message"]
  }
}
```

### Common HTTP Status Codes

| Code | Description | Example |
|------|-------------|---------|
| `200` | Success | Resource retrieved/updated |
| `201` | Created | Resource created |
| `400` | Bad Request | Invalid request format |
| `401` | Unauthorized | Missing/invalid JWT token |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `422` | Unprocessable Entity | Validation failed |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server error |

### Example Error Responses

**401 Unauthorized:**
```json
{
  "message": "Unauthenticated"
}
```

**403 Forbidden:**
```json
{
  "message": "You do not have access to this company",
  "error": "COMPANY_ACCESS_DENIED"
}
```

**422 Validation Error:**
```json
{
  "message": "Validation failed",
  "errors": {
    "q": ["The q field must be at least 2 characters."],
    "limit": ["The limit field must not be greater than 20."]
  }
}
```

**429 Rate Limit:**
```json
{
  "message": "Too Many Attempts."
}
```

---

## WebSocket Events (Future)

**Phase 2 Feature:** Real-time notifications via Laravel Reverb (WebSockets)

### Planned Implementation

**Channel:** `private-user.{user_id}`

**Events:**
- `NotificationCreated` - New notification created
- `NotificationRead` - Notification marked as read
- `NotificationArchived` - Notification archived

**Frontend Integration:**

```javascript
Echo.private(`user.${userId}`)
  .listen('NotificationCreated', (e) => {
    console.log('New notification:', e.notification);
    // Update UI, show toast, increment badge count
  });
```

**Benefits:**
- Instant notifications without polling
- Reduced API calls
- Better user experience

---

## Best Practices

### 1. Frontend Implementation

**Polling for notifications (current approach):**
```javascript
// Poll every 30 seconds for unread count
setInterval(() => {
  fetch('/api/v0/notifications/unread-count')
    .then(res => res.json())
    .then(data => updateBadge(data.count));
}, 30000);
```

**Search debouncing:**
```javascript
// Debounce search input to avoid excessive API calls
const debouncedSearch = debounce((query) => {
  fetch(`/api/v0/search?q=${query}`)
    .then(res => res.json())
    .then(data => displayResults(data));
}, 300);
```

### 2. Performance Tips

- Use `unread_only=true` for notification lists (faster query)
- Limit search results per category (default: 5)
- Implement infinite scroll for notifications (load more on scroll)
- Cache notification preferences locally (TTL: 5 minutes)

### 3. Multi-Tenancy

- All queries automatically scoped by `company_id` from JWT
- Users cannot access data from other companies
- Company switching requires new JWT token (security)

### 4. Security

- **Never** expose sensitive data in notifications
- Validate all user inputs
- Rate limiting prevents abuse
- RBAC controls notification visibility (e.g., HR can't see accountant notifications)

---

## Changelog

### Version 0.1.0 (2025-10-28)

**Initial Release:**
- ✅ Notifications API (CRUD, filtering, preferences)
- ✅ Global Search API (drivers only, vehicles/orders/invoices planned)
- ✅ Companies API (list, switch)
- ✅ User Preferences API (notification channels)
- ✅ Multi-tenancy support
- ✅ Rate limiting
- ✅ JWT authentication

**Future Enhancements:**
- [ ] WebSocket real-time notifications (Phase 2)
- [ ] Full-text search with PostgreSQL tsvector
- [ ] Search vehicles, orders, invoices
- [ ] Telegram bot integration for notifications
- [ ] Email notification templates
- [ ] Notification scheduling (digest emails)

---

## Support

**Documentation:** https://docs.g-track.eu
**API Status:** https://gtrack-backend-gtrack-backend-lnf9mi.laravel.cloud/api/v0/health
**Email:** support@g-track.eu

For issues or feature requests, contact the development team.
