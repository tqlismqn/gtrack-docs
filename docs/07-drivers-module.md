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

## Driver Rating System (NEW FEATURE 🆕)

**Status:** Planned for Week 1 (November 2025)
**Source:** `docs/business-logic/WEEK_1_ACTION_PLAN.md` (October 29, 2025)

### Overview

The Driver Rating System provides an automated, transparent, and configurable way to evaluate driver performance based on multiple metrics.

**Key Features:**
- ✅ Configurable metrics with adjustable weights
- ✅ Historical rating snapshots (trends over time)
- ✅ Rating explainability (transparency for drivers + HR)
- ✅ Telegram Bot integration
- ✅ Audit trail for all rating changes

### Metrics (Version 1)

**Configurable Metrics:**

| Metric | Type | Weight | Description |
|--------|------|--------|-------------|
| **Document Expiration** | Binary + Quantitative | 30% | 0 = all documents valid<br>1 = has expired documents<br>Quantitative: % of expired docs |
| **Penalties Count** | Quantitative | 20% | Number of penalties per period |
| **Penalties Amount** | Quantitative | 15% | Total penalty amount (CZK) |
| **Profile Completeness** | Percentage | 10% | % of filled fields (KYC data) |
| **Upload Timeliness** | Binary | 15% | Document uploaded before/after deadline |
| **Activity** | Quantitative | 10% | Logins, confirmations, reactions |

**Total:** 100% (weights configurable per company)

### Database Tables

**New Tables (4):**

**1. driver_score_config**
```sql
CREATE TABLE driver_score_config (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL REFERENCES companies(id),
    metric_name VARCHAR(50) NOT NULL,
    weight DECIMAL(5,2) NOT NULL, -- 0.00 to 100.00
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- Example data:
INSERT INTO driver_score_config VALUES
('uuid-1', 'company-1', 'document_expiration', 30.00, true),
('uuid-2', 'company-1', 'penalties_count', 20.00, true),
('uuid-3', 'company-1', 'penalties_amount', 15.00, true);
```

**2. driver_score_weights**
```sql
CREATE TABLE driver_score_weights (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    weight_value DECIMAL(5,2) NOT NULL,
    effective_from DATE NOT NULL,
    effective_until DATE,
    created_at TIMESTAMPTZ
);

-- Allows weight changes over time (historical tracking)
```

**3. driver_score_snapshots**
```sql
CREATE TABLE driver_score_snapshots (
    id UUID PRIMARY KEY,
    driver_id UUID NOT NULL REFERENCES drivers(id),
    total_score DECIMAL(5,2) NOT NULL, -- 0.00 to 100.00
    rating_period DATE NOT NULL, -- e.g., 2025-10-01 (monthly snapshot)
    components JSONB NOT NULL, -- { "document_expiration": 25.5, ... }
    created_at TIMESTAMPTZ
);

-- Example:
{
    "document_expiration": 30.0,
    "penalties_count": 18.5,
    "penalties_amount": 15.0,
    "profile_completeness": 9.8,
    "upload_timeliness": 12.0,
    "activity": 8.2
}
-- Total: 93.5 / 100
```

**4. driver_score_components**
```sql
CREATE TABLE driver_score_components (
    id UUID PRIMARY KEY,
    snapshot_id UUID NOT NULL REFERENCES driver_score_snapshots(id),
    metric_name VARCHAR(50) NOT NULL,
    raw_value DECIMAL(10,2), -- e.g., 3 expired documents
    normalized_score DECIMAL(5,2) NOT NULL, -- e.g., 20.5 / 30 points
    weight DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMPTZ
);

-- Detailed breakdown for explainability
```

### Rating Calculation Logic

**Step 1: Collect Raw Metrics**

```typescript
interface RawMetrics {
    documentExpiration: {
        totalDocuments: number;
        expiredDocuments: number;
        expiringDocuments: number;
    };
    penalties: {
        count: number; // last 30 days
        totalAmount: number; // CZK
    };
    profileCompleteness: {
        totalFields: number;
        filledFields: number;
    };
    uploadTimeliness: {
        onTimeUploads: number;
        lateUploads: number;
    };
    activity: {
        logins: number; // last 30 days
        confirmations: number;
        reactions: number;
    };
}
```

**Step 2: Normalize Each Metric (0-100)**

```typescript
function normalizeDocumentExpiration(raw: RawMetrics): number {
    if (raw.documentExpiration.totalDocuments === 0) return 0;

    const expiredRatio = raw.documentExpiration.expiredDocuments /
                         raw.documentExpiration.totalDocuments;

    // 0 expired = 100 points, all expired = 0 points
    return (1 - expiredRatio) * 100;
}

function normalizePenaltiesCount(raw: RawMetrics): number {
    // 0 penalties = 100 points
    // 1 penalty = 80 points
    // 5+ penalties = 0 points
    const penalties = raw.penalties.count;
    if (penalties === 0) return 100;
    if (penalties >= 5) return 0;

    return 100 - (penalties * 20);
}
```

**Step 3: Apply Weights**

```typescript
function calculateTotalScore(
    normalizedScores: Record<string, number>,
    weights: Record<string, number>
): number {
    let totalScore = 0;

    for (const [metric, score] of Object.entries(normalizedScores)) {
        const weight = weights[metric] || 0;
        totalScore += (score / 100) * weight;
    }

    return Math.round(totalScore * 100) / 100; // e.g., 87.35
}
```

**Step 4: Create Snapshot**

```typescript
// Save to database
await DriverScoreSnapshot.create({
    driver_id: driver.id,
    total_score: 87.35,
    rating_period: '2025-10-01',
    components: {
        document_expiration: 28.5, // 95% normalized × 30% weight
        penalties_count: 16.0,     // 80% normalized × 20% weight
        // ... other components
    }
});
```

### Telegram Bot Integration

**Commands:**

**1. Show Current Rating**
```
/rating

Response:
━━━━━━━━━━━━━━━━━━━━━━
⭐ YOUR DRIVER RATING ⭐
━━━━━━━━━━━━━━━━━━━━━━

Overall Score: 87.5 / 100 🟢

📊 Breakdown:
✅ Documents: 95% (28.5 pts)
⚠️ Penalties: 80% (16.0 pts)
💰 Penalty Amount: 100% (15.0 pts)
👤 Profile: 98% (9.8 pts)
⏰ Timeliness: 80% (12.0 pts)
📱 Activity: 82% (8.2 pts)

Rank: Top 15% in your company

[View Details] [History]
━━━━━━━━━━━━━━━━━━━━━━
```

**2. Explain Score**
```
/rating_explain

Response:
━━━━━━━━━━━━━━━━━━━━━━
📖 RATING EXPLANATION
━━━━━━━━━━━━━━━━━━━━━━

How your score is calculated:

🟢 Documents (95% → 28.5/30 pts)
   - All 14 documents valid ✅
   - No expired documents ✅
   - 0 missing documents ✅

🟡 Penalties (80% → 16.0/20 pts)
   - 1 penalty in last 30 days ⚠️
   - Details: Speeding (20 km/h over)
   - Tip: Drive carefully to avoid fines

🟢 Penalty Amount (100% → 15.0/15 pts)
   - Total: 500 CZK (low amount) ✅
   - Threshold: <1000 CZK = full points

🟢 Profile (98% → 9.8/10 pts)
   - Missing: Emergency contact ⚠️
   - Action: Update in your profile

🟡 Timeliness (80% → 12.0/15 pts)
   - 4 on-time uploads ✅
   - 1 late upload ⚠️
   - Tip: Upload documents before deadline

🟡 Activity (82% → 8.2/10 pts)
   - 12 logins in last 30 days ✅
   - 5 confirmations ✅
   - Tip: Respond to HR requests faster

━━━━━━━━━━━━━━━━━━━━━━

Need help improving?
Contact HR: hr@company.cz

━━━━━━━━━━━━━━━━━━━━━━
```

**3. Notifications**
```
🔔 RATING ALERT

Your rating decreased from 92.5 to 87.5

Reason:
⚠️ Medical Examination expired
⚠️ New penalty added (+500 CZK)

Action Required:
1. Upload new Medical Examination
2. Check penalty details in Finance tab

[View Rating] [Contact HR]
```

**4. Positive Badges**
```
🎉 ACHIEVEMENT UNLOCKED

🏆 Perfect Documents Badge
All 14 documents valid for 3 months!

Keep it up! 💪

[Share with HR] [View History]
```

### Explainability & Transparency

**For Drivers:**
- Clear breakdown of each metric
- Visual indicators (🟢🟡🔴)
- Actionable tips for improvement
- Historical trends (rating over time)

**For HR Managers:**
- Compare drivers side-by-side
- Identify training needs (e.g., many drivers with low timeliness)
- Export rating reports (Excel/PDF)
- Adjust weights based on company priorities

**UI Example:**

```
┌──────────────────────────────────────────────┐
│ Driver Rating - Jan Novák                    │
├──────────────────────────────────────────────┤
│                                              │
│ Current Rating: 87.5 / 100 🟢                │
│                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        │
│ 87.5%                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                              │
│ Metric Breakdown:                            │
│                                              │
│ 🟢 Documents (95%)          [28.5 / 30 pts] │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░       │
│                                              │
│ 🟡 Penalties Count (80%)    [16.0 / 20 pts] │
│    ━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░       │
│                                              │
│ 🟢 Penalty Amount (100%)    [15.0 / 15 pts] │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                              │
│ 🟢 Profile Complete (98%)   [9.8 / 10 pts]  │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░   │
│                                              │
│ 🟡 Upload Timely (80%)      [12.0 / 15 pts] │
│    ━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░       │
│                                              │
│ 🟡 Activity (82%)           [8.2 / 10 pts]  │
│    ━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░       │
│                                              │
│ [View History] [Compare with Others]         │
└──────────────────────────────────────────────┘
```

### API Endpoints (Planned)

```typescript
// Get current rating
GET /api/v0/drivers/{id}/rating

Response:
{
    total_score: 87.5,
    period: "2025-10",
    components: {
        document_expiration: { score: 28.5, weight: 30 },
        penalties_count: { score: 16.0, weight: 20 },
        // ...
    },
    rank_percentile: 85 // top 15%
}

// Get rating history (trends)
GET /api/v0/drivers/{id}/rating/history?months=6

Response:
{
    snapshots: [
        { period: "2025-10", score: 87.5 },
        { period: "2025-09", score: 92.1 },
        { period: "2025-08", score: 88.3 },
        // ...
    ]
}

// Configure rating weights (HR Manager+)
PUT /api/v0/companies/{id}/rating-config

Body:
{
    weights: {
        document_expiration: 30,
        penalties_count: 20,
        // ...
    }
}
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 7 (Module 1: Drivers) + WEEK_1_ACTION_PLAN.md
