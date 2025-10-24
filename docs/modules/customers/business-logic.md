# Customers Module: Business Logic

## Data Model

### Company (Customer/Carrier)

**Core Fields:**
- `id` - auto-generated unique ID
- `company_name` - company legal name
- `vat_number` - VAT/Tax ID
- `type` - enum: `customer` | `carrier` | `both`

**Address:**
- `country` - country code (ISO 3166-1)
- `postcode` - postal/ZIP code
- `city` - city name
- `street` - street address

**Contacts:**
- `email` - primary email
- `email_accounting` - accounting department email
- `phone` - primary phone number

**Financial:**
- `terms_of_payment` - payment terms in days (e.g., 30, 60, 90)
- `credit_limit` - maximum credit limit (amount)
- `available_credit_limit` - calculated field: `credit_limit - sum(unpaid orders)`
- `currency` - default currency (EUR, CZK, etc.)

**Additional:**
- `rating` - quality rating (color-coded: green/yellow/no rating)
- `pallet_balance` - pallet exchange balance
- `created_at`, `updated_at` - timestamps

### Bank Account (Multiple per Company)

- `bank_name` - bank name
- `swift` - SWIFT/BIC code
- `iban` - IBAN or account number
- `is_default` - boolean (one default per company)

## Business Rules

### Credit Limit Calculation

```
Available Credit Limit = Credit Limit - ∑(Order Prices where status != "Payment received")
```

**Validation:**
- Cannot create new order if `Available Credit Limit < 0`
- Warning shown when `Available Credit Limit < Order Price`

### Rating System

**Color Indicators:**
- 🟢 Green circle - good rating
- 🟡 Yellow circle - medium rating  
- ⚪ No circle - no rating
- ⚫ Black - (currently not displayed - bug in OLD version)

### VAT Handling

- VAT Number validation via EU VIES system
- TVA 21% applied for Czech companies (CZ)
- Different VAT rates for other countries

## API Endpoints (OLD Version)

### List Customers
```
GET /api/customers
Query params: 
  - search (string) - search by ID, Name, VAT Number
  - type (customer|carrier|both)
  - limit, offset
Response: { items: [...], total: number }
```

### Get Customer Details
```
GET /api/customers/{id}
Response: { ...customer data, bank_accounts: [...] }
```

### Create Customer
```
POST /api/customers
Body: { company_name, vat_number, email, ... }
```

### Update Customer
```
PATCH /api/customers/{id}
Body: { ...fields to update }
```

### Delete Customer
```
DELETE /api/customers/{id}
Note: Soft delete (changes status to inactive)
```

## UI/UX Features

### Table View (List)
**Columns:**
- ID
- Company Name
- VAT Number
- Credit Limit
- Available Limit
- Rating (colored indicator)

**Actions:**
- Search by: ID, Name, VAT Number
- Sort by: ID, Name, VAT Number, Limit, Available Limit, Rating
- Export to CSV
- Create new customer
- Edit existing
- Delete (with confirmation)

### Detail View (Card)

**Sections:**
1. **Personal Data** (green block)
   - Company name, VAT, address, contacts
   
2. **Financial Information**
   - Payment terms, credit limits, currency
   - Rating indicator
   - Pallet balance

3. **Bank Accounts**
   - List of all bank accounts
   - Add/edit/delete accounts
   - Mark default account

4. **History**
   - Audit log of all changes
   - Document history

## Known Issues (from OLD version)

1. ⚠️ Incorrect spelling: "RaIting" instead of "Rating"
2. ⚠️ Black color rating not displayed
3. ⚠️ Validation allows creating customer without required fields
4. ⚠️ Can create customer with negative credit limit
5. ⚠️ Spaces at start/end of fields not trimmed

These issues will be fixed in V2 migration.

## Migration Notes

**Priority for V2:**
1. Fix all validation issues
2. Implement proper VAT ID check (EU VIES API)
3. Add real-time credit limit updates
4. Improve rating system UX
5. Add activity timeline

**Database Migration:**
- Port from OLD Laravel version to Laravel 11
- Keep data compatibility
- Add audit_log table
- Improve indexes for search performance
