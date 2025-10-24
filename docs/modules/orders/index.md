# Module: Orders (Transport Orders)

## Overview
Orders module is the core of G-Track TMS - it manages the entire lifecycle of transportation orders from creation to invoice.

This module connects Customers (who order transport) with Carriers (who provide transport), tracks all order statuses, documents, and financials.

## Status
- **OLD Version**: ✅ 85% complete (functional but needs improvements)
- **V2 Migration**: 🔒 Coming Soon (after Drivers + Vehicles modules)

## Key Features
- Full order lifecycle management (9 statuses)
- Multiple loading/unloading points
- Document management (CMR, POD, etc.)
- Financial tracking (prices, margins, payments)
- Integration with Customers, Carriers, and Drivers
- Automatic status transitions
- Due date tracking with warnings

## Order Lifecycle

```
Draft → Open → In Progress → Loaded → Unloaded → 
Ready for Invoice → Invoice Sent → Payment Received/Closed
                                  ↓
                             Partly Paid
```

## Integration Points

**With Customers Module:**
- Select customer from Address Book
- Check available credit limit
- Apply payment terms

**With Drivers Module (Future):**
- Assign driver to order
- Check driver document validity
- Track driver status

**With Vehicles Module (Future):**
- Assign vehicle + trailer
- Verify technical readiness

**With Invoices Module:**
- Auto-create invoice when status = "Ready for Invoice"
- Track payment status

## User Roles
- **Admin**: Full CRUD access
- **Dispatcher**: Create, read, update orders; assign carriers/drivers
- **Verfolger** (Delivery Manager): Update delivery status, upload documents
- **Accounting**: Read access, update payment status
- **Carrier**: Read assigned orders (future feature)

## Next Steps
1. Complete Drivers module
2. Add Vehicles & Trailers module
3. Migrate Orders to v2 with enhanced features:
   - Real-time status tracking
   - Mobile app for drivers
   - GPS integration
   - Advanced route optimization

See [Business Logic](business-logic.md) for detailed specifications.
