# Orders Module: Business Logic

## Order Statuses (9 States)

### 1. Draft (Черновик)
**Purpose:** Initial order creation, filling basic information  
**Required fields:** Customer, loading address, unloading address  
**Allowed actions:** Edit all fields, Delete  
**Next status:** Open (manual)

### 2. Open (Открыт)
**Purpose:** Order ready for execution, all data filled  
**Required fields:** All basic info + cargo details  
**Allowed actions:** Assign carrier, Edit  
**Next status:** In Progress (when carrier assigned)

### 3. In Progress (В работе)
**Purpose:** Carrier assigned, preparing for loading  
**Required fields:** Carrier, vehicle number, trailer number  
**Allowed actions:** Upload documents, Update details  
**Next status:** Loaded (manual)

### 4. Loaded (Загружен)
**Purpose:** Cargo loaded at pickup point  
**Required fields:** Loading date/time confirmation  
**Allowed actions:** Upload CMR, Update status  
**Next status:** Unloaded (manual)

### 5. Unloaded (Разгружен)
**Purpose:** Cargo delivered at destination  
**Required fields:** Unloading date/time confirmation  
**Allowed actions:** Upload POD (Proof of Delivery)  
**Next status:** Ready for Invoice (automatic if CMR + POD uploaded)

### 6. Ready for Invoice (Готов к выставлению счёта)
**Purpose:** All documents received, ready to invoice customer  
**Trigger:** Automatic when status = Unloaded AND CMR uploaded AND POD uploaded  
**Allowed actions:** Create invoice  
**Next status:** Invoice Sent (automatic when invoice created)

### 7. Invoice Sent (Счёт отправлен)
**Purpose:** Invoice sent to customer  
**Trigger:** Automatic when invoice generated and sent  
**Allowed actions:** Track payment  
**Next status:** Payment Received or Partly Paid

### 8. Payment Received / Closed (Оплата получена)
**Purpose:** Full payment received, order closed  
**Trigger:** Manual when payment amount = order price  
**Allowed actions:** Archive, Export  
**Final status:** Yes

### 9. Partly Paid (Частичная оплата)
**Purpose:** Partial payment received  
**Trigger:** Manual when 0 < payment amount < order price  
**Allowed actions:** Track remaining balance  
**Next status:** Payment Received (when fully paid)

## Data Model

### Order Core Fields

**Order Information (Green Block - Customer Side):**
```
order_number: string (auto, format: YYYYMMDD-XXX)
customer_id: uuid (FK → customers)
client_reference: string (optional, customer's internal order #)
order_price: decimal (price for customer)
currency: string (EUR, CZK, etc.)
order_issued_by: string (employee name)
created_at: timestamp (auto)
status: enum (9 statuses above)
```

**Transport Information:**
```
loading_addresses: array [
  {
    type: 'loading',
    date: date,
    time: time,
    fixed_time: boolean (exact time required?),
    company_name: string,
    address: string,
    nation: string (country code),
    zip_code: string,
    city: string,
    reference: string (optional)
  }
]

unloading_addresses: array [
  {
    type: 'unloading',
    // ... same structure as loading
  }
]
```

**Cargo Information:**
```
cargo_type: string (free text)
trailer_type: enum (Standard, Mega, Frigo, VAN, Other)
adr: boolean (dangerous goods?)
pallets: boolean (EUR pallets?)
temperature_required: boolean (for Frigo)
temperature_value: int (degrees, if required)
weight: decimal (kg or tons)
```

**Carrier Information (Blue Block):**
```
carrier_id: uuid (FK → customers where type=carrier)
vehicle_number: string (truck license plate)
trailer_number: string (trailer license plate)
driver_id: uuid (FK → drivers) // Future integration
empty_km: int (empty kilometers)
total_km: int (total distance)
carrier_price: decimal (cost from carrier)
date_of_order_sale: date (when order sent to carrier)
```

**Financial Tracking:**
```
telax_invoice_status: enum (Sent, Not Sent)
telax_invoice_due_date: date (= creation_date + customer.terms_of_payment)
days_left_client: int (calculated: due_date - today)
  // Highlighting:
  // < 3 days → yellow background
  // < 0 days → red background + negative number

tva: decimal (21% for CZ companies)
carrier_invoice_status: enum (Received, Not Received)
carrier_invoice_number: string
carrier_invoice_due_date: date
carrier_payment_status: enum (Paid, Not Paid)

selling_price: decimal (final price)
revenue: decimal (= order_price - carrier_price) // Margin
recommended_selling_price: decimal
```

**Documents:**
```
documents: array [
  {
    type: enum (order_file, cmr, pallets, carrier_invoice, pod),
    file_path: string,
    uploaded_at: timestamp,
    uploaded_by: string
  }
]
```

## Business Rules

### Order Creation Validation

**Cannot create order if:**
- Customer's `available_credit_limit < 0`
- First loading date > Last unloading date
- Required fields missing (customer, addresses)

**Warnings shown if:**
- Customer's `available_credit_limit < order_price` (can still create, but warning)
- Loading/unloading dates in the past
- No carrier assigned and status changed to "In Progress"

### Automatic Status Transitions

**Ready for Invoice:**
- Triggered automatically when:
  - Current status = "Unloaded"
  - CMR document uploaded
  - POD (Proof of Delivery) uploaded

**Invoice Sent:**
- Triggered automatically when:
  - Invoice created in Invoices module
  - Invoice sent to customer email

### Financial Calculations

**Days Left Calculation:**
```javascript
days_left = telax_invoice_due_date - current_date

if (days_left < 3 && days_left >= 0) {
  background_color = 'yellow'
} else if (days_left < 0) {
  background_color = 'red'
  display_value = days_left // negative number
}
```

**Revenue Calculation:**
```javascript
revenue = order_price - carrier_price
```

**TVA (VAT) Calculation:**
```javascript
if (customer.country === 'CZ' || carrier.country === 'CZ') {
  tva = price * 0.21 // 21% for Czech companies
} else {
  // Apply country-specific VAT rules
}
```

### Credit Limit Impact

When order is created or price updated:
```javascript
customer.available_credit_limit = 
  customer.credit_limit - 
  SUM(order.order_price WHERE order.status NOT IN ['Payment received', 'Closed'])
```

## API Endpoints (OLD Version)

### List Orders
```
GET /api/orders
Query params:
  - search (order_number, customer_name)
  - status (filter by status)
  - customer_id
  - created_from, created_to (date range)
  - delivery_from, delivery_to (date range)
  - limit, offset
Response: { items: [...], total: number }
```

### Get Order Details
```
GET /api/orders/{id}
Response: { ...full order data with nested addresses, documents }
```

### Create Order
```
POST /api/orders
Body: {
  customer_id,
  order_price,
  currency,
  loading_addresses: [...],
  unloading_addresses: [...],
  cargo_type,
  trailer_type,
  ...
}
```

### Update Order
```
PATCH /api/orders/{id}
Body: { ...fields to update }
```

### Upload Document
```
POST /api/orders/{id}/documents
Multipart form:
  - type (order_file|cmr|pallets|carrier_invoice|pod)
  - file (PDF, PNG, JPEG)
Max size: 20MB
```

### Change Status
```
PATCH /api/orders/{id}/status
Body: { status: 'new_status' }
Note: Should validate status transition rules
```

## UI/UX Features

### Dashboard/Overviews

**Table Columns:**
- Order №
- Customer (name)
- Client Reference
- Carrier
- Loading Address (country + postcode of first loading)
- Unloading Address (country + postcode of first unloading)
- Start Date/Time (first loading)
- End Date/Time (last unloading)
- Total KM
- Order Value (Price)
- Price EUR (converted if different currency)
- Selling Price
- Days Left Client (with color coding)
- Due Date Client
- Due Date Carrier
- Status

**Filters:**
- By customer
- By date range
- By status
- By carrier

**Actions:**
- Click on Order № → open full order details
- Export to CSV
- Bulk status update (future)

### Order Form

**Layout:**
- Green block (top): Customer information
- White block (middle): Transport and cargo details
- Blue block (bottom): Carrier information
- Documents section (right): Upload/download files
- Financial section: Calculations and payment tracking

**Validation:**
- Real-time credit limit check
- Date logic validation (loading before unloading)
- Required fields highlighting
- VAT ID check (via EU VIES)

## Known Issues (from OLD version)

### Dashboard:
1. ⚠️ Table doesn't fit on screen (too many columns)
2. ⚠️ No fixed header when scrolling
3. ⚠️ Some orders from Orders list don't appear in Dashboard
4. ⚠️ Some orders appear in Dashboard but not in Orders list

### Order Form:
1. ⚠️ Field naming inconsistency: "Order №" vs "Order ID"
2. ⚠️ Can manually select any status (should follow status rules)
3. ⚠️ Price field validation incorrect (allows negative)
4. ⚠️ Loading/Unloading addresses sometimes don't save
5. ⚠️ Incorrect credit limit calculation
6. ⚠️ Can create order with negative available limit (should block)
7. ⚠️ VAT ID check doesn't work
8. ⚠️ Can attach only one document per type (should allow multiple versions)
9. ⚠️ Dates in the past allowed for future events
10. ⚠️ No undo functionality

### Currency:
1. ⚠️ Currency conversion works incorrectly
2. ⚠️ No automatic exchange rate updates

## Migration Notes for V2

**High Priority Fixes:**
1. Implement proper status state machine (prevent invalid transitions)
2. Fix all validation issues
3. Add real-time credit limit updates
4. Implement version control for documents
5. Add undo/redo functionality
6. Fix currency conversion with real-time rates
7. Responsive design for Dashboard table

**New Features for V2:**
1. Integration with Drivers module (assign driver, check validity)
2. Integration with Vehicles module (assign truck + trailer)
3. GPS tracking integration
4. Mobile app for drivers (update status, upload photos)
5. Real-time notifications (email, SMS, in-app)
6. Advanced route optimization
7. Automatic carrier matching based on availability
8. Weather and traffic warnings
9. Carbon footprint calculation

**Performance Improvements:**
1. Optimize Dashboard query (currently slow with 100+ orders)
2. Add caching for frequently accessed data
3. Implement lazy loading for documents
4. Add full-text search for orders

**Database Changes:**
- Add proper indexes
- Normalize addresses table
- Add audit_log table
- Implement soft deletes
- Add version control for order changes
