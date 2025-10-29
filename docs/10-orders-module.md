# Orders Module

**Status:** 🟡 85% Complete in OLD version (needs migration + fixes)
**Action:** Mark "Coming Soon" until Drivers finished

## Order Status Flow (9 Statuses)

```
1. Draft
   ↓ (HR/Dispatcher confirms order)
2. Open
   ↓ (Transport Unit assigned)
3. In Progress
   ↓ (Cargo loaded, CMR signed)
4. Loaded
   ↓ (Cargo delivered, POD signed)
5. Unloaded
   ↓ (CMR + POD uploaded → automatic)
6. Ready for Invoice
   ↓ (Accountant creates invoice → automatic)
7. Invoice Sent
   ↓ (Payment received in full)
8. Payment Received / Closed

OR (Payment received partially)

9. Partly Paid
   ↓ (Remaining payment received)
8. Payment Received / Closed
```

**Automatic Transitions:**

```php
// Order reaches "Unloaded" + CMR + POD uploaded
if ($order->status === 'unloaded'
    && $order->hasCMR()
    && $order->hasPOD()) {
    $order->status = 'ready_for_invoice';
    $order->save();
}

// Invoice created and sent
if ($invoice->status === 'sent') {
    $order = $invoice->order;
    $order->status = 'invoice_sent';
    $order->save();
}

// Payment received
if ($payment->amount >= $invoice->total_amount) {
    $invoice->status = 'paid';
    $order->status = 'payment_received';
} else {
    $order->status = 'partly_paid';
}
```

## Order Structure

**Key Fields:**

```typescript
interface Order {
    // Identification
    id: string;
    order_number: string; // YYYYMMDD-XXX (e.g., 20251027-001)

    // Customer
    customer_id: string;
    client_reference: string; // Customer's internal order number
    order_price: number;
    currency: string;
    order_issued_by: string; // user who created order

    // Route
    loading_addresses: LoadingPoint[];
    unloading_addresses: UnloadingPoint[];

    // Cargo
    cargo_description: string;
    trailer_type: 'standard' | 'mega' | 'frigo' | 'van';
    adr: boolean; // dangerous goods
    pallets: boolean;
    temperature_required: boolean;
    temperature_value?: number; // if frigo
    weight_kg: number;

    // Transport
    transport_unit_id: string; // Driver + Vehicle + Trailer
    driver_id: string;
    vehicle_id: string;
    trailer_id: string;

    // Distances
    empty_km: number; // from office to loading point
    total_km: number; // total trip distance

    // Carrier (if external)
    carrier_id?: string;
    carrier_price?: number; // cost from carrier

    // Financial
    vat_mode: 'domestic' | 'reverse_charge' | 'non_vat';
    vat_rate: number;
    vat_amount: number;
    total_amount: number;
    revenue: number; // order_price - carrier_price

    // Dates
    pickup_scheduled: Date;
    pickup_actual?: Date;
    delivery_scheduled: Date;
    delivery_actual?: Date;

    // Documents
    order_file_id?: string; // PDF from customer
    cmr_file_id?: string;
    pod_file_id?: string;
    carrier_invoice_file_id?: string;

    // Status
    status: OrderStatus;
}
```

## Order Profitability

**Calculation:**

```typescript
interface OrderProfitability {
    // Income
    revenue_from_customer: number; // order_price

    // Expenses
    expenses: {
        driver_salary: number; // calculated from driver rate
        fuel_cost: number; // estimated or actual
        carrier_cost: number; // if external carrier used
        fines: number; // driver fines during this order
        damages: number; // cargo damage, accidents
        tolls: number; // highway tolls
        other: number;
    };

    total_expenses: number; // sum of all expenses

    // Result
    net_profit: number; // revenue - total_expenses
    profit_margin: number; // (net_profit / revenue) * 100
}
```

**Example:**

```
Order: ORD-2025-0123
Route: Praha → Berlin → Praha

Income:
├─ Customer pays: 1,200 EUR

Expenses:
├─ Driver salary (2 days): 200 EUR
├─ Fuel (1,500 km): 450 EUR
├─ Tolls (D1, D8): 80 EUR
├─ Fine (speeding): 50 EUR
├─ Total expenses: 780 EUR

Net Profit: 1,200 - 780 = 420 EUR
Profit Margin: (420 / 1,200) * 100 = 35%
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 10 (Module 4: Orders)
