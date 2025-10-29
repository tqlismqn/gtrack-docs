# G-Track Documentation Changelog

All notable changes to the G-Track project documentation and specifications.

**Format:** Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
**Versioning:** Follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased] - October 29, 2025

### 🚨 CRITICAL NEW FEATURES (Not in Master Spec v3.1)

These features were discovered in local development documents dated October 29, 2025, and represent significant additions to the original Master Specification v3.1 (dated October 27, 2025).

#### 1. Driver Rating System (NEW)

**Status:** Planned for Week 1 implementation
**Source:** `docs/business-logic/WEEK_1_ACTION_PLAN.md`

**Database Changes:**
- **New Tables:**
  - `driver_score_config` - Configurable rating system parameters
  - `driver_score_weights` - Metric weights per company
  - `driver_score_snapshots` - Historical ratings (audit trail)
  - `driver_score_components` - Individual metric scores

**Features:**
- Configurable metrics (v1):
  - Document expiration tracking (0/1 + quantitative score)
  - Penalties count/amount per period
  - Profile completeness/KYC verification
  - Document upload timeliness (before/after deadline)
  - Activity tracking (logins, confirmations, reactions)
- Rating explainability (transparency for drivers + HR)
- Historical trends tracking
- Telegram Bot integration:
  - Show current rating
  - Explain score breakdown
  - Notify about upcoming document deadlines
  - Positive badges (e.g., "0 expired documents")

**Impact:**
- Adds 4 new database tables
- Requires API endpoints for rating calculation
- Telegram Bot development (Phase 1)
- Frontend dashboard for rating visualization

---

#### 2. Finance Tracking 100% (EXPANDED from "basic")

**Status:** Full implementation in Phase 1 (not "basic" as in Master Spec v3.1)
**Source:** `docs/business-logic/WEEK_1_ACTION_PLAN.md`

**Original Scope (Master Spec v3.1):**
- Basic finance tracking: salaries, fines, bonuses

**NEW Scope (October 29, 2025):**
- **FULL financial contour** with 4 new tables:
  - `driver_finance` - Main financial records
  - `driver_penalties` - Penalties with dispute tracking
  - `driver_finance_periods` - Period-based aggregations
  - `driver_finance_agg` - Pre-calculated aggregates for performance

**Enhanced Features:**
- Salaries:
  - Начисления (accruals) vs Выплаты (payouts)
  - Period-based tracking
  - Binding to drivers/shifts/orders
- Penalties (Штрафы):
  - Incidents tracking
  - Violations logging
  - Dispute management
  - Status tracking (pending/approved/disputed/resolved)
- Audit Trail:
  - Complete history (who changed what, when)
  - Reason for changes
  - Approval workflow
- Aggregates:
  - Period totals (MTD, YTD)
  - Counters for rating system integration
  - Performance analytics

**Impact:**
- Adds 4 new database tables (vs 1 table in original plan)
- Complex business logic for financial workflows
- Integration with Driver Rating System
- +1 week to Phase 1 timeline

---

#### 3. Multi-Storage Provider (NEW)

**Status:** Architectural requirement
**Source:** `docs/business-logic/WEEK_1_ACTION_PLAN.md`

**Original Scope (Master Spec v3.1):**
- AWS S3 only (eu-central-1, Frankfurt)

**NEW Scope (October 29, 2025):**
- **Multiple storage providers:**
  - AWS S3 (default, private buckets with signed URLs)
  - Google Cloud Storage (optional for clients)
  - Microsoft SharePoint (optional for clients)
- **Per-tenant configuration:**
  - `StorageProvider` interface abstraction
  - Company-level storage preference
  - Automatic failover to default (S3) if provider unavailable
- **Security enhancements:**
  - MIME type validation (strict whitelist)
  - File size limits (10MB per file, configurable)
  - Antivirus scanning (ClamAV or AWS Lambda)
  - Comprehensive audit logging (all file operations)
- **Optional features:**
  - Local backup via API/webhooks
  - S3 → GCS replication
  - SharePoint integration for enterprise clients

**Impact:**
- Major architectural change (abstraction layer needed)
- 3 provider integrations instead of 1
- Additional security infrastructure (ClamAV/Lambda)
- Per-tenant storage configuration UI
- Migration strategy for existing S3 files

---

### 📋 Development Plan Updates

**Source:** `docs/business-logic/STRATEGIC_DEVELOPMENT_PLAN.md` (October 29, 2025)

#### 8-Week Timeline (Week 1 - Week 11)

**Week 1 (Oct 28 - Nov 3):** Critical Fixes 🔴
- Deploy gtrack-backend to Laravel Cloud
- Enable permission middleware
- Implement Super Admin check
- Security scan with Semgrep
- Fix compact logo SVG

**Week 2 (Nov 4-10):** Row-Level Security + Testing 🔒
- Implement PostgreSQL RLS (Row-Level Security)
- Setup frontend testing (Jasmine + Karma)
- Create multi-tenancy test suite
- 20+ backend tests, 10+ frontend tests

**Week 3 (Nov 11-17):** Driver Finance + Document Upload 💰
- Driver Finance Tracking UI (full implementation)
- Document Upload UI with drag & drop
- File upload security (MIME validation, antivirus)
- Tests: >80% coverage

**Week 4 (Nov 18-24):** Readiness Dashboard + Drivers 100% ✅
- Readiness Dashboard with visual indicators
- Driver Comments Section
- Audit trail UI
- **Drivers Module 100% COMPLETE**

**Week 5 (Nov 25 - Dec 1):** Vehicles Module Start 🚗
- Apply Drivers Module patterns (2x faster)
- Vehicles CRUD + Transport Unit concept

**Week 6 (Dec 2-8):** Vehicles Module Complete 🔧
- Service Management
- Integration tests
- Beta testing preparation

**Week 7 (Dec 9-15):** Security Audit + Documentation 🔒
- Full security audit (OWASP Top 10)
- PostgreSQL performance optimization
- API documentation generation

**Week 8 (Dec 16-22):** Pre-Launch + GDPR 📋
- GDPR compliance implementation
- E2E testing suite
- Performance optimization
- **READY FOR BETA LAUNCH**

**Week 9-10 (Dec 23 - Jan 5):** Beta Testing 🐛
- 2-3 pilot companies
- Bug fixes and polishing

**Week 11 (Jan 6-12):** PRODUCTION LAUNCH 🚀
- Final smoke tests
- Production deployment
- Monitor and support

---

### 🔐 Security & Compliance Additions

**Source:** `docs/business-logic/STRATEGIC_DEVELOPMENT_PLAN.md`

#### PostgreSQL Row-Level Security (RLS)

**Implementation Details:**
```sql
-- Enable RLS on all tenant tables
ALTER TABLE drivers ENABLE ROW LEVEL SECURITY;
ALTER TABLE driver_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_files ENABLE ROW LEVEL SECURITY;

-- Policy: Company isolation
CREATE POLICY company_isolation ON drivers
  FOR ALL
  USING (company_id = current_setting('app.current_company_id')::uuid);

-- Policy: Super Admin bypass
CREATE POLICY super_admin_access ON drivers
  FOR ALL
  TO super_admin
  USING (true);

-- Policy: Cross-office visibility
CREATE POLICY office_isolation ON drivers
  FOR SELECT
  USING (
    company_id = current_setting('app.current_company_id')::uuid
    AND (
      current_setting('app.allow_cross_office')::boolean = true
      OR office_id = current_setting('app.current_office_id')::uuid
    )
  );
```

**Laravel Integration:**
```php
// Middleware: Set PostgreSQL session variables
class SetTenantContext {
    public function handle($request, Closure $next) {
        $user = auth()->user();
        DB::statement("SET app.current_company_id = ?", [$user->company_id]);
        DB::statement("SET app.current_office_id = ?", [$user->office_id]);
        DB::statement("SET app.allow_cross_office = ?", [$user->company->allow_cross_office]);
        return $next($request);
    }
}
```

**Benefits:**
- Defense in depth (application + database layers)
- Impossible to bypass with SQL injection
- Automatic enforcement
- GDPR compliance at database level

---

#### Security Checklist (80+ Items)

**Before Launch (Week 8):**

**Authentication & Authorization:**
- [ ] Auth0 JWT validation working
- [ ] Refresh tokens implemented
- [ ] Token blacklist on logout
- [ ] Permission middleware enabled on ALL routes
- [ ] Super Admin check functional

**Multi-Tenancy:**
- [ ] RLS enabled on all tables
- [ ] Cross-tenant access blocked (tested)
- [ ] Office-level isolation working
- [ ] Automatic company_id assignment

**Input Validation:**
- [ ] All API endpoints have validation rules
- [ ] File uploads: MIME validation + size limits + antivirus
- [ ] SQL injection: 0 vulnerabilities (Semgrep scan)
- [ ] XSS: 0 vulnerabilities

**Data Protection:**
- [ ] Database encryption at rest
- [ ] S3 bucket private (signed URLs only)
- [ ] HTTPS enforced (HSTS headers)
- [ ] Sensitive fields encrypted

**GDPR Compliance:**
- [ ] DPA (Data Processing Agreement) signed
- [ ] Privacy Policy published
- [ ] Terms of Service published
- [ ] Right to be Forgotten implemented
- [ ] Data export functionality (portability)
- [ ] Audit logging (who accessed what)
- [ ] 30-day data retention policy

**Rate Limiting:**
- [ ] API endpoints: 300 req/min per user
- [ ] File uploads: 20 req/min per user
- [ ] IP-based global rate limiting

**Monitoring:**
- [ ] Sentry error tracking
- [ ] UptimeRobot monitoring (5 min intervals)
- [ ] Alert on API errors >10/min
- [ ] Alert on uptime <99%

**Backups:**
- [ ] Daily database backups (30 days retention)
- [ ] S3 versioning enabled
- [ ] Backup restore tested
- [ ] Disaster recovery plan documented

---

### 💳 Billing Integration (Detailed)

**Source:** `docs/business-logic/STRATEGIC_DEVELOPMENT_PLAN.md`

#### Stripe vs Chargebee Decision

**Chosen:** **Laravel Cashier (Stripe)**

**Rationale:**
1. **Laravel Ecosystem:**
   - Laravel Cashier has 38 code snippets in Context7
   - Native integration, extensive community support
   - Simpler for MVP

2. **G-Track Billing Model (Module-Based):**
   - Starter: €29/month (base modules)
   - Professional: +€19/month (orders module)
   - Business: +€15/month (invoicing module)
   - Enterprise: +€25/month (GPS module)

3. **Stripe Advantages:**
   - No monthly platform fee (vs Chargebee €299-899/month)
   - EU SCA (Strong Customer Authentication) built-in
   - Webhook reliability
   - Test mode for development

4. **Implementation:**
```bash
# Install Laravel Cashier
composer require laravel/cashier

# Setup webhooks
# Stripe Dashboard → Webhooks → Add endpoint:
# https://api.g-track.eu/stripe/webhook
```

**Key Pattern (from Stripe Recommendations):**
```php
// Sync ALL subscription data to KV store (Redis)
// Avoid split states and race conditions
Event::listen(SubscriptionCreated::class, function($event) {
    Cache::put("company:{$event->company_id}:subscription", [
        'tier' => $event->tier,
        'modules' => $event->modules,
        'status' => 'active',
        'stripe_id' => $event->stripe_subscription_id,
    ], now()->addDays(7));
});
```

**Resources:**
- Context7: `/laravel/cashier-stripe` (38 snippets)
- Stripe Guide: `/t3dotgg/stripe-recommendations` (Trust: 9.7)

---

### ❓ Critical Questions for Client

**Source:** `docs/business-logic/STRATEGIC_DEVELOPMENT_PLAN.md`

#### 🔴 P0 - Must Answer Before Launch

**1. Finance Tracking Priority**
```
Q: Включить Finance tracking (зарплаты, штрафы, бонусы) в Drivers Module (Phase 1)?
   Или вынести в отдельный Finance Module (Phase 2+)?

Options:
A) Включить в Phase 1 (Drivers 100% = Document + Finance) [+1 week]
B) Отложить на Phase 2 (отдельный Finance Module)
C) Базовый Finance в Phase 1, расширенный в Phase 2 [RECOMMENDED]

Recommendation: Option C (базовый finance: salaries + fines, без сложной аналитики)
```

**2. GDPR Documents**
```
Q: Готовы ли legal документы для GDPR compliance?

Required:
- Data Processing Agreement (DPA)
- Privacy Policy
- Terms of Service

Status: ❌ Not created
Action: Hire GDPR lawyer (€1500-3000) OR use template + review (€500-1000)
Timeline: 2 weeks
Deadline: BEFORE beta testing (Week 5)

Blocker: Cannot launch without GDPR docs (EU legal requirement)
```

**3. Penetration Testing Budget**
```
Q: Бюджет на external penetration testing?

Options:
A) €0 - Only automated scans (Semgrep, OWASP ZAP)
B) €2000 - Basic pen test (1-2 days) [RECOMMENDED]
C) €5000 - Comprehensive pen test (5 days) + report

Why Critical:
- Multi-tenant SaaS = high risk target
- Production data (driver passports, visas)
- EU compliance requirement

Timeline: Week 7 (2 weeks before launch)
```

**4. Expected Load (Scaling Plan)**
```
Q: Сколько companies ожидаете на launch + 6 months?

Launch (January 2026):
- [ ] 5 companies (pilot)
- [ ] 10 companies (beta)
- [ ] 50 companies (aggressive)

6 Months (July 2026):
- [ ] 20 companies
- [ ] 100 companies
- [ ] 500 companies

Architecture Support:
✅ 1-100 companies (no changes needed)
⚠️ 100-500 companies (need read replicas)
❌ 500+ companies (need sharding)
```

**5. Beta Testing Plan**
```
Q: Есть ли 2-3 pilot companies для beta testing?

Ideal Beta Companies:
- Small (10-30 drivers) - easier onboarding
- Willing to report bugs
- Representative of target market (CZ/PL/DE)

Timeline:
- Week 6: Invite beta users
- Week 7: Beta testing (1 week)
- Week 8: Fix critical bugs
- Week 9: Production launch

Benefits:
- Real-world testing
- User feedback
- Case studies for marketing
```

---

## [2.0.1] - October 29, 2025

### Documentation Migration Complete ✅

**Completed:** All 16 sections migrated from Master Specification v3.1 to MkDocs

#### Added Sections (PR #180, #181, #182):

**Core Modules (Section 01-05):**
- 01-executive-summary.md
- 02-technology-stack.md
- 03-system-architecture.md
- 04-subscription-tiers.md
- 05-multi-tenancy.md

**Security & UI (Section 06, 12-13):**
- 06-security.md
- 12-internationalization.md
- 13-ui-ux.md

**Module Specifications (Section 07-11):**
- 07-drivers-module.md - **Priority #1 Module** (90% complete)
- 08-vehicles-module.md - Transport Unit concept
- 09-customers-module.md - EU VAT compliance
- 10-orders-module.md - 9-status lifecycle
- 11-invoices-module.md - Reverse Charge automation

**Technical Reference (Section 14-16):**
- 14-database-schema.md - PostgreSQL schema with RLS
- 15-api-specification.md - RESTful API v0
- 16-roadmap.md - 4-phase development plan

**Total:** 1,299 lines added across 16 documentation files

**Deployment:**
- Live at https://docs.g-track.eu
- GitHub Actions CI/CD automatic deployment
- MkDocs Material theme

---

## [2.0.0] - October 27, 2025

### Initial Master Specification v3.1

**Source:** `docs/archive/G-Track_Master_Specification_v3.0.md`
**Size:** 4,054 lines
**Status:** Archive reference

**Key Features (Original Scope):**
- Drivers Module (Priority #1)
- Multi-tenancy with company_id isolation
- 14 document types tracking
- Document status indicators (🟢🟡🟠🔴⚪)
- AWS S3 file storage
- Auth0 authentication
- PostgreSQL 16+ database
- Laravel 12 + Angular 20 stack

**Timeline:**
- Phase 1: MVP - Drivers Module (Q4 2025 - Q1 2026)
- Phase 2: Orders & Invoicing (Q1-Q2 2026)
- Phase 3: GPS & Analytics (Q2-Q3 2026)
- Phase 4: Advanced Features (Q3-Q4 2026)

---

## Version History

**[Unreleased]** - October 29, 2025
- **3 NEW FEATURES:** Driver Rating System, Finance Tracking 100%, Multi-Storage Provider
- **8-Week Development Plan:** Detailed week-by-week breakdown
- **Security Checklist:** 80+ pre-launch items
- **Critical Questions:** 5 P0 questions for client decision

**[2.0.1]** - October 29, 2025
- Documentation migration: 16/16 sections (100% complete)
- Live deployment: https://docs.g-track.eu

**[2.0.0]** - October 27, 2025
- Master Specification v3.1 (archive reference)

---

## Next Updates

### Pending Changes (To Be Deployed):

**Driver Rating System Implementation:**
- Database migrations for 4 new tables
- API endpoints for rating calculation
- Telegram Bot integration
- Frontend dashboard component

**Finance Tracking 100% Implementation:**
- Database migrations for 4 new tables
- Financial workflow business logic
- Audit trail implementation
- Frontend finance components

**Multi-Storage Provider Implementation:**
- Storage abstraction layer
- Provider integrations (S3, GCS, SharePoint)
- Security infrastructure (ClamAV)
- Per-tenant configuration UI

**Expected Deployment:** Week 1-2 (November 2025)

---

**Last Updated:** October 29, 2025
**Maintainer:** Development Team
**Format:** [Keep a Changelog](https://keepachangelog.com/)
**License:** Proprietary

---

## How to Use This Changelog

1. **Check [Unreleased]** - See upcoming features not yet deployed
2. **Review Critical Questions** - Client decisions needed before implementation
3. **Track Version History** - Understand project evolution
4. **Next Updates** - Plan for upcoming changes

**Related Documents:**
- `docs/archive/G-Track_Master_Specification_v3.1.md` - Original specification
- `docs/business-logic/WEEK_1_ACTION_PLAN.md` - NEW features (Oct 29)
- `docs/business-logic/STRATEGIC_DEVELOPMENT_PLAN.md` - 8-week plan
- `docs/roadmap/EXECUTION_PLAN_DRIVERS_MODULE.md` - Drivers Module details
