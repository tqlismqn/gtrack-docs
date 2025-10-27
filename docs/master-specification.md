# G-Track Master Specification v3.1

**Version:** 3.1
**Date:** October 27, 2025
**Status:** 🟢 Active Development
**Current Phase:** Drivers Module (90% Complete) - Document Management Functional

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Authentication & Authorization](#authentication--authorization)
6. [Onboarding & Company Setup](#onboarding--company-setup)
7. [Core Modules](#core-modules)
8. [Financial System](#financial-system)
9. [Internationalization (i18n)](#internationalization-i18n)
10. [UI/UX Architecture](#uiux-architecture)
11. [Database Schema](#database-schema)
12. [API Specification](#api-specification)
13. [Audit & History System](#audit--history-system)
14. [Integrations & APIs](#integrations--apis)
15. [Roadmap](#roadmap)
16. [CHANGELOG](#changelog)

---

## 🎯 EXECUTIVE SUMMARY

**G-Track** is a modern SaaS Transport Management System (TMS) designed for small-to-medium logistics companies (2-50 vehicles) operating across European Union. The platform addresses critical pain points in driver document management, vehicle tracking, order processing, and financial operations.

### Key Features:
- ✅ **Document Expiration Tracking** - Automated alerts for 14 document types
- ✅ **Multi-tenant Architecture** - Company → Offices → Users isolation
- ✅ **EU VAT Compliance** - Domestic, Reverse Charge, Non-VAT modes
- ✅ **5 Languages** - Russian, English, Czech, Polish, German
- ✅ **RBAC** - 5 roles with granular permissions
- ✅ **Real-time GPS** - Vehicle tracking (future integration)
- ✅ **Financial Dashboard** - Profitability per driver/vehicle/order

### Target Market:
- 🇨🇿 Czech Republic (primary)
- 🇵🇱 Poland
- 🇩🇪 Germany
- 🇦🇹 Austria
- 🇳🇱 Netherlands
- 🇮🇹 Italy (future)

### Business Model:
- **Free Trial:** 30 days
- **Module-based Pricing:**
  - Core (Drivers + Vehicles): €29/month
  - Orders Management: +€19/month
  - Invoicing: +€15/month
  - GPS Tracking: +€25/month
  - Service Management: +€10/month

---

## 🌟 PROJECT OVERVIEW

### What is G-Track?

G-Track transforms chaotic Excel-based transport management into a streamlined digital platform. The system eliminates manual document tracking, prevents expired licenses from causing fines, optimizes order assignment, and provides real-time financial insights.

### Client Pain Points:

**Problem 1: Document Chaos (Drivers)**
```
Client has 150-170 drivers in Excel spreadsheet
❌ No visibility on document expiration dates
❌ Manual checking every week (5+ hours)
❌ Missed expirations → fines, insurance issues
❌ Cannot quickly answer "Who is ready for delivery?"
```

**Solution:**
```
✅ Automated expiration tracking (14 document types)
✅ Visual status indicators (🟢🟡🔴)
✅ Email/SMS alerts 30/15/7 days before expiry
✅ "Readiness Dashboard" - see who can work TODAY
✅ Mobile upload via Telegram Bot
```

**Problem 2: Order Assignment Inefficiency**
```
Dispatcher spends 30-45 minutes per order:
❌ Check driver availability (documents OK?)
❌ Check vehicle status (service due?)
❌ Check trailer availability
❌ Manual Excel updates
```

**Solution:**
```
✅ Transport Unit = Driver + Vehicle + Trailer (pre-validated)
✅ One-click order assignment
✅ Automatic status transitions
✅ Real-time availability view
```

**Problem 3: Financial Opacity**
```
❌ Unknown profitability per order/driver
❌ Hidden costs (fines, damages, repairs)
❌ Manual calculations in Excel
❌ No visibility on VAT handling
```

**Solution:**
```
✅ Real-time profitability tracking
✅ Automatic cost allocation (fines → driver → order)
✅ EU VAT compliance (Reverse Charge automation)
✅ Financial dashboards by driver/vehicle/customer
```

### Target Users:

| Role | Count | Primary Tasks |
|------|-------|---------------|
| **Owner/CEO** | 1 | Financial oversight, strategic decisions |
| **Admin** | 1-2 | Full system management, user setup |
| **Accountant** | 1-2 | Invoicing, payments, financial reports |
| **HR Manager** | 1-2 | Driver management, document tracking |
| **Dispatcher** | 2-5 | Order assignment, transport coordination |
| **Driver** | 20-150 | Document upload, order status updates |

---

## 🛠️ TECHNOLOGY STACK

### Frontend

```
Angular 20.0.0+
├── @angular/material 20.0.0+ (Material Design 3)
├── TypeScript 5.6+
├── RxJS 7.8+
├── Signals (native Angular state management)
├── @ngx-translate/core (i18n)
└── Leaflet (GPS maps)
```

**Key Architecture Decisions:**
- **Standalone Components** - no NgModules
- **Signal-based State** - reactive without Zone.js
- **OnPush Change Detection** - performance optimization
- **Lazy Loading** - routes loaded on-demand
- **PWA Support** - installable mobile web app

**Deployment:**
- **Platform:** Vercel
- **URL:** https://app.g-track.eu
- **CI/CD:** GitHub Actions → Auto-deploy on merge to main
- **Environment:** Node.js 20 LTS

---

### Backend

```
Laravel 12.35.0+
├── PHP 8.3.12+
├── PostgreSQL 16.4+ or 17.0
├── Redis 7.0+ (cache, sessions, queues)
├── Laravel Reverb (WebSockets)
├── Laravel Horizon (queue management)
├── Laravel Passport/Sanctum (API auth)
└── Pest (testing framework)
```

**Key Packages:**
- `stancl/tenancy` - Multi-tenant isolation
- `spatie/laravel-permission` - RBAC
- `barryvdh/laravel-dompdf` - PDF generation
- `laravel/cashier` - Stripe subscriptions
- `league/flysystem-aws-s3-v3` - File storage

**Deployment:**
- **Platform:** Laravel Cloud
- **URL:** https://api.g-track.eu
- **Database:** Serverless PostgreSQL (Neon)
- **File Storage:** AWS S3 (eu-central-1)
- **CI/CD:** GitHub Actions → Laravel Cloud auto-deploy

---

### Database

```
PostgreSQL 16.4+ / 17.0
├── PostGIS 3.4+ (geospatial queries)
├── TimescaleDB 2.13+ (GPS time-series)
└── pg_cron (scheduled tasks)
```

**Performance Optimizations:**
- Connection pooling via PgBouncer
- Indexes on all foreign keys
- Composite indexes for common queries
- Partitioning for GPS history (by month)
- Materialized views for analytics

---

### Third-Party Services

| Service | Purpose | Pricing |
|---------|---------|---------|
| **Auth0** | Authentication (OAuth, SSO) | $23/month (Essentials) |
| **Stripe** | Subscriptions, payments | 1.4% + €0.25 per transaction |
| **AWS S3** | File storage | ~$5/month (500GB) |
| **Mailgun** | Transactional emails | $35/month (50k emails) |
| **Sentry** | Error tracking | Free tier (5k errors/month) |
| **Vercel** | Frontend hosting | Free tier (hobby) |
| **Laravel Cloud** | Backend hosting | $19/month (starter) |

**Total Monthly Cost (MVP):** ~$80-100/month

---

## 🏗️ SYSTEM ARCHITECTURE

### Multi-Tenancy Model

**Architecture:** Single Database with Tenant Isolation

```
Database: gtrack_production
├── companies (tenants)
│   ├── id (uuid)
│   ├── name
│   ├── country_code
│   └── currency
├── offices (sub-tenants)
│   ├── id (uuid)
│   ├── company_id (FK)
│   ├── name
│   └── country_code
└── All other tables with:
    ├── company_id (FK) ← MANDATORY
    └── office_id (FK) ← OPTIONAL
```

**Key Principles:**
1. **Every query** includes `WHERE company_id = ?`
2. **Global Middleware** automatically scopes queries
3. **Cross-Office Visibility** controlled via settings
4. **Data Isolation** enforced at database + application level

**Example: Cross-Office Driver Search**

```php
// Setting: Allow cross-office driver search
$company->settings->allow_cross_office_driver_search = true;

// HR Manager in Prague office searches drivers
Driver::where('company_id', auth()->user()->company_id)
    ->when(!$company->settings->allow_cross_office_driver_search, function ($q) {
        $q->where('office_id', auth()->user()->office_id);
    })
    ->search($request->query)
    ->get();
```

**Use Case: Preventing Driver Rehire**

```
Scenario:
- Driver fired from Czech office (reason: multiple fines)
- Driver applies to Polish office (same company)

System behavior:
1. HR enters driver name + birth_date
2. System checks: "Similar driver found in Czech office"
3. Alert: "⚠️ Jan Novák (DOB: 1985-03-15) worked in Czech office (2020-2024)"
4. HR sees history → decides not to hire
```

---

### Module-Based Architecture

**Core Concept:** Each module is a separate subscription tier

```
┌─────────────────────────────────────────────┐
│ Subscription Tiers                          │
├─────────────────────────────────────────────┤
│ FREE (Trial 30 days)                        │
│   ✅ 5 drivers, 3 vehicles                  │
│   ✅ Basic dashboard                        │
│                                             │
│ STARTER (€29/month)                         │
│   ✅ Unlimited drivers                      │
│   ✅ Unlimited vehicles                     │
│   ✅ Document management                    │
│   ✅ Service requests                       │
│                                             │
│ PROFESSIONAL (€48/month = Starter + €19)    │
│   ✅ Everything in Starter                  │
│   ✅ Order management                       │
│   ✅ Customer management                    │
│   ✅ Transport Unit assignments             │
│                                             │
│ BUSINESS (€63/month = Pro + €15)            │
│   ✅ Everything in Professional             │
│   ✅ Invoicing with EU VAT compliance       │
│   ✅ Payment tracking                       │
│   ✅ Financial dashboards                   │
│                                             │
│ ENTERPRISE (€88/month = Business + €25)     │
│   ✅ Everything in Business                 │
│   ✅ GPS tracking integration               │
│   ✅ Real-time vehicle locations            │
│   ✅ Route history & analytics              │
└─────────────────────────────────────────────┘
```

**Feature Flags (Database):**

```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    tier VARCHAR(20), -- 'free', 'starter', 'professional', 'business', 'enterprise'
    
    -- Feature flags
    modules JSONB, -- ['drivers', 'vehicles', 'orders', 'invoices', 'gps']
    
    -- Limits
    max_drivers INT,
    max_vehicles INT,
    max_users INT,
    
    stripe_subscription_id VARCHAR(100),
    trial_ends_at TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ
);
```

**Middleware: Check Module Access**

```php
// app/Http/Middleware/CheckModuleAccess.php
public function handle(Request $request, Closure $next, string $module)
{
    $company = auth()->user()->company;
    
    if (!$company->subscription->hasModule($module)) {
        return response()->json([
            'error' => 'Module not available',
            'message' => "Upgrade to access {$module} module",
            'upgrade_url' => route('billing.upgrade', ['module' => $module])
        ], 403);
    }
    
    return $next($request);
}

// Route protection
Route::middleware(['auth', 'module:orders'])->group(function () {
    Route::apiResource('orders', OrderController::class);
});
```

---

## 🔐 AUTHENTICATION & AUTHORIZATION

### Authentication Flow (Auth0)

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
  "iat": 1729987200,
  "azp": "client_id_here",
  "scope": "openid profile email",
  "permissions": ["read:drivers", "write:orders"]
}
```

**Backend Validation (Laravel):**

```php
// config/auth.php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],

// Middleware
Route::middleware('auth:api')->get('/user', function (Request $request) {
    return $request->user();
});
```

---

### RBAC - Role-Based Access Control

**5 Roles:**

| Role | Scope | Key Permissions |
|------|-------|-----------------|
| **Admin** | Full system | Everything |
| **Accountant** | Financial | Invoices, payments, financial reports, driver salaries |
| **HR Manager** | People | Drivers, documents, comments, hiring/firing |
| **Dispatcher** | Operations | Orders, transport units, assignments, readiness view |
| **Driver** | Self-service | Own profile, own documents, assigned orders |

**Detailed Permission Matrix:**

```
┌────────────────┬───────┬────────────┬──────┬────────────┬──────────┐
│ Feature        │ Admin │ Accountant │ HR   │ Dispatcher │ Driver   │
├────────────────┼───────┼────────────┼──────┼────────────┼──────────┤
│ DRIVERS                                                              │
│ - View all     │ ✅    │ ✅         │ ✅   │ ✅         │ ❌       │
│ - View self    │ ✅    │ ✅         │ ✅   │ ✅         │ ✅       │
│ - Create       │ ✅    │ ❌         │ ✅   │ ❌         │ ❌       │
│ - Edit         │ ✅    │ ❌         │ ✅   │ ❌         │ Self     │
│ - Delete       │ ✅    │ ❌         │ ✅   │ ❌         │ ❌       │
│                                                                      │
│ DOCUMENTS                                                            │
│ - View         │ ✅    │ ✅*        │ ✅   │ ✅**       │ Self     │
│ - Upload       │ ✅    │ ❌         │ ✅   │ ❌         │ Self     │
│ - Delete       │ ✅    │ ❌         │ ✅   │ ❌         │ ❌       │
│                                                                      │
│ FINANCE                                                              │
│ - Driver salary│ ✅    │ ✅         │ ❌   │ ❌         │ Self     │
│ - Fines/Bonuses│ ✅    │ ✅         │ ✅   │ ❌         │ Self     │
│ - Invoices     │ ✅    │ ✅         │ ❌   │ ❌         │ ❌       │
│ - Payments     │ ✅    │ ✅         │ ❌   │ ❌         │ ❌       │
│                                                                      │
│ ORDERS                                                               │
│ - View all     │ ✅    │ ✅         │ ❌   │ ✅         │ Assigned │
│ - Create       │ ✅    │ ❌         │ ❌   │ ✅         │ ❌       │
│ - Assign       │ ✅    │ ❌         │ ❌   │ ✅         │ ❌       │
│ - Update status│ ✅    │ ❌         │ ❌   │ ✅         │ Assigned │
│ - Cancel       │ ✅    │ ❌         │ ❌   │ ✅         │ ❌       │
│                                                                      │
│ VEHICLES                                                             │
│ - View all     │ ✅    │ ✅         │ ✅   │ ✅         │ Assigned │
│ - Create       │ ✅    │ ❌         │ ✅   │ ❌         │ ❌       │
│ - Service      │ ✅    │ ✅         │ ✅   │ ✅         │ Request  │
│                                                                      │
│ SETTINGS                                                             │
│ - Company      │ ✅    │ ❌         │ ❌   │ ❌         │ ❌       │
│ - Users        │ ✅    │ ❌         │ ❌   │ ❌         │ ❌       │
│ - Billing      │ ✅    │ ✅         │ ❌   │ ❌         │ ❌       │
└────────────────┴───────┴────────────┴──────┴────────────┴──────────┘

* Accountant cannot view personal documents (passport, visa)
** Dispatcher only sees document status (🟢🟡🔴), not actual files
```

**Implementation (Laravel + Spatie):**

```php
// database/seeders/RoleSeeder.php
Role::create(['name' => 'admin']);
Role::create(['name' => 'accountant']);
Role::create(['name' => 'hr_manager']);
Role::create(['name' => 'dispatcher']);
Role::create(['name' => 'driver']);

Permission::create(['name' => 'view:drivers']);
Permission::create(['name' => 'create:drivers']);
Permission::create(['name' => 'edit:drivers']);
Permission::create(['name' => 'delete:drivers']);
// ... etc

// Assign permissions to roles
$admin = Role::findByName('admin');
$admin->givePermissionTo(Permission::all());

$dispatcher = Role::findByName('dispatcher');
$dispatcher->givePermissionTo([
    'view:drivers',
    'view:vehicles',
    'create:orders',
    'assign:orders',
]);

// Check permissions in controller
public function store(Request $request)
{
    $this->authorize('create:drivers');
    
    // Create driver logic
}

// Blade/Vue directive
@can('edit:drivers')
    <button>Edit Driver</button>
@endcan
```

---

## 🚀 ONBOARDING & COMPANY SETUP

### Registration Flow

**Step 1: Auth0 Registration**

```
User visits: https://app.g-track.eu
  ↓
Clicks "Get Started"
  ↓
Auth0 registration form:
  - Email
  - Password
  - Accept Terms & Privacy
  ↓
Email verification
  ↓
Redirects to Company Setup
```

---

**Step 2: Company Setup**

```
┌──────────────────────────────────────────────┐
│ Welcome to G-Track! 🚀                       │
│ Let's set up your company                    │
├──────────────────────────────────────────────┤
│                                              │
│ 1️⃣ Company Name: *                          │
│    [Trans Logistics s.r.o.___________]      │
│                                              │
│ 2️⃣ Country/Region: *                        │
│    ┌─────────────────────────────────────┐  │
│    │ 🇨🇿 Czech Republic (CZK)             │  │
│    │ 🇵🇱 Poland (PLN)                     │  │
│    │ 🇩🇪 Germany (EUR)                    │  │
│    │ 🇦🇹 Austria (EUR)                    │  │
│    │ 🇳🇱 Netherlands (EUR)                │  │
│    │ 🇮🇹 Italy (EUR)                      │  │
│    └─────────────────────────────────────┘  │
│                                              │
│ 3️⃣ Interface Language: *                    │
│    ┌─────────────────────────────────────┐  │
│    │ 🇷🇺 Russian                          │  │
│    │ 🇬🇧 English                          │  │
│    │ 🇨🇿 Czech                            │  │
│    │ 🇵🇱 Polish                           │  │
│    │ 🇩🇪 German                           │  │
│    └─────────────────────────────────────┘  │
│                                              │
│ 4️⃣ VAT ID (optional):                       │
│    [CZ12345678________________]             │
│    💡 You can add this later in Settings    │
│                                              │
│         [Create Company & Start Trial]      │
│                                              │
│ ✨ 30-day free trial, no credit card needed │
└──────────────────────────────────────────────┘
```

**Auto-Configuration Based on Country:**

```php
$countryConfig = [
    'CZ' => [
        'currency' => 'CZK',
        'tax_rate' => 21.00,
        'date_format' => 'DD.MM.YYYY',
        'timezone' => 'Europe/Prague',
        'first_day_of_week' => 'monday',
    ],
    'PL' => [
        'currency' => 'PLN',
        'tax_rate' => 23.00,
        'date_format' => 'DD.MM.YYYY',
        'timezone' => 'Europe/Warsaw',
        'first_day_of_week' => 'monday',
    ],
    'DE' => [
        'currency' => 'EUR',
        'tax_rate' => 19.00,
        'date_format' => 'DD.MM.YYYY',
        'timezone' => 'Europe/Berlin',
        'first_day_of_week' => 'monday',
    ],
];
```

---

**Step 3: First Login - Dashboard Tour**

After company creation, user sees:

```
┌──────────────────────────────────────────────┐
│ 🎉 Welcome to G-Track!                       │
│                                              │
│ Quick Tour (Skip →)                          │
├──────────────────────────────────────────────┤
│                                              │
│ [Highlight: Sidebar]                         │
│ 👈 Navigate between modules here             │
│    - Drivers (your main module)              │
│    - Vehicles                                │
│    - Orders (Coming Soon)                    │
│    - Invoices (Coming Soon)                  │
│                                              │
│            [Next]                            │
└──────────────────────────────────────────────┘

[Tour continues with 5-6 highlights]

Final screen:
┌──────────────────────────────────────────────┐
│ You're all set! 🚀                           │
│                                              │
│ What would you like to do first?            │
│                                              │
│ ┌──────────────────────────────────────┐    │
│ │ ➕ Add your first driver              │    │
│ └──────────────────────────────────────┘    │
│                                              │
│ ┌──────────────────────────────────────┐    │
│ │ 📤 Import drivers from CSV/Excel      │    │
│ └──────────────────────────────────────┘    │
│                                              │
│ ┌──────────────────────────────────────┐    │
│ │ 👥 Invite team members                │    │
│ └──────────────────────────────────────┘    │
│                                              │
│ ┌──────────────────────────────────────┐    │
│ │ ⚙️ Configure company settings         │    │
│ └──────────────────────────────────────┘    │
│                                              │
│         [Skip - Take me to Dashboard]        │
└──────────────────────────────────────────────┘
```

---

### User Invitation System

**Admin → Invite User:**

```
┌──────────────────────────────────────────────┐
│ Invite Team Member                           │
├──────────────────────────────────────────────┤
│                                              │
│ Email: *                                     │
│ [petr.novak@company.cz_______________]      │
│                                              │
│ Roles: * (select multiple)                  │
│ ☐ Admin                                     │
│ ☑ HR Manager                                │
│ ☐ Accountant                                │
│ ☐ Dispatcher                                │
│ ☐ Driver                                    │
│                                              │
│ Interface Language:                          │
│ [🇨🇿 Czech ▼]                                │
│                                              │
│ Office (if multi-office):                   │
│ [Prague Office ▼]                           │
│                                              │
│         [Send Invitation]                    │
└──────────────────────────────────────────────┘
```

**Email Template (Czech example):**

```
Subject: Pozvánka do G-Track TMS

Dobrý den, Petr!

Byli jste pozváni do společnosti "Trans Logistics s.r.o." 
pro práci se systémem G-Track TMS.

Vaše role: HR Manager
Jazyk rozhraní: Čeština

┌─────────────────────────────────┐
│   [Přijmout pozvánku]           │
└─────────────────────────────────┘

Tato pozvánka je platná 7 dní.

S pozdravem,
G-Track Team
```

---

### Driver Invitation (Special Case)

**When creating a new driver:**

```
┌──────────────────────────────────────────────┐
│ Add Driver                                   │
├──────────────────────────────────────────────┤
│                                              │
│ First Name: [Jan______________]             │
│ Last Name: [Novák_____________]             │
│ Email: [jan.novak@driver.cz____]            │
│ Phone: [+420 777 123 456_______]            │
│                                              │
│ ☑ Send system invitation                    │
│   (assigns Driver role automatically)        │
│                                              │
│ 💬 Invitation will include:                 │
│    • Login credentials                       │
│    • Telegram Bot instructions               │
│    • How to upload documents via mobile      │
│                                              │
│         [Create Driver]                      │
└──────────────────────────────────────────────┘
```

**Email to Driver (Russian example):**

```
Subject: Добро пожаловать в G-Track!

Здравствуйте, Jan!

Вы добавлены в систему G-Track компании "Trans Logistics".

🔐 Войти в систему:
https://app.g-track.eu/login
Ваш email: jan.novak@driver.cz

📱 Telegram Bot (загрузка документов):
1. Найдите бота: @GTrackBot
2. Отправьте команду: /start
3. Введите ваш код: DRV-0001

Вы сможете:
✅ Загружать фото документов через телефон
✅ Проверять статус своих документов
✅ Видеть назначенные заказы

📖 Инструкция: https://docs.g-track.eu/driver-guide

--
G-Track Team
```

---

## 📦 CORE MODULES

### Module 1: Drivers (PRIORITY #1)

**Status:** 🟡 70% Complete (in active development)  
**Goal:** Complete before other modules  
**Target:** 150-200 drivers per company

---

#### Business Logic

**Problem Statement:**

```
Client manages 150-170 drivers in Excel:
❌ Manual tracking of 14 document types
❌ No alerts for expiring documents
❌ 5+ hours/week checking expirations manually
❌ Cannot answer "Who is ready for delivery today?"
❌ Fines from expired licenses/permits
```

**Solution:**

```
✅ Digital driver profiles with 14 document types
✅ Automatic expiration tracking (30/15/7 day alerts)
✅ Visual status indicators: 🟢 valid, 🟡 expiring, 🔴 expired
✅ "Readiness Dashboard" - instant overview
✅ Mobile document upload via Telegram Bot
✅ RBAC - HR sees everything, Dispatcher sees readiness only
```

---

#### 14 Document Types

Each driver has these documents tracked:

| # | Document Type | Fields | Expiration Logic |
|---|---------------|--------|------------------|
| 1 | **Passport** | Number, Country, Valid Until | Alert 30 days before |
| 2 | **Visa/Biometrics** | Number, Type, Valid Until | Alert 30 days before |
| 3 | **Residence Permit** | Valid From, Valid Until | Alert 30 days before |
| 4 | **Work Permit/License** | Valid From, Valid Until | Alert 30 days before |
| 5 | **A1 Certificate (EU)** | Valid From, Valid Until | Alert 30 days before |
| 6 | **A1 Switzerland** | Valid From, Valid Until | Alert 30 days before |
| 7 | **Declaration** | Valid Until | Alert 30 days before |
| 8 | **Health Insurance** | Valid Until | Alert 15 days before |
| 9 | **Travel Insurance** | Valid Until | Alert 15 days before |
| 10 | **Driver's License** | Number, Categories, Valid Until | Alert 60 days before |
| 11 | **ADR Certificate** | Valid Until | Alert 30 days before |
| 12 | **Tachograph Card** | Number, Valid Until | Alert 30 days before |
| 13 | **Code 95** | Valid Until | Alert 60 days before |
| 14 | **Medical Examination** | Valid From, Valid Until | Special logic* |

**Special Logic - Medical Examination (Psychotest):**
```
IF driver age < 60:
    Validity = 3 years
ELSE:
    Validity = 1 year
    
Alert timing:
    60 days before expiry
```

---

#### Status Indicators

**Visual System:**

```
🟢 Valid (Zelený)
   - Document is valid for >30 days
   - Driver can work
   
🟡 Expiring Soon (Žlutý)
   - Document expires within 30 days
   - Driver can still work (warning)
   
🟠 Warning (Oranžový)
   - Document expires within 15 days
   - Urgent renewal needed
   
🔴 Expired (Červený)
   - Document has expired
   - Driver CANNOT work
   
⚪ No Data (Šedý)
   - Document not uploaded
   - Cannot determine readiness
```

**Readiness Logic:**

```typescript
function isDriverReady(driver: Driver): boolean {
    const statuses = driver.documents.map(d => d.status);
    
    // Driver is ready if:
    // - Status is Active
    // - All documents are 🟢 (valid) OR 🟡 (expiring soon)
    // - NO documents are 🔴 (expired) or ⚪ (missing)
    
    if (driver.status !== 'active') return false;
    
    const hasExpiredOrMissing = statuses.some(s => 
        s === 'expired' || s === 'no_data'
    );
    
    return !hasExpiredOrMissing;
}
```

---

#### UI/UX - Drivers Module

**Layout: Split View (Desktop)**

```
┌────────────────────────────────────────────────────────────┐
│ Sidebar │ Drivers List            │ Driver Detail         │
├─────────┼─────────────────────────┼───────────────────────┤
│ [Menu]  │ 🔍 Search drivers...    │ Jan Novák (#DRV-0001) │
│         │                         │                       │
│         │ Filters:                │ Tabs:                 │
│         │ Status: [All ▼]        │ • Overview            │
│         │ Documents: [All ▼]     │ • Documents ✓         │
│         │ Location: [All ▼]      │ • Finance             │
│         │                         │ • Comments            │
│         │ ┌─ Jan Novák ────────┐ │ • History             │
│         │ │ #DRV-0001          │ │                       │
│         │ │ 🟢 Ready           │ │ Documents (14):       │
│         │ │ 🇨🇿 CZ, Praha      │ │                       │
│         │ └────────────────────┘ │ 🟢 Passport           │
│         │                         │ 🟢 Driver's License   │
│         │ ┌─ Petr Svoboda ────┐ │ 🟡 Medical Exam       │
│         │ │ #DRV-0002          │ │ 🔴 ADR Certificate    │
│         │ │ 🟡 Warning (1)     │ │ ⚪ A1 Switzerland     │
│         │ │ 🇨🇿 CZ, Kladno     │ │                       │
│         │ └────────────────────┘ │ [Upload Document]     │
│         │                         │                       │
│         │ [More drivers...]       │                       │
│         │                         │                       │
│ [150 drivers]  Page 1/8           │                       │
└─────────┴─────────────────────────┴───────────────────────┘
```

**Mobile View:**

```
┌────────────────────────────┐
│ ☰  Drivers          🔍  ⚙️ │
├────────────────────────────┤
│ Filters: Active ▼          │
│                            │
│ ┌────────────────────────┐ │
│ │ Jan Novák #DRV-0001    │ │
│ │ 🟢 Ready               │ │
│ │ 🇨🇿 CZ, Praha          │ │
│ │ [View Details →]       │ │
│ └────────────────────────┘ │
│                            │
│ ┌────────────────────────┐ │
│ │ Petr Svoboda #DRV-0002 │ │
│ │ 🟡 Warning (1 doc)     │ │
│ │ 🇨🇿 CZ, Kladno         │ │
│ │ [View Details →]       │ │
│ └────────────────────────┘ │
│                            │
│ [Load more...]             │
└────────────────────────────┘
```

---

#### Driver Profile Structure

**Overview Tab:**

```
┌──────────────────────────────────────────────┐
│ Jan Novák                          #DRV-0001 │
├──────────────────────────────────────────────┤
│                                              │
│ Status: 🟢 Active                            │
│ Readiness: ✅ Ready for delivery             │
│                                              │
│ Personal Info                                │
│ ├─ Birth Date: 1985-03-15 (40 years)        │
│ ├─ Citizenship: 🇨🇿 Czech Republic           │
│ ├─ Rodné číslo: 850315/1234                 │
│ ├─ Email: jan.novak@driver.cz               │
│ ├─ Phone: +420 777 123 456                  │
│ └─ Address: Praha 3, Vinohradská 123        │
│                                              │
│ Employment                                   │
│ ├─ Hire Date: 2020-01-15                    │
│ ├─ Contract: Indefinite                     │
│ ├─ Work Location: Praha                     │
│ └─ Internal Number: DRV-0001 (never changes)│
│                                              │
│ Documents Summary                            │
│ ├─ 🟢 Valid: 12                             │
│ ├─ 🟡 Expiring: 1                           │
│ ├─ 🔴 Expired: 1                            │
│ └─ ⚪ Missing: 0                             │
│                                              │
│         [Edit Profile]  [Terminate]          │
└──────────────────────────────────────────────┘
```

---

**Documents Tab:**

```
┌──────────────────────────────────────────────┐
│ Documents (14 types)                         │
├──────────────────────────────────────────────┤
│                                              │
│ 🟢 Passport                                  │
│    Number: CZ1234567                         │
│    Valid Until: 2028-05-20                   │
│    📎 passport_scan.pdf (2.1 MB)            │
│    [View] [Replace] [History]               │
│                                              │
│ 🟢 Driver's License                          │
│    Number: DL987654                          │
│    Categories: C, CE, D                      │
│    Valid Until: 2027-03-15                   │
│    📎 drivers_license.pdf (1.8 MB)          │
│    [View] [Replace] [History]               │
│                                              │
│ 🟡 Medical Examination                       │
│    Valid From: 2023-10-01                    │
│    Valid Until: 2025-12-15 (49 days left)   │
│    📎 medical_exam_2023.pdf (0.9 MB)        │
│    ⚠️ Renewal needed soon!                   │
│    [View] [Replace] [Schedule Renewal]      │
│                                              │
│ 🔴 ADR Certificate                           │
│    Valid Until: 2024-08-30 (EXPIRED)        │
│    📎 adr_cert_2022.pdf (1.2 MB)            │
│    ❌ Driver cannot transport dangerous goods│
│    [Upload New Document] [Request from HR]  │
│                                              │
│ ⚪ A1 Switzerland                            │
│    No document uploaded                      │
│    [Upload Document]                         │
│                                              │
│ [+ Upload New Document Type]                 │
└──────────────────────────────────────────────┘
```

---

**Finance Tab:**

```
┌──────────────────────────────────────────────┐
│ Finance - Jan Novák (#DRV-0001)              │
├──────────────────────────────────────────────┤
│                                              │
│ Current Month (October 2025)                 │
│                                              │
│ Base Salary:         50,000 CZK              │
│ Business Trips:      +8,500 CZK              │
│ Bonuses:             +2,000 CZK              │
│ Fines:               -1,500 CZK              │
│ Damages (accidents): -5,000 CZK              │
│ ───────────────────────────────              │
│ NET SALARY:          54,000 CZK              │
│                                              │
│ Transaction History                          │
│ ┌────────────────────────────────────────┐  │
│ │ 🟢 27.10.2025 | Bonus | +2,000 CZK     │  │
│ │    Reason: Urgent delivery completed   │  │
│ │    Order: ORD-2025-0123                │  │
│ │                                        │  │
│ │ 🔴 20.10.2025 | Fine | -500 CZK        │  │
│ │    Reason: Speeding (20 km/h over)     │  │
│ │    Order: ORD-2025-0098                │  │
│ │    Location: D1, km 45                 │  │
│ │                                        │  │
│ │ 🔴 15.10.2025 | Damage | -5,000 CZK    │  │
│ │    Reason: Accident (cargo damaged)    │  │
│ │    Order: ORD-2025-0087                │  │
│ │    Insurance claim: Pending            │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ [Add Transaction] [Export Report]            │
└──────────────────────────────────────────────┘
```

---

**Comments Tab:**

```
┌──────────────────────────────────────────────┐
│ Comments & Notes                             │
├──────────────────────────────────────────────┤
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ 📝 New Comment                         │  │
│ │ [Write comment here_________________]  │  │
│ │                                        │  │
│ │ 📎 Attach file (optional)              │  │
│ │ [Choose file...]                       │  │
│ │                                        │  │
│ │         [Post Comment]                 │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ Comments (5):                                │
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ admin@company.cz | 26.10.2025 14:30    │  │
│ │                                        │  │
│ │ Driver complained about low salary.    │  │
│ │ Discussed with HR, will review in Q4.  │  │
│ │                                        │  │
│ │ 💬 Reply  ✏️ Edit  🗑️ Delete           │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ hr@company.cz | 20.10.2025 09:15       │  │
│ │                                        │  │
│ │ Received complaint from dispatcher     │  │
│ │ about driver attitude. Will monitor.   │  │
│ │                                        │  │
│ │ 📎 complaint_form.pdf                  │  │
│ │                                        │  │
│ │ 💬 Reply  ✏️ Edit  🗑️ Delete           │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ [Load more comments...]                      │
└──────────────────────────────────────────────┘
```

---

**History Tab (Audit Log):**

```
┌──────────────────────────────────────────────┐
│ Activity History                             │
├──────────────────────────────────────────────┤
│                                              │
│ Filters:                                     │
│ ☐ Profile changes  ☐ Documents              │
│ ☐ Comments        ☐ Finance                 │
│ ☐ Status changes  ☑ Show all                │
│                                              │
│ ────────────────────────────────────────     │
│                                              │
│ 🕐 27.10.2025 14:32  admin@company.cz        │
│    📄 Document uploaded: Passport            │
│    File: passport_new_2025.pdf (2.1 MB)     │
│                                              │
│ 🕐 25.10.2025 10:15  hr@company.cz           │
│    🔄 Status changed: Inactive → Active      │
│    Reason: Returned from sick leave         │
│                                              │
│ 🕐 20.10.2025 09:00  system                  │
│    ⚠️ Document expiring soon: Medical Exam   │
│    Alert sent via email                      │
│                                              │
│ 🕐 15.10.2025 16:45  accountant@company.cz   │
│    💰 Fine added: -500 CZK                   │
│    Reason: Speeding                          │
│    Order: ORD-2025-0098                      │
│                                              │
│ 🕐 01.10.2025 08:00  admin@company.cz        │
│    👤 Driver created                         │
│    Internal Number: DRV-0001                 │
│                                              │
│ [Load more history...]                       │
└──────────────────────────────────────────────┘
```

---

#### API Endpoints - Drivers

**Base URL:** `https://api.g-track.eu/api/v1`

**Authentication:** Bearer token (JWT from Auth0)

---

**GET /drivers**

List all drivers with filters

```bash
GET /drivers?status=active&search=jan&per_page=20

Response 200 OK:
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a906-446655440000",
      "internal_number": "DRV-0001",
      "first_name": "Jan",
      "last_name": "Novák",
      "email": "jan.novak@driver.cz",
      "phone": "+420 777 123 456",
      "status": "active",
      "readiness": {
        "is_ready": true,
        "documents": {
          "valid": 12,
          "expiring": 1,
          "expired": 1,
          "missing": 0
        }
      },
      "citizenship": "CZ",
      "work_location": "Praha",
      "created_at": "2025-10-01T08:00:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total": 150,
    "last_page": 8
  }
}
```

---

**GET /drivers/{id}**

Get driver details

```bash
GET /drivers/550e8400-e29b-41d4-a906-446655440000

Response 200 OK:
{
  "id": "550e8400-e29b-41d4-a906-446655440000",
  "internal_number": "DRV-0001",
  "first_name": "Jan",
  "last_name": "Novák",
  "middle_name": null,
  "email": "jan.novak@driver.cz",
  "phone": "+420 777 123 456",
  "birth_date": "1985-03-15",
  "citizenship": "CZ",
  "rodne_cislo": "850315/1234",
  "status": "active",
  "readiness": {
    "is_ready": false,
    "blocking_documents": ["adr_certificate"]
  },
  "employment": {
    "hire_date": "2020-01-15",
    "fire_date": null,
    "contract_from": "2020-01-15",
    "contract_to": null,
    "contract_indefinite": true,
    "work_location": "praha"
  },
  "addresses": {
    "registration": "Praha 3, Vinohradská 123",
    "residence": "Praha 3, Vinohradská 123"
  },
  "banking": {
    "bank_country": "CZ",
    "bank_account": "1234567890",
    "iban": "CZ6508000000001234567890",
    "swift": "GIBACZPX"
  },
  "documents": [
    {
      "id": "doc-uuid-1",
      "type": "passport",
      "number": "CZ1234567",
      "country": "CZ",
      "valid_until": "2028-05-20",
      "status": "valid",
      "days_until_expiry": 945,
      "files": [
        {
          "id": "file-uuid-1",
          "filename": "passport_scan.pdf",
          "size_bytes": 2198234,
          "uploaded_at": "2025-01-15T10:30:00Z"
        }
      ]
    }
  ],
  "created_at": "2025-10-01T08:00:00Z",
  "updated_at": "2025-10-27T14:32:00Z"
}
```

---

**POST /drivers**

Create new driver

```bash
POST /drivers
Content-Type: application/json

{
  "first_name": "Pavel",
  "last_name": "Horák",
  "email": "pavel.horak@driver.cz",
  "phone": "+420 777 987 654",
  "birth_date": "1990-07-20",
  "citizenship": "CZ",
  "status": "active",
  "hire_date": "2025-11-01",
  "contract_indefinite": true,
  "work_location": "kladno",
  "send_invitation": true  // Send email + Telegram instructions
}

Response 201 Created:
{
  "id": "new-uuid",
  "internal_number": "DRV-0151",
  "message": "Driver created successfully",
  "invitation_sent": true
}
```

---

**PUT /drivers/{id}**

Update driver

```bash
PUT /drivers/550e8400-e29b-41d4-a906-446655440000
Content-Type: application/json

{
  "phone": "+420 777 111 222",
  "work_location": "praha",
  "status": "on_leave"
}

Response 200 OK:
{
  "message": "Driver updated successfully"
}
```

---

**DELETE /drivers/{id}**

Soft delete driver

```bash
DELETE /drivers/550e8400-e29b-41d4-a906-446655440000

Response 200 OK:
{
  "message": "Driver deleted successfully"
}
```

---

**POST /drivers/{id}/documents**

Upload document

```bash
POST /drivers/550e8400-e29b-41d4-a906-446655440000/documents
Content-Type: multipart/form-data

{
  "type": "passport",
  "number": "CZ1234567",
  "country": "CZ",
  "valid_until": "2028-05-20",
  "file": <binary>
}

Response 201 Created:
{
  "document_id": "doc-uuid",
  "message": "Document uploaded successfully"
}
```

---

### Module 2: Vehicles & Trailers

**Status:** 🔴 Not Started (Next after Drivers)  
**Types:** LKV (Heavy Trucks) + PKV (Light Vehicles) + Trailers

---

#### Business Logic

**Problem:**
```
❌ No centralized vehicle database
❌ Service schedules tracked in Excel
❌ Fines arrive months late (lost paperwork)
❌ Cannot see which vehicles are available
❌ Accident costs not tracked per vehicle
```

**Solution:**
```
✅ Digital vehicle profiles (technical specs + documents)
✅ Service request system (internal + external)
✅ Fine/accident tracking
✅ Availability dashboard
✅ Cost per vehicle analytics
```

---

#### Vehicle Types

**1. LKV - Heavy Trucks (Nákladní vozidla)**

Used for:
- Long-haul transport
- International deliveries
- Assigned to Orders

Examples:
- MAN TGX 18.440
- Mercedes-Benz Actros
- Scania R450

Documents tracked:
- Vehicle Registration (Technický průkaz)
- Insurance (OSAGO, KASKO)
- Annual Inspection (STK)
- Tachograph Calibration
- CMR Insurance

---

**2. PKV - Light Vehicles (Osobní vozidla)**

Used for:
- Office errands
- Quick deliveries (documents, small cargo)
- Employee transport
- NOT assigned to Orders

Examples:
- Škoda Octavia
- VW Transporter
- Ford Transit

Assignment modes:
```
A) Assigned to specific driver (exclusive use)
B) Pool vehicle (anyone can use)
C) Unassigned (spare)
```

Documents tracked:
- Vehicle Registration
- Insurance
- Annual Inspection

---

**3. Trailers (Návěsy/přívěsy)**

Types:
- Standard (Standard)
- Mega (extra height)
- Frigo (refrigerated)
- Van (enclosed box)
- Tautliner (curtain-side)

Documents tracked:
- Trailer Registration
- Annual Inspection
- Refrigeration Service (if Frigo)

---

#### Transport Unit Concept

**Definition:** Transport Unit = Driver + Vehicle + Trailer

**Ready State:**
```typescript
interface TransportUnit {
    driver: {
        id: string;
        status: 'active';
        all_documents_valid: true;  // All 🟢 or 🟡
    };
    vehicle: {
        id: string;
        type: 'lkv';
        all_documents_valid: true;
        not_in_service: true;
    };
    trailer: {
        id: string;
        type: 'standard' | 'mega' | 'frigo';
        all_documents_valid: true;
        not_in_service: true;
    };
    ready_for_order: true;
}
```

**Order Assignment:**
```
When Dispatcher creates Order:
1. Select Transport Unit from "Ready" list
2. Order.transport_unit_id = [unit_id]
3. System tracks:
   - Which driver drove
   - Which vehicle was used
   - Which trailer was attached
4. If accident/fine → linked to correct driver + vehicle
```

---

#### Sub-Module: Service Management

**Scenario 1: Planned Service (Internal)**

```
1. Vehicle VEH-0045 has 95,000 km
2. System alert: "Service due at 100,000 km"
3. HR/Admin creates Service Request:
   - Type: Scheduled Maintenance
   - Service Provider: Internal Workshop
   - Scheduled Date: 2025-11-05
4. Mechanic performs service:
   - Oil change
   - Brake inspection
   - Filter replacement
5. Cost: 3,500 CZK (internal labor + parts)
6. Vehicle status: Back to Active
```

---

**Scenario 2: Emergency Repair (External)**

```
1. Driver reports: "Strange engine noise"
2. Dispatcher creates Service Request:
   - Priority: 🔴 High
   - Location: Wrocław, Poland
   - Issue: Engine noise
3. System finds nearby services:
   - Auto Service PL (5 km) ⭐ 4.5/5
   - MAN Service Center (12 km) ⭐ 4.8/5
4. Dispatcher selects: Auto Service PL
5. Service completed:
   - Invoice uploaded: 500 EUR (Reverse Charge)
   - Work done: Alternator replacement
6. Expense logged:
   - vehicle_expenses table
   - Category: External Service
   - VAT mode: Reverse Charge (0%)
```

---

#### Sub-Module: Fines & Accidents

**Scenario: Speeding Fine**

```
1. Fine letter arrives:
   - Vehicle: VEH-0045 (MAN TGX 18.440)
   - Date: 2025-10-15, 14:30
   - Location: D1, km 45 (Czech Republic)
   - Offense: Speeding (140 km/h in 120 zone)
   - Amount: 500 CZK
   
2. Admin checks: Who was driving?
   - Lookup Order history for that date/time
   - Order: ORD-2025-0098
   - Driver: Jan Novák (#DRV-0001)
   
3. System creates transaction:
   - Fine added to driver_transactions
   - Deducted from driver's salary
   - Linked to Order (profitability impact)
   
4. History logs:
   - Vehicle VEH-0045: "Fine: 500 CZK (Speeding)"
   - Driver DRV-0001: "Fine: -500 CZK (Speeding, Order ORD-2025-0098)"
   - Order ORD-2025-0098: "Fine expense: 500 CZK"
```

---

**Scenario: Accident**

```
1. Driver calls: "Accident on highway"
   - Vehicle: VEH-0045
   - Order: ORD-2025-0087
   - Damage: Cargo damaged, truck body dented
   
2. Dispatcher creates Accident Report:
   - Photos uploaded (via mobile)
   - Police report number
   - Damage estimate: 50,000 CZK
   
3. Vehicle status → "In Repair"
   
4. Insurance claim initiated:
   - Claim #: INS-2025-123
   - Status: Pending
   
5. Repair completed:
   - Invoice from body shop: 48,000 CZK
   - Insurance pays: 40,000 CZK
   - Company pays: 8,000 CZK
   - Driver pays: 5,000 CZK (deductible from salary)
   
6. Financial impact:
   - Order ORD-2025-0087 profitability: -8,000 CZK
   - Driver DRV-0001 salary: -5,000 CZK
   - Vehicle VEH-0045 total costs YTD: +48,000 CZK
```

---

#### Database Schema - Vehicles

```sql
-- Vehicles (trucks + light vehicles)
CREATE TABLE vehicles (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    office_id UUID,
    
    -- Identification
    internal_number VARCHAR(20) UNIQUE, -- VEH-0001
    type VARCHAR(10), -- 'lkv' or 'pkv'
    identifier VARCHAR(50), -- User-friendly name
    
    -- Technical specs
    make VARCHAR(100), -- MAN, Mercedes, Škoda
    model VARCHAR(100), -- TGX 18.440
    year INT,
    vin VARCHAR(50),
    plate_number VARCHAR(20),
    
    -- Status
    status VARCHAR(20), -- 'active', 'in_service', 'inactive', 'sold'
    
    -- Assignment (for PKV)
    assignment_mode VARCHAR(20), -- 'assigned', 'pool', 'unassigned'
    assigned_driver_id UUID,
    
    -- Specs
    fuel_type VARCHAR(20),
    engine_capacity_cc INT,
    max_weight_kg INT,
    euro_class VARCHAR(10), -- Euro 5, Euro 6
    
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- Trailers
CREATE TABLE trailers (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    office_id UUID,
    
    internal_number VARCHAR(20) UNIQUE, -- TRL-0001
    type VARCHAR(20), -- 'standard', 'mega', 'frigo', 'van', 'tautliner'
    identifier VARCHAR(50),
    
    make VARCHAR(100),
    model VARCHAR(100),
    year INT,
    plate_number VARCHAR(20),
    
    status VARCHAR(20),
    
    -- Frigo specs
    has_refrigeration BOOLEAN DEFAULT false,
    min_temp_celsius DECIMAL(4,1),
    max_temp_celsius DECIMAL(4,1),
    
    created_at TIMESTAMPTZ
);

-- Transport Units (combinations)
CREATE TABLE transport_units (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    
    driver_id UUID NOT NULL,
    vehicle_id UUID NOT NULL,
    trailer_id UUID,
    
    is_ready BOOLEAN, -- computed from document statuses
    
    assigned_at TIMESTAMPTZ,
    unassigned_at TIMESTAMPTZ,
    
    UNIQUE (driver_id, vehicle_id, trailer_id, unassigned_at)
);

-- Vehicle documents
CREATE TABLE vehicle_documents (
    id UUID PRIMARY KEY,
    vehicle_id UUID NOT NULL,
    
    type VARCHAR(50), -- 'registration', 'insurance', 'inspection', 'tachograph'
    number VARCHAR(100),
    valid_from DATE,
    valid_until DATE,
    
    status VARCHAR(20), -- 'valid', 'expiring_soon', 'expired', 'no_data'
    days_until_expiry INT,
    
    created_at TIMESTAMPTZ
);

-- Service requests
CREATE TABLE service_requests (
    id UUID PRIMARY KEY,
    request_number VARCHAR(50) UNIQUE, -- SR-2025-001
    company_id UUID NOT NULL,
    
    vehicle_id UUID NOT NULL,
    driver_id UUID,
    
    issue_description TEXT,
    priority VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    status VARCHAR(20), -- 'open', 'in_progress', 'completed', 'cancelled'
    
    service_type VARCHAR(20), -- 'internal' or 'external'
    service_provider_id UUID,
    
    scheduled_date DATE,
    completed_date DATE,
    
    cost DECIMAL(10,2),
    currency CHAR(3),
    vat_mode VARCHAR(20),
    
    invoice_file_id UUID,
    
    created_by UUID,
    created_at TIMESTAMPTZ
);

-- Vehicle expenses (repairs, fines, fuel)
CREATE TABLE vehicle_expenses (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    
    vehicle_id UUID NOT NULL,
    order_id UUID, -- if related to order
    service_request_id UUID,
    
    type VARCHAR(50), -- 'service', 'repair', 'fine', 'fuel', 'accident'
    amount DECIMAL(10,2),
    currency CHAR(3),
    vat_mode VARCHAR(20),
    description TEXT,
    
    expense_date DATE,
    invoice_file_id UUID,
    
    created_by UUID,
    created_at TIMESTAMPTZ
);
```

---

### Module 3: Customers (Migration from OLD)

**Status:** 🟡 90% Complete in OLD version (needs migration to v2)  
**Action:** Mark "Coming Soon" until Drivers finished

---

#### Business Logic

**Types:**

1. **Customer** - Companies ordering transport
2. **Carrier** - External transport companies (subcontractors)
3. **Both** - Company can be both customer AND carrier

---

#### Key Features

**Credit Limit Management:**

```typescript
Available Credit = Credit Limit - ∑(Open Orders)

Open Orders = Orders where status NOT IN ('payment_received', 'closed', 'cancelled')

Example:
Credit Limit: 10,000 EUR
Open Order #1: 3,000 EUR (in_transit)
Open Order #2: 2,500 EUR (delivered)
Open Order #3: 1,500 EUR (confirmed)
─────────────────────────────────
Used: 7,000 EUR
Available: 3,000 EUR

Validation:
- Can create new order for 2,800 EUR → ✅ OK
- Cannot create order for 3,500 EUR → ❌ Exceeds limit
```

**Alert Logic:**
```
IF Available Credit < 1,000 EUR:
    Show warning: "Low credit limit for this customer"
    
IF Available Credit < 0:
    Block new order creation
    Show error: "Customer credit limit exceeded"
```

---

#### EU VAT Validation

**VAT ID Format:**

```
CZ12345678 (Czech Republic)
PL8992982297 (Poland)
DE123456789 (Germany)
ATU12345678 (Austria)
```

**Validation Service:**
```php
// Validate VAT ID via EU VIES system
public function validateVatId(string $vatId): bool
{
    // Call EU VIES web service
    $client = new SoapClient("http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl");
    
    $countryCode = substr($vatId, 0, 2);
    $vatNumber = substr($vatId, 2);
    
    $result = $client->checkVat([
        'countryCode' => $countryCode,
        'vatNumber' => $vatNumber
    ]);
    
    return $result->valid;
}
```

---

#### Database Schema - Customers

```sql
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL, -- tenant
    
    -- Identification
    internal_number VARCHAR(20) UNIQUE, -- CUST-0001
    company_name VARCHAR(200),
    type VARCHAR(20), -- 'customer', 'carrier', 'both'
    
    -- VAT
    vat_number VARCHAR(50),
    vat_validated_at TIMESTAMPTZ,
    
    -- Contact
    email VARCHAR(255),
    email_accounting VARCHAR(255),
    phone VARCHAR(50),
    
    -- Address
    country_code CHAR(2),
    postcode VARCHAR(20),
    city VARCHAR(100),
    street VARCHAR(200),
    
    -- Financial
    currency CHAR(3) DEFAULT 'EUR',
    terms_of_payment INT DEFAULT 30, -- days
    credit_limit DECIMAL(10,2),
    available_credit_limit DECIMAL(10,2), -- computed
    
    -- Rating
    rating VARCHAR(20), -- 'excellent', 'good', 'neutral', 'poor'
    
    -- Logistics
    pallet_balance INT DEFAULT 0, -- EUR pallets balance
    
    created_at TIMESTAMPTZ
);

-- Bank accounts (multiple per customer)
CREATE TABLE customer_bank_accounts (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    
    bank_name VARCHAR(200),
    swift VARCHAR(11),
    iban VARCHAR(34),
    is_default BOOLEAN DEFAULT false,
    
    created_at TIMESTAMPTZ
);
```

---

### Module 4: Orders (Migration from OLD)

**Status:** 🟡 85% Complete in OLD version (needs migration + fixes)  
**Action:** Mark "Coming Soon"

---

#### Order Status Flow (9 Statuses)

```
1. Draft
   ↓ (HR/Dispatcher confirms order)
2. Open
   ↓ (Transport Unit assigned)
3. In Progress
   ↓ (Cargo loaded, CMR signed)
4. Loaded
   ↓ (Cargo delivered, POD signed)
5. Unloaded
   ↓ (CMR + POD uploaded → automatic)
6. Ready for Invoice
   ↓ (Accountant creates invoice → automatic)
7. Invoice Sent
   ↓ (Payment received in full)
8. Payment Received / Closed
   
OR (Payment received partially)
   
9. Partly Paid
   ↓ (Remaining payment received)
8. Payment Received / Closed
```

**Automatic Transitions:**

```php
// Order reaches "Unloaded" + CMR + POD uploaded
if ($order->status === 'unloaded' 
    && $order->hasCMR() 
    && $order->hasPOD()) {
    $order->status = 'ready_for_invoice';
    $order->save();
}

// Invoice created and sent
if ($invoice->status === 'sent') {
    $order = $invoice->order;
    $order->status = 'invoice_sent';
    $order->save();
}

// Payment received
if ($payment->amount >= $invoice->total_amount) {
    $invoice->status = 'paid';
    $order->status = 'payment_received';
} else {
    $order->status = 'partly_paid';
}
```

---

#### Order Structure

**Key Fields:**

```typescript
interface Order {
    // Identification
    id: string;
    order_number: string; // YYYYMMDD-XXX (e.g., 20251027-001)
    
    // Customer
    customer_id: string;
    client_reference: string; // Customer's internal order number
    order_price: number;
    currency: string;
    order_issued_by: string; // user who created order
    
    // Route
    loading_addresses: LoadingPoint[];
    unloading_addresses: UnloadingPoint[];
    
    // Cargo
    cargo_description: string;
    trailer_type: 'standard' | 'mega' | 'frigo' | 'van';
    adr: boolean; // dangerous goods
    pallets: boolean;
    temperature_required: boolean;
    temperature_value?: number; // if frigo
    weight_kg: number;
    
    // Transport
    transport_unit_id: string; // Driver + Vehicle + Trailer
    driver_id: string;
    vehicle_id: string;
    trailer_id: string;
    
    // Distances
    empty_km: number; // from office to loading point
    total_km: number; // total trip distance
    
    // Carrier (if external)
    carrier_id?: string;
    carrier_price?: number; // cost from carrier
    
    // Financial
    vat_mode: 'domestic' | 'reverse_charge' | 'non_vat';
    vat_rate: number;
    vat_amount: number;
    total_amount: number;
    revenue: number; // order_price - carrier_price
    
    // Dates
    pickup_scheduled: Date;
    pickup_actual?: Date;
    delivery_scheduled: Date;
    delivery_actual?: Date;
    
    // Documents
    order_file_id?: string; // PDF from customer
    cmr_file_id?: string;
    pod_file_id?: string;
    carrier_invoice_file_id?: string;
    
    // Status
    status: OrderStatus;
}
```

---

#### Order Profitability

**Calculation:**

```typescript
interface OrderProfitability {
    // Income
    revenue_from_customer: number; // order_price
    
    // Expenses
    expenses: {
        driver_salary: number; // calculated from driver rate
        fuel_cost: number; // estimated or actual
        carrier_cost: number; // if external carrier used
        fines: number; // driver fines during this order
        damages: number; // cargo damage, accidents
        tolls: number; // highway tolls
        other: number;
    };
    
    total_expenses: number; // sum of all expenses
    
    // Result
    net_profit: number; // revenue - total_expenses
    profit_margin: number; // (net_profit / revenue) * 100
}
```

**Example:**

```
Order: ORD-2025-0123
Route: Praha → Berlin → Praha

Income:
├─ Customer pays: 1,200 EUR

Expenses:
├─ Driver salary (2 days): 200 EUR
├─ Fuel (1,500 km): 450 EUR
├─ Tolls (D1, D8): 80 EUR
├─ Fine (speeding): 50 EUR
├─ Total expenses: 780 EUR

Net Profit: 1,200 - 780 = 420 EUR
Profit Margin: (420 / 1,200) * 100 = 35%
```

---

#### Database Schema - Orders

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    order_number VARCHAR(50) UNIQUE,
    
    -- Customer
    customer_id UUID NOT NULL,
    client_reference VARCHAR(100),
    order_price DECIMAL(10,2),
    currency CHAR(3) DEFAULT 'EUR',
    
    -- Transport
    transport_unit_id UUID,
    driver_id UUID,
    vehicle_id UUID,
    trailer_id UUID,
    
    -- Route
    loading_addresses JSONB, -- array of points
    unloading_addresses JSONB,
    
    -- Cargo
    cargo_description TEXT,
    trailer_type VARCHAR(20),
    adr BOOLEAN DEFAULT false,
    pallets BOOLEAN DEFAULT false,
    temperature_required BOOLEAN DEFAULT false,
    temperature_value DECIMAL(4,1),
    weight_kg DECIMAL(8,2),
    
    -- Distances
    empty_km INT,
    total_km INT,
    
    -- Carrier
    carrier_id UUID,
    carrier_price DECIMAL(10,2),
    
    -- VAT
    vat_mode VARCHAR(20),
    vat_rate DECIMAL(4,2),
    vat_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    
    -- Dates
    pickup_scheduled TIMESTAMPTZ,
    pickup_actual TIMESTAMPTZ,
    delivery_scheduled TIMESTAMPTZ,
    delivery_actual TIMESTAMPTZ,
    
    -- Status
    status VARCHAR(30),
    
    -- Documents
    order_file_id UUID,
    cmr_file_id UUID,
    pod_file_id UUID,
    carrier_invoice_file_id UUID,
    
    created_by UUID,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- Order profitability (calculated)
CREATE TABLE order_profitability (
    id UUID PRIMARY KEY,
    order_id UUID UNIQUE NOT NULL,
    
    revenue DECIMAL(10,2),
    
    expenses JSONB, -- detailed breakdown
    total_expenses DECIMAL(10,2),
    
    net_profit DECIMAL(10,2),
    profit_margin DECIMAL(5,2),
    
    updated_at TIMESTAMPTZ
);
```

---

### Module 5: Invoices (Migration from OLD)

**Status:** 🔴 20% Complete in OLD version (needs major development)  
**Action:** Mark "Coming Soon"

---

#### Business Logic

**Invoice Creation Flow:**

```
1. Order reaches "Ready for Invoice" status
   ↓
2. Accountant clicks "Create Invoice"
   ↓
3. System pre-fills:
   - Customer info
   - Order details
   - VAT mode (auto-detected)
   - Amount (from order_price)
   ↓
4. Accountant reviews/adjusts
   ↓
5. Save as Draft → Review → Send
   ↓
6. PDF generated + sent via email
   ↓
7. Order status → "Invoice Sent"
```

---

#### EU VAT Modes

**Automatic Detection:**

```php
function determineVatMode(Customer $customer, Company $company): string
{
    $customerEU = in_array($customer->country_code, EU_COUNTRIES);
    $companyEU = in_array($company->country_code, EU_COUNTRIES);
    
    // Both in EU, different countries → Reverse Charge
    if ($customerEU && $companyEU 
        && $customer->country_code !== $company->country_code 
        && $customer->vat_number) {
        return 'reverse_charge'; // 0% VAT
    }
    
    // Same country → Domestic
    if ($customer->country_code === $company->country_code) {
        return 'domestic'; // full VAT
    }
    
    // Customer without VAT number
    if (!$customer->vat_number) {
        return 'non_vat'; // 0% VAT (special case)
    }
    
    return 'domestic'; // default
}
```

**VAT Rates by Country:**

```php
const VAT_RATES = [
    'CZ' => 21.00,
    'PL' => 23.00,
    'DE' => 19.00,
    'AT' => 20.00,
    'NL' => 21.00,
    'IT' => 22.00,
];
```

---

#### Invoice PDF Template

**Example (Reverse Charge):**

```
╔═══════════════════════════════════════════════════════╗
║                  FAKTURA / INVOICE                    ║
║                                                       ║
║   Číslo / Number: INV-2025-0123                       ║
║   Datum vystavení / Issue Date: 27.10.2025            ║
║   Datum splatnosti / Due Date: 26.11.2025 (30 days)   ║
╚═══════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────┐
│ DODAVATEL / SUPPLIER                                  │
├───────────────────────────────────────────────────────┤
│ Trans Logistics s.r.o.                                │
│ Vinohradská 123, 130 00 Praha 3                       │
│ Česká republika / Czech Republic                      │
│                                                       │
│ IČ / VAT ID: CZ12345678                               │
│ Email: accounting@translogistics.cz                   │
│ Tel: +420 123 456 789                                 │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│ ODBĚRATEL / CUSTOMER                                  │
├───────────────────────────────────────────────────────┤
│ GoldenScreen s.r.o.                                   │
│ Ul. Przykładowa 45, 00-001 Warszawa                   │
│ Polska / Poland                                       │
│                                                       │
│ NIP / VAT ID: PL8992982297                            │
│ Email: ap@goldenscreen.pl                             │
└───────────────────────────────────────────────────────┘

┌────────────────────────────────────────────┬──────────┐
│ POPIS / DESCRIPTION                        │ ČÁSTKA   │
├────────────────────────────────────────────┼──────────┤
│ Dopravní služby / Transport Services      │          │
│                                            │          │
│ Trasa / Route:                             │          │
│ Praha (CZ) → Warszawa (PL)                 │          │
│                                            │          │
│ Č. objednávky / Order: ORD-2025-0123       │          │
│ Datum přepravy / Date: 15.10.2025          │          │
│ Náklad / Cargo: 20 palet / pallets         │          │
│                                            │          │
│ Cena bez DPH / Price excl. VAT:            │ 1,000.00 │
│ DPH 0% (Reverse Charge)                    │     0.00 │
├────────────────────────────────────────────┼──────────┤
│ CELKEM K ÚHRADĚ / TOTAL DUE                │ 1,000.00 │
└────────────────────────────────────────────┴──────────┘

Currency: EUR

Platební údaje / Payment Details:
IBAN: CZ65 0800 0000 1920 0014 5399
SWIFT: GIBACZPX
Bank: Česká spořitelna

Poznámka / Note:
Režim přenesení daňové povinnosti dle čl. 196 směrnice 
o DPH 2006/112/ES
VAT reverse charge applies per Art. 196 of the VAT 
Directive 2006/112/EC

───────────────────────────────────────────────────────
Vystavil / Issued by: Petr Novák
accounting@translogistics.cz
```

---

#### Database Schema - Invoices

```sql
CREATE TABLE invoices (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    
    -- Identification
    invoice_number VARCHAR(50) UNIQUE, -- INV-2025-0123
    
    -- Related
    order_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    
    -- Dates
    issue_date DATE,
    due_date DATE,
    payment_date DATE,
    
    -- VAT
    vat_mode VARCHAR(20), -- 'domestic', 'reverse_charge', 'non_vat'
    vat_rate DECIMAL(4,2),
    vat_note TEXT, -- "VAT reverse charge applies..."
    
    -- Amounts
    subtotal DECIMAL(10,2), -- without VAT
    vat_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2), -- with VAT
    
    amount_paid DECIMAL(10,2) DEFAULT 0,
    amount_remaining DECIMAL(10,2), -- total - paid
    
    currency CHAR(3),
    
    -- Status
    status VARCHAR(20), -- 'draft', 'sent', 'paid', 'overdue', 'cancelled'
    
    -- PDF
    pdf_file_id UUID,
    pdf_generated_at TIMESTAMPTZ,
    
    created_by UUID,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- Payment tracking
CREATE TABLE invoice_payments (
    id UUID PRIMARY KEY,
    invoice_id UUID NOT NULL,
    
    amount DECIMAL(10,2),
    currency CHAR(3),
    payment_date DATE,
    payment_method VARCHAR(50), -- 'bank_transfer', 'cash', 'card'
    reference VARCHAR(100), -- bank transaction reference
    
    notes TEXT,
    
    created_by UUID,
    created_at TIMESTAMPTZ
);
```

---

## 💰 FINANCIAL SYSTEM

### Driver Finance Tracking

**Salary Calculation:**

```typescript
interface DriverSalary {
    base_salary: number; // Fixed monthly
    business_trips_allowance: number; // Per-diem * days
    bonuses: number; // Performance bonuses
    fines: number; // Negative (speeding, etc.)
    damages: number; // Negative (cargo damage, accidents)
    
    gross_salary: number; // base + trips + bonuses - fines - damages
    tax_deductions: number; // Income tax + social insurance
    net_salary: number; // gross - tax
}
```

**Example:**

```
Driver: Jan Novák (#DRV-0001)
Month: October 2025

Base Salary:         50,000 CZK
Business Trips:      +8,500 CZK (17 days × 500 CZK)
Bonuses:             +2,000 CZK (urgent delivery bonus)
Fines:               -1,500 CZK (2× speeding)
Damages:             -5,000 CZK (cargo damage, accident)
─────────────────────────────────────────
Gross Salary:        54,000 CZK

Tax (15%):           -8,100 CZK
Social Insurance:    -3,500 CZK
─────────────────────────────────────────
NET SALARY:          42,400 CZK
```

---

### Order Profitability Tracking

**Real-time Calculation:**

```typescript
// When order is closed
function calculateOrderProfitability(order: Order): Profitability {
    const revenue = order.order_price;
    
    const expenses = {
        driver_salary: calculateDriverCost(order),
        fuel: estimateFuelCost(order.total_km),
        carrier: order.carrier_price || 0,
        fines: getFinesForOrder(order.id),
        damages: getDamagesForOrder(order.id),
        tolls: getHollsForOrder(order.id),
        other: getOtherExpenses(order.id),
    };
    
    const totalExpenses = Object.values(expenses).reduce((a, b) => a + b, 0);
    const netProfit = revenue - totalExpenses;
    const profitMargin = (netProfit / revenue) * 100;
    
    return {
        revenue,
        expenses,
        totalExpenses,
        netProfit,
        profitMargin
    };
}
```

---

### Financial Dashboard

**View 1: By Driver**

```
┌──────────────────────────────────────────────┐
│ Driver Performance (October 2025)            │
├──────────────────────────────────────────────┤
│                                              │
│ Top Performers:                              │
│ 1. Jan Novák (#DRV-0001)                     │
│    Orders completed: 12                      │
│    Revenue generated: 15,000 EUR             │
│    Net profit: 5,500 EUR (37%)               │
│    Fines/Damages: -500 EUR                   │
│                                              │
│ 2. Petr Svoboda (#DRV-0002)                  │
│    Orders completed: 10                      │
│    Revenue generated: 12,000 EUR             │
│    Net profit: 4,200 EUR (35%)               │
│    Fines/Damages: 0 EUR                      │
│                                              │
│ Bottom Performers:                           │
│ 25. Pavel Horák (#DRV-0025)                  │
│    Orders completed: 3                       │
│    Revenue generated: 3,500 EUR              │
│    Net profit: -500 EUR (LOSS)               │
│    Fines/Damages: -2,000 EUR (accident)      │
└──────────────────────────────────────────────┘
```

---

**View 2: By Vehicle**

```
┌──────────────────────────────────────────────┐
│ Vehicle Expenses (October 2025)              │
├──────────────────────────────────────────────┤
│                                              │
│ Most Expensive:                              │
│ 1. VEH-0045 (MAN TGX 18.440)                 │
│    Service: 2 times, 5,000 EUR               │
│    Repairs: 1 accident, 48,000 CZK           │
│    Fines: 3 times, 1,500 CZK                 │
│    TOTAL: 54,500 CZK                         │
│                                              │
│ 2. VEH-0012 (Mercedes Actros)                │
│    Service: 1 time, 3,500 CZK                │
│    Repairs: None                             │
│    Fines: 1 time, 500 CZK                    │
│    TOTAL: 4,000 CZK                          │
└──────────────────────────────────────────────┘
```

---

**View 3: Overall (Company)**

```
┌──────────────────────────────────────────────┐
│ Company Financial Overview (October 2025)    │
├──────────────────────────────────────────────┤
│                                              │
│ INCOME                                       │
│ ├─ Orders revenue:      +150,000 EUR         │
│ └─ Other income:        +2,000 EUR           │
│                                              │
│ EXPENSES                                     │
│ ├─ Driver salaries:     -45,000 EUR          │
│ ├─ Business trips:      -12,000 EUR          │
│ ├─ Vehicle expenses:    -25,000 EUR          │
│ ├─ Fuel:                -20,000 EUR          │
│ ├─ Fines (returned):    +3,500 EUR           │
│ ├─ Office rent:         -5,000 EUR           │
│ └─ Software (G-Track):  -88 EUR              │
│                                              │
│ ═══════════════════════════════════════      │
│ NET PROFIT:             +48,412 EUR          │
│ PROFIT MARGIN:          31.8%                │
└──────────────────────────────────────────────┘
```

---

## 🌍 INTERNATIONALIZATION (i18n)

### Supported Languages

**MVP (Launch):**
- 🇷🇺 Russian (Русский)
- 🇬🇧 English (English)
- 🇨🇿 Czech (Čeština)
- 🇵🇱 Polish (Polski)
- 🇩🇪 German (Deutsch)

**Roadmap:**
- 🇮🇹 Italian (Italiano)
- 🇳🇱 Dutch (Nederlands)
- 🇫🇷 French (Français)
- 🇪🇸 Spanish (Español)

---

### Language Selection Hierarchy

```
1. User-level (personal preference)
   └─ Overrides everything
   
2. Company-level (default for all users)
   └─ Applied on registration
   
3. Browser-level (detected from Accept-Language header)
   └─ Used only for login page before authentication
```

---

### Implementation (Angular)

**Setup:**

```typescript
// app.config.ts
import { provideTranslateService, TranslateLoader } from '@ngx-translate/core';
import { HttpClient } from '@angular/common/http';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideTranslateService({
      defaultLanguage: 'en',
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient]
      }
    })
  ]
};
```

**Translation Files:**

```
src/assets/i18n/
├── en.json  (English)
├── ru.json  (Russian)
├── cs.json  (Czech)
├── pl.json  (Polish)
└── de.json  (German)
```

**Example - en.json:**

```json
{
  "COMMON": {
    "SAVE": "Save",
    "CANCEL": "Cancel",
    "DELETE": "Delete",
    "EDIT": "Edit",
    "SEARCH": "Search",
    "FILTER": "Filter"
  },
  "DRIVERS": {
    "TITLE": "Drivers",
    "ADD_DRIVER": "Add Driver",
    "READINESS": {
      "READY": "Ready for delivery",
      "NOT_READY": "Not ready",
      "WARNING": "Warning"
    },
    "DOCUMENTS": {
      "PASSPORT": "Passport",
      "DRIVERS_LICENSE": "Driver's License",
      "MEDICAL_EXAM": "Medical Examination",
      "ADR_CERTIFICATE": "ADR Certificate"
    },
    "STATUS": {
      "ACTIVE": "Active",
      "ON_LEAVE": "On Leave",
      "INACTIVE": "Inactive",
      "TERMINATED": "Terminated"
    }
  }
}
```

**Example - cs.json:**

```json
{
  "COMMON": {
    "SAVE": "Uložit",
    "CANCEL": "Zrušit",
    "DELETE": "Smazat",
    "EDIT": "Upravit",
    "SEARCH": "Hledat",
    "FILTER": "Filtr"
  },
  "DRIVERS": {
    "TITLE": "Řidiči",
    "ADD_DRIVER": "Přidat řidiče",
    "READINESS": {
      "READY": "Připraven k přepravě",
      "NOT_READY": "Nepřipraven",
      "WARNING": "Varování"
    },
    "DOCUMENTS": {
      "PASSPORT": "Pas",
      "DRIVERS_LICENSE": "Řidičský průkaz",
      "MEDICAL_EXAM": "Lékařská prohlídka",
      "ADR_CERTIFICATE": "ADR certifikát"
    },
    "STATUS": {
      "ACTIVE": "Aktivní",
      "ON_LEAVE": "Na dovolené",
      "INACTIVE": "Neaktivní",
      "TERMINATED": "Ukončen"
    }
  }
}
```

**Usage in Components:**

```typescript
// Component
export class DriversListComponent {
  constructor(private translate: TranslateService) {
    // Switch language
    this.translate.use('cs'); // Czech
  }
  
  getReadinessText(driver: Driver): string {
    return driver.isReady 
      ? this.translate.instant('DRIVERS.READINESS.READY')
      : this.translate.instant('DRIVERS.READINESS.NOT_READY');
  }
}
```

```html
<!-- Template -->
<h1>{{ 'DRIVERS.TITLE' | translate }}</h1>

<button mat-raised-button>
  {{ 'DRIVERS.ADD_DRIVER' | translate }}
</button>

<mat-select [(value)]="selectedLanguage" (selectionChange)="switchLanguage($event)">
  <mat-option value="en">🇬🇧 English</mat-option>
  <mat-option value="ru">🇷🇺 Русский</mat-option>
  <mat-option value="cs">🇨🇿 Čeština</mat-option>
  <mat-option value="pl">🇵🇱 Polski</mat-option>
  <mat-option value="de">🇩🇪 Deutsch</mat-option>
</mat-select>
```

---

### Date/Time/Number Formatting

**Angular Pipes with Locales:**

```typescript
// app.config.ts
import { registerLocaleData } from '@angular/common';
import localeCs from '@angular/common/locales/cs';
import localePl from '@angular/common/locales/pl';
import localeDe from '@angular/common/locales/de';
import localeRu from '@angular/common/locales/ru';

registerLocaleData(localeCs);
registerLocaleData(localePl);
registerLocaleData(localeDe);
registerLocaleData(localeRu);
```

```html
<!-- Template -->
<!-- Date formatting based on locale -->
<p>{{ driver.hire_date | date:'short':'':currentLocale }}</p>

<!-- Czech: 27. 10. 2025 14:30 -->
<!-- English: 10/27/2025, 2:30 PM -->
<!-- German: 27.10.2025, 14:30 -->

<!-- Currency formatting -->
<p>{{ order.total_amount | currency:order.currency:'symbol':'1.2-2':currentLocale }}</p>

<!-- Czech: 1 000,00 Kč -->
<!-- English: €1,000.00 -->
<!-- Polish: 1 000,00 zł -->
```

---

### Email Templates (Multi-language)

**Template Structure:**

```
resources/views/emails/
├── drivers/
│   ├── invitation_en.blade.php
│   ├── invitation_cs.blade.php
│   ├── invitation_pl.blade.php
│   ├── invitation_de.blade.php
│   └── invitation_ru.blade.php
└── shared/
    └── header.blade.php
```

**Dynamic Template Selection:**

```php
// Laravel Mail
Mail::to($driver->email)
    ->send(new DriverInvitation($driver, $preferredLanguage));

// Mail class
class DriverInvitation extends Mailable
{
    public function build()
    {
        $template = "emails.drivers.invitation_{$this->language}";
        
        return $this->view($template)
                    ->subject($this->getSubject());
    }
    
    private function getSubject(): string
    {
        return match($this->language) {
            'cs' => 'Pozvánka do G-Track TMS',
            'pl' => 'Zaproszenie do G-Track TMS',
            'de' => 'Einladung zu G-Track TMS',
            'ru' => 'Приглашение в G-Track TMS',
            default => 'Invitation to G-Track TMS',
        };
    }
}
```

---

## 🎨 UI/UX ARCHITECTURE

### Layout Structure

**Desktop Layout:**

```
┌──────────────────────────────────────────────────────┐
│ Top Bar (Header)                                     │
├────────┬─────────────────────────────────────────────┤
│        │                                             │
│ Side   │ Main Content Area                          │
│ bar    │                                             │
│        │                                             │
│ (Nav)  │                                             │
│        │                                             │
│        │                                             │
│        │                                             │
│        │                                             │
└────────┴─────────────────────────────────────────────┘
```

---

**Top Bar Components:**

```
┌──────────────────────────────────────────────────────┐
│ [☰] G-Track    [🔍 Global Search...]  [🔔] [👤] [⚙️] │
└──────────────────────────────────────────────────────┘

Components:
├─ [☰] Burger Menu (toggle sidebar on mobile)
├─ G-Track Logo + App Name
├─ [🔍] Global Search (Ctrl+K / Cmd+K)
├─ [🔔] Notifications (badge with count)
├─ [👤] User Profile Menu
└─ [⚙️] Settings
```

---

**Sidebar Navigation:**

```
┌────────────────────┐
│ [Dashboard] 📊     │
├────────────────────┤
│ OPERATIONS         │
│ Drivers 🚗         │
│ Vehicles 🚛        │
│ Orders 📦          │
│                    │
│ FINANCE            │
│ Invoices 💰        │
│ Payments 💳        │
│                    │
│ ADMIN              │
│ Customers 👥       │
│ Users ⚙️           │
│ Settings 🔧        │
└────────────────────┘

States:
├─ Expanded (default on desktop)
└─ Collapsed (icon-only, toggle with [☰])
```

---

**Mobile Layout:**

```
┌──────────────────────┐
│ [☰] G-Track   [🔍] [👤]│
├──────────────────────┤
│                      │
│ Main Content         │
│ (Full Width)         │
│                      │
│                      │
│                      │
│                      │
│                      │
│                      │
├──────────────────────┤
│ Bottom Navigation    │
│ [📊] [🚗] [📦] [⚙️]  │
└──────────────────────┘
```

---

### View Modes

**Split View (Default for Desktop):**

```
┌──────────────────────────────┬───────────────────────┐
│ List (40% width)             │ Detail (60% width)    │
├──────────────────────────────┼───────────────────────┤
│ [Search...]                  │ Jan Novák #DRV-0001   │
│ [Filters ▼]                  │                       │
│                              │ Tabs:                 │
│ ┌─ Jan Novák ────────────┐  │ • Overview            │
│ │ #DRV-0001              │◄─┼─• Documents          │
│ │ 🟢 Ready               │  │ • Finance             │
│ └────────────────────────┘  │ • Comments            │
│                              │                       │
│ ┌─ Petr Svoboda ────────┐  │ [Content here...]     │
│ │ #DRV-0002              │  │                       │
│ │ 🟡 Warning             │  │                       │
│ └────────────────────────┘  │                       │
└──────────────────────────────┴───────────────────────┘
```

---

**Full Screen View (Optional):**

```
┌──────────────────────────────────────────────────────┐
│ [← Back to List]  Jan Novák #DRV-0001                │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Tabs: Overview | Documents | Finance | Comments     │
│                                                      │
│ [Full width content...]                              │
│                                                      │
│                                                      │
│                                                      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Trigger:** Click "Expand" icon or double-click item

---

### Global Search (Cmd+K / Ctrl+K)

**Functionality:**

- Search ALL modules at once
- Fuzzy search (typo-tolerant)
- Recent searches saved
- Keyboard navigation

**Indexed Entities:**

- Drivers (name, email, internal number)
- Vehicles (identifier, plate number, VIN)
- Orders (order number, customer name, route)
- Invoices (invoice number, customer name)
- Customers (company name, VAT ID)

**UI:**

```
┌──────────────────────────────────────────────────────┐
│ 🔍 Search G-Track...                         [Ctrl+K]│
├──────────────────────────────────────────────────────┤
│                                                      │
│ Type to search drivers, vehicles, orders, etc.       │
│                                                      │
│ Recent Searches:                                     │
│ • Jan Novák                                          │
│ • VEH-0045                                           │
│ • ORD-2025-0123                                      │
└──────────────────────────────────────────────────────┘

[User types: "jan"]

┌──────────────────────────────────────────────────────┐
│ 🔍 jan                                        [Ctrl+K]│
├──────────────────────────────────────────────────────┤
│ DRIVERS (2)                                          │
│ ┌────────────────────────────────────────────────┐  │
│ │ 🚗 Jan Novák (#DRV-0001)                       │  │
│ │    Praha, Active, 🟢 Ready                     │  │
│ └────────────────────────────────────────────────┘  │
│ ┌────────────────────────────────────────────────┐  │
│ │ 🚗 Jan Horák (#DRV-0045)                       │  │
│ │    Kladno, On Leave                            │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ ORDERS (1)                                           │
│ ┌────────────────────────────────────────────────┐  │
│ │ 📦 ORD-2025-0098                               │  │
│ │    Driver: Jan Novák, Praha → Berlin           │  │
│ └────────────────────────────────────────────────┘  │
│                                                      │
│ [Esc to close]  [↑↓ to navigate]  [Enter to open]  │
└──────────────────────────────────────────────────────┘
```

**Backend Implementation:**

```php
// Laravel Scout + Meilisearch
use Laravel\Scout\Searchable;

class Driver extends Model
{
    use Searchable;
    
    public function toSearchableArray()
    {
        return [
            'id' => $this->id,
            'internal_number' => $this->internal_number,
            'full_name' => $this->first_name . ' ' . $this->last_name,
            'email' => $this->email,
            'type' => 'driver',
        ];
    }
}

// Search controller
public function search(Request $request)
{
    $query = $request->input('q');
    
    $results = [
        'drivers' => Driver::search($query)->take(5)->get(),
        'vehicles' => Vehicle::search($query)->take(5)->get(),
        'orders' => Order::search($query)->take(5)->get(),
    ];
    
    return response()->json($results);
}
```

---

### Keyboard Shortcuts

**Global:**

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` / `Cmd+K` | Open global search |
| `Ctrl+/` / `Cmd+/` | Show shortcuts help |
| `Esc` | Close modals/search |
| `?` | Show help |

**Navigation:**

| Shortcut | Action |
|----------|--------|
| `G then D` | Go to Drivers |
| `G then V` | Go to Vehicles |
| `G then O` | Go to Orders |
| `G then I` | Go to Invoices |

**Actions:**

| Shortcut | Action |
|----------|--------|
| `N` | New item (context-aware) |
| `E` | Edit selected item |
| `Del` | Delete selected item |
| `Ctrl+S` / `Cmd+S` | Save changes |

**Lists:**

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | Navigate items |
| `Enter` | Open selected item |
| `/` | Focus search input |
| `F` | Open filters |

---

### Responsive Design Breakpoints

```css
/* Mobile */
@media (max-width: 599px) {
  /* Stack all content vertically */
  /* Hide sidebar, show bottom nav */
  /* Full-width forms */
}

/* Tablet Portrait */
@media (min-width: 600px) and (max-width: 959px) {
  /* 2-column grid where applicable */
  /* Collapsible sidebar */
}

/* Tablet Landscape */
@media (min-width: 960px) and (max-width: 1279px) {
  /* Split view with narrower sidebar */
  /* 3-column grid for cards */
}

/* Desktop */
@media (min-width: 1280px) {
  /* Full split view (40% list + 60% detail) */
  /* 4-column grid for cards */
  /* Expanded sidebar by default */
}

/* Large Desktop */
@media (min-width: 1920px) {
  /* Max width container (1800px) */
  /* More whitespace */
}
```

---

## 🗄️ DATABASE SCHEMA

### Core Tables

**companies (tenants)**

```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    name VARCHAR(200) NOT NULL,
    country_code CHAR(2) NOT NULL, -- ISO 3166-1 alpha-2
    currency CHAR(3) NOT NULL, -- ISO 4217
    
    -- VAT
    vat_number VARCHAR(50),
    is_vat_payer BOOLEAN DEFAULT true,
    tax_rate DECIMAL(4,2), -- 21.00, 23.00, etc.
    
    -- Contact
    email VARCHAR(255),
    phone VARCHAR(50),
    
    -- Address
    street VARCHAR(200),
    city VARCHAR(100),
    postcode VARCHAR(20),
    
    -- Localization
    default_language CHAR(2) DEFAULT 'en', -- ISO 639-1
    timezone VARCHAR(50) DEFAULT 'UTC',
    date_format VARCHAR(20) DEFAULT 'DD.MM.YYYY',
    first_day_of_week VARCHAR(10) DEFAULT 'monday',
    
    -- Banking
    bank_accounts JSONB, -- array of {iban, swift, bank_name}
    
    -- Subscription
    subscription_tier VARCHAR(20), -- 'free', 'starter', 'professional', etc.
    trial_ends_at TIMESTAMPTZ,
    
    -- Settings
    settings JSONB, -- {allow_cross_office_search, etc.}
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_companies_country ON companies(country_code);
```

---

**offices (sub-tenants)**

```sql
CREATE TABLE offices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    
    name VARCHAR(200) NOT NULL,
    country_code CHAR(2) NOT NULL,
    city VARCHAR(100),
    
    is_headquarters BOOLEAN DEFAULT false,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_offices_company ON offices(company_id);
```

---

**users**

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    office_id UUID REFERENCES offices(id) ON DELETE SET NULL,
    
    -- Auth0
    auth0_user_id VARCHAR(100) UNIQUE,
    
    -- Identity
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    
    -- Roles (JSONB array)
    roles JSONB DEFAULT '[]'::jsonb, -- ['admin', 'hr_manager']
    
    -- Preferences
    preferred_language CHAR(2) DEFAULT 'en',
    theme VARCHAR(20) DEFAULT 'light', -- 'light' or 'dark'
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMPTZ,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth0 ON users(auth0_user_id);
```

---

**drivers**

```sql
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    office_id UUID REFERENCES offices(id) ON DELETE SET NULL,
    
    -- Identification
    internal_number BIGSERIAL UNIQUE, -- DRV-0001 (auto-increment)
    
    -- Personal
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    
    birth_date DATE,
    citizenship CHAR(2), -- ISO 3166-1 alpha-2
    rodne_cislo VARCHAR(20), -- Czech/Slovak birth number
    
    -- Contact
    email VARCHAR(255),
    phone VARCHAR(50),
    
    -- Addresses
    registration_address TEXT,
    residence_address TEXT,
    
    -- Employment
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'on_leave', 'inactive', 'terminated'
    hire_date DATE,
    fire_date DATE,
    
    contract_from DATE,
    contract_to DATE,
    contract_indefinite BOOLEAN DEFAULT false,
    
    work_location VARCHAR(50), -- 'praha', 'kladno', etc.
    
    -- Banking
    bank_country CHAR(2),
    bank_account VARCHAR(50),
    iban VARCHAR(34),
    swift VARCHAR(11),
    
    -- Flags (JSONB)
    flags JSONB DEFAULT '{}'::jsonb, -- {pas_souhlas: true, propiska_cz: false}
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_drivers_company ON drivers(company_id);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_internal_number ON drivers(internal_number);
```

---

**driver_documents**

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

CREATE TYPE document_status AS ENUM (
    'valid',        -- >30 days until expiry
    'warning',      -- 15-30 days
    'expiring_soon',-- <15 days
    'expired',      -- past expiry date
    'no_data'       -- not uploaded
);

CREATE TABLE driver_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    
    type document_type NOT NULL,
    
    -- Document details
    number VARCHAR(100),
    country CHAR(2),
    valid_from DATE,
    valid_until DATE,
    
    -- Computed
    status document_status,
    days_until_expiry INT,
    
    -- Metadata
    meta JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_driver_documents_driver ON driver_documents(driver_id);
CREATE INDEX idx_driver_documents_type ON driver_documents(type);
CREATE INDEX idx_driver_documents_status ON driver_documents(status);
CREATE INDEX idx_driver_documents_expiry ON driver_documents(valid_until) WHERE valid_until IS NOT NULL;
```

---

**document_files (versioning)**

```sql
CREATE TABLE document_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES driver_documents(id) ON DELETE CASCADE,
    
    -- File info
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    
    -- Storage
    storage_disk VARCHAR(20) DEFAULT 's3', -- 's3', 'local'
    storage_path TEXT NOT NULL,
    
    -- Versioning
    version INT DEFAULT 1,
    is_current BOOLEAN DEFAULT true,
    
    -- Security
    hash_sha256 VARCHAR(64),
    
    -- Upload info
    uploaded_by UUID REFERENCES users(id),
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_document_files_document ON document_files(document_id);
CREATE INDEX idx_document_files_current ON document_files(document_id, is_current) WHERE is_current = true;
```

---

**driver_transactions (salary, fines, bonuses)**

```sql
CREATE TABLE driver_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    
    -- Transaction
    type VARCHAR(50) NOT NULL, -- 'base_salary', 'business_trip', 'bonus', 'fine', 'damage'
    amount DECIMAL(10,2) NOT NULL, -- positive or negative
    currency CHAR(3) NOT NULL,
    
    description TEXT,
    reference VARCHAR(100), -- external reference number
    
    -- Date
    transaction_date DATE NOT NULL,
    
    -- Metadata
    meta JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_driver_transactions_driver ON driver_transactions(driver_id);
CREATE INDEX idx_driver_transactions_company ON driver_transactions(company_id);
CREATE INDEX idx_driver_transactions_date ON driver_transactions(transaction_date);
```

---

**vehicles**

```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    office_id UUID REFERENCES offices(id) ON DELETE SET NULL,
    
    -- Identification
    internal_number VARCHAR(20) UNIQUE, -- VEH-0001
    type VARCHAR(10) NOT NULL, -- 'lkv' (heavy truck) or 'pkv' (light vehicle)
    identifier VARCHAR(50) NOT NULL, -- User-friendly name
    
    -- Technical specs
    make VARCHAR(100),
    model VARCHAR(100),
    year INT,
    vin VARCHAR(50) UNIQUE,
    plate_number VARCHAR(20) UNIQUE,
    
    -- Engine
    fuel_type VARCHAR(20), -- 'diesel', 'petrol', 'electric', 'hybrid'
    engine_capacity_cc INT,
    euro_class VARCHAR(10), -- 'Euro 5', 'Euro 6'
    
    -- Capacity
    max_weight_kg INT,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'in_service', 'inactive', 'sold'
    
    -- Assignment (for PKV only)
    assignment_mode VARCHAR(20), -- 'assigned', 'pool', 'unassigned'
    assigned_driver_id UUID REFERENCES drivers(id) ON DELETE SET NULL,
    
    -- Odometer
    current_odometer_km INT DEFAULT 0,
    last_service_km INT,
    next_service_km INT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_vehicles_company ON vehicles(company_id);
CREATE INDEX idx_vehicles_type ON vehicles(type);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_plate ON vehicles(plate_number);
```

---

**trailers**

```sql
CREATE TABLE trailers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    office_id UUID REFERENCES offices(id) ON DELETE SET NULL,
    
    -- Identification
    internal_number VARCHAR(20) UNIQUE, -- TRL-0001
    type VARCHAR(20) NOT NULL, -- 'standard', 'mega', 'frigo', 'van', 'tautliner'
    identifier VARCHAR(50) NOT NULL,
    
    -- Technical specs
    make VARCHAR(100),
    model VARCHAR(100),
    year INT,
    plate_number VARCHAR(20) UNIQUE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',
    
    -- Refrigeration (if frigo)
    has_refrigeration BOOLEAN DEFAULT false,
    min_temp_celsius DECIMAL(4,1),
    max_temp_celsius DECIMAL(4,1),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_trailers_company ON trailers(company_id);
CREATE INDEX idx_trailers_type ON trailers(type);
```

---

**transport_units (Driver + Vehicle + Trailer)**

```sql
CREATE TABLE transport_units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Components
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    trailer_id UUID REFERENCES trailers(id) ON DELETE SET NULL,
    
    -- Readiness (computed)
    is_ready BOOLEAN DEFAULT false,
    
    -- Lifecycle
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    unassigned_at TIMESTAMPTZ,
    
    -- Constraint: Unique active combination
    UNIQUE (driver_id, vehicle_id, trailer_id, unassigned_at)
);

CREATE INDEX idx_transport_units_company ON transport_units(company_id);
CREATE INDEX idx_transport_units_driver ON transport_units(driver_id);
CREATE INDEX idx_transport_units_active ON transport_units(driver_id, vehicle_id, unassigned_at) WHERE unassigned_at IS NULL;
```

---

**audit_logs (complete history)**

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Auditable entity
    auditable_type VARCHAR(50) NOT NULL, -- 'Driver', 'Vehicle', 'Order', etc.
    auditable_id UUID NOT NULL,
    
    -- User who made the change
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255), -- Denormalized for history
    
    -- Action
    action VARCHAR(100) NOT NULL, -- 'created', 'updated', 'deleted', 'document.uploaded', etc.
    
    -- Changes
    old_values JSONB,
    new_values JSONB,
    
    -- Request metadata
    ip_address INET,
    user_agent TEXT,
    
    -- Timestamp
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_auditable ON audit_logs(auditable_type, auditable_id);
CREATE INDEX idx_audit_logs_company ON audit_logs(company_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at DESC);
```

---

## 📡 API SPECIFICATION

### Base URL

```
Production: https://api.g-track.eu/api/v1
Staging: https://staging-api.g-track.eu/api/v1
Local: http://localhost:8000/api/v1
```

---

### Authentication

**Method:** Bearer Token (JWT from Auth0)

**Headers:**

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
Content-Type: application/json
```

**Error Responses:**

```json
// 401 Unauthorized
{
  "error": "Unauthenticated",
  "message": "Token is invalid or expired"
}

// 403 Forbidden
{
  "error": "Forbidden",
  "message": "You do not have permission to access this resource"
}
```

---

### Pagination

**Cursor-based (recommended for large datasets):**

```http
GET /drivers?cursor=eyJpZCI6IjU1MGU4NDAwIn0&per_page=20

Response:
{
  "data": [...],
  "meta": {
    "per_page": 20,
    "next_cursor": "eyJpZCI6IjU1MGU4NDExIn0",
    "prev_cursor": null,
    "has_more": true
  }
}
```

**Offset-based (simpler, for small datasets):**

```http
GET /drivers?page=2&per_page=20

Response:
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total": 150,
    "last_page": 8
  }
}
```

---

### Filtering & Sorting

**Query Params:**

```http
GET /drivers?
    status=active,on_leave&
    work_location=praha&
    search=jan&
    sort=-created_at,last_name

Explanation:
- status: comma-separated (OR logic)
- work_location: exact match
- search: fuzzy search across name, email
- sort: '-' prefix = DESC, '+' or no prefix = ASC
```

---

### Error Handling

**Standard Error Response:**

```json
{
  "error": "ValidationException",
  "message": "The given data was invalid",
  "errors": {
    "email": ["The email field is required."],
    "birth_date": ["The birth date must be a valid date."]
  }
}
```

**HTTP Status Codes:**

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 204 | No Content - Request succeeded, no response body |
| 400 | Bad Request - Invalid request format |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Authenticated but not authorized |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Temporary outage |

---

### Rate Limiting

**Limits:**

```
Free tier: 60 requests/minute
Starter: 120 requests/minute
Professional+: 300 requests/minute
```

**Headers:**

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1730073600
```

**429 Response:**

```json
{
  "error": "TooManyRequestsException",
  "message": "Rate limit exceeded. Try again in 45 seconds.",
  "retry_after": 45
}
```

---

## 🔗 INTEGRATIONS & APIs

### Future Integrations (Roadmap)

**GPS Tracking:**
- Webfleet (TomTom)
- Geotab
- Samsara
- Verizon Connect

**Accounting Software:**
- 🇨🇿 Pohoda (Czech)
- 🇨🇿 ABRA FlexiBee (Czech)
- 🇵🇱 Comarch ERP (Poland)
- 🇩🇪 DATEV (Germany)
- 🇩🇪 Lexware (Germany)

**Communication:**
- Telegram Bot (document uploads, notifications)
- SMS Gateway (Twilio)
- Email (transactional)

**Payment:**
- Stripe (subscriptions)
- Bank APIs (payment verification)

---

## 🗺️ ROADMAP

### Phase 1: MVP (Q4 2025 - Q1 2026)

**Focus:** Drivers Module + Core Infrastructure

- ✅ Authentication (Auth0)
- ✅ Multi-tenancy
- ✅ RBAC (5 roles)
- 🔄 Drivers Module (80% complete)
  - Document tracking (14 types)
  - Readiness indicator
  - Mobile upload (Telegram Bot)
- 🔜 Vehicles Module (LKV + PKV)
- 🔜 Basic Dashboard
- 🔜 User management
- 🔜 Company settings

**Target Launch:** January 2026  
**Paying Customers Goal:** 10 companies

---

### Phase 2: Orders & Invoicing (Q1-Q2 2026)

**Focus:** Order Management + Financial Operations

- 🔜 Customers Module (migration from OLD)
- 🔜 Orders Module (9 statuses)
- 🔜 Transport Unit assignments
- 🔜 Invoices Module (EU VAT compliance)
- 🔜 Payment tracking
- 🔜 Financial dashboards
- 🔜 Service Management (basic)

**Target:** March 2026  
**Paying Customers Goal:** 50 companies

---

### Phase 3: GPS & Analytics (Q2-Q3 2026)

**Focus:** Real-time Tracking + Business Intelligence

- 🔮 GPS integration (Webfleet/Geotab)
- 🔮 Real-time vehicle locations
- 🔮 Route history & replay
- 🔮 Geofencing alerts
- 🔮 Advanced analytics
- 🔮 Custom reports
- 🔮 API webhooks

**Target:** June 2026  
**Paying Customers Goal:** 100 companies

---

### Phase 4: Advanced Features (Q3-Q4 2026)

**Focus:** Automation + Integrations

- 🔮 Accounting software integrations
- 🔮 Predictive maintenance (AI)
- 🔮 Route optimization
- 🔮 Mobile app (native iOS/Android)
- 🔮 Advanced RBAC (custom roles)
- 🔮 Multi-currency support
- 🔮 White-label option

**Target:** September 2026  
**Paying Customers Goal:** 250 companies

---

## 📝 CHANGELOG

### Version 3.1 (October 27, 2025) - **CURRENT**

**Backend:** Document Business Logic + API Complete

**Added:**
- ✨ **Document Status Calculation:** Automatic calculation of document statuses (🟢 valid, 🟡 expiring_soon, 🟠 warning, 🔴 expired, ⚪ no_data)
- ✨ **Driver Readiness Logic:** Calculates if driver can work today based on all 14 documents
- ✨ **Document CRUD API:**
  - `POST /api/v0/drivers/{id}/documents` - Create/update document
  - `POST /api/v0/drivers/{id}/documents/{doc_id}/upload` - Upload file to S3
  - `GET /api/v0/drivers/{id}/documents/{doc_id}/download/{file_id}` - Get temporary download URL
  - `GET /api/v0/drivers/{id}/documents/{doc_id}/versions` - File version history
  - `PUT /api/v0/drivers/{id}/documents/{doc_id}` - Update metadata
  - `DELETE /api/v0/drivers/{id}/documents/{doc_id}/files/{file_id}` - Delete file
- ✨ **File Versioning System:** Automatic version tracking with `is_latest` flag
- ✨ **S3 Integration:** Upload to `gtrack-documents-eu-central-1` bucket
- ✨ **Readiness API Response:** Driver list and detail now include `is_ready` and `readiness` fields

**Frontend:**
- ✨ **Auth0 Integration:** Full OAuth2/OIDC authentication with JWT tokens
- ✨ **Drivers List Component:** Pagination, search, filters (status, readiness)
- ✨ **Driver Detail Component:** Complete profile view with all 14 document types
- ✨ **API Interceptor:** Automatic JWT token injection and base URL handling
- ✨ **Production Deployment:** Live at https://app.g-track.eu

**Testing:**
- ✨ **Pest Framework:** Configured with RefreshDatabase trait
- ✨ **SQLite Support:** Migrations compatible with SQLite for testing
- ✅ **17 Unit Tests Passing:** Driver and DriverDocument logic validated

**DevOps:**
- ✨ **PostgreSQL Sequence Support:** Auto-increment with fallback for SQLite
- ✨ **phpunit.xml:** SQLite in-memory database configuration

**Current Status:**
- Drivers Module: **90% complete** (up from 80%)
- Backend API: **Fully functional and deployed**
- Frontend: **Basic CRUD + Auth working**
- Next: Driver Form component, Document upload UI

---

### Version 3.0 (October 27, 2025)

**Major Update:** Complete system redesign with new tech stack

**Added:**
- ✨ Angular 20 + Material 20 frontend
- ✨ Laravel 12 backend with PostgreSQL 16
- ✨ Multi-tenant architecture with office support
- ✨ RBAC system (5 roles with granular permissions)
- ✨ EU VAT compliance (Domestic, Reverse Charge, Non-VAT)
- ✨ 5 languages (Russian, English, Czech, Polish, German)
- ✨ Driver Finance tracking (salary, fines, bonuses)
- ✨ Order Profitability tracking
- ✨ Service Management (internal + external)
- ✨ Fines & Accidents tracking
- ✨ Audit logging for all entities
- ✨ UUID + Internal Number (dual identification)
- ✨ User invitation system with language selection
- ✨ Driver invitation with Telegram Bot
- ✨ Global search (Cmd+K)
- ✨ Keyboard shortcuts
- ✨ Responsive design (mobile web)

**Changed:**
- 🔄 Complete UI/UX redesign
- 🔄 Split view layout (list + detail)
- 🔄 Improved document status indicators
- 🔄 New sidebar navigation
- 🔄 Better mobile experience

**Technical:**
- 🔧 Signal-based state management
- 🔧 OnPush change detection
- 🔧 Cursor pagination
- 🔧 S3 file storage
- 🔧 Auth0 authentication
- 🔧 Stripe subscriptions

---

### Version 2.0 (October 24, 2025)

**Status:** Deprecated (OLD version)

**Completed:**
- Customers Module (90%)
- Orders Module (85%)
- Invoices Module (20%)

**Issues:**
- Outdated tech stack
- Performance issues
- UI/UX problems
- No mobile support

---

### Version 1.0 (2020-2023)

**Status:** Archived

Initial version, no longer maintained.

---

## 🎯 SUCCESS METRICS

### Technical KPIs

- API Response Time: <300ms (P95)
- Database Query Time: <100ms (P95)
- Frontend Load Time: <2s (P95)
- Uptime: >99.9%
- Error Rate: <0.1%

### Business KPIs

- Customer Acquisition Cost (CAC): <€500
- Monthly Recurring Revenue (MRR): €10,000+ by Q2 2026
- Customer Churn Rate: <5% monthly
- Net Promoter Score (NPS): >50
- Customer Lifetime Value (LTV): >€2,000

---

## 📞 CONTACT & SUPPORT

**Documentation:** https://docs.g-track.eu  
**Support Email:** support@g-track.eu  
**Sales:** sales@g-track.eu  

**GitHub:**
- Frontend: https://github.com/gtrack/gtrack-app
- Backend: https://github.com/gtrack/gtrack-backend
- Docs: https://github.com/gtrack/gtrack-docs

---

**END OF DOCUMENT**

**Version:** 3.0  
**Last Updated:** October 27, 2025  
**Total Pages:** ~50  
**Document Size:** ~60 KB

---

*This document is the single source of truth for G-Track development.  
Keep it updated as the system evolves.*
