# Authentication & Authorization

## Authentication Flow (Auth0)

**Technology:** Auth0 (OAuth 2.0 + OpenID Connect)

**Flow:**

```
1. User visits https://app.g-track.eu
   ↓
2. Clicks "Login" → Redirects to Auth0
   ↓
3. Auth0 Login Page:
   - Email/Password
   - Google SSO
   - Microsoft SSO
   ↓
4. Auth0 redirects back with JWT token
   ↓
5. Frontend stores token → Makes API calls
   ↓
6. Backend validates JWT signature (RS256)
   ↓
7. Backend extracts user_id → Loads user from DB
```

**JWT Token Structure:**

```json
{
  "iss": "https://gtrack.eu.auth0.com/",
  "sub": "auth0|67890abcdef",
  "aud": "https://api.g-track.eu",
  "exp": 1730073600,
  "permissions": ["read:drivers", "write:orders"]
}
```

## RBAC - Role-Based Access Control

**5 Roles:**

| Role | Scope | Key Permissions |
|------|-------|-----------------|
| **Admin** | Full system | Everything |
| **Accountant** | Financial | Invoices, payments, financial reports, driver salaries |
| **HR Manager** | People | Drivers, documents, comments, hiring/firing |
| **Dispatcher** | Operations | Orders, transport units, assignments, readiness view |
| **Driver** | Self-service | Own profile, own documents, assigned orders |

**Permission Matrix Example:**

```
Feature: DRIVERS
├── View all     → Admin, Accountant, HR Manager, Dispatcher
├── View self    → All roles (including Driver)
├── Create       → Admin, HR Manager
├── Edit         → Admin, HR Manager (Driver can edit self)
└── Delete       → Admin, HR Manager

Feature: DOCUMENTS
├── View         → Admin, HR Manager, Dispatcher (limited), Driver (self)
├── Upload       → Admin, HR Manager, Driver (self)
└── Delete       → Admin, HR Manager

Feature: FINANCE
├── Driver salary → Admin, Accountant, Driver (self, view only)
├── Invoices      → Admin, Accountant
└── Payments      → Admin, Accountant

Feature: ORDERS
├── View all      → Admin, Accountant, Dispatcher
├── Create        → Admin, Dispatcher
├── Assign        → Admin, Dispatcher
└── Update status → Admin, Dispatcher, Driver (assigned only)
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 5
