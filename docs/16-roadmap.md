# Development Roadmap

## Overview

G-Track development is organized into **4 major phases** spanning 12 months (Q4 2025 - Q4 2026). Each phase focuses on specific modules and features, with clear deliverables and success criteria.

**Current Status (October 29, 2025):**
- **Phase 1:** In Progress (90% Drivers Module complete)
- **Target MVP Launch:** January 2026
- **Beta Testing:** December 2025 with 3 pilot clients

## Phase 1: MVP - Drivers Module + Core Infrastructure
**Timeline:** Q4 2025 - Q1 2026 (October 2025 - January 2026)

**Primary Goal:** Launch production-ready application with complete Drivers Module

### Deliverables

**1.1 Drivers Module (PRIORITY #1) - December 10, 2025**
- ✅ Driver List with search, filters, sorting (DONE)
- ✅ Driver Profile with 4 tabs: Overview, Documents, Finance, Comments (DONE)
- ✅ Document status tracking with 5 indicators: 🟢🟡🟠🔴⚪ (DONE)
- ✅ Document expiration calculations and readiness logic (DONE)
- 🔄 Driver Form (Create/Edit) - In Progress
- 🔄 Document Upload UI with drag-and-drop - In Progress
- 🔄 Document Management (versions, download, delete) - In Progress
- 🔄 Comments Section with real-time updates - In Progress
- ⏳ Readiness Dashboard (who can work today?) - Planned
- ⏳ Finance Tracking (salary, fines, bonuses) - Planned

**1.2 Layout & Navigation - November 5, 2025**
- ✅ Layout v2.0 with Material Design 3 (DONE - deployed October 27)
- ✅ Responsive sidebar with collapse/expand (DONE)
- ✅ Dark mode toggle (DONE)
- ✅ User menu with profile/settings/logout (DONE)
- ✅ Breadcrumbs and page headers (DONE)

**1.3 Authentication & Authorization - October 15, 2025**
- ✅ Auth0 integration (OAuth 2.0 + OpenID Connect) (DONE)
- ✅ JWT token validation on backend (DONE)
- ✅ RBAC with 5 roles: Admin, Accountant, HR Manager, Dispatcher, Driver (DONE)
- ✅ Permission-based UI guards (DONE)

**1.4 Backend API - November 15, 2025**
- ✅ Laravel 12 RESTful API (DONE)
- ✅ Multi-tenancy middleware (company_id isolation) (DONE)
- ✅ Drivers endpoints (list, get, create, update, delete) (DONE)
- 🔄 Documents endpoints (upload, download, versions) - In Progress
- ⏳ Comments endpoints - Planned

**1.5 File Storage - November 20, 2025**
- ⏳ AWS S3 bucket setup (eu-central-1, Frankfurt)
- ⏳ Document versioning system (automatic version tracking)
- ⏳ File upload with validation (max 10MB, PDF/JPG/PNG only)
- ⏳ Secure file access with signed URLs (time-limited)

**1.6 Testing & QA - December 15, 2025**
- 🔄 Unit tests for business logic (Pest for Laravel, Jasmine for Angular) - In Progress
- ⏳ Integration tests for API endpoints
- ⏳ E2E tests for critical user flows (Playwright)
- ⏳ Security audit (multi-tenancy isolation, authentication, authorization)
- ⏳ Performance testing (target: <500ms API response time)

**1.7 Beta Testing - December 20 - January 10, 2026**
- ⏳ Onboard 3 pilot clients (150-170 drivers total)
- ⏳ Daily feedback sessions with HR managers
- ⏳ Bug fixes and UX improvements based on feedback
- ⏳ Load testing with real data

**1.8 Documentation - January 5, 2026**
- ✅ Master Specification v3.1 (DONE)
- ✅ MkDocs documentation site structure (DONE)
- 🔄 English-only content migration (75% complete - sections 01-13 done)
- ⏳ User guides (onboarding, driver management, document upload)
- ⏳ API documentation (OpenAPI/Swagger spec)
- ⏳ Admin guides (user management, permissions, settings)

**1.9 Deployment & Monitoring - January 15, 2026**
- ✅ Frontend on Vercel (DONE)
- ✅ Backend on Laravel Cloud (DONE)
- ✅ GitHub Actions CI/CD (DONE)
- ✅ Sentry for error tracking (DONE)
- ⏳ CloudWatch for performance monitoring
- ⏳ Uptime monitoring (target: 99.5% uptime SLA)

### Success Criteria
- [ ] All 14 document types tracked and validated
- [ ] 100% of drivers with document status visible (🟢🟡🟠🔴⚪)
- [ ] Document upload working on web + mobile (Telegram Bot)
- [ ] Readiness dashboard shows accurate "who can work today" data
- [ ] 3 pilot clients onboarded with positive feedback (NPS ≥8/10)
- [ ] Zero critical bugs, <10 minor bugs
- [ ] Average API response time <500ms (p95)

---

## Detailed 8-Week Plan (NEW 🆕)

**UPDATED:** October 29, 2025 - Based on STRATEGIC_DEVELOPMENT_PLAN.md

This is the detailed week-by-week execution plan for achieving Phase 1 MVP by mid-January 2026. Total timeline: **11 weeks (Oct 29, 2025 - Jan 20, 2026)**.

### Week 0: Critical Fixes + Documentation Sync
**Timeline:** Oct 29 - Nov 4, 2025
**Status:** ✅ COMPLETED

**Goal:** Fix critical backend issues, sync documentation, establish baseline

**Deliverables:**
- ✅ Fix backend 404 errors (deploy gtrack-backend to Laravel Cloud)
- ✅ Sync Master Specification v3.1 with MkDocs site (100% complete)
- ✅ Create CHANGELOG for 3 NEW features (Driver Rating, Finance 100%, Multi-Storage)
- ✅ Establish 8-week development plan with priorities

---

### Week 1: Drivers Module to 100%
**Timeline:** Nov 5 - Nov 11, 2025
**Status:** ⏳ PLANNED

**Goal:** Complete remaining 10% of Drivers Module

**NEW FEATURES TO IMPLEMENT:**
1. **Driver Rating System** (configurable with 6 metrics)
2. **Finance Tracking 100%** (full financial contour with penalties)
3. **Multi-Storage Provider** (AWS S3 + GCS + SharePoint)

**Deliverables:**

**Driver Form Component (2 days):**
- Create/Edit Driver form with reactive validation
- Address autocomplete (Google Places API)
- Bank account validation (CZ format vs IBAN/SWIFT)
- Contract date validation (indefinite vs fixed-term)

**Document Upload UI (2 days):**
- Drag-and-drop file upload component
- Multi-file upload with progress bars
- File validation (PDF/JPG/PNG, max 10MB)
- Preview before upload
- Upload to configurable storage (S3/GCS/SharePoint)

**Document Management UI (2 days):**
- Document card with status indicator (🟢🟡🟠🔴⚪)
- Version history viewer
- Download/Delete actions
- Expiration date reminder UI

**Comments Section (1 day):**
- Real-time comments with WebSockets (Laravel Reverb)
- Rich text editor (Quill.js or TinyMCE)
- @mention support for users
- File attachments in comments

**Success Criteria:**
- [ ] All 4 sub-features fully functional
- [ ] Drivers Module at 100% feature completion
- [ ] All UI components responsive on mobile (375px width)
- [ ] Zero TypeScript errors, 80%+ test coverage

---

### Week 2: Finance Tracking 100% + Driver Rating System
**Timeline:** Nov 12 - Nov 18, 2025
**Status:** ⏳ PLANNED

**Goal:** Implement NEW financial features discovered on Oct 29, 2025

**Deliverables:**

**Finance Tracking 100% (3 days):**
- Implement 4 new database tables (driver_finance, driver_penalties, driver_finance_periods, driver_finance_agg)
- Create Finance Tracking UI (transactions list, create/edit forms)
- Penalty Management with dispute workflow
- Financial periods (MTD, YTD aggregates)
- API endpoints (12 new endpoints)

**Driver Rating System (3 days):**
- Implement 4 new database tables (driver_score_config, driver_score_snapshots, driver_score_components)
- Rating calculation engine (6 configurable metrics)
- Rating history UI with trend charts
- Telegram Bot integration (rating commands: /rating, /rating_explain)
- API endpoints (4 new endpoints)

**Testing (1 day):**
- Unit tests for rating calculation logic
- Integration tests for finance workflows
- Dispute workflow E2E test

**Success Criteria:**
- [ ] All 8 new database tables migrated
- [ ] Rating system calculating correctly with configurable weights
- [ ] Finance tracking with full dispute workflow
- [ ] Telegram Bot integration working (basic commands)
- [ ] 80%+ test coverage for new features

---

### Week 3: Testing Phase 1 (Unit + Integration Tests)
**Timeline:** Nov 19 - Nov 25, 2025
**Status:** ⏳ PLANNED

**Goal:** Achieve 80%+ test coverage, fix all critical bugs

**Deliverables:**

**Backend Testing (3 days):**
- Unit tests for all business logic (Pest)
- Multi-tenancy isolation tests (CRITICAL)
- API endpoint integration tests
- Database transaction tests

**Frontend Testing (3 days):**
- Component unit tests (Jasmine)
- Service unit tests with mocked HTTP
- Form validation tests
- Routing tests

**Security Testing (1 day):**
- Semgrep automated scan
- Manual code review for security issues
- OWASP Top 10 checklist

**Success Criteria:**
- [ ] Backend: 80%+ code coverage
- [ ] Frontend: 70%+ code coverage
- [ ] Zero multi-tenancy isolation failures
- [ ] All P0 and P1 bugs fixed
- [ ] Security checklist: 0 critical issues

---

### Week 4: Testing Phase 2 (E2E + Security Audit)
**Timeline:** Nov 26 - Dec 2, 2025
**Status:** ⏳ PLANNED

**Goal:** End-to-end testing, comprehensive security audit

**Deliverables:**

**E2E Testing with Playwright (4 days):**
- User authentication flow (login, logout, token refresh)
- Driver CRUD operations (create, view, edit, delete)
- Document upload and management flow
- Finance tracking workflows (create transaction, file dispute, resolve)
- Rating system UI testing (view rating, historical trends)

**Security Audit (2 days):**
- PostgreSQL RLS (Row-Level Security) implementation
- API authentication/authorization review
- Rate limiting validation (300 req/min per user)
- Sensitive data encryption check (bank accounts, etc.)
- GDPR compliance review (DPA, Privacy Policy, Terms)

**Performance Testing (1 day):**
- Load testing with 100 concurrent users
- API response time validation (<500ms p95)
- Database query optimization
- Frontend FCP (First Contentful Paint) <1.5s

**Success Criteria:**
- [ ] All critical E2E flows passing
- [ ] Zero security vulnerabilities (Critical/High)
- [ ] Performance targets met (<500ms API, <1.5s FCP)
- [ ] PostgreSQL RLS policies active on all tables
- [ ] GDPR documentation complete (draft, marked for lawyer review)

---

### Week 5: Vehicles Module Setup + Vehicle Form
**Timeline:** Dec 3 - Dec 9, 2025
**Status:** ⏳ PLANNED

**Goal:** Start Vehicles Module (Phase 2), implement vehicle profiles

**Deliverables:**

**Database Schema (1 day):**
- Create vehicles table (LKV + PKV)
- Create trailers table (5 types: Standard, Mega, Frigo, Van, Tautliner)
- Create transport_units table (Driver + Vehicle + Trailer)
- Migrations with seed data

**Backend API (2 days):**
- Vehicles CRUD endpoints
- Trailers CRUD endpoints
- Transport Units endpoints
- Readiness calculation logic

**Frontend Components (3 days):**
- Vehicle List component with filters
- Vehicle Form (Create/Edit)
- Trailer Form (Create/Edit)
- Transport Unit assignment UI

**Testing (1 day):**
- Unit tests for readiness logic
- API integration tests
- Component tests

**Success Criteria:**
- [ ] Vehicles Module: 50% complete
- [ ] Vehicle/Trailer CRUD fully functional
- [ ] Transport Unit assignment working
- [ ] 80%+ test coverage

---

### Week 6: Vehicles Module Integration + Transport Units
**Timeline:** Dec 10 - Dec 16, 2025
**Status:** ⏳ PLANNED

**Goal:** Complete Vehicles Module, integrate with Drivers

**Deliverables:**

**Vehicle Documents (2 days):**
- Technical inspection tracking (STK)
- Insurance document management
- Service history records

**Transport Unit Readiness (2 days):**
- Readiness dashboard UI
- Real-time readiness calculation
- Alert system for unready units

**Integration with Drivers (2 days):**
- Driver → Vehicle assignment
- Readiness validation (driver docs + vehicle docs)
- Historical assignment tracking

**Testing (1 day):**
- E2E tests for vehicle workflows
- Integration tests with Drivers Module
- Readiness logic validation

**Success Criteria:**
- [ ] Vehicles Module: 100% complete
- [ ] Transport Unit readiness working correctly
- [ ] Integration with Drivers Module seamless
- [ ] Readiness dashboard functional

---

### Week 7-8: Beta Testing + Final Polish
**Timeline:** Dec 17 - Dec 30, 2025
**Status:** ⏳ PLANNED

**Goal:** Beta testing with 2-3 pilot companies, bug fixes, UX polish

**Deliverables:**

**Beta Testing Setup (2 days):**
- Onboard 2-3 pilot companies (50-100 drivers each)
- Migrate real data from Excel spreadsheets
- User training sessions (HR managers)

**Beta Testing Period (8 days):**
- Daily feedback sessions with HR managers
- Bug tracking and prioritization
- UI/UX improvements based on feedback
- Performance monitoring with real load

**Critical Fixes (2 days):**
- Fix all P0 bugs immediately
- Fix all P1 bugs before launch
- Performance optimization if needed

**Documentation (2 days):**
- User guides (onboarding, driver management, document upload)
- Admin guides (user management, permissions, settings)
- Video tutorials (3-5 minute screencasts)

**Success Criteria:**
- [ ] 3 pilot clients successfully onboarded
- [ ] NPS score ≥8/10 from HR managers
- [ ] Zero critical bugs (P0)
- [ ] <10 minor bugs (P2)
- [ ] User documentation complete

---

### Week 9: Production Deployment
**Timeline:** Dec 31, 2025 - Jan 6, 2026
**Status:** ⏳ PLANNED

**Goal:** Final production deployment, monitoring setup

**Deliverables:**

**Deployment (2 days):**
- Final production build and deployment
- Database migration to production
- SSL certificates and domain configuration
- CDN setup for static assets (CloudFront)

**Monitoring Setup (2 days):**
- Sentry error tracking configured
- CloudWatch dashboards (API latency, DB queries)
- Uptime monitoring (Pingdom or StatusCake)
- Alert configuration (Slack/email)

**Smoke Testing (1 day):**
- Verify all features in production
- Load testing with realistic traffic
- SSL/TLS validation
- Backup and disaster recovery test

**Go-Live (1 day):**
- Official launch announcement
- Invite beta clients to production
- Press release (optional)

**Success Criteria:**
- [ ] Production deployment successful
- [ ] Monitoring dashboards live
- [ ] Zero downtime during migration
- [ ] SSL/TLS configured correctly
- [ ] Backup strategy verified

---

### Week 10-11: Client Onboarding + Post-Launch
**Timeline:** Jan 7 - Jan 20, 2026
**Status:** ⏳ PLANNED

**Goal:** Onboard first 10 production clients, post-launch support

**Deliverables:**

**Client Onboarding (10 days):**
- Onboard 10 production clients (2-10 per day)
- Data migration from Excel/legacy systems
- User training for each client
- Customization (company logos, branding)

**Post-Launch Support (4 days):**
- 24/7 support for first week
- Bug fixes and hotfixes as needed
- Performance optimization based on real usage
- Feedback collection and prioritization

**Success Criteria:**
- [ ] 10 production clients onboarded
- [ ] Average onboarding time <2 hours per client
- [ ] Client satisfaction ≥8/10
- [ ] <5 support tickets per client in first week
- [ ] System uptime ≥99.5%

---

### Quality Gates (Applied to Every Week)

**🚦 Quality Gate Checklist:**

Before moving to the next week, ALL of the following must be TRUE:

1. **Code Quality:**
   - [ ] TypeScript: 0 errors, 0 warnings
   - [ ] ESLint: 0 errors, <5 warnings
   - [ ] PHP: Laravel Pint passing, 0 errors
   - [ ] Code review completed by peer

2. **Testing:**
   - [ ] Unit tests: 80%+ coverage (backend), 70%+ coverage (frontend)
   - [ ] Integration tests: All API endpoints tested
   - [ ] E2E tests: Critical user flows passing
   - [ ] Manual testing: No obvious bugs

3. **Security:**
   - [ ] Multi-tenancy: All queries include company_id
   - [ ] Authentication: JWT validation working
   - [ ] Authorization: RBAC permissions enforced
   - [ ] Semgrep scan: 0 critical/high issues

4. **Performance:**
   - [ ] API response time: <500ms (p95)
   - [ ] Frontend FCP: <1.5s
   - [ ] Database queries: <50ms (p95)
   - [ ] No N+1 queries detected

5. **Documentation:**
   - [ ] README updated for new features
   - [ ] API endpoints documented (OpenAPI)
   - [ ] User guides updated (if user-facing features)
   - [ ] CHANGELOG updated

**⚠️ If any quality gate fails, STOP and fix before proceeding.**

---

### Key Milestones

**🎯 Milestone 1: Drivers Module 100%** (Week 1 - Nov 11, 2025)
- All 4 sub-features complete
- 80%+ test coverage
- Zero critical bugs

**🎯 Milestone 2: NEW Features Complete** (Week 2 - Nov 18, 2025)
- Driver Rating System live
- Finance Tracking 100% live
- Multi-Storage Provider configured

**🎯 Milestone 3: Testing Complete** (Week 4 - Dec 2, 2025)
- 80%+ code coverage
- Security audit passed
- Performance targets met

**🎯 Milestone 4: Vehicles Module Complete** (Week 6 - Dec 16, 2025)
- Vehicle/Trailer CRUD working
- Transport Unit readiness functional
- Integration with Drivers seamless

**🎯 Milestone 5: Beta Testing Complete** (Week 8 - Dec 30, 2025)
- 3 pilot clients onboarded
- NPS ≥8/10
- <10 minor bugs

**🎯 Milestone 6: Production Launch** (Week 9 - Jan 6, 2026)
- Production deployment successful
- Monitoring live
- Zero downtime

**🎯 Milestone 7: First 10 Clients Live** (Week 11 - Jan 20, 2026)
- 10 production clients
- Client satisfaction ≥8/10
- System uptime ≥99.5%

---

### Critical Questions for Client (URGENT - Priority P0)

**These questions MUST be answered BEFORE Week 2:**

1. **Driver Rating System:**
   - Do you want the default 6 metrics, or custom metrics?
   - Which metric weights are most important for your company?
   - Should rating affect driver bonuses automatically?

2. **Finance Tracking 100%:**
   - Do you need salary calculation automation (base + bonuses)?
   - Should penalties be deducted automatically from salary?
   - Do you need integration with accounting software (POHODA, Money S3)?

3. **Multi-Storage Provider:**
   - Which storage provider do you prefer: AWS S3 (default), Google Cloud Storage, or Microsoft SharePoint?
   - Do you need multi-region storage for compliance?
   - What is your expected document storage volume (GB/month)?

4. **Telegram Bot:**
   - Do you want Telegram Bot for document uploads (mobile-first)?
   - Which Telegram Bot features are most important (rating alerts, penalty disputes, document expiration)?

5. **GDPR Compliance:**
   - Do you need DPA (Data Processing Agreement) reviewed by lawyer?
   - Do you need Privacy Policy and Terms of Service customized?
   - Are there specific GDPR requirements for your industry?

---

## Phase 2: Orders & Invoicing
**Timeline:** Q1-Q2 2026 (February - June 2026)

**Primary Goal:** Complete Order Management and Invoicing modules for operational workflow

### Deliverables

**2.1 Vehicles & Trailers Module - February 28, 2026**
- Vehicle profiles (LKV heavy trucks, PKV light vehicles)
- Trailer profiles (Standard, Mega, Frigo, Van, Tautliner)
- Technical specs and documents tracking
- Service management (internal + external)
- Fuel consumption tracking
- Fines & accidents tracking
- Transport Unit concept (Driver + Vehicle + Trailer)

**2.2 Customers Module - March 15, 2026**
- Customer companies (order transport)
- Carrier companies (provide transport)
- Credit limit management with real-time tracking
- Bank account details (multiple per customer)
- EU VAT validation via VIES system
- Customer rating system (Excellent, Good, Neutral, Poor)

**2.3 Orders Module - April 30, 2026**
- Order lifecycle with 9 statuses (Draft → Closed)
- Loading/unloading points with addresses
- Route planning with distance calculation
- Document management (CMR, POD, order files)
- Transport Unit assignment
- Automatic status transitions (when CMR + POD uploaded)
- Financial tracking (revenue, costs, profit per order)

**2.4 Invoices Module - May 31, 2026**
- Invoice generation with EU VAT compliance
- 3 VAT modes: Domestic, Reverse Charge, Non-VAT
- Automatic VAT mode detection based on customer country
- Multi-currency support (CZK, PLN, EUR, USD)
- PDF generation with bilingual templates (EN + customer language)
- Payment tracking (Paid, Partly Paid, Overdue)
- Integration with order profitability

**2.5 Financial Dashboard - June 15, 2026**
- Revenue vs Expenses charts
- Profitability per order, per driver, per vehicle
- Overdue invoices alerts
- Credit limit usage by customer
- Monthly/quarterly financial reports

### Success Criteria
- [ ] Complete order flow from creation to invoice to payment
- [ ] Automatic VAT calculation with 100% accuracy (tested with 50+ scenarios)
- [ ] Transport Unit readiness validation working
- [ ] Financial dashboard showing accurate profit margins
- [ ] 10+ production clients using the system

---

## Phase 3: GPS & Analytics
**Timeline:** Q2-Q3 2026 (July - September 2026)

**Primary Goal:** Add real-time GPS tracking and advanced analytics

### Deliverables

**3.1 GPS Tracking Integration - July 31, 2026**
- GPS device integration (Teltonika, Ruptela, or similar)
- Real-time position tracking on map (Google Maps API)
- Route history visualization
- Geofencing alerts (driver enters/exits zones)
- TimescaleDB for time-series GPS data storage
- REST API + WebSockets for live updates (Laravel Reverb)

**3.2 Driver Behavior Analytics - August 15, 2026**
- Speeding detection and alerts
- Harsh braking/acceleration events
- Driving hours tracking (compliance with EU regulations)
- Idle time analysis (fuel waste)
- Driver safety score

**3.3 Advanced Reporting - September 15, 2026**
- Custom report builder (drag-and-drop)
- Pre-built reports: Driver Performance, Vehicle Utilization, Order Profitability
- Export to Excel/PDF/CSV
- Scheduled reports via email
- Dashboard widgets (customizable per user role)

**3.4 Mobile App (PWA) - September 30, 2026**
- Progressive Web App installable on iOS/Android
- Driver self-service: view profile, upload documents, view assigned orders
- Push notifications for document expiration
- Offline mode for document viewing
- Telegram Bot integration (document upload via chat)

### Success Criteria
- [ ] Real-time GPS tracking with <30 second latency
- [ ] Geofencing alerts with 100m accuracy
- [ ] Driver behavior analytics with weekly safety reports
- [ ] Mobile app with 4.5+ stars on app stores
- [ ] 30+ production clients

---

## Phase 4: Advanced Features & Integrations
**Timeline:** Q3-Q4 2026 (October - December 2026)

**Primary Goal:** Enterprise features, integrations, and AI-powered automation

### Deliverables

**4.1 Fuel Card Integration - October 15, 2026**
- API integration with fuel card providers (DKV, UTA, Shell)
- Automatic fuel expense tracking
- Fuel consumption analytics per vehicle/driver
- Fuel fraud detection (unusual consumption patterns)

**4.2 Accounting System Integration - October 31, 2026**
- Export invoices to accounting systems (POHODA, Money S3, Winfakt)
- Automatic expense categorization
- VAT reports for tax authorities
- Bank statement reconciliation

**4.3 AI-Powered Features - November 30, 2026**
- Predictive document expiration (warn 60 days in advance)
- Route optimization (AI suggests best routes based on historical data)
- Dynamic pricing (recommend order prices based on costs + profit margin)
- Chatbot for driver support (answer FAQs via Telegram)

**4.4 Multi-Office Management - December 15, 2026**
- Office hierarchy (HQ → Regional Offices)
- Cross-office visibility controls
- Office-specific settings (work hours, holidays, languages)
- Consolidated reports across all offices

**4.5 White-Label & API for Partners - December 30, 2026**
- White-label branding (custom logo, colors, domain)
- Public REST API for third-party integrations
- Webhooks for real-time event notifications
- API rate limiting and usage analytics

### Success Criteria
- [ ] Fuel card integration with 90%+ automatic expense matching
- [ ] Accounting export with 100% accuracy (no manual adjustments)
- [ ] AI features adopted by 50%+ of users
- [ ] Multi-office management working for 10+ clients
- [ ] White-label deployed for 3+ partners
- [ ] 100+ production clients, €50k+ MRR (Monthly Recurring Revenue)

---

## Development Principles

**1. Drivers Module First (ALWAYS)**
- Drivers Module is Priority #1 and MUST reach 100% before moving to other modules
- Target: November 10, 2025 for Drivers Module 100% complete
- All other modules (Vehicles, Orders, Invoices) marked as "Coming Soon" until Drivers is finished

**2. Multi-Tenancy Security (NON-NEGOTIABLE)**
- Every query MUST include `company_id` filter (global scope)
- Row-Level Security (RLS) in PostgreSQL for defense-in-depth
- Regular security audits (monthly during MVP, quarterly in production)

**3. Mobile-First Design**
- Many drivers use mobile phones (not desktops)
- All UI components must work on 375px width (iPhone SE)
- PWA for installable mobile app experience

**4. EU Compliance**
- GDPR: Data protection, right to erasure, data portability
- eIDAS: Digital signatures for CMR documents (future)
- EU VAT Directive 2006/112/EC: Reverse Charge compliance

**5. Performance Targets**
- API response time: <500ms (p95), <200ms (p50)
- Frontend First Contentful Paint: <1.5s
- Database queries: <50ms (p95)
- Uptime SLA: 99.5% (max 43 hours downtime/year)

**6. Testing Coverage**
- Backend: 80%+ code coverage (Pest)
- Frontend: 70%+ code coverage (Jasmine)
- E2E: All critical user flows (Drivers Module CRUD, Document Upload, Order Flow)

---

## Risks & Mitigation

**Risk 1: Document Upload Complexity**
- **Mitigation:** Start with simple file upload, iterate based on user feedback
- **Fallback:** Manual upload via admin UI if Telegram Bot integration fails

**Risk 2: Multi-Tenancy Data Leaks**
- **Mitigation:** Automated tests for tenant isolation on EVERY API endpoint
- **Fallback:** Row-Level Security (RLS) in PostgreSQL as backup defense layer

**Risk 3: GPS Tracking Vendor Lock-in**
- **Mitigation:** Abstract GPS provider behind interface (support multiple vendors)
- **Fallback:** Manual order tracking if GPS integration fails

**Risk 4: Scaling Beyond 100 Clients**
- **Mitigation:** Database read replicas, Redis caching, CDN for static assets
- **Fallback:** Vertical scaling (upgrade server specs) as interim solution

**Risk 5: EU VAT Regulation Changes**
- **Mitigation:** Configurable VAT rates and rules (no hardcoding)
- **Fallback:** Manual invoice adjustment by accountants

---

## Technology Stack Evolution

**Current (Phase 1 - MVP):**
- Frontend: Angular 20, Angular Material 20, RxJS
- Backend: Laravel 12, PostgreSQL 16, Redis
- Deployment: Vercel (frontend), Laravel Cloud (backend)
- Monitoring: Sentry, CloudWatch

**Phase 2 Additions:**
- Payment gateway: Stripe (for subscription billing)
- PDF generation: Browsershot (headless Chrome)
- Email: Mailgun (transactional emails)

**Phase 3 Additions:**
- GPS data: TimescaleDB (time-series extension for PostgreSQL)
- Maps: Google Maps API (routes, geocoding)
- WebSockets: Laravel Reverb (real-time updates)

**Phase 4 Additions:**
- AI/ML: OpenAI API (route optimization, chatbot)
- Queue: Laravel Horizon (job monitoring)
- Search: Meilisearch (full-text search for drivers, orders)

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 16 (Development Roadmap)
