# System Architecture

## Multi-Tenancy Model

**Architecture:** Single Database with Tenant Isolation

```
Database: gtrack_production
├── companies (tenants)
│   ├── id (uuid)
│   ├── name
│   ├── country_code
│   └── currency
├── offices (sub-tenants)
│   ├── id (uuid)
│   ├── company_id (FK)
│   ├── name
│   └── country_code
└── All other tables with:
    ├── company_id (FK) ← MANDATORY
    └── office_id (FK) ← OPTIONAL
```

**Key Principles:**
1. **Every query** includes `WHERE company_id = ?`
2. **Global Middleware** automatically scopes queries
3. **Cross-Office Visibility** controlled via settings
4. **Data Isolation** enforced at database + application level

**Example: Cross-Office Driver Search**

```php
// Setting: Allow cross-office driver search
$company->settings->allow_cross_office_driver_search = true;

// HR Manager in Prague office searches drivers
Driver::where('company_id', auth()->user()->company_id)
    ->when(!$company->settings->allow_cross_office_driver_search, function ($q) {
        $q->where('office_id', auth()->user()->office_id);
    })
    ->search($request->query)
    ->get();
```

## Module-Based Architecture

**Core Concept:** Each module is a separate subscription tier

| Tier | Price/Month | Features |
|------|-------------|----------|
| **FREE** (Trial) | €0 | 5 drivers, 3 vehicles, basic dashboard |
| **STARTER** | €29 | Unlimited drivers/vehicles, document management |
| **PROFESSIONAL** | €48 | + Order management, customer management |
| **BUSINESS** | €63 | + Invoicing with EU VAT compliance |
| **ENTERPRISE** | €88 | + GPS tracking integration |

**Module Activation:**

```php
// Check if company has access to Orders module
Route::middleware(['auth', 'module:orders'])->group(function () {
    Route::get('/orders', [OrderController::class, 'index']);
});

// Frontend: Hide "Orders" menu if module not enabled
*ngIf="hasModule('orders')"
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 4
