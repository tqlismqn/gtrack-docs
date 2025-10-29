# Technology Stack

## Frontend

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
- **Database:** Serverless PostgreSQL (Neon)
- **File Storage:** AWS S3 (eu-central-1)
- **CI/CD:** GitHub Actions → Laravel Cloud auto-deploy

## Database

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

## Third-Party Services

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

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 3
