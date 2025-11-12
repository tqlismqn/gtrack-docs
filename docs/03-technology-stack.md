# Technology Stack

## Frontend

```
Angular 20.0.0+
├── @taiga-ui/* 4.60.0 (Taiga UI - Modern Angular UI Kit)
│   ├── @taiga-ui/core (Base components, themes)
│   ├── @taiga-ui/kit (Advanced components)
│   ├── @taiga-ui/cdk (Utilities, directives)
│   ├── @taiga-ui/icons (Icon library)
│   └── @taiga-ui/layout (Layout components)
├── TypeScript 5.6+
├── RxJS 7.8+
├── Signals (native Angular state management)
├── @jsverse/transloco (i18n - modern alternative to ngx-translate)
└── Leaflet (GPS maps)
```

**UI Library Migration (November 2025):**
- ✅ **Migrated from Material Design 3 to Taiga UI 4.60.0**
- **Rationale:** Superior visual design, 120+ components, built-in dark mode/i18n
- **Documentation:** [Taiga UI Migration Guide](frontend/taiga-ui-migration-guide.md)

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

## Backend

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
- **Database:** Supabase PostgreSQL 17.6+ (serverless)
- **File Storage:** AWS S3 (eu-central-1)
- **CI/CD:** GitHub Actions → Laravel Cloud auto-deploy

## Database & Authentication

**Technology:** Supabase (PostgreSQL 17.6+ + Auth)

```
Supabase
├── PostgreSQL 17.6+ (Database)
│   ├── PostGIS 3.4+ (geospatial queries)
│   ├── TimescaleDB 2.13+ (GPS time-series)
│   └── pg_cron (scheduled tasks)
├── Supabase Auth (Authentication)
│   ├── Email/Password
│   ├── Magic Link
│   ├── OAuth (Google, Microsoft)
│   └── JWT tokens with custom claims
└── Row Level Security (RLS)
    └── Multi-tenancy isolation (company_id)
```

**Performance Optimizations:**
- Connection pooling via PgBouncer
- Indexes on all foreign keys
- Composite indexes for common queries
- Partitioning for GPS history (by month)
- Materialized views for analytics

**Authentication Migration (November 2025):**
- ✅ **Migrated from Auth0 to Supabase Auth**
- **Rationale:** Integrated database + auth, RLS for authorization, lower cost
- **Documentation:** [Authentication Guide](05-authentication.md)

## Third-Party Services

| Service | Purpose | Pricing |
|---------|---------|---------|
| **Supabase** | Database + Auth + Storage | $25/month (Pro) |
| **Stripe** | Subscriptions, payments | 1.4% + €0.25 per transaction |
| **AWS S3** | File storage (documents) | ~$5/month (500GB) |
| **Mailgun** | Transactional emails | $35/month (50k emails) |
| **Sentry** | Error tracking | Free tier (5k errors/month) |
| **Vercel** | Frontend hosting | Free tier (hobby) |
| **Laravel Cloud** | Backend hosting | $19/month (starter) |

**Total Monthly Cost (MVP):** ~$85/month

**Cost Optimization Notes:**
- Supabase Pro ($25) replaces Auth0 ($23) + managed PostgreSQL
- Free tiers cover development and initial MVP testing
- Scaling costs predictable with usage-based pricing

---

**Last Updated:** November 12, 2025
**Version:** 3.0.0 (Supabase Migration)
**Source:** Master Specification v3.1, Section 3 + November 2025 Supabase Migration
