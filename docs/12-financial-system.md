# Financial System

## Driver Finance Tracking

**Salary Calculation:**

```typescript
interface DriverSalary {
    base_salary: number; // Fixed monthly
    business_trips_allowance: number; // Per-diem × days
    bonuses: number; // Performance bonuses
    fines: number; // Negative (speeding, etc.)
    damages: number; // Negative (cargo damage, accidents)

    gross_salary: number; // base + trips + bonuses - fines - damages
    tax_deductions: number; // Income tax + social insurance
    net_salary: number; // gross - tax
}
```

**Example:**

```
Driver: Jan Novák (#DRV-0001)
Month: October 2025

Base Salary:         50,000 CZK
Business Trips:      +8,500 CZK (17 days × 500 CZK)
Bonuses:             +2,000 CZK (urgent delivery bonus)
Fines:               -1,500 CZK (2× speeding)
Damages:             -5,000 CZK (cargo damage, accident)
─────────────────────────────────────────
Gross Salary:        54,000 CZK

Tax (15%):           -8,100 CZK
Social Insurance:    -3,500 CZK
─────────────────────────────────────────
NET SALARY:          42,400 CZK
```

## Order Profitability Tracking

**Real-time Calculation:**

```typescript
// When order is closed
function calculateOrderProfitability(order: Order): Profitability {
    const revenue = order.order_price;

    const expenses = {
        driver_salary: calculateDriverCost(order),
        fuel: estimateFuelCost(order.total_km),
        carrier: order.carrier_price || 0,
        fines: getFinesForOrder(order.id),
        damages: getDamagesForOrder(order.id),
        tolls: getHollsForOrder(order.id),
        other: getOtherExpenses(order.id),
    };

    const totalExpenses = Object.values(expenses).reduce((a, b) => a + b, 0);
    const netProfit = revenue - totalExpenses;
    const profitMargin = (netProfit / revenue) * 100;

    return {
        revenue,
        expenses,
        totalExpenses,
        netProfit,
        profitMargin
    };
}
```

## Financial Dashboard

**View 1: By Driver**

```
┌──────────────────────────────────────────────┐
│ Driver Performance (October 2025)            │
├──────────────────────────────────────────────┤
│                                              │
│ Top Performers:                              │
│ 1. Jan Novák (#DRV-0001)                     │
│    Orders completed: 12                      │
│    Revenue generated: 15,000 EUR             │
│    Net profit: 5,500 EUR (37%)               │
│    Fines/Damages: -500 EUR                   │
│                                              │
│ 2. Petr Svoboda (#DRV-0002)                  │
│    Orders completed: 10                      │
│    Revenue generated: 12,000 EUR             │
│    Net profit: 4,200 EUR (35%)               │
│    Fines/Damages: 0 EUR                      │
│                                              │
│ Bottom Performers:                           │
│ 25. Pavel Horák (#DRV-0025)                  │
│    Orders completed: 3                       │
│    Revenue generated: 3,500 EUR              │
│    Net profit: -500 EUR (LOSS)               │
│    Fines/Damages: -2,000 EUR (accident)      │
└──────────────────────────────────────────────┘
```

**View 2: By Vehicle**

```
┌──────────────────────────────────────────────┐
│ Vehicle Expenses (October 2025)              │
├──────────────────────────────────────────────┤
│                                              │
│ Most Expensive:                              │
│ 1. VEH-0045 (MAN TGX 18.440)                 │
│    Service: 2 times, 5,000 EUR               │
│    Repairs: 1 accident, 48,000 CZK           │
│    Fines: 3 times, 1,500 CZK                 │
│    TOTAL: 54,500 CZK                         │
│                                              │
│ 2. VEH-0012 (Mercedes Actros)                │
│    Service: 1 time, 3,500 CZK                │
│    Repairs: None                             │
│    Fines: 1 time, 500 CZK                    │
│    TOTAL: 4,000 CZK                          │
└──────────────────────────────────────────────┘
```

**View 3: Overall (Company)**

```
┌──────────────────────────────────────────────┐
│ Company Financial Overview (October 2025)    │
├──────────────────────────────────────────────┤
│                                              │
│ INCOME                                       │
│ ├─ Orders revenue:      +150,000 EUR         │
│ └─ Other income:        +2,000 EUR           │
│                                              │
│ EXPENSES                                     │
│ ├─ Driver salaries:     -45,000 EUR          │
│ ├─ Business trips:      -12,000 EUR          │
│ ├─ Vehicle expenses:    -25,000 EUR          │
│ ├─ Fuel:                -20,000 EUR          │
│ ├─ Fines (returned):    +3,500 EUR           │
│ ├─ Office rent:         -5,000 EUR           │
│ └─ Software (G-Track):  -88 EUR              │
│                                              │
│ ═══════════════════════════════════════      │
│ NET PROFIT:             +48,412 EUR          │
│ PROFIT MARGIN:          31.8%                │
└──────────────────────────────────────────────┘
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 12
