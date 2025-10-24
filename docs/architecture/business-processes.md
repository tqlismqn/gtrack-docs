# G-Track Business Processes

**Last Updated:** 2025-10-24  
**Related:** [System Overview](system-overview.md), [Data Flow](data-flow.md)

---

## Introduction

This document describes the key business processes in G-Track TMS and how they map to system workflows. Each process shows the step-by-step flow from business trigger to system outcome.

---

## Process 1: Transport Order Lifecycle

### Business Flow

```
Customer needs transport → Order created → Transport assigned →
Goods loaded → Goods delivered → Invoice sent → Payment received
```

### Detailed Process

#### Stage 1: Order Creation

**Actors:** Dispatcher, Customer (external)

**Trigger:** Customer contacts company with transport request

**Steps:**
1. Dispatcher receives transport request (email, phone, web form)
2. Dispatcher logs into G-Track
3. Dispatcher navigates to Orders → Create New Order
4. Dispatcher selects Customer from address book
   - System checks customer's credit limit
   - ⚠️ Warning if `available_credit_limit < order_price`
   - ❌ Block if `available_credit_limit < 0`
5. Dispatcher enters order details:
   - Order price and currency
   - Loading addresses (date, time, location)
   - Unloading addresses (date, time, location)
   - Cargo type and details
   - Special requirements (ADR, temperature, etc.)
6. Dispatcher saves order with status = **"Draft"**

**System Actions:**
- Create order record with unique order_number (YYYYMMDD-XXX format)
- Link order to customer
- Initialize order status = "Draft"
- Calculate `telax_invoice_due_date` = creation_date + customer.terms_of_payment
- Log action in audit trail

**Outcome:** Order exists in system, status = "Draft"

---

#### Stage 2: Order Validation & Opening

**Actors:** Dispatcher

**Trigger:** Order details are complete and verified

**Steps:**
1. Dispatcher reviews draft order for completeness
2. Dispatcher changes status to **"Open"**
3. System validates:
   - All required fields filled
   - Loading date < Unloading date
   - Customer credit limit OK
4. Order becomes visible to all dispatchers

**System Actions:**
- Validate order data
- Change status to "Open"
- Send notification to dispatch team
- Update order in dashboard

**Outcome:** Order is ready for carrier assignment

---

#### Stage 3: Carrier Assignment

**Actors:** Dispatcher

**Trigger:** Order is open and ready for execution

**Steps:**
1. Dispatcher searches for available carrier
2. Dispatcher contacts carrier (phone, email) for pricing
3. Dispatcher enters carrier details in order:
   - Carrier company (from address book)
   - Carrier price
   - Expected vehicle number
   - Expected trailer number
4. Dispatcher changes status to **"In Progress"**

**System Actions:**
- Link order to carrier
- Record carrier price
- Calculate `revenue = order_price - carrier_price`
- Change status to "In Progress"
- Send order confirmation to carrier (future: automated email)

**Outcome:** Order assigned to carrier, status = "In Progress"

---

#### Stage 4: Transport Execution - Loading

**Actors:** Driver (external), Verfolger (Delivery Manager)

**Trigger:** Driver arrives at loading point

**Steps:**
1. Driver loads cargo at pickup location
2. Driver receives CMR document (signed by sender)
3. Verfolger or Dispatcher updates order:
   - Changes status to **"Loaded"**
   - Uploads CMR document
   - Confirms actual loading date/time
4. System timestamps loading completion

**System Actions:**
- Change status to "Loaded"
- Store CMR document with version control
- Record loading timestamp
- Send notification to customer (future feature)
- Update order timeline

**Outcome:** Cargo is loaded, status = "Loaded", CMR uploaded

---

#### Stage 5: Transport Execution - Delivery

**Actors:** Driver (external), Verfolger (Delivery Manager)

**Trigger:** Driver arrives at delivery location

**Steps:**
1. Driver unloads cargo at destination
2. Driver receives POD (Proof of Delivery) signed by recipient
3. Verfolger or Dispatcher updates order:
   - Changes status to **"Unloaded"**
   - Uploads POD document
   - Confirms actual delivery date/time

**System Actions:**
- Change status to "Unloaded"
- Store POD document with version control
- Record delivery timestamp
- Check if CMR + POD both uploaded
- **If both documents present:**
  - **Automatically** change status to "Ready for Invoice"
  - Notify accounting department
- Update customer's order history

**Outcome:** Cargo delivered, status = "Ready for Invoice" (automatic)

---

#### Stage 6: Invoicing

**Actors:** Accounting

**Trigger:** Order status = "Ready for Invoice" (automatic after CMR + POD uploaded)

**Steps:**
1. Accounting receives notification
2. Accounting reviews order details
3. Accounting creates invoice:
   - Invoice references order
   - Invoice includes VAT calculation (21% for CZ)
   - PDF invoice generated
4. Accounting sends invoice to customer (email)
5. System automatically changes order status to **"Invoice Sent"**

**System Actions:**
- Generate invoice record
- Link invoice to order
- Calculate VAT (TVA)
- Generate PDF
- **Automatically** change order status to "Invoice Sent"
- Send email with PDF attachment
- Track invoice due date
- Update dashboard

**Outcome:** Invoice sent to customer, status = "Invoice Sent"

---

#### Stage 7: Payment Tracking

**Actors:** Accounting

**Trigger:** Payment received from customer

**Steps:**
1. Accounting receives payment confirmation (bank statement)
2. Accounting marks invoice as paid
3. Accounting updates order status:
   - **If full payment:** status = **"Payment Received / Closed"**
   - **If partial payment:** status = **"Partly Paid"**

**System Actions:**
- Record payment amount and date
- Update invoice payment status
- Change order status accordingly
- **Recalculate customer's available credit limit:**
  - `available_credit_limit = credit_limit - sum(unpaid orders)`
- Archive completed order
- Update financial reports

**Outcome:** Order closed, payment received, credit limit restored

---

### Process Diagram

```
Draft
  │
  │ [Dispatcher completes all fields]
  │
  ▼
Open
  │
  │ [Dispatcher assigns carrier]
  │
  ▼
In Progress
  │
  │ [Driver loads cargo]
  │
  ▼
Loaded
  │
  │ [Driver delivers cargo]
  │
  ▼
Unloaded
  │
  │ [AUTOMATIC: CMR + POD uploaded]
  │
  ▼
Ready for Invoice
  │
  │ [AUTOMATIC: Accounting creates invoice]
  │
  ▼
Invoice Sent
  │
  │ [Accounting receives payment]
  │
  ├─────────────┬─────────────┐
  │             │             │
  ▼             ▼             ▼
Full          Partial      No Payment
Payment       Payment      (Overdue)
  │             │             │
  ▼             ▼             │
Payment    Partly Paid        │
Received       │              │
/ Closed       │              │
               ▼              ▼
           [More payments] [Follow-up]
               │
               ▼
           Payment
           Received
           / Closed
```

---

## Process 2: Driver Readiness Management

### Business Flow

```
New driver hired → Documents collected → Expiry tracking →
Notification before expiry → Document renewal → Always ready
```

### Detailed Process

#### Stage 1: Driver Onboarding

**Actors:** HR Manager

**Trigger:** New driver hired

**Steps:**
1. HR receives driver's personal information and documents
2. HR logs into G-Track
3. HR navigates to Drivers → Add New Driver
4. HR enters driver profile:
   - Personal data (name, birth date, citizenship)
   - Contact info (email, phone, address)
   - Contract details (hire date, work location)
   - Bank account (for salary payments)
5. HR saves driver profile
   - System assigns unique `internal_number` (auto-increment, never changes)

**System Actions:**
- Create driver record with UUID
- Assign internal_number (e.g., Driver #42)
- Set status = "active"
- Initialize empty documents array
- Create audit log entry
- Send welcome email (future feature)

**Outcome:** Driver profile created with internal number

---

#### Stage 2: Document Upload

**Actors:** HR Manager

**Trigger:** HR has driver's documents (physical or digital)

**Steps:**
1. HR clicks on driver profile
2. HR navigates to Documents tab
3. For each of 14 document types, HR:
   - Selects document type (Passport, Visa, Drivers License, etc.)
   - Enters document details (number, dates, country)
   - Uploads file (PDF, PNG, JPEG)
4. System validates and stores documents

**System Actions:**
- Create `driver_document` record for each document
- Store file in versioned `document_files` table
- Calculate expiry status:
  - 🟢 Green: valid (>60 days until expiry)
  - 🟠 Orange: warning (31-60 days)
  - 🟡 Yellow: expiring soon (≤30 days)
  - 🔴 Red: expired
  - ⚪ Gray: no data
- Update driver's readiness indicator
- Schedule expiry notification job

**Outcome:** All driver documents uploaded and tracked

---

#### Stage 3: Automatic Monitoring

**Actors:** System (automated)

**Trigger:** Daily cron job at 00:00 UTC

**Steps:**
1. System checks all driver documents for expiry dates
2. For each document, calculate days until expiry
3. Update color indicators based on thresholds
4. Identify documents needing notifications:
   - 60 days before expiry (first warning)
   - 30 days before expiry (urgent warning)
   - On expiry date (critical alert)
   - 7 days after expiry (follow-up)

**System Actions:**
- Recalculate all document statuses
- Update dashboard indicators
- Queue notification jobs
- Update driver readiness status:
  - **Ready:** All docs 🟢 or 🟡 (green or yellow), NO 🔴 (red)
  - **Not Ready:** Any doc 🔴 (red/expired)
- Log status changes in audit trail

**Outcome:** All drivers have current status, notifications queued

---

#### Stage 4: Proactive Notifications

**Actors:** System (automated), HR Manager (recipient)

**Trigger:** Document approaching expiry or expired

**Steps:**
1. System sends email notification to HR Manager:
   - Subject: "Driver Document Expiring Soon: [Driver Name] - [Document Type]"
   - Body: Document details, expiry date, days remaining
   - Link to driver profile in G-Track
2. HR Manager reviews notification
3. HR Manager contacts driver to renew document

**System Actions:**
- Send email notification
- Mark notification as sent in database
- Track notification history
- Show notification badge in UI
- Update dashboard "Expiring Documents" widget

**Outcome:** HR is aware of expiring documents proactively

---

#### Stage 5: Document Renewal

**Actors:** HR Manager, Driver (external)

**Trigger:** Document renewed by driver

**Steps:**
1. Driver provides renewed document to HR
2. HR logs into G-Track
3. HR navigates to driver profile → Documents
4. HR finds the expired/expiring document
5. HR uploads new version:
   - New file upload (PDF, PNG, JPEG)
   - Update document number (if changed)
   - Update expiry date
6. System stores new version

**System Actions:**
- Create new row in `document_files` with `version = N+1`
- Set `is_current = true` for new version
- Set `is_current = false` for old version
- Recalculate document status (likely 🟢 green now)
- Update driver readiness indicator
- Cancel pending notifications for this document
- Log document update in audit trail
- Send confirmation email to driver (future feature)

**Outcome:** Document renewed, driver ready again, old version preserved

---

### Process Diagram

```
New Driver Hired
       │
       ▼
Create Driver Profile
       │
       ▼
Upload Documents (14 types)
       │
       ▼
System Calculates Expiry Status
       │
       ├─────────────┬──────────────┬──────────────┐
       │             │              │              │
       ▼             ▼              ▼              ▼
    🟢 Green     🟠 Orange      🟡 Yellow       🔴 Red
    (>60d)       (31-60d)       (≤30d)       (Expired)
       │             │              │              │
       │             │              ▼              │
       │             │      Notify HR (30d)       │
       │             │              │              │
       │             ▼              │              │
       │      Notify HR (60d)       │              │
       │             │              │              │
       │             └──────────────┴──────────────┘
       │                            │
       │                            ▼
       │                    HR Renews Document
       │                            │
       │                            ▼
       │                    Upload New Version
       │                            │
       └────────────────────────────┘
                                    │
                                    ▼
                           Driver Ready Again
                                    │
                                    ▼
                           Continue Monitoring
                              (Daily Check)
```

---

## Process 3: Credit Limit Management

### Business Flow

```
Set credit limit → Orders consume limit → Monitor usage →
Warn if low → Block if exceeded → Payment restores limit
```

### Detailed Process

#### Stage 1: Customer Onboarding

**Actors:** Admin, Sales

**Trigger:** New customer signs contract

**Steps:**
1. Admin creates customer in system
2. Admin sets credit limit (e.g., €50,000)
3. Admin sets payment terms (e.g., 30 days)

**System Actions:**
- Create customer record
- Initialize `credit_limit = €50,000`
- Initialize `available_credit_limit = €50,000`
- Set `terms_of_payment = 30` days

**Outcome:** Customer has credit limit

---

#### Stage 2: Order Creation (Credit Check)

**Actors:** Dispatcher

**Trigger:** Creating new order

**Steps:**
1. Dispatcher selects customer
2. Dispatcher enters order price (e.g., €5,000)
3. System checks credit:
   - **If `available_credit_limit >= order_price`:** ✅ Allow creation (may show warning if close)
   - **If `available_credit_limit < order_price` but >= 0:** ⚠️ Show warning but allow
   - **If `available_credit_limit < 0`:** ❌ Block creation, show error message

**System Actions:**
- Calculate available credit:
  ```
  available_credit_limit = credit_limit - SUM(order_price WHERE status NOT IN ['Payment Received', 'Closed'])
  ```
- Validate order creation
- **If allowed:**
  - Create order
  - **Do NOT change `available_credit_limit` yet** (recalculated on-the-fly)
- **If blocked:**
  - Show error: "Customer credit limit exceeded. Available: €X, Required: €Y"

**Outcome:** Order created (or blocked), credit monitored

---

#### Stage 3: Real-time Credit Monitoring

**Actors:** System (automated)

**Trigger:** Any order status change or customer view

**Steps:**
1. User views customer profile or order list
2. System calculates available credit in real-time:
   ```sql
   available_credit_limit = credit_limit - (
     SELECT SUM(order_price) 
     FROM orders 
     WHERE customer_id = X 
     AND status NOT IN ('Payment Received', 'Closed')
   )
   ```
3. Display credit status with color coding:
   - 🟢 Green: >20% of limit available
   - 🟡 Yellow: 5-20% of limit available
   - 🔴 Red: <5% of limit available

**System Actions:**
- Real-time calculation (not stored value)
- Update UI with credit indicator
- Send alert to accounting if <10% (future feature)

**Outcome:** Credit usage is always current

---

#### Stage 4: Payment Received (Credit Restoration)

**Actors:** Accounting

**Trigger:** Customer pays invoice

**Steps:**
1. Accounting marks order as "Payment Received"
2. Order status changes to "Closed"

**System Actions:**
- Change order status to "Closed"
- **Automatically recalculate available credit:**
  - This order's price NO LONGER counts in the SUM
  - Available credit increases by order_price
- Update customer's credit indicator
- Remove order from "unpaid orders" list

**Outcome:** Credit limit restored, customer can place more orders

---

### Process Diagram

```
Customer Created
(Credit Limit = €50,000)
       │
       ▼
Available = €50,000
       │
       ▼
Order #1 Created (€5,000)
       │
       ▼
Available = €45,000
       │
       ▼
Order #2 Created (€10,000)
       │
       ▼
Available = €35,000
       │
       ├───────────┬───────────┐
       │           │           │
       ▼           ▼           ▼
  More Orders   Payment     Credit
   Created    Received #1   Monitoring
       │           │           │
       │           ▼           │
       │    Available += €5k   │
       │    (now €40,000)      │
       │           │           │
       └───────────┴───────────┘
                   │
                   ▼
           Continue Cycle
```

---

## Process 4: Transport Unit Formation

### Business Flow

```
Assign driver + Assign vehicle + Assign trailer →
Check all ready (🟢 green) → Form Transport Unit →
Assign to order → Track execution
```

### Detailed Process

#### Stage 1: Resource Readiness

**Actors:** HR (for drivers), Maintenance (for vehicles/trailers)

**Preconditions:**
- Driver: All 14 documents 🟢 or 🟡 (green/yellow), NO 🔴 (red)
- Vehicle: Technical inspection 🟢, insurance 🟢
- Trailer: Technical inspection 🟢

**System Actions:**
- Continuously monitor document expiry
- Update readiness indicators
- Make ready resources visible in "Available" lists

---

#### Stage 2: Transport Unit Assembly

**Actors:** Dispatcher

**Trigger:** Order needs transport assignment

**Steps:**
1. Dispatcher opens order (status = "Open")
2. Dispatcher navigates to "Assign Transport Unit"
3. System shows lists of ready resources:
   - **Ready Drivers** (🟢 all docs valid)
   - **Ready Vehicles** (🟢 inspections valid)
   - **Ready Trailers** (🟢 inspections valid)
4. Dispatcher selects:
   - Driver (e.g., Driver #42 - Jan Novák)
   - Vehicle (e.g., Truck 1AB 2345)
   - Trailer (e.g., Trailer 2BC 3456)
5. System validates compatibility (future: automatic matching)
6. Dispatcher confirms assignment

**System Actions:**
- Create `transport_unit` record
- Link: transport_unit → driver, vehicle, trailer
- Link: order → transport_unit
- Verify all components are 🟢 ready
- Update order status to "In Progress"
- Mark resources as "assigned" (unavailable for other orders)
- Send notification to driver (future: mobile app push)

**Outcome:** Transport Unit formed and assigned to order

---

#### Stage 3: Execution & Tracking

**Actors:** Driver, Dispatcher, Verfolger

**Steps:**
1. Driver receives assignment (future: via mobile app)
2. Driver uses assigned vehicle and trailer for transport
3. System tracks:
   - Order status (Loaded → Unloaded)
   - GPS location (future feature)
   - Document uploads (CMR, POD)
4. After delivery, Transport Unit is released

**System Actions:**
- Track order progress
- Update Transport Unit availability
- When order completed:
  - Mark transport_unit as "available" again
  - Driver, vehicle, trailer can be assigned to new orders
- Log Transport Unit performance (km driven, fuel consumption - future)

**Outcome:** Transport executed, resources available again

---

### Process Diagram

```
        ┌───────────────┐
        │ Ready Driver  │ (All docs 🟢)
        └───────┬───────┘
                │
                │ Combine
                │
        ┌───────▼────────┐
        │                │
        │  Transport     │
        │    Unit        │
        │                │
        └───────┬────────┘
                │
                │ Assign to
                │
        ┌───────▼────────┐
        │                │
        │    Order       │
        │  (In Progress) │
        │                │
        └───────┬────────┘
                │
                │ Execute
                │
        ┌───────▼────────┐
        │   Delivery     │
        │   Complete     │
        └───────┬────────┘
                │
                │ Release
                │
        ┌───────▼────────┐
        │   Resources    │
        │   Available    │
        │   Again        │
        └────────────────┘

    Simultaneously:
    ┌───────────────┐
    │ Ready Vehicle │ (Inspection 🟢)
    └───────┬───────┘
            │
    ┌───────▼───────┐
    │ Ready Trailer │ (Inspection 🟢)
    └───────────────┘
```

---

## Key Business Rules Summary

### Order Status Rules
1. **Draft → Open:** All required fields must be filled
2. **Open → In Progress:** Carrier must be assigned
3. **In Progress → Loaded:** Loading confirmed by verfolger
4. **Loaded → Unloaded:** Delivery confirmed by verfolger
5. **Unloaded → Ready for Invoice:** 🤖 **AUTOMATIC** when CMR + POD uploaded
6. **Ready for Invoice → Invoice Sent:** 🤖 **AUTOMATIC** when invoice created
7. **Invoice Sent → Payment Received:** Manual, when payment confirmed

### Credit Limit Rules
1. **Cannot create order** if `available_credit_limit < 0`
2. **Warning shown** if `available_credit_limit < order_price` (but can create)
3. **Available credit** = `credit_limit - SUM(unpaid orders)`
4. **Unpaid orders** = orders WHERE status NOT IN ['Payment Received', 'Closed']

### Driver Readiness Rules
1. **Driver is ready** if:
   - All documents 🟢 (green) OR 🟡 (yellow)
   - NO documents 🔴 (red/expired)
2. **Document is 🟢** if: >60 days until expiry
3. **Document is 🟠** if: 31-60 days until expiry
4. **Document is 🟡** if: ≤30 days until expiry
5. **Document is 🔴** if: expired (past expiry date)

### Transport Unit Rules
1. **Can form Transport Unit** only if:
   - Driver is ready (🟢)
   - Vehicle is ready (🟢)
   - Trailer is ready (🟢)
2. **Transport Unit is operational** = all 3 components 🟢
3. **Once assigned to order:** Components unavailable for other orders

---

## Related Documentation

- **[System Overview](system-overview.md)** - Technical architecture
- **[Data Flow](data-flow.md)** - How data moves through system
- **[Modules](../modules/drivers/index.md)** - Detailed module documentation
- **[API Reference](../api/index.md)** - API endpoints for each process

---

**Status:** ✅ Current  
**Next Review:** After core modules migration complete
