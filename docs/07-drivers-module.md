# Drivers Module (PRIORITY #1)

**Status:** 🟡 90% Complete (in active development)
**Goal:** Complete before other modules
**Target:** 150-200 drivers per company

## Business Logic

**Problem Statement:**

```
Client manages 150-170 drivers in Excel:
❌ Manual tracking of 14 document types
❌ No alerts for expiring documents
❌ 5+ hours/week checking expirations manually
❌ Cannot answer "Who is ready for delivery today?"
❌ Fines from expired licenses/permits
```

**Solution:**

```
✅ Digital driver profiles with 14 document types
✅ Automatic expiration tracking (30/15/7 day alerts)
✅ Visual status indicators: 🟢 valid, 🟡 expiring, 🔴 expired
✅ "Readiness Dashboard" - instant overview
✅ Mobile document upload via Telegram Bot
✅ RBAC - HR sees everything, Dispatcher sees readiness only
```

## 14 Document Types

Each driver has these documents tracked:

| # | Document Type | Fields | Expiration Logic |
|---|---------------|--------|------------------|
| 1 | **Passport** | Number, Country, Valid Until | Alert 30 days before |
| 2 | **Visa/Biometrics** | Number, Type, Valid Until | Alert 30 days before |
| 3 | **Residence Permit** | Valid From, Valid Until | Alert 30 days before |
| 4 | **Work Permit/License** | Valid From, Valid Until | Alert 30 days before |
| 5 | **A1 Certificate (EU)** | Valid From, Valid Until | Alert 30 days before |
| 6 | **A1 Switzerland** | Valid From, Valid Until | Alert 30 days before |
| 7 | **Declaration** | Valid Until | Alert 30 days before |
| 8 | **Health Insurance** | Valid Until | Alert 15 days before |
| 9 | **Travel Insurance** | Valid Until | Alert 15 days before |
| 10 | **Driver's License** | Number, Categories, Valid Until | Alert 60 days before |
| 11 | **ADR Certificate** | Valid Until | Alert 30 days before |
| 12 | **Tachograph Card** | Number, Valid Until | Alert 30 days before |
| 13 | **Code 95** | Valid Until | Alert 60 days before |
| 14 | **Medical Examination** | Valid From, Valid Until | Special logic* |

**Special Logic - Medical Examination (Psychotest):**
```
IF driver age < 60:
    Validity = 3 years
ELSE:
    Validity = 1 year

Alert timing:
    60 days before expiry
```

## Status Indicators

**Visual System:**

```
🟢 Valid (Zelený)
   - Document is valid for >30 days
   - Driver can work

🟡 Expiring Soon (Žlutý)
   - Document expires within 30 days
   - Driver can still work (warning)

🟠 Warning (Oranžový)
   - Document expires within 15 days
   - Urgent renewal needed

🔴 Expired (Červený)
   - Document has expired
   - Driver CANNOT work

⚪ No Data (Šedý)
   - Document not uploaded
   - Cannot determine readiness
```

**Readiness Logic:**

```typescript
function isDriverReady(driver: Driver): boolean {
    const statuses = driver.documents.map(d => d.status);

    // Driver is ready if:
    // - Status is Active
    // - All documents are 🟢 (valid) OR 🟡 (expiring soon)
    // - NO documents are 🔴 (expired) or ⚪ (missing)

    if (driver.status !== 'active') return false;

    const hasExpiredOrMissing = statuses.some(s =>
        s === 'expired' || s === 'no_data'
    );

    return !hasExpiredOrMissing;
}
```

## Driver Profile Structure

**Overview Tab:**

```
┌──────────────────────────────────────────────┐
│ Jan Novák                          #DRV-0001 │
├──────────────────────────────────────────────┤
│                                              │
│ Status: 🟢 Active                            │
│ Readiness: ✅ Ready for delivery             │
│                                              │
│ Personal Info                                │
│ ├─ Birth Date: 1985-03-15 (40 years)        │
│ ├─ Citizenship: 🇨🇿 Czech Republic           │
│ ├─ Rodné číslo: 850315/1234                 │
│ ├─ Email: jan.novak@driver.cz               │
│ ├─ Phone: +420 777 123 456                  │
│ └─ Address: Praha 3, Vinohradská 123        │
│                                              │
│ Employment                                   │
│ ├─ Hire Date: 2020-01-15                    │
│ ├─ Contract: Indefinite                     │
│ ├─ Work Location: Praha                     │
│ └─ Internal Number: DRV-0001 (never changes)│
│                                              │
│ Documents Summary                            │
│ ├─ 🟢 Valid: 12                             │
│ ├─ 🟡 Expiring: 1                           │
│ ├─ 🔴 Expired: 1                            │
│ └─ ⚪ Missing: 0                             │
│                                              │
│         [Edit Profile]  [Terminate]          │
└──────────────────────────────────────────────┘
```

**Documents Tab:**

```
┌──────────────────────────────────────────────┐
│ Documents (14 types)                         │
├──────────────────────────────────────────────┤
│                                              │
│ 🟢 Passport                                  │
│    Number: CZ1234567                         │
│    Valid Until: 2028-05-20                   │
│    📎 passport_scan.pdf (2.1 MB)            │
│    [View] [Replace] [History]               │
│                                              │
│ 🟢 Driver's License                          │
│    Number: DL987654                          │
│    Categories: C, CE, D                      │
│    Valid Until: 2027-03-15                   │
│    📎 drivers_license.pdf (1.8 MB)          │
│    [View] [Replace] [History]               │
│                                              │
│ 🟡 Medical Examination                       │
│    Valid From: 2023-10-01                    │
│    Valid Until: 2025-12-15 (49 days left)   │
│    📎 medical_exam_2023.pdf (0.9 MB)        │
│    ⚠️ Renewal needed soon!                   │
│    [View] [Replace] [Schedule Renewal]      │
│                                              │
│ 🔴 ADR Certificate                           │
│    Valid Until: 2024-08-30 (EXPIRED)        │
│    📎 adr_cert_2022.pdf (1.2 MB)            │
│    ❌ Driver cannot transport dangerous goods│
│    [Upload New Document] [Request from HR]  │
│                                              │
│ ⚪ A1 Switzerland                            │
│    No document uploaded                      │
│    [Upload Document]                         │
│                                              │
│ [+ Upload New Document Type]                 │
└──────────────────────────────────────────────┘
```

**Finance Tab:**

```
┌──────────────────────────────────────────────┐
│ Finance - Jan Novák (#DRV-0001)              │
├──────────────────────────────────────────────┤
│                                              │
│ Current Month (October 2025)                 │
│                                              │
│ Base Salary:         50,000 CZK              │
│ Business Trips:      +8,500 CZK              │
│ Bonuses:             +2,000 CZK              │
│ Fines:               -1,500 CZK              │
│ Damages (accidents): -5,000 CZK              │
│ ───────────────────────────────              │
│ NET SALARY:          54,000 CZK              │
│                                              │
│ Transaction History                          │
│ ┌────────────────────────────────────────┐  │
│ │ 🟢 27.10.2025 | Bonus | +2,000 CZK     │  │
│ │    Reason: Urgent delivery completed   │  │
│ │    Order: ORD-2025-0123                │  │
│ │                                        │  │
│ │ 🔴 20.10.2025 | Fine | -500 CZK        │  │
│ │    Reason: Speeding (20 km/h over)     │  │
│ │    Order: ORD-2025-0098                │  │
│ │                                        │  │
│ │ 🔴 15.10.2025 | Damage | -5,000 CZK    │  │
│ │    Reason: Accident (cargo damaged)    │  │
│ │    Order: ORD-2025-0087                │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ [Add Transaction] [Export Report]            │
└──────────────────────────────────────────────┘
```

**Comments Tab:**

```
┌──────────────────────────────────────────────┐
│ Comments & Notes                             │
├──────────────────────────────────────────────┤
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ 📝 New Comment                         │  │
│ │ [Write comment here_________________]  │  │
│ │                                        │  │
│ │ 📎 Attach file (optional)              │  │
│ │                                        │  │
│ │         [Post Comment]                 │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ Comments (5):                                │
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ admin@company.cz | 26.10.2025 14:30    │  │
│ │                                        │  │
│ │ Driver complained about low salary.    │  │
│ │ Discussed with HR, will review in Q4.  │  │
│ │                                        │  │
│ │ 💬 Reply  ✏️ Edit  🗑️ Delete           │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ [Load more comments...]                      │
└──────────────────────────────────────────────┘
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 7 (Module 1: Drivers)
