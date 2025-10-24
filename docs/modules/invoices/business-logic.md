# Invoices Module: Business Logic

## Data Model

### Invoice (Core Entity)

**Basic Information:**
```
invoice_id: uuid (primary key)
invoice_number: string (format: INV-YYYYMMDD-XXX, unique)
order_id: uuid (FK → orders)
customer_id: uuid (FK → customers)
issue_date: date (invoice creation date)
due_date: date (= issue_date + customer.terms_of_payment)
```

**Financial Data:**
```
subtotal: decimal (order price before VAT)
vat_rate: decimal (e.g., 21.00 for 21%)
vat_amount: decimal (= subtotal * vat_rate / 100)
total_amount: decimal (= subtotal + vat_amount)
currency: string (EUR, CZK, USD, etc.)
exchange_rate: decimal (if currency != EUR, rate to EUR)
```

**Payment Tracking:**
```
payment_status: enum (unpaid, partly_paid, paid, overdue)
paid_amount: decimal (sum of all payments)
remaining_amount: decimal (= total_amount - paid_amount)
payment_method: string (bank_transfer, cash, card, etc.)
payment_date: date (when fully paid)
```

**Billing Details:**
```
billing_company_name: string
billing_address: text
billing_vat_number: string
billing_bank_account: string (IBAN)
billing_swift: string
```

**Metadata:**
```
notes: text (optional notes visible on invoice)
internal_notes: text (internal notes, not on PDF)
created_by: uuid (FK → users)
sent_at: timestamp (when email sent)
sent_to: string (recipient email)
pdf_path: string (path to generated PDF)
```

**Timestamps:**
```
created_at: timestamp
updated_at: timestamp
```

---

### Invoice Item (Line Items)

For future enhancement - currently invoices have single item (the order).

```
item_id: uuid
invoice_id: uuid (FK → invoices)
description: text
quantity: decimal
unit_price: decimal
vat_rate: decimal
amount: decimal (= quantity * unit_price)
vat_amount: decimal
total_amount: decimal (= amount + vat_amount)
```

---

### Payment (Payment Records)

Track individual payments against invoices:

```
payment_id: uuid
invoice_id: uuid (FK → invoices)
amount: decimal
payment_date: date
payment_method: string
reference_number: string (bank transaction reference)
notes: text
recorded_by: uuid (FK → users)
created_at: timestamp
```

---

## Business Rules

### Rule 1: Invoice Generation Trigger

**Trigger Conditions:**
```javascript
if (
  order.status === 'unloaded' &&
  order.documents.includes('cmr') &&
  order.documents.includes('pod')
) {
  // Automatically change order.status to 'ready_for_invoice'
  // Trigger invoice creation
  createInvoice(order);
}
```

**What Happens:**
1. Order status changes to "Ready for Invoice" (automatic)
2. Notification sent to accounting team
3. Accounting reviews order details
4. Accounting clicks "Generate Invoice"
5. System creates invoice record
6. System generates PDF
7. System sends email to customer
8. Order status changes to "Invoice Sent" (automatic)

---

### Rule 2: Invoice Number Generation

**Format:** `INV-YYYYMMDD-XXX`

**Logic:**
```javascript
function generateInvoiceNumber(date) {
  const dateStr = date.format('YYYYMMDD'); // e.g., "20251024"
  
  // Find highest number for this date
  const lastInvoice = Invoice
    .where('invoice_number', 'LIKE', `INV-${dateStr}-%`)
    .orderBy('invoice_number', 'DESC')
    .first();
  
  let sequence = 1;
  if (lastInvoice) {
    const lastSeq = parseInt(lastInvoice.invoice_number.split('-')[2]);
    sequence = lastSeq + 1;
  }
  
  // Zero-pad to 3 digits
  const seqStr = sequence.toString().padStart(3, '0');
  
  return `INV-${dateStr}-${seqStr}`;
}

// Examples:
// INV-20251024-001 (first invoice on 2025-10-24)
// INV-20251024-002 (second invoice same day)
// INV-20251025-001 (first invoice next day)
```

---

### Rule 3: VAT Calculation

**Czech Companies (CZ):**
```javascript
if (customer.country === 'CZ') {
  vat_rate = 21.00;
  vat_amount = subtotal * 0.21;
  total_amount = subtotal + vat_amount;
}
```

**EU Companies (B2B Reverse Charge):**
```javascript
if (
  customer.country IN ['SK', 'DE', 'PL', 'AT', ...] &&
  customer.vat_number !== null &&
  isValidEUVAT(customer.vat_number)
) {
  // Reverse charge - no VAT charged
  vat_rate = 0.00;
  vat_amount = 0.00;
  total_amount = subtotal;
  notes += "Reverse charge - VAT to be accounted for by recipient";
}
```

**Non-EU Companies:**
```javascript
if (customer.country NOT IN EU_COUNTRIES) {
  // No VAT
  vat_rate = 0.00;
  vat_amount = 0.00;
  total_amount = subtotal;
}
```

**Other EU Countries (B2C or invalid VAT):**
```javascript
// Apply customer's country VAT rate
const vatRates = {
  'SK': 20.00,
  'DE': 19.00,
  'PL': 23.00,
  'AT': 20.00,
  // ... other countries
};

vat_rate = vatRates[customer.country] || 0.00;
vat_amount = subtotal * (vat_rate / 100);
total_amount = subtotal + vat_amount;
```

---

### Rule 4: Due Date Calculation

```javascript
due_date = issue_date + customer.terms_of_payment;

// Example:
// Issue Date: 2025-10-24
// Terms: 30 days
// Due Date: 2025-11-23
```

**Overdue Check (Daily Cron):**
```javascript
// Run daily at 00:00
function checkOverdueInvoices() {
  const overdueInvoices = Invoice
    .where('payment_status', '!=', 'paid')
    .where('due_date', '<', today())
    .get();
  
  for (const invoice of overdueInvoices) {
    // Mark as overdue
    invoice.update({ payment_status: 'overdue' });
    
    // Send reminder (future feature)
    sendPaymentReminder(invoice);
    
    // Notify accounting
    notifyAccounting(invoice);
  }
}
```

---

### Rule 5: Payment Processing

**Full Payment:**
```javascript
function recordPayment(invoice, amount, date, method, reference) {
  // Create payment record
  Payment.create({
    invoice_id: invoice.id,
    amount: amount,
    payment_date: date,
    payment_method: method,
    reference_number: reference
  });
  
  // Update invoice
  invoice.paid_amount += amount;
  invoice.remaining_amount = invoice.total_amount - invoice.paid_amount;
  
  if (invoice.remaining_amount <= 0) {
    // Full payment
    invoice.payment_status = 'paid';
    invoice.payment_date = date;
    
    // Update order
    invoice.order.update({ status: 'payment_received' });
    
    // Restore customer credit limit
    recalculateCustomerCreditLimit(invoice.customer_id);
    
  } else {
    // Partial payment
    invoice.payment_status = 'partly_paid';
    invoice.order.update({ status: 'partly_paid' });
  }
  
  invoice.save();
}
```

**Credit Limit Restoration:**
```javascript
function recalculateCustomerCreditLimit(customerId) {
  const unpaidOrders = Order
    .where('customer_id', customerId)
    .whereNotIn('status', ['payment_received', 'closed'])
    .sum('order_price');
  
  const customer = Customer.find(customerId);
  customer.available_credit_limit = 
    customer.credit_limit - unpaidOrders;
  
  customer.save();
}
```

---

### Rule 6: Currency Handling

**Invoice in Customer's Currency:**
```javascript
function createInvoice(order) {
  const customer = order.customer;
  const invoice_currency = customer.currency; // e.g., "CZK"
  
  let subtotal = order.order_price;
  let exchange_rate = 1.0;
  
  // If customer currency is not EUR, convert
  if (invoice_currency !== 'EUR') {
    exchange_rate = getExchangeRate('EUR', invoice_currency);
    subtotal = order.order_price * exchange_rate;
  }
  
  return Invoice.create({
    order_id: order.id,
    customer_id: customer.id,
    subtotal: subtotal,
    currency: invoice_currency,
    exchange_rate: exchange_rate,
    // ... VAT calculation based on subtotal
  });
}
```

**Exchange Rate API (V2):**
```javascript
function getExchangeRate(from, to) {
  // Current: hard-coded rates (OLD version)
  const rates = {
    'EUR-CZK': 25.00,
    'EUR-USD': 1.10,
    // ...
  };
  
  // V2: Use live API
  const response = fetch(
    `https://api.exchangerate.host/latest?base=${from}&symbols=${to}`
  );
  return response.rates[to];
}
```

---

## PDF Generation (V2)

### Invoice PDF Structure

**Header:**
- Company logo
- Company name, address, VAT number
- Invoice number, issue date, due date

**Billing Details:**
- Bill To: Customer name, address, VAT number

**Invoice Items Table:**
| Description | Quantity | Unit Price | VAT Rate | Amount | VAT Amount | Total |
|-------------|----------|------------|----------|---------|------------|-------|
| Transport: [loading] → [unloading] | 1 | €X | 21% | €X | €X | €X |

**Totals:**
- Subtotal: €X
- VAT (21%): €X
- **Total: €X**

**Payment Details:**
- Bank: [bank_name]
- IBAN: [iban]
- SWIFT: [swift]
- Reference: [invoice_number]

**Footer:**
- Payment terms: [X] days
- Due date: [date]
- Late payment: [penalty terms]

**Notes:**
- Special instructions
- Reverse charge notice (if applicable)

---

### PDF Generation Code (V2)

```php
// Laravel + DomPDF
use Barryvdh\DomPDF\Facade\Pdf;

public function generateInvoicePDF(Invoice $invoice)
{
    $data = [
        'invoice' => $invoice,
        'customer' => $invoice->customer,
        'order' => $invoice->order,
        'company' => config('company'), // Our company details
    ];
    
    $pdf = Pdf::loadView('invoices.pdf', $data)
        ->setPaper('a4')
        ->setOption('margin-top', '10mm')
        ->setOption('margin-bottom', '10mm');
    
    $filename = "invoice-{$invoice->invoice_number}.pdf";
    $path = "invoices/{$filename}";
    
    Storage::put($path, $pdf->output());
    
    $invoice->update(['pdf_path' => $path]);
    
    return $path;
}
```

---

## Email Delivery (V2)

### Email Template

**Subject:** Invoice [INV-YYYYMMDD-XXX] from G-Track Transport

**Body:**
```
Dear [Customer Name],

Please find attached invoice [INV-YYYYMMDD-XXX] for the transport service we provided.

Order Reference: [ORDER-YYYYMMDD-XXX]
Route: [Loading City] → [Unloading City]
Delivery Date: [Date]

Invoice Total: [Total Amount] [Currency]
Due Date: [Due Date]

Payment Details:
Bank: [Bank Name]
IBAN: [IBAN]
SWIFT: [SWIFT]
Reference: [Invoice Number]

If you have any questions, please contact our accounting department.

Best regards,
G-Track Transport Team

---
This is an automated email. Please do not reply.
```

**Attachment:** invoice-INV-YYYYMMDD-XXX.pdf

---

## API Endpoints (V2 Planned)

### List Invoices
```
GET /api/v0/invoices
Query params:
  - customer_id (filter by customer)
  - status (unpaid, partly_paid, paid, overdue)
  - date_from, date_to (issue date range)
  - due_date_from, due_date_to (due date range)
  - currency (filter by currency)
  - limit, offset (pagination)
Response: { items: [...], total: number, totals_by_currency: {...} }
```

### Get Invoice Details
```
GET /api/v0/invoices/{id}
Response: { ...invoice data, order: {...}, customer: {...}, payments: [...] }
```

### Create Invoice
```
POST /api/v0/invoices
Body: { order_id, issue_date?, send_email: true }
Note: Most fields auto-filled from order
Response: { invoice: {...}, pdf_url: "..." }
```

### Generate PDF
```
POST /api/v0/invoices/{id}/generate-pdf
Response: { pdf_url: "...", pdf_path: "..." }
```

### Send Invoice Email
```
POST /api/v0/invoices/{id}/send
Body: { to?: "custom@email.com" } // Optional, defaults to customer.email
Response: { sent: true, sent_at: "...", sent_to: "..." }
```

### Record Payment
```
POST /api/v0/invoices/{id}/payments
Body: {
  amount: 1500.00,
  payment_date: "2025-10-24",
  payment_method: "bank_transfer",
  reference_number: "TXN123456",
  notes?: "Optional notes"
}
Response: { payment: {...}, invoice: {...updated status} }
```

### Cancel Invoice (Credit Note)
```
POST /api/v0/invoices/{id}/cancel
Body: { reason: "Customer cancellation", create_credit_note: true }
Response: { cancelled_invoice: {...}, credit_note: {...} }
```

---

## UI/UX Features (V2)

### Invoice List View

**Columns:**
- Invoice № (clickable → detail)
- Issue Date
- Due Date
- Customer Name
- Order № (link to order)
- Amount (with currency)
- Status (color-coded badge)
- Days Overdue (if overdue, red text)
- Actions (View PDF, Send Email, Record Payment)

**Filters:**
- Status dropdown (All, Unpaid, Partly Paid, Paid, Overdue)
- Date range picker (issue date, due date)
- Customer search
- Currency filter

**Actions:**
- Create Invoice (from order)
- Export to CSV
- Print selected invoices
- Bulk send emails

---

### Invoice Detail View

**Sections:**

1. **Invoice Information** (Top Card)
   - Invoice №, Issue Date, Due Date
   - Status badge with color
   - Days until due / days overdue

2. **Customer & Order** (Green Card)
   - Customer name, address, VAT
   - Order reference (link)
   - Route: Loading → Unloading

3. **Financial Details** (Blue Card)
   - Subtotal, VAT Rate, VAT Amount, Total
   - Currency and exchange rate (if applicable)
   - Payment Terms

4. **Payment Tracking** (Orange Card)
   - Paid Amount / Total Amount progress bar
   - Payment history table
   - "Record Payment" button

5. **Documents** (Gray Card)
   - PDF preview thumbnail
   - Download PDF button
   - View PDF in new tab

6. **Actions** (Button Row)
   - Send Email
   - Generate PDF (if not generated)
   - Record Payment
   - Print
   - Cancel Invoice (Admin only)

---

### Payment Recording Form

**Fields:**
- Amount (prefilled with remaining_amount)
- Payment Date (prefilled with today)
- Payment Method (dropdown: Bank Transfer, Cash, Card, Other)
- Reference Number (optional)
- Notes (optional)

**Validation:**
- Amount cannot exceed remaining_amount
- Payment date cannot be in future
- Reference number recommended for bank transfers

**On Submit:**
- Create payment record
- Update invoice status
- Update order status
- Restore customer credit limit
- Show success notification
- Refresh invoice view

---

## Reporting Features (Future)

### Financial Reports

1. **Revenue Report**
   - Total invoiced per month
   - Total paid per month
   - Outstanding balance
   - By customer, by currency

2. **Cash Flow Forecast**
   - Expected payments (based on due dates)
   - Overdue amounts
   - Projected revenue

3. **Customer Payment Analysis**
   - Average payment delay per customer
   - On-time payment rate
   - Overdue amount per customer

4. **VAT Report**
   - Total VAT collected
   - By period (monthly, quarterly)
   - Ready for tax filing

---

## Integration with Accounting Systems (Future)

### Pohoda (Czech Accounting Software)

**Export Format:** XML

```xml
<Invoice>
  <InvoiceHeader>
    <InvoiceNumber>INV-20251024-001</InvoiceNumber>
    <IssueDate>2025-10-24</IssueDate>
    <DueDate>2025-11-23</DueDate>
    <!-- ... -->
  </InvoiceHeader>
  <InvoicePartner>
    <CompanyName>Customer Name</CompanyName>
    <!-- ... -->
  </InvoicePartner>
  <InvoiceItem>
    <!-- ... -->
  </InvoiceItem>
</Invoice>
```

### Money S3 (Czech Accounting Software)

**Export Format:** CSV

```csv
invoice_number,issue_date,due_date,customer_name,vat_number,amount,vat,total
INV-20251024-001,2025-10-24,2025-11-23,"Customer Name",CZ12345678,1000.00,210.00,1210.00
```

---

## Migration Notes (OLD → V2)

### Data Migration Strategy

**Phase 1: Schema Creation**
```sql
-- Create new tables in PostgreSQL
CREATE TABLE invoices (...);
CREATE TABLE payments (...);
-- Add indexes, constraints
```

**Phase 2: Data Migration**
```sql
-- Migrate existing invoices from OLD version
INSERT INTO invoices (...)
SELECT ... FROM old_invoices;

-- Verify data integrity
SELECT COUNT(*) FROM invoices;
```

**Phase 3: Feature Parity**
- Implement all OLD version features in V2
- Add missing features (PDF, email)
- Test thoroughly

**Phase 4: Parallel Running**
- Run OLD and V2 side-by-side
- Cross-check invoice generation
- Validate calculations

**Phase 5: Cutover**
- Disable invoice creation in OLD version
- All new invoices in V2
- Monitor for issues

---

## Known Issues (OLD Version) - To Fix in V2

1. ❌ **Manual invoice numbering** - should be automatic
2. ❌ **No PDF generation** - must use external tool
3. ❌ **No email sending** - manual process
4. ❌ **Hard-coded exchange rates** - should use API
5. ❌ **Limited VAT rules** - only CZ 21%, need all EU countries
6. ❌ **No payment reminders** - manual follow-up
7. ❌ **No multi-currency totals** - reporting difficult
8. ❌ **Cannot split payments** - all-or-nothing
9. ❌ **No credit notes** - refunds difficult
10. ❌ **No recurring invoices** - for regular customers

All these will be addressed in V2 implementation.

---

## Testing Strategy (V2)

### Unit Tests
- Invoice number generation (uniqueness)
- VAT calculation (all scenarios)
- Due date calculation
- Payment processing logic
- Currency conversion

### Integration Tests
- Order → Invoice flow
- Invoice → Email delivery
- Payment → Credit limit restoration
- PDF generation

### E2E Tests
- Complete order-to-cash flow
- Multi-currency invoicing
- Overdue payment handling
- Credit note creation

### Performance Tests
- Generate 100 invoices in <10 seconds
- PDF generation <2 seconds per invoice
- Email sending <5 seconds per invoice

---

## Related Documentation

- **[Orders Module](../orders/index.md)** - Integration with orders
- **[Customers Module](../customers/index.md)** - Customer billing data
- **[Business Processes](../../architecture/business-processes.md)** - Order-to-cash flow
- **[System Overview](../../architecture/system-overview.md)** - System architecture

---

**Status:** 🔒 Coming Soon  
**Migration Priority:** After Customers + Orders  
**Target Date:** Q1 2026
