# Vehicles & Trailers Module

**Status:** 🔴 Not Started (Next after Drivers)
**Types:** LKV (Heavy Trucks) + PKV (Light Vehicles) + Trailers

## Business Logic

**Problem:**
```
❌ No centralized vehicle database
❌ Service schedules tracked in Excel
❌ Fines arrive months late (lost paperwork)
❌ Cannot see which vehicles are available
❌ Accident costs not tracked per vehicle
```

**Solution:**
```
✅ Digital vehicle profiles (technical specs + documents)
✅ Service request system (internal + external)
✅ Fine/accident tracking
✅ Availability dashboard
✅ Cost per vehicle analytics
```

## Vehicle Types

**1. LKV - Heavy Trucks (Nákladní vozidla)**

Used for:
- Long-haul transport
- International deliveries
- Assigned to Orders

Examples:
- MAN TGX 18.440
- Mercedes-Benz Actros
- Scania R450

Documents tracked:
- Vehicle Registration (Technický průkaz)
- Insurance (OSAGO, KASKO)
- Annual Inspection (STK)
- Tachograph Calibration
- CMR Insurance

**2. PKV - Light Vehicles (Osobní vozidla)**

Used for:
- Office errands
- Quick deliveries (documents, small cargo)
- Employee transport
- NOT assigned to Orders

Examples:
- Škoda Octavia
- VW Transporter
- Ford Transit

Assignment modes:
```
A) Assigned to specific driver (exclusive use)
B) Pool vehicle (anyone can use)
C) Unassigned (spare)
```

Documents tracked:
- Vehicle Registration
- Insurance
- Annual Inspection

**3. Trailers (Návěsy/přívěsy)**

Types:
- Standard (Standard)
- Mega (extra height)
- Frigo (refrigerated)
- Van (enclosed box)
- Tautliner (curtain-side)

Documents tracked:
- Trailer Registration
- Annual Inspection
- Refrigeration Service (if Frigo)

## Transport Unit Concept

**Definition:** Transport Unit = Driver + Vehicle + Trailer

**Ready State:**
```typescript
interface TransportUnit {
    driver: {
        id: string;
        status: 'active';
        all_documents_valid: true;  // All 🟢 or 🟡
    };
    vehicle: {
        id: string;
        type: 'lkv';
        all_documents_valid: true;
        not_in_service: true;
    };
    trailer: {
        id: string;
        type: 'standard' | 'mega' | 'frigo';
        all_documents_valid: true;
        not_in_service: true;
    };
    ready_for_order: true;
}
```

**Order Assignment:**
```
When Dispatcher creates Order:
1. Select Transport Unit from "Ready" list
2. Order.transport_unit_id = [unit_id]
3. System tracks:
   - Which driver drove
   - Which vehicle was used
   - Which trailer was attached
4. If accident/fine → linked to correct driver + vehicle
```

## Service Management

**Scenario 1: Planned Service (Internal)**

```
1. Vehicle VEH-0045 has 95,000 km
2. System alert: "Service due at 100,000 km"
3. HR/Admin creates Service Request:
   - Type: Scheduled Maintenance
   - Service Provider: Internal Workshop
   - Scheduled Date: 2025-11-05
4. Mechanic performs service:
   - Oil change
   - Brake inspection
   - Filter replacement
5. Cost: 3,500 CZK (internal labor + parts)
6. Vehicle status: Back to Active
```

**Scenario 2: Emergency Repair (External)**

```
1. Driver reports: "Strange engine noise"
2. Dispatcher creates Service Request:
   - Priority: 🔴 High
   - Location: Wrocław, Poland
   - Issue: Engine noise
3. System finds nearby services:
   - Auto Service PL (5 km) ⭐ 4.5/5
   - MAN Service Center (12 km) ⭐ 4.8/5
4. Dispatcher selects: Auto Service PL
5. Service completed:
   - Invoice uploaded: 500 EUR (Reverse Charge)
   - Work done: Alternator replacement
6. Expense logged:
   - vehicle_expenses table
   - Category: External Service
   - VAT mode: Reverse Charge (0%)
```

## Fines & Accidents

**Scenario: Speeding Fine**

```
1. Fine letter arrives:
   - Vehicle: VEH-0045 (MAN TGX 18.440)
   - Date: 2025-10-15, 14:30
   - Location: D1, km 45 (Czech Republic)
   - Offense: Speeding (140 km/h in 120 zone)
   - Amount: 500 CZK

2. Admin checks: Who was driving?
   - Lookup Order history for that date/time
   - Order: ORD-2025-0098
   - Driver: Jan Novák (#DRV-0001)

3. System creates transaction:
   - Fine added to driver_transactions
   - Deducted from driver's salary
   - Linked to Order (profitability impact)

4. History logs:
   - Vehicle VEH-0045: "Fine: 500 CZK (Speeding)"
   - Driver DRV-0001: "Fine: -500 CZK (Speeding, Order ORD-2025-0098)"
   - Order ORD-2025-0098: "Fine expense: 500 CZK"
```

**Scenario: Accident**

```
1. Driver calls: "Accident on highway"
   - Vehicle: VEH-0045
   - Order: ORD-2025-0087
   - Damage: Cargo damaged, truck body dented

2. Dispatcher creates Accident Report:
   - Photos uploaded (via mobile)
   - Police report number
   - Damage estimate: 50,000 CZK

3. Vehicle status → "In Repair"

4. Insurance claim initiated:
   - Claim #: INS-2025-123
   - Status: Pending

5. Repair completed:
   - Invoice from body shop: 48,000 CZK
   - Insurance pays: 40,000 CZK
   - Company pays: 8,000 CZK
   - Driver pays: 5,000 CZK (deductible from salary)

6. Financial impact:
   - Order ORD-2025-0087 profitability: -8,000 CZK
   - Driver DRV-0001 salary: -5,000 CZK
   - Vehicle VEH-0045 total costs YTD: +48,000 CZK
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 8 (Module 2: Vehicles & Trailers)
