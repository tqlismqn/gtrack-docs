# Architecture Overview

This section contains architecture documentation for G-Track TMS, including:

## Architecture Decision Records (ADRs)

ADRs document significant architectural decisions made during the development of G-Track.

### V2 Stack
- **[2025-10-24: V2 Technology Stack](adr/2025-10-24-v2-technology-stack.md)** ⭐ Current
  - Comprehensive documentation of Angular 20, Laravel 11, PostgreSQL 16 stack
  - Rationale, alternatives, consequences, and migration strategy

- **[2025-10-19: V2 Stack Decision](adr/2025-10-19-v2-stack.md)** 
  - Initial decision for V2 technology stack

### Legacy Decisions (Archive)
Historical ADRs from OLD version are preserved in the [Legacy ADR collection](../adr/README.md) for reference.

## Key Architectural Principles

### 1. Separation of Concerns
- **Frontend:** Angular 20 SPA (Single Page Application)
- **Backend:** Laravel 11 RESTful API
- **Database:** PostgreSQL 16 for data persistence
- **Documentation:** MkDocs for technical documentation

### 2. Security First
- Auth0 for authentication (OAuth 2.0 / OIDC)
- RS256 JWT tokens for API authorization
- RBAC (Role-Based Access Control) for permissions
- HTTPS everywhere (enforced)

### 3. API-First Development
- RESTful JSON API design
- OpenAPI 3.0 specification
- Versioned endpoints (v0, v1)
- Consistent error handling

### 4. Test-Driven Quality
- Frontend: Jest + Angular Testing Library
- Backend: Pest PHP (>80% coverage target)
- E2E: Playwright for critical workflows
- CI/CD: Automated testing on every PR

### 5. Documentation as Code
- MkDocs Material for technical docs
- Auto-sync from code repositories
- API documentation from code (OpenAPI)
- Strict build to prevent broken links

### 6. Scalable Architecture
- Stateless API (horizontal scaling)
- Queue workers for async tasks
- Database read replicas (future)
- CDN for static assets

## System Diagrams

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           Users (Web Browsers, Mobile)          │
│                                                 │
└────────────────────┬────────────────────────────┘
                     │
                     │ HTTPS
                     │
         ┌───────────▼───────────┐
         │                       │
         │   Vercel CDN (FE)     │
         │   Angular 20 SPA      │
         │                       │
         └───────────┬───────────┘
                     │
                     │ REST API (HTTPS + JWT)
                     │
         ┌───────────▼────────────┐
         │                        │
         │  Laravel Cloud (BE)    │
         │  Laravel 11 API        │
         │  + Queue Workers       │
         │                        │
         └────┬──────────────┬────┘
              │              │
              │              │
    ┌─────────▼──┐      ┌───▼─────────┐
    │            │      │             │
    │ PostgreSQL │      │   Auth0     │
    │    16      │      │ (OAuth2.0)  │
    │            │      │             │
    └────────────┘      └─────────────┘
```

### Module Dependencies

```
         ┌─────────────┐
         │   Customer  │
         │  (Address)  │
         └──────┬──────┘
                │
                │ references
                │
    ┌───────────▼────────────┐
    │                        │
    │       Order            │
    │  (Transport Order)     │
    │                        │
    └───┬───────────────┬────┘
        │               │
        │ creates       │ references
        │               │
┌───────▼──────┐   ┌────▼─────────┐
│              │   │              │
│   Invoice    │   │ Transport    │
│              │   │    Unit      │
│              │   │              │
└──────────────┘   └────┬─────────┘
                        │
                        │ consists of
                        │
        ┌───────────────┼───────────────┐
        │               │               │
  ┌─────▼────┐   ┌──────▼────┐   ┌─────▼────┐
  │          │   │           │   │          │
  │  Driver  │   │  Vehicle  │   │  Trailer │
  │          │   │           │   │          │
  └──────────┘   └───────────┘   └──────────┘
```

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Angular | 20 | SPA framework |
| UI Library | Material UI | Latest | Component library |
| Backend | Laravel | 11 | API framework |
| Language | PHP | 8.3+ | Backend language |
| Testing | Pest | Latest | Backend testing |
| Database | PostgreSQL | 16 | Primary datastore |
| Auth | Auth0 | SaaS | Authentication |
| FE Deploy | Vercel | SaaS | Frontend hosting |
| BE Deploy | Laravel Cloud | SaaS | Backend hosting |
| Docs | MkDocs | Latest | Documentation |

## Next Steps

- Review [ADR: V2 Technology Stack](adr/2025-10-24-v2-technology-stack.md) for detailed rationale
- See the [Drivers Module](../modules/drivers/index.md) for feature documentation patterns
- Check [API Documentation](../api/index.md) for integration details
