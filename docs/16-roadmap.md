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
