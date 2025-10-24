# Archive - Legacy Documentation

## About This Section

This archive contains documentation from the **OLD version** of G-Track (legacy Angular + Laravel stack) that has been superseded by V2 documentation.

**Status:** 🗄️ Historical reference only  
**Relevance:** For understanding past decisions and migration context

---

## Why Archive?

The OLD version of G-Track served as a successful proof-of-concept and validated the business model with real customers. However, as we transition to V2 (Angular 20 + Laravel 11 + PostgreSQL 16), much of the OLD documentation is no longer accurate or relevant.

**We keep this archive for:**
- Understanding historical context
- Migration planning (comparing OLD vs V2 approaches)
- Learning from past decisions
- Reference for customers still on OLD version during transition

---

## What's Archived?

### Legacy Architecture Decision Records (ADRs)
Located in `archive/legacy-adr/`:
- Old technology stack decisions
- Previous architectural patterns
- Deprecated approaches
- Lessons learned

### Old Architecture Diagrams
- System diagrams from OLD version
- Database schemas (MySQL-based)
- Component architecture (legacy Angular)

### Deprecated API Documentation
- v0 API endpoints that won't be in V2
- Old authentication methods
- Legacy data models

---

## Current Documentation

**For up-to-date information, see:**
- **[Modules](../modules/drivers/index.md)** - Current V2 module documentation
- **[Architecture](../architecture/index.md)** - V2 architectural decisions
- **[API Reference](../api/index.md)** - Current API v0 and planned v1
- **[Overview](../overview.md)** - High-level system overview

---

## Archive Navigation

### Legacy ADRs
See [Legacy ADR Overview](legacy-adr/index.md) for a list of all archived architectural decision records from the OLD version.

**Note:** These ADRs are kept for historical reference but are no longer active. Current architectural decisions are documented in [Architecture > ADR](../architecture/index.md#architecture-decision-records-adrs).

---

## Migration Notes

If you're migrating from OLD version to V2, key differences include:

| Aspect | OLD Version | V2 |
|--------|------------|-----|
| Frontend | Angular (old) | Angular 20 |
| Backend | Laravel (old) | Laravel 11 |
| Database | MySQL | PostgreSQL 16 |
| Auth | Mixed approach | Auth0 (RS256) |
| Deployment | Manual | Vercel + Laravel Cloud |
| Testing | Limited | Comprehensive (Jest + Pest) |
| Documentation | Sparse | Comprehensive (MkDocs) |

For detailed migration strategy, see [V2 Technology Stack ADR](../architecture/adr/2025-10-24-v2-technology-stack.md#migration-strategy).

---

## Contributing to Archive

**Do NOT add new content to Archive** unless:
- You're documenting a deprecated feature for reference
- You're preserving an old ADR that's being replaced
- You're adding migration notes for a sunset feature

All new documentation should go in the main sections (Modules, Architecture, API, etc.).

---

**Last Updated:** 2025-10-24  
**Maintained by:** G-Track Development Team
