# Customers Module

**Status:** 🟡 90% Complete in OLD version (needs migration to v2)
**Action:** Mark "Coming Soon" until Drivers finished

## Business Logic

**Types:**

1. **Customer** - Companies ordering transport
2. **Carrier** - External transport companies (subcontractors)
3. **Both** - Company can be both customer AND carrier

## Credit Limit Management

```typescript
Available Credit = Credit Limit - ∑(Open Orders)

Open Orders = Orders where status NOT IN ('payment_received', 'closed', 'cancelled')

Example:
Credit Limit: 10,000 EUR
Open Order #1: 3,000 EUR (in_transit)
Open Order #2: 2,500 EUR (delivered)
Open Order #3: 1,500 EUR (confirmed)
─────────────────────────────────
Used: 7,000 EUR
Available: 3,000 EUR

Validation:
- Can create new order for 2,800 EUR → ✅ OK
- Cannot create order for 3,500 EUR → ❌ Exceeds limit
```

**Alert Logic:**
```
IF Available Credit < 1,000 EUR:
    Show warning: "Low credit limit for this customer"

IF Available Credit < 0:
    Block new order creation
    Show error: "Customer credit limit exceeded"
```

## EU VAT Validation

**VAT ID Format:**

```
CZ12345678 (Czech Republic)
PL8992982297 (Poland)
DE123456789 (Germany)
ATU12345678 (Austria)
```

**Validation Service:**
```php
// Validate VAT ID via EU VIES system
public function validateVatId(string $vatId): bool
{
    // Call EU VIES web service
    $client = new SoapClient("http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl");

    $countryCode = substr($vatId, 0, 2);
    $vatNumber = substr($vatId, 2);

    $result = $client->checkVat([
        'countryCode' => $countryCode,
        'vatNumber' => $vatNumber
    ]);

    return $result->valid;
}
```

## Customer Profile Structure

**Key Fields:**

- **Identification:** Internal Number (CUST-0001), Company Name, Type
- **VAT:** VAT Number, Validation Status
- **Contact:** Email, Accounting Email, Phone
- **Address:** Country, City, Street, Postcode
- **Financial:** Currency, Payment Terms (days), Credit Limit
- **Rating:** Excellent, Good, Neutral, Poor
- **Logistics:** Pallet Balance (EUR pallets)

**Bank Accounts:**

Multiple bank accounts per customer:
- Bank Name
- SWIFT
- IBAN
- Default flag

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 9 (Module 3: Customers)
