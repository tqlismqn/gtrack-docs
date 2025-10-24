# G-Track System Architecture Overview

**Last Updated:** 2025-10-24  
**Status:** ✅ Current (V2)  
**Related:** [Technology Stack ADR](adr/2025-10-24-v2-technology-stack.md)

---

## Introduction

G-Track is a **Transport Management System (TMS)** designed as a SaaS platform for logistics companies. The system manages the entire lifecycle of transport operations: from customer orders through driver/vehicle assignment, delivery tracking, invoicing, and payment.

**Target Users:**
- Logistics companies (transport operators)
- Dispatchers (order management)
- HR departments (driver/vehicle management)
- Accounting (invoicing and payments)
- Drivers (mobile access - future)

---

## System Context Diagram

```
External Systems & Users
═══════════════════════════════════════════════════════════════

    ┌──────────────┐         ┌──────────────┐
    │   Customer   │         │   Carrier    │
    │  Companies   │         │  Companies   │
    └───────┬──────┘         └──────┬───────┘
            │                       │
            │ Places orders         │ Provides transport
            │                       │
            ▼                       ▼
    ┌────────────────────────────────────────┐
    │                                        │
    │          G-Track TMS (Web)             │
    │     https://app.g-track.eu             │
    │                                        │
    │  Used by:                              │
    │  - Admin                               │
    │  - HR Manager                          │
    │  - Dispatcher (Verfolger)              │
    │  - Accounting                          │
    │                                        │
    └────────────┬──────────────┬────────────┘
                 │              │
                 │              │ API access
                 │              │
    ┌────────────▼──────┐  ┌───▼────────────┐
    │                   │  │                 │
    │   Drivers (Web)   │  │  Future: Mobile │
    │   Self-Service    │  │  Driver App     │
    │                   │  │                 │
    └───────────────────┘  └─────────────────┘

External Integrations (Future)
───────────────────────────────
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   GPS        │  │ Accounting   │  │   Payment    │
    │   Tracking   │  │   Systems    │  │   Gateways   │
    └──────────────┘  └──────────────┘  └──────────────┘
```

---

## High-Level Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Presentation Layer                  │
│                                                     │
│  Angular 20 SPA (Single Page Application)          │
│  - Material UI Components                          │
│  - Reactive Forms                                  │
│  - State Management (Signals + RxJS)               │
│  - Routing & Navigation                            │
│                                                     │
│  Hosted on: Vercel (https://app.g-track.eu)        │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTPS + JWT (RS256)
                     │ RESTful JSON API
                     │
┌────────────────────▼────────────────────────────────┐
│                  Application Layer                  │
│                                                     │
│  Laravel 11 API (PHP 8.3+)                         │
│  - Controllers (HTTP handlers)                     │
│  - Services (business logic)                       │
│  - Repositories (data access)                      │
│  - Events & Listeners                              │
│  - Queue Jobs (async tasks)                        │
│  - Middleware (auth, logging, etc.)                │
│                                                     │
│  Hosted on: Laravel Cloud                          │
└────────────────────┬────────────────────────────────┘
                     │
                     │ SQL Queries
                     │ Eloquent ORM
                     │
┌────────────────────▼────────────────────────────────┐
│                    Data Layer                       │
│                                                     │
│  PostgreSQL 16                                      │
│  - Relational tables                               │
│  - JSONB columns (metadata)                        │
│  - Indexes (performance)                           │
│  - Constraints (data integrity)                    │
│  - Full-text search                                │
│                                                     │
│  Hosted on: Laravel Cloud (Managed PostgreSQL)     │
└─────────────────────────────────────────────────────┘
```

### Supporting Services

```
┌─────────────────────────────────────────────────────┐
│                Authentication & Auth                │
│                                                     │
│  Auth0 (OAuth 2.0 / OIDC)                          │
│  - User authentication                             │
│  - Token generation (RS256 JWT)                    │
│  - MFA support                                     │
│  - User management                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│               Documentation & Knowledge             │
│                                                     │
│  MkDocs Material (https://docs.g-track.eu)         │
│  - Technical documentation                         │
│  - API specifications                              │
│  - Architecture decisions                          │
│  - User guides                                     │
│                                                     │
│  Hosted on: GitHub Pages                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                CI/CD & Automation                   │
│                                                     │
│  GitHub Actions                                     │
│  - Automated testing (Jest + Pest)                 │
│  - Build & deployment                              │
│  - Documentation sync                              │
│  - Policy checks                                   │
└─────────────────────────────────────────────────────┘
```

---

## Module Architecture

### Core Modules (Microservices-Style Organization)

G-Track is organized into distinct **business modules**, each responsible for a specific domain:

```
┌────────────────────────────────────────────────────┐
│                    Core Modules                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. Drivers Module (✅ In Development)             │
│     - Driver profiles & documents                  │
│     - Document expiration tracking                 │
│     - Readiness indicators                         │
│     - RBAC: Admin, HR, Dispatcher, Driver          │
│                                                    │
│  2. Vehicles & Trailers (🔜 Next Priority)         │
│     - Vehicle registration & docs                  │
│     - Technical inspection tracking                │
│     - Service history                              │
│     - Transport Unit = Driver + Vehicle + Trailer  │
│                                                    │
│  3. Customers Module (🔒 Coming Soon)              │
│     - Customer companies (order transport)         │
│     - Carrier companies (provide transport)        │
│     - Credit limit management                      │
│     - Bank account details                         │
│                                                    │
│  4. Orders Module (🔒 Coming Soon)                 │
│     - Transport order lifecycle (9 statuses)       │
│     - Loading/unloading points                     │
│     - Document management (CMR, POD)               │
│     - Financial tracking                           │
│                                                    │
│  5. Invoices Module (🔒 Coming Soon)               │
│     - Invoice generation                           │
│     - Payment tracking                             │
│     - Multi-currency support                       │
│     - PDF generation                               │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Module Relationships

```
                 ┌─────────────┐
                 │  Customers  │
                 │  (Address   │
                 │   Book)     │
                 └──────┬──────┘
                        │
                        │ Customer orders transport
                        │ Carrier provides transport
                        │
            ┌───────────▼───────────┐
            │                       │
            │       Orders          │
            │  (Transport Orders)   │
            │                       │
            └───┬───────────────┬───┘
                │               │
                │               │
        ┌───────▼──────┐   ┌────▼─────────┐
        │              │   │              │
        │   Invoices   │   │  Transport   │
        │              │   │     Unit     │
        │              │   │              │
        └──────────────┘   └──────┬───────┘
                                  │
                                  │ consists of
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
           ┌─────▼────┐    ┌──────▼────┐    ┌─────▼────┐
           │          │    │           │    │          │
           │  Driver  │    │  Vehicle  │    │  Trailer │
           │          │    │           │    │          │
           └──────────┘    └───────────┘    └──────────┘
```

**Key Relationships:**

1. **Customer → Order**
   - Customer places orders for transport
   - One customer can have many orders
   - Credit limit affects order creation

2. **Order → Transport Unit**
   - Order requires Transport Unit for execution
   - Transport Unit = 1 Driver + 1 Vehicle + 1 Trailer
   - Assignment happens when order status changes to "In Progress"

3. **Transport Unit Components**
   - Driver must be ready (all documents valid)
   - Vehicle must be ready (technical inspection valid)
   - Trailer must be ready (technical inspection valid)
   - All three must be 🟢 green for Transport Unit to be operational

4. **Order → Invoice**
   - Order generates invoice when status = "Ready for Invoice"
   - Invoice references order details and prices
   - Payment tracking updates order status

5. **Carrier → Order**
   - Carrier (also stored as Customer type="carrier") executes order
   - Carrier provides pricing
   - Carrier may provide their own Transport Unit (future feature)

---

## Technology Layers

### Frontend (Angular 20)

```
┌─────────────────────────────────────────────┐
│          Angular Application                │
├─────────────────────────────────────────────┤
│                                             │
│  Core Modules:                              │
│  ├─ AppModule (root)                        │
│  ├─ CoreModule (singletons: auth, http)     │
│  ├─ SharedModule (common components, pipes) │
│  └─ Feature Modules:                        │
│     ├─ DriversModule                        │
│     ├─ CustomersModule                      │
│     ├─ OrdersModule                         │
│     ├─ InvoicesModule                       │
│     └─ VehiclesModule                       │
│                                             │
│  Services:                                  │
│  ├─ AuthService (Auth0 integration)         │
│  ├─ ApiService (HTTP client wrapper)        │
│  ├─ StateService (app-wide state)           │
│  └─ Feature Services (module-specific)      │
│                                             │
│  Guards & Interceptors:                     │
│  ├─ AuthGuard (route protection)            │
│  ├─ RoleGuard (RBAC)                        │
│  ├─ TokenInterceptor (JWT attachment)       │
│  └─ ErrorInterceptor (global error handling)│
│                                             │
└─────────────────────────────────────────────┘
```

### Backend (Laravel 11)

```
┌─────────────────────────────────────────────┐
│          Laravel Application                │
├─────────────────────────────────────────────┤
│                                             │
│  API Routes (routes/api.php):               │
│  ├─ /api/v0/* (current API)                 │
│  ├─ /api/v1/* (future surface API)          │
│  └─ Versioned, RESTful endpoints            │
│                                             │
│  Controllers (HTTP layer):                  │
│  ├─ DriverController                        │
│  ├─ CustomerController                      │
│  ├─ OrderController                         │
│  ├─ InvoiceController                       │
│  └─ VehicleController                       │
│                                             │
│  Services (business logic):                 │
│  ├─ DriverService                           │
│  │  └─ Document expiration logic            │
│  ├─ OrderService                            │
│  │  └─ Status transition rules              │
│  ├─ InvoiceService                          │
│  │  └─ Invoice generation logic             │
│  └─ NotificationService                     │
│     └─ Email/SMS notifications              │
│                                             │
│  Repositories (data access):                │
│  ├─ DriverRepository                        │
│  ├─ CustomerRepository                      │
│  ├─ OrderRepository                         │
│  └─ Uses Eloquent ORM                       │
│                                             │
│  Models (Eloquent):                         │
│  ├─ Driver, DriverDocument, DocumentFile    │
│  ├─ Customer, BankAccount                   │
│  ├─ Order, OrderAddress, OrderDocument      │
│  ├─ Invoice, InvoiceItem                    │
│  └─ Vehicle, Trailer                        │
│                                             │
│  Middleware:                                │
│  ├─ Auth0Middleware (JWT verification)      │
│  ├─ RoleMiddleware (RBAC)                   │
│  ├─ LoggingMiddleware                       │
│  └─ ThrottleMiddleware (rate limiting)      │
│                                             │
│  Jobs (queue workers):                      │
│  ├─ SendDocumentExpiryNotification          │
│  ├─ GenerateInvoicePDF                      │
│  ├─ SyncCustomerCreditLimit                 │
│  └─ Runs via Laravel Horizon                │
│                                             │
│  Events & Listeners:                        │
│  ├─ DocumentExpiringSoon → NotifyHR         │
│  ├─ OrderStatusChanged → NotifyDispatcher   │
│  └─ InvoiceCreated → SendToCustomer         │
│                                             │
└─────────────────────────────────────────────┘
```

### Database (PostgreSQL 16)

```
┌─────────────────────────────────────────────┐
│          Database Schema                    │
├─────────────────────────────────────────────┤
│                                             │
│  Core Tables:                               │
│  ├─ drivers (driver profiles)               │
│  ├─ driver_documents (14 document types)    │
│  ├─ document_files (versioned files)        │
│  ├─ driver_comments (audit trail)           │
│  │                                           │
│  ├─ customers (both customers & carriers)   │
│  ├─ bank_accounts (multiple per customer)   │
│  │                                           │
│  ├─ orders (transport orders)               │
│  ├─ order_addresses (loading/unloading)     │
│  ├─ order_documents (CMR, POD, etc.)        │
│  │                                           │
│  ├─ invoices (billing)                      │
│  ├─ invoice_items (line items)              │
│  │                                           │
│  ├─ vehicles (trucks)                       │
│  ├─ trailers                                │
│  └─ transport_units (driver+vehicle+trailer)│
│                                             │
│  System Tables:                             │
│  ├─ users (Auth0 sync)                      │
│  ├─ roles (RBAC)                            │
│  ├─ permissions                             │
│  ├─ audit_logs (all changes)                │
│  └─ notifications                           │
│                                             │
│  Indexes:                                   │
│  ├─ Primary keys (UUID)                     │
│  ├─ Foreign keys (relationships)            │
│  ├─ Search indexes (full-text)              │
│  └─ Performance indexes (queries)           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Security Architecture

### Authentication Flow (Auth0 + RS256)

```
1. User Login
   │
   │ Browser → Auth0 Login Page
   │
   ▼
2. Auth0 Authentication
   │
   │ Username/Password or Social Login
   │ MFA (if enabled)
   │
   ▼
3. Token Generation
   │
   │ Auth0 generates JWT (RS256)
   │ Token contains: user_id, email, roles
   │ Token signed with Auth0 private key
   │
   ▼
4. Redirect to App
   │
   │ Browser receives token
   │ Angular stores token in memory (not localStorage)
   │
   ▼
5. API Requests
   │
   │ Angular attaches token to every API call
   │ Header: Authorization: Bearer <JWT>
   │
   ▼
6. Backend Verification
   │
   │ Laravel middleware verifies JWT signature
   │ Uses Auth0 public key (no API call needed)
   │ Extracts user_id and roles
   │
   ▼
7. Authorization (RBAC)
   │
   │ Check user's role (Admin, HR, Dispatcher, etc.)
   │ Check permissions for requested action
   │ Allow or deny request
   │
   ▼
8. Response
   │
   │ If authorized: return data
   │ If not: return 403 Forbidden
```

### Role-Based Access Control (RBAC)

```
┌─────────────────────────────────────────────┐
│              User Roles                     │
├─────────────────────────────────────────────┤
│                                             │
│  Admin                                      │
│  └─ Full access to everything               │
│                                             │
│  HR Manager                                 │
│  ├─ Drivers: Full CRUD                      │
│  ├─ Vehicles: Full CRUD                     │
│  ├─ Documents: Upload, manage               │
│  └─ Notifications: Send                     │
│                                             │
│  Dispatcher (Verfolger)                     │
│  ├─ Orders: Full CRUD                       │
│  ├─ Customers: Read                         │
│  ├─ Drivers: Read, assign to orders         │
│  ├─ Vehicles: Read, assign to orders        │
│  └─ Documents: Upload delivery docs         │
│                                             │
│  Accounting                                 │
│  ├─ Invoices: Full CRUD                     │
│  ├─ Orders: Read, update payment status     │
│  ├─ Customers: Read financial data          │
│  └─ Reports: Generate                       │
│                                             │
│  Driver (Self-Service)                      │
│  ├─ Own Profile: Read                       │
│  ├─ Own Documents: View, upload             │
│  ├─ Assigned Orders: Read                   │
│  └─ Comments: Add to own orders             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────┐
│              Internet (Users)                   │
└───────────────────┬─────────────────────────────┘
                    │
                    │ HTTPS (SSL/TLS)
                    │
        ┌───────────▼──────────────┐
        │                          │
        │   CDN (Vercel Edge)      │
        │   - Global distribution  │
        │   - Static assets cache  │
        │   - DDoS protection      │
        │                          │
        └───────────┬──────────────┘
                    │
                    │
    ┌───────────────┴───────────────┐
    │                               │
    │ Frontend                      │ Backend
    │ (Vercel)                      │ (Laravel Cloud)
    │                               │
    ▼                               ▼
┌────────────────┐          ┌────────────────┐
│                │          │                │
│  Angular App   │◄────────►│  Laravel API   │
│  (Static)      │   API    │  (Dynamic)     │
│                │  Calls   │                │
└────────────────┘          └───────┬────────┘
                                    │
                                    │ Database
                                    │ Queries
                                    │
                            ┌───────▼────────┐
                            │                │
                            │  PostgreSQL 16 │
                            │   (Managed)    │
                            │                │
                            └────────────────┘
```

### CI/CD Pipeline

```
GitHub Repository Changes
    │
    ▼
GitHub Actions Triggered
    │
    ├─────────────────┬─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
Frontend CI      Backend CI       Docs CI
    │                 │                 │
    │ Build           │ Build           │ Build
    │ Lint            │ Test (Pest)     │ Strict
    │ Test (Jest)     │ Coverage        │ Check
    │                 │                 │
    ▼                 ▼                 ▼
Policy Checks    Policy Checks    Policy Checks
    │                 │                 │
    │ Branch name     │ Branch name     │ Branch name
    │ Fresh branch    │ Fresh branch    │ Fresh branch
    │ Docs block      │ Docs block      │ Docs updated
    │                 │                 │
    ▼                 ▼                 ▼
All Green?       All Green?       All Green?
    │                 │                 │
    │                 │                 │
    ▼                 ▼                 ▼
Vercel Deploy    Laravel Cloud    GitHub Pages
(Preview)        (Staging)        (Preview)
    │                 │                 │
    │                 │                 │
    ▼                 ▼                 ▼
Merge to Main    Merge to Main    Merge to Main
    │                 │                 │
    │                 │                 │
    ▼                 ▼                 ▼
Production       Production       Production
Deploy           Deploy           Deploy
```

---

## Scalability & Performance

### Current Capacity (V2 Target)

```
┌─────────────────────────────────────────────┐
│          System Capacity Goals              │
├─────────────────────────────────────────────┤
│                                             │
│  Concurrent Users: 100+                     │
│  - Admin: 5-10                              │
│  - HR: 5-10                                 │
│  - Dispatchers: 10-20                       │
│  - Accounting: 5-10                         │
│  - Drivers: 50-100 (future mobile)          │
│                                             │
│  Data Scale:                                │
│  - Drivers: 200-300 active                  │
│  - Vehicles: 150-200                        │
│  - Orders: 10,000+ per year                 │
│  - Invoices: 10,000+ per year               │
│  - Documents: 50,000+ files                 │
│                                             │
│  Performance Targets:                       │
│  - Page Load: < 2 seconds                   │
│  - API Response: < 500ms (p95)              │
│  - Database Queries: < 100ms (p95)          │
│  - Document Upload: < 5 seconds (20MB)      │
│                                             │
└─────────────────────────────────────────────┘
```

### Scaling Strategy

```
Phase 1: Vertical Scaling (Current)
├─ Single Laravel instance
├─ Single PostgreSQL instance
└─ Sufficient for 100-200 users

Phase 2: Horizontal Scaling (Future)
├─ Multiple Laravel instances (load balanced)
├─ Database read replicas
├─ Redis cache layer
└─ Queue workers on separate servers

Phase 3: Microservices (Future, if needed)
├─ Separate services per module
├─ API gateway
├─ Service mesh
└─ For 1000+ users
```

---

## Monitoring & Observability

### Logging

```
Frontend Logging:
├─ Console errors (development)
├─ Sentry error tracking (production)
└─ User analytics (privacy-compliant)

Backend Logging:
├─ Laravel Log (daily rotation)
├─ Error tracking (Sentry/Bugsnag)
├─ API request logging
├─ Audit trail (all data changes)
└─ Performance monitoring

Database Logging:
├─ Slow query log (>100ms)
├─ Connection pool stats
└─ Replication lag (if using replicas)
```

### Health Checks

```
GET /api/health
Response:
{
  "status": "healthy",
  "database": "connected",
  "cache": "operational",
  "queue": "processing",
  "timestamp": "2025-10-24T10:30:00Z"
}
```

---

## Future Architecture Enhancements

### Planned Features

1. **Mobile App for Drivers**
   - React Native or Flutter
   - GPS tracking integration
   - Offline mode for documents
   - Push notifications

2. **Real-time Features**
   - WebSockets for live updates
   - Real-time order status
   - Live GPS tracking on map

3. **Advanced Analytics**
   - Business intelligence dashboard
   - Route optimization
   - Cost analysis
   - Driver performance metrics

4. **Third-party Integrations**
   - Accounting software (Pohoda, Money S3)
   - Payment gateways (Stripe, PayPal)
   - GPS tracking systems
   - E-invoice systems

5. **Multi-tenant Support**
   - Separate data per company
   - White-label option
   - Custom branding

---

## Related Documentation

- **[Technology Stack ADR](adr/2025-10-24-v2-technology-stack.md)** - Detailed rationale for tech choices
- **[Business Processes](business-processes.md)** - How business workflows map to system
- **[Data Flow](data-flow.md)** - How data moves through the system
- **[Modules Overview](../modules/drivers/index.md)** - Detailed module documentation
- **[API Reference](../api/index.md)** - API endpoint specifications

---

**Status:** ✅ Current and Maintained  
**Next Review:** Q2 2026 (after core modules migration)
