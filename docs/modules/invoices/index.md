# Module: Invoices

## Overview
Invoices module manages billing and payment tracking for completed transport orders. It automatically generates invoices from orders, handles multi-currency billing, tracks payments, and integrates with accounting workflows.

This module is the final step in the order-to-cash cycle: Order → Delivery → Invoice → Payment.

## Status
- **OLD Version**: ~20% complete (basic functionality exists)
- **V2 Migration**: 🔒 Coming Soon (planned Q1 2026, after Customers + Orders migration)

## Key Features

### Automatic Invoice Generation
- Auto-create invoice when order status = "Ready for Invoice"
- Pre-fill invoice data from order details
- Apply customer's payment terms automatically

### Multi-Currency Support
- Invoice in customer's preferred currency (EUR, CZK, USD, etc.)
- Automatic currency conversion with current rates
- Support for multiple exchange rates per invoice period

### VAT/TVA Handling
- Automatic VAT calculation based on customer country
- 21% VAT for Czech companies
- Different VAT rates for other EU/non-EU countries
- Reverse charge mechanism for B2B EU transactions

### PDF Generation
- Professional invoice PDF with company branding
- Automatic numbering (format: INV-YYYYMMDD-XXX)
- Multi-language support (Czech, English, German - future)
- Email delivery with PDF attachment

### Payment Tracking
- Track payment status (Unpaid, Partly Paid, Paid)
- Record payment date and method
- Link payments to specific invoices
- Automatic order status update on payment

### Integration Points
- **With Orders Module:**
  - Automatically triggered when order = "Ready for Invoice"
  - Updates order status to "Invoice Sent"
  - Links invoice to order for reference
  
- **With Customers Module:**
  - Retrieves customer billing details
  - Applies payment terms
  - Updates credit limit on payment

- **With Accounting Systems (Future):**
  - Export to Pohoda, Money S3
  - Bank statement reconciliation
  - Financial reporting

## Business Rules

### Invoice Creation Rules
1. **Trigger:** Order status = "Ready for Invoice" (automatic after CMR + POD uploaded)
2. **Pre-conditions:**
   - Order must have customer assigned
   - Order must have order_price filled
   - Loading and unloading completed
3. **Automatic actions:**
   - Generate invoice number (INV-YYYYMMDD-XXX)
   - Copy order details to invoice
   - Calculate VAT based on customer country
   - Set due date = invoice_date + customer.terms_of_payment
   - Change order status to "Invoice Sent"

### Payment Rules
1. **Full Payment:**
   - Invoice status = "Paid"
   - Order status = "Payment Received / Closed"
   - Restore customer's available credit limit
   
2. **Partial Payment:**
   - Invoice status = "Partly Paid"
   - Order status = "Partly Paid"
   - Track remaining balance
   
3. **Overdue Payment:**
   - Due date passed, no payment received
   - Mark invoice as "Overdue"
   - Send reminder to customer (automatic - future)
   - Escalate to management (future)

## User Roles

| Role | Create | Edit | View | Delete | Send | Track Payment |
|------|--------|------|------|--------|------|---------------|
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Accounting | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Dispatcher | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| HR | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Driver | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Current Limitations (OLD Version)

⚠️ **Known Issues to Fix in V2:**
1. Manual invoice number assignment (should be automatic)
2. No PDF generation (currently manual in external tool)
3. No email delivery (manual send)
4. Currency conversion rates hard-coded (should be API-based)
5. Limited VAT rules (only Czech 21%)
6. No payment reminders
7. No multi-currency reporting
8. Cannot split payment across multiple bank accounts
9. No credit note support (for refunds)
10. No recurring invoices

## Next Steps for V2

### Phase 1: Core Functionality (Q1 2026)
- ✅ Automatic invoice generation from orders
- ✅ Professional PDF generation (Laravel + DomPDF)
- ✅ Email delivery with SMTP
- ✅ Payment tracking
- ✅ VAT calculation for all EU countries
- ✅ Multi-currency support with live rates

### Phase 2: Advanced Features (Q2 2026)
- 📧 Automatic payment reminders
- 💳 Payment gateway integration (Stripe, PayPal)
- 🔄 Credit notes for refunds
- 📊 Financial reporting dashboard
- 🌍 Multi-language PDFs (CZ, EN, DE)
- 🔗 Accounting system exports (Pohoda, Money S3)

### Phase 3: Automation (Q3 2026)
- 🤖 AI-powered payment prediction
- 📲 SMS payment reminders
- 🔔 Real-time payment notifications
- 📈 Cash flow forecasting
- 🔍 Automatic anomaly detection (unusual payments)

## Related Documentation

- **[Orders Module](../orders/index.md)** - How invoices are triggered
- **[Customers Module](../customers/index.md)** - Customer billing details
- **[Business Processes](../../architecture/business-processes.md)** - Order-to-cash flow
- **[Data Flow](../../architecture/data-flow.md)** - System data flow

---

**Status:** 🔒 Coming Soon  
**Priority:** After Customers + Orders migration  
**Target:** Q1 2026
