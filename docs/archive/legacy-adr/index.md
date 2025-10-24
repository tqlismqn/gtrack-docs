# Legacy ADRs - Architecture Decision Records (OLD Version)

## About Legacy ADRs

This section contains Architecture Decision Records (ADRs) from the **OLD version** of G-Track, before the V2 rewrite with Angular 20 + Laravel 11 + PostgreSQL 16.

**Status:** 🗄️ Historical reference only  
**Current ADRs:** See [Architecture > ADR](../../architecture/index.md#architecture-decision-records-adrs) for active decisions

---

## Why Keep Legacy ADRs?

1. **Historical Context** - Understanding why certain decisions were made originally
2. **Lessons Learned** - Documenting what worked and what didn't
3. **Migration Planning** - Comparing OLD vs V2 approaches
4. **Institutional Knowledge** - Preserving the thinking behind technical choices

---

## Legacy ADR List

Below is a list of ADRs from the OLD version. These are preserved for reference but are **not active** decisions for V2 development.

**Note:** The actual legacy ADR files are preserved in the repository under `docs/archive/legacy-adr/` but are not shown in the navigation to keep it clean. If you need to reference a specific legacy ADR, you can:
- Browse the `docs/archive/legacy-adr/` folder directly in the repository
- Use the site search function
- Contact the development team

---

## Common Legacy ADRs (Examples)

The following types of ADRs are typically found in the legacy archive:

- **Technology Stack Choices** (OLD stack)
  - Angular version selection (pre-v20)
  - Laravel version selection (pre-v11)
  - MySQL vs other databases (superseded by PostgreSQL decision)
  
- **Authentication Approaches** (pre-Auth0)
  - Laravel Passport implementation
  - JWT token handling (old approach)
  
- **Architecture Patterns** (OLD patterns)
  - Monolith vs microservices discussions
  - API versioning strategy (pre-v0/v1)
  
- **Frontend Patterns** (OLD Angular)
  - State management approaches (pre-Signals)
  - Component architecture
  
- **Deployment Strategies** (pre-Vercel/Laravel Cloud)
  - Manual deployment processes
  - Server configuration decisions

---

## How Legacy ADRs Informed V2

The V2 technology stack decisions documented in [V2 Technology Stack ADR](../../architecture/adr/2025-10-24-v2-technology-stack.md) were informed by lessons learned from the OLD version:

**What We Kept:**
- Laravel backend (upgraded to v11) - strong business logic framework
- Angular frontend (upgraded to v20) - team expertise and ecosystem
- RESTful API approach - works well, no need to change

**What We Changed:**
- MySQL → PostgreSQL 16 - better for complex queries and JSON data
- Manual auth → Auth0 - reduced security burden
- Manual deployment → Vercel + Laravel Cloud - better DX and reliability
- Ad-hoc docs → MkDocs Material - professional, maintainable documentation

**What We Added:**
- Comprehensive testing (Jest + Pest)
- CI/CD automation (GitHub Actions)
- Proper versioning (v0, v1 APIs)
- Role-Based Access Control (RBAC)

---

## Current Architecture Decisions

**For V2 architectural decisions, see:**
- **[Architecture Overview](../../architecture/index.md)** - High-level architecture
- **[V2 Technology Stack ADR](../../architecture/adr/2025-10-24-v2-technology-stack.md)** - Comprehensive V2 decisions
- **[Initial V2 Decision](../../architecture/adr/2025-10-19-v2-stack.md)** - Initial V2 planning

---

## Notes on ADR Process

**Current ADR Process:**
1. Identify architectural decision needed
2. Research alternatives
3. Document in ADR format (Context, Decision, Consequences)
4. Review with team
5. Commit to `docs/architecture/adr/`
6. Update [Architecture Overview](../../architecture/index.md)

**Legacy ADR Process:**
- Legacy ADRs followed varying formats and processes
- Not all decisions were documented consistently
- V2 ADRs follow a standardized, comprehensive format

---

**Last Updated:** 2025-10-24  
**For Questions:** Contact G-Track Development Team
