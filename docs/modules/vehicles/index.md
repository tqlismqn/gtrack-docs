# Module: Vehicles & Trailers

## Status
🔜 **Next Priority** - Documentation starts after Drivers module completion

## Overview
Vehicles & Trailers module manages the fleet of trucks and trailers used for transport operations.

This module is the **second priority** after Drivers module and is required before Orders can be fully integrated.

## Planned Timeline
1. ✅ Drivers module (current - in development)
2. 🔜 **Vehicles & Trailers module** (next)
3. 📝 Customers & Orders migration
4. 📝 Invoices module

## Key Features (Planned)

### Vehicles (Trucks)
- Vehicle registration and documentation
- Technical inspection tracking (STK)
- Insurance management
- Service history
- Fuel consumption tracking
- GPS tracking integration

### Trailers
- Trailer registration
- Technical documentation
- Inspection schedules
- Maintenance history
- Compatibility with vehicles

### Transport Units
- **Transport Unit** = Driver + Vehicle + Trailer
- Readiness checking (all documents valid)
- Assignment to orders
- Performance tracking

## Integration Points

**With Drivers Module:**
```
Driver (🟢 ready) + Vehicle (🟢 ready) + Trailer (🟢 ready) 
= Transport Unit (ready for order assignment)
```

**With Orders Module:**
- Transport Unit assigned to Order
- Tracking and status updates
- Document management (CMR, POD, etc.)

## Document Types

### For Vehicles:
- Registration certificate (Technický průkaz)
- Insurance policy (Pojištění)
- Technical inspection (STK)
- Emission test certificate
- Service records

### For Trailers:
- Registration certificate
- Technical inspection (STK)
- Service records
- Compatibility documentation

## Business Rules (Draft)

**Vehicle/Trailer is ready if:**
- All documents 🟢 (valid) OR 🟡 (expiring soon, ≤30 days)
- NO 🔴 (expired) documents

**Document validity indicators:**
- 🟢 Green - valid (>60 days until expiration)
- 🟠 Orange - warning (31-60 days)
- 🟡 Yellow - expiring soon (≤30 days)
- 🔴 Red - expired
- ⚪ Gray - no data

## Next Steps
Full technical specification and data model documentation will be published in Q4 2025 after Drivers module launch.

## Notes
This is a placeholder. Comprehensive documentation including:
- Technical specifications
- Data model
- API endpoints
- RBAC (roles and permissions)
- Validation rules
- UI/UX guidelines

...will be added as part of the V2 development cycle.
