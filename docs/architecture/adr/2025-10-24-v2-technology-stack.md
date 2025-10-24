# ADR: V2 Technology Stack Selection

**Date:** 2025-10-24  
**Status:** ✅ Accepted  
**Decision Makers:** Technical Team  
**Related:** [V2 Stack Decision (2025-10-19)](2025-10-19-v2-stack.md)

---

## Context

G-Track TMS (Transport Management System) is being rebuilt from scratch as **Version 2** with modern technologies and best practices. The OLD version (legacy Angular + Laravel) served well for proof-of-concept and initial customer validation (~2.5 modules ready), but has accumulated technical debt and lacks modern development practices.

### Business Drivers
- Need for scalable, maintainable SaaS platform
- Support for multi-tenant architecture
- Real-time features (notifications, GPS tracking, status updates)
- Mobile-first approach (responsive web + future mobile apps)
- Compliance with EU data protection regulations (GDPR)
- Fast deployment cycles with CI/CD

### Technical Challenges in OLD Version
- Outdated Angular version (difficult to upgrade)
- Laravel version several years old
- No comprehensive test coverage
- Mixed authentication approaches
- No structured documentation
- Manual deployment process
- Performance issues with 100+ orders

---

## Decision

We will build G-Track V2 with the following technology stack:

### Frontend Stack

**Framework:** Angular 20 (latest stable)
- **Rationale:** 
  - Team has Angular expertise from OLD version
  - Strong TypeScript support
  - Mature ecosystem with extensive tooling
  - Excellent Material Design integration
  - Built-in CLI for scaffolding and testing
  - Server-side rendering (SSR) support for SEO
  - Signals for reactive state management

**UI Framework:** Angular Material UI
- **Rationale:**
  - Official Material Design implementation for Angular
  - Consistent, professional look and feel
  - Accessibility (a11y) built-in
  - Responsive components out of the box
  - Active maintenance by Google
  - Theming support for custom branding

**State Management:** Angular Signals + RxJS
- **Rationale:**
  - Native Angular Signals (new in v16+) for simpler reactivity
  - RxJS for complex async operations
  - Less boilerplate than NgRx
  - Better performance with fine-grained reactivity

**Build Tool:** Vite (via Angular CLI)
- **Rationale:**
  - Faster development builds
  - Hot Module Replacement (HMR)
  - Modern ES modules support
  - Native Angular 20 integration

### Backend Stack

**Framework:** Laravel 11 (latest LTS)
- **Rationale:**
  - Mature PHP framework with excellent ecosystem
  - Built-in API support (Laravel Sanctum, Passport)
  - Eloquent ORM for database abstraction
  - Queue system for background jobs
  - Event broadcasting for real-time features
  - Strong security features
  - Active community and extensive packages

**Language:** PHP 8.3+
- **Rationale:**
  - Modern PHP with type hints and attributes
  - Performance improvements (JIT compiler)
  - Better error handling
  - Enum support for status types

**Testing:** Pest PHP
- **Rationale:**
  - Modern testing framework for PHP
  - Elegant, readable test syntax
  - Built-in expectations API
  - Faster than PHPUnit for most cases
  - Better developer experience

**API Style:** RESTful JSON API
- **Rationale:**
  - Standard, well-understood approach
  - Easy to document (OpenAPI/Swagger)
  - Works with any frontend framework
  - Good caching support
  - Future GraphQL layer possible if needed

### Database

**Primary Database:** PostgreSQL 16
- **Rationale:**
  - ACID compliance for financial data
  - JSON/JSONB support for flexible metadata
  - Full-text search capabilities
  - Excellent performance with large datasets
  - Advanced indexing (GiST, GIN)
  - PostGIS for future GPS tracking features
  - Strong data integrity constraints
  - Better for complex queries than MySQL

**Schema Migration:** Laravel Migrations
- **Rationale:**
  - Version control for database schema
  - Rollback capabilities
  - Seeding for test data
  - Team synchronization

### Authentication & Authorization

**Auth Provider:** Auth0
- **Rationale:**
  - Enterprise-grade authentication
  - OAuth 2.0 / OpenID Connect standards
  - Multi-factor authentication (MFA) support
  - Social login options (future feature)
  - Passwordless authentication options
  - Compliance with security standards
  - Reduces security implementation burden

**Token Type:** RS256 (RSA Signature with SHA-256)
- **Rationale:**
  - Asymmetric signing (public/private keys)
  - Backend can verify tokens without Auth0 API calls
  - Better for distributed systems
  - Industry standard for JWTs

**Authorization:** Custom RBAC in Laravel
- **Rationale:**
  - Domain-specific roles (Admin, HR, Dispatcher, Accounting, Driver)
  - Granular permissions per module
  - Policies for complex authorization logic
  - Audit trail for permission changes

### Deployment & Infrastructure

**Frontend Deployment:** Vercel
- **Rationale:**
  - Optimized for Angular/React/Next.js
  - Automatic deployments from Git
  - Global CDN for fast page loads
  - Preview deployments for PRs
  - Zero-config SSL
  - Excellent developer experience

**Backend Deployment:** Laravel Cloud
- **Rationale:**
  - Official Laravel hosting solution
  - Optimized for Laravel applications
  - Built-in queue workers
  - Database backups
  - Monitoring and logging
  - Horizontal scaling support
  - Managed PostgreSQL

**Documentation Hosting:** GitHub Pages
- **Rationale:**
  - Free hosting for public repos
  - Automatic deployment via GitHub Actions
  - Custom domain support (docs.g-track.eu)
  - Version control integrated
  - Fast and reliable

**Documentation Tool:** MkDocs Material
- **Rationale:**
  - Beautiful, professional documentation sites
  - Markdown-based (easy to write and review)
  - Full-text search
  - Responsive design
  - Code syntax highlighting
  - Navigation breadcrumbs
  - Dark mode support

### CI/CD

**Platform:** GitHub Actions
- **Rationale:**
  - Native Git integration
  - Free for public repos
  - Matrix builds for testing multiple environments
  - Extensive marketplace of actions
  - Secrets management

**Frontend Pipeline:**
- `gtrack-ci-v2` workflow: Node.js build + linting
- `gtrack-policy-v2` workflow: Branch name, fresh branch, docs block checks
- Preview deployments on Vercel for PRs

**Backend Pipeline:**
- `gtrack-ci-v2` workflow: PHP build + Pest tests + code coverage
- `gtrack-policy-v2` workflow: Same policy checks as frontend
- Deployment to Laravel Cloud on merge to main

**Documentation Pipeline:**
- `mkdocs build --strict` on every PR
- Preview deployments for docs changes
- Auto-sync from frontend/backend `docs/**` folders
- Deployment to GitHub Pages on merge to main

### Development Tools

**Version Control:** Git + GitHub
- Monorepo approach: 3 separate repos (gtrack-app, gtrack-backend, gtrack-docs)
- Protected main branch
- PR-based workflow
- Automated checks before merge

**Code Quality:**
- **Frontend:** ESLint + Prettier
- **Backend:** PHP CS Fixer + PHPStan (static analysis)
- **Tests:** Jest (FE), Pest (BE)
- **Coverage:** Minimum 80% for critical paths

**API Documentation:** 
- OpenAPI 3.0 specification
- Swagger UI for interactive docs
- Auto-generated from Laravel routes and controllers

---

## Alternatives Considered

### Frontend Alternatives

**React + Next.js**
- ✅ Pros: Huge ecosystem, modern, SSR/SSG support
- ❌ Cons: Team has Angular expertise, would require retraining
- **Decision:** Stick with Angular (team familiarity, faster development)

**Vue.js 3 + Nuxt**
- ✅ Pros: Easier learning curve, good performance
- ❌ Cons: Smaller ecosystem than Angular/React, less enterprise adoption
- **Decision:** Angular more suitable for large-scale enterprise app

**Svelte + SvelteKit**
- ✅ Pros: Less boilerplate, excellent performance
- ❌ Cons: Smaller ecosystem, less mature tooling
- **Decision:** Too risky for production SaaS

### Backend Alternatives

**Node.js + Express/NestJS**
- ✅ Pros: JavaScript everywhere, good async performance
- ❌ Cons: Team has PHP expertise, less mature ecosystem for ERP-like apps
- **Decision:** Laravel provides better structure for complex business logic

**Django (Python)**
- ✅ Pros: "Batteries included" framework, Django admin
- ❌ Cons: Team has no Python experience, smaller hosting options
- **Decision:** Laravel Cloud makes Laravel more attractive

**FastAPI (Python)**
- ✅ Pros: Modern, fast, automatic API docs
- ❌ Cons: Newer framework, less ecosystem maturity
- **Decision:** Laravel has better TMS/ERP packages available

### Database Alternatives

**MySQL 8**
- ✅ Pros: Familiar to team, good Laravel support
- ❌ Cons: Less advanced features than PostgreSQL, weaker JSON support
- **Decision:** PostgreSQL better for complex queries and future features (PostGIS)

**MongoDB**
- ✅ Pros: Flexible schema, good for rapid development
- ❌ Cons: No ACID guarantees, not suitable for financial data
- **Decision:** ACID compliance critical for TMS financial transactions

### Auth Alternatives

**Laravel Sanctum (Self-hosted)**
- ✅ Pros: Free, full control, Laravel-native
- ❌ Cons: More security responsibility, need to implement MFA ourselves
- **Decision:** Auth0 provides enterprise features out of the box

**Firebase Auth**
- ✅ Pros: Easy setup, Google ecosystem
- ❌ Cons: Vendor lock-in, harder to migrate data
- **Decision:** Auth0 more flexible and enterprise-focused

---

## Consequences

### Positive

✅ **Developer Experience:**
- Modern tooling and frameworks
- Fast development cycles with HMR and auto-reload
- Comprehensive testing support
- Clear separation of concerns

✅ **Performance:**
- Angular Signals for reactive UI updates
- PostgreSQL indexing for fast queries
- Vercel CDN for global content delivery
- Laravel Cloud optimized for PHP

✅ **Scalability:**
- Horizontal scaling on Laravel Cloud
- Database read replicas support
- Queue workers for background jobs
- CDN for static assets

✅ **Security:**
- Auth0 handles auth complexity
- RS256 tokens for secure API access
- Laravel security features (CSRF, XSS protection)
- Regular security updates from framework vendors

✅ **Maintainability:**
- Comprehensive documentation (MkDocs)
- Automated testing (Jest + Pest)
- Code quality tools (ESLint, PHPStan)
- Clear architecture patterns (MVC, Service layer)

✅ **Cost-Effective:**
- Vercel free tier for small teams
- Laravel Cloud pricing scales with usage
- GitHub Actions free for public repos
- Auth0 free tier sufficient for MVP

### Negative

⚠️ **Learning Curve:**
- Angular 20 has breaking changes from OLD version
- Auth0 requires understanding of OAuth 2.0/OIDC
- PostgreSQL JSON queries different from MySQL

⚠️ **Migration Effort:**
- Need to rewrite frontend completely (Angular OLD → Angular 20)
- Database migration from MySQL → PostgreSQL
- Auth migration to Auth0
- Estimated: 3-4 months for core modules

⚠️ **Vendor Dependencies:**
- Auth0 pricing may increase as user base grows
- Laravel Cloud is newer service (less proven than AWS/Azure)
- Vercel pricing for high-traffic scenarios

⚠️ **Testing Requirements:**
- Need comprehensive test coverage before migration
- E2E testing required for critical workflows
- Load testing for performance validation

---

## Migration Strategy

### Phase 1: Foundation (Months 1-2)
- ✅ Setup repositories (gtrack-app, gtrack-backend, gtrack-docs)
- ✅ Configure CI/CD pipelines
- ✅ Setup Auth0 tenant
- ✅ Create base Angular 20 project structure
- ✅ Create base Laravel 11 API structure
- ✅ Setup PostgreSQL database

### Phase 2: Core Module - Drivers (Month 2-3)
- 🔄 **Current Phase**
- Implement Drivers module (first priority)
- Full documentation (TECH_SPEC, API, DATA_MODEL, RBAC)
- Complete test coverage (>80%)
- User acceptance testing
- Production deployment with real data

### Phase 3: Vehicle & Trailers (Month 3-4)
- Implement Vehicles & Trailers module
- Integration with Drivers (Transport Unit)
- Document management system
- Testing and deployment

### Phase 4: Migration of Existing Modules (Months 4-6)
- Migrate Customers module (90% ready in OLD → 100% in V2)
- Migrate Orders module (85% ready in OLD → 100% in V2)
- Migrate Invoices module (20% ready in OLD → 100% in V2)
- Data migration scripts (MySQL → PostgreSQL)
- Parallel running (OLD + V2) for validation

### Phase 5: Advanced Features (Months 6-8)
- GPS tracking integration
- Mobile app (future)
- Advanced analytics and reporting
- Third-party integrations (accounting software)
- Webhooks for event notifications

---

## Risks & Mitigation

### Risk: Laravel Cloud Stability
**Mitigation:** 
- Have migration path to AWS/Azure documented
- Use standard Laravel features (avoid Cloud-specific features)
- Regular backups

### Risk: Auth0 Cost Growth
**Mitigation:**
- Monitor user growth and plan budget
- Document migration path to self-hosted Keycloak if needed
- Use Auth0 Actions carefully (billed separately)

### Risk: PostgreSQL Performance
**Mitigation:**
- Proper indexing strategy
- Query optimization from day 1
- Regular VACUUM and ANALYZE
- Connection pooling (PgBouncer)

### Risk: Angular Breaking Changes
**Mitigation:**
- Follow Angular update guides carefully
- Maintain good test coverage
- Regular updates (don't skip versions)

---

## Review & Update Schedule

This ADR should be reviewed:
- ✅ After Phase 2 completion (Drivers module) - Validate technology choices
- 📅 Q2 2026 - After Phase 4 completion (all modules migrated)
- 📅 Q4 2026 - Annual technology review
- 🔄 Whenever major version updates available (Angular, Laravel, PostgreSQL)

---

## References

- [Angular 20 Documentation](https://angular.dev/)
- [Laravel 11 Documentation](https://laravel.com/docs/11.x)
- [PostgreSQL 16 Documentation](https://www.postgresql.org/docs/16/)
- [Auth0 Documentation](https://auth0.com/docs)
- [Material Design 3](https://m3.material.io/)
- [Vercel Documentation](https://vercel.com/docs)
- [Laravel Cloud Documentation](https://cloud.laravel.com/docs)

---

## Appendix: Version Compatibility Matrix

| Component | Version | Released | Support Until | Notes |
|-----------|---------|----------|---------------|-------|
| Angular | 20.x | Oct 2024 | Oct 2026 | LTS version |
| Laravel | 11.x | Feb 2024 | Feb 2026 | LTS version |
| PHP | 8.3.x | Nov 2023 | Nov 2026 | Active support |
| PostgreSQL | 16.x | Sep 2023 | Nov 2028 | 5 years support |
| Node.js | 20.x LTS | Oct 2023 | Apr 2026 | LTS version |
| Auth0 | SaaS | N/A | N/A | Managed service |

All versions selected are LTS (Long Term Support) to ensure stability and reduce upgrade frequency.

---

**Status:** ✅ Accepted and In Implementation  
**Next Review:** After Drivers Module Launch (Q1 2026)
