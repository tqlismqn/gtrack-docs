# Module: Customers (Address Book / Contacts)

## Overview
Customers module manages all counterparties in the system:
- **Customers** - companies that order transportation services
- **Carriers** - companies that provide transportation services

This is one of the core modules of G-Track TMS, providing a single source of truth for all business relationships.

## Status
- **OLD Version**: ✅ 90% complete (2.5 modules ready)
- **V2 Migration**: 🔒 Coming Soon (after Drivers module completion)

## Key Features
- Unified management of customers and carriers
- Credit limit tracking
- Rating system
- Bank account management (multiple accounts per company)
- Document history and audit log

## User Roles
- **Admin**: Full CRUD access
- **HR**: Read access
- **Dispatcher**: Read access
- **Accounting**: Full access to financial data

## Next Steps
Full migration to v2 stack (Angular 20 + Laravel 11) is planned after successful Drivers module launch.

See [Business Logic](business-logic.md) for detailed specifications.
