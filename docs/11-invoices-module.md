# Invoices Module

**Status:** 🔴 20% Complete in OLD version (needs major development)
**Action:** Mark "Coming Soon" until Drivers finished

## Invoice Creation Flow

```
1. Order reaches "Ready for Invoice" status
   ↓
2. Accountant clicks "Create Invoice"
   ↓
3. System pre-fills:
   - Customer info
   - Order details
   - VAT mode (auto-detected)
   - Amount (from order_price)
   ↓
4. Accountant reviews/adjusts
   ↓
5. Save as Draft → Review → Send
   ↓
6. PDF generated + sent via email
   ↓
7. Order status → "Invoice Sent"
```

## EU VAT Modes

**Automatic Detection:**

```php
function determineVatMode(Customer $customer, Company $company): string
{
    $customerEU = in_array($customer->country_code, EU_COUNTRIES);
    $companyEU = in_array($company->country_code, EU_COUNTRIES);

    // Both in EU, different countries → Reverse Charge
    if ($customerEU && $companyEU
        && $customer->country_code !== $company->country_code
        && $customer->vat_number) {
        return 'reverse_charge'; // 0% VAT
    }

    // Same country → Domestic
    if ($customer->country_code === $company->country_code) {
        return 'domestic'; // full VAT
    }

    // Customer without VAT number
    if (!$customer->vat_number) {
        return 'non_vat'; // 0% VAT (special case)
    }

    return 'domestic'; // default
}
```

**VAT Rates by Country:**

```php
const VAT_RATES = [
    'CZ' => 21.00,
    'PL' => 23.00,
    'DE' => 19.00,
    'AT' => 20.00,
    'NL' => 21.00,
    'IT' => 22.00,
];
```

## Invoice PDF Example (Reverse Charge)

```
╔═══════════════════════════════════════════════════════╗
║                  FAKTURA / INVOICE                    ║
║                                                       ║
║   Číslo / Number: INV-2025-0123                       ║
║   Datum vystavení / Issue Date: 27.10.2025            ║
║   Datum splatnosti / Due Date: 26.11.2025 (30 days)   ║
╚═══════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────┐
│ DODAVATEL / SUPPLIER                                  │
├───────────────────────────────────────────────────────┤
│ Trans Logistics s.r.o.                                │
│ Vinohradská 123, 130 00 Praha 3                       │
│ Česká republika / Czech Republic                      │
│                                                       │
│ IČ / VAT ID: CZ12345678                               │
│ Email: accounting@translogistics.cz                   │
│ Tel: +420 123 456 789                                 │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│ ODBĚRATEL / CUSTOMER                                  │
├───────────────────────────────────────────────────────┤
│ GoldenScreen s.r.o.                                   │
│ Ul. Przykładowa 45, 00-001 Warszawa                   │
│ Polska / Poland                                       │
│                                                       │
│ NIP / VAT ID: PL8992982297                            │
│ Email: ap@goldenscreen.pl                             │
└───────────────────────────────────────────────────────┘

┌────────────────────────────────────────────┬──────────┐
│ POPIS / DESCRIPTION                        │ ČÁSTKA   │
├────────────────────────────────────────────┼──────────┤
│ Dopravní služby / Transport Services      │          │
│                                            │          │
│ Trasa / Route:                             │          │
│ Praha (CZ) → Warszawa (PL)                 │          │
│                                            │          │
│ Č. objednávky / Order: ORD-2025-0123       │          │
│ Datum přepravy / Date: 15.10.2025          │          │
│ Náklad / Cargo: 20 palet / pallets         │          │
│                                            │          │
│ Cena bez DPH / Price excl. VAT:            │ 1,000.00 │
│ DPH 0% (Reverse Charge)                    │     0.00 │
├────────────────────────────────────────────┼──────────┤
│ CELKEM K ÚHRADĚ / TOTAL DUE                │ 1,000.00 │
└────────────────────────────────────────────┴──────────┘

Currency: EUR

Platební údaje / Payment Details:
IBAN: CZ65 0800 0000 1920 0014 5399
SWIFT: GIBACZPX
Bank: Česká spořitelna

Poznámka / Note:
Režim přenesení daňové povinnosti dle čl. 196 směrnice
o DPH 2006/112/ES
VAT reverse charge applies per Art. 196 of the VAT
Directive 2006/112/EC

───────────────────────────────────────────────────────
Vystavil / Issued by: Petr Novák
accounting@translogistics.cz
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 11 (Module 5: Invoices)
