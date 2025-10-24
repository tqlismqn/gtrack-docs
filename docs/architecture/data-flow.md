# G-Track Data Flow

**Last Updated:** 2025-10-24  
**Related:** [System Overview](system-overview.md), [Business Processes](business-processes.md)

---

## Introduction

This document describes how data flows through G-Track system: from user input through business logic processing to database storage and back to the user interface.

---

## Data Flow Pattern (General)

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ 1. User Action (click, input)
       │
       ▼
┌─────────────────────────┐
│   Angular Component     │
│   - User interaction    │
│   - Form validation     │
└──────┬──────────────────┘
       │ 2. Call Service Method
       │
       ▼
┌─────────────────────────┐
│   Angular Service       │
│   - HTTP Request        │
│   - JWT Token attached  │
└──────┬──────────────────┘
       │ 3. HTTPS Request
       │ Authorization: Bearer <JWT>
       │
       ▼
┌─────────────────────────┐
│   Laravel Middleware    │
│   - Verify JWT          │
│   - Check permissions   │
└──────┬──────────────────┘
       │ 4. If authorized
       │
       ▼
┌─────────────────────────┐
│   Laravel Controller    │
│   - Validate request    │
│   - Call service        │
└──────┬──────────────────┘
       │ 5. Business logic
       │
       ▼
┌─────────────────────────┐
│   Laravel Service       │
│   - Process data        │
│   - Apply rules         │
└──────┬──────────────────┘
       │ 6. Data access
       │
       ▼
┌─────────────────────────┐
│   Laravel Repository    │
│   - Eloquent queries    │
└──────┬──────────────────┘
       │ 7. SQL Query
       │
       ▼
┌─────────────────────────┐
│   PostgreSQL Database   │
│   - Store/retrieve data │
└──────┬──────────────────┘
       │ 8. Return data
       │
       ▼
┌─────────────────────────┐
│   Laravel Controller    │
│   - Format response     │
│   - Add metadata        │
└──────┬──────────────────┘
       │ 9. JSON Response
       │
       ▼
┌─────────────────────────┐
│   Angular Service       │
│   - Parse response      │
│   - Update state        │
└──────┬──────────────────┘
       │ 10. Emit data
       │
       ▼
┌─────────────────────────┐
│   Angular Component     │
│   - Render UI           │
│   - Show to user        │
└──────┬──────────────────┘
       │
       ▼
┌─────────────┐
│    User     │
│ (sees result)
└─────────────┘
```

---

## Data Flow Example 1: Create New Driver

### Step-by-Step Flow

**1. User Input (Frontend)**
```typescript
// Component: drivers/create/create-driver.component.ts
onSubmit() {
  if (this.driverForm.valid) {
    const driverData = this.driverForm.value;
    this.driverService.createDriver(driverData)
      .subscribe({
        next: (response) => {
          this.router.navigate(['/drivers', response.data.id]);
          this.notification.success('Driver created successfully');
        },
        error: (error) => {
          this.notification.error(error.message);
        }
      });
  }
}
```

**2. Service Call (Frontend)**
```typescript
// Service: drivers/driver.service.ts
createDriver(data: CreateDriverRequest): Observable<DriverResponse> {
  return this.http.post<DriverResponse>('/api/v0/drivers', data)
    .pipe(
      catchError(this.handleError),
      tap(response => this.cache.invalidate('drivers'))
    );
}
```

**3. HTTP Request**
```http
POST /api/v0/drivers HTTP/1.1
Host: api.g-track.eu
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "first_name": "Jan",
  "last_name": "Novák",
  "birth_date": "1985-03-15",
  "citizenship": "CZ",
  "email": "jan.novak@example.com",
  "phone": "+420 123 456 789",
  "hire_date": "2025-01-01"
}
```

**4. Middleware (Backend)**
```php
// Middleware: Auth0Middleware
public function handle($request, Closure $next)
{
    // Verify JWT signature with Auth0 public key
    $token = $request->bearerToken();
    $payload = $this->verifyToken($token);
    
    // Extract user info
    $request->attributes->set('auth_user_id', $payload['sub']);
    $request->attributes->set('auth_roles', $payload['roles']);
    
    return $next($request);
}
```

**5. Controller (Backend)**
```php
// Controller: DriverController
public function store(CreateDriverRequest $request)
{
    // Request already validated by FormRequest
    
    // Call service
    $driver = $this->driverService->createDriver(
        $request->validated()
    );
    
    // Return response
    return response()->json([
        'data' => new DriverResource($driver),
        'message' => 'Driver created successfully'
    ], 201);
}
```

**6. Service (Backend)**
```php
// Service: DriverService
public function createDriver(array $data): Driver
{
    DB::beginTransaction();
    
    try {
        // Create driver record
        $driver = $this->driverRepository->create([
            'id' => Uuid::uuid4(),
            'first_name' => $data['first_name'],
            'last_name' => $data['last_name'],
            'birth_date' => $data['birth_date'],
            'citizenship' => $data['citizenship'],
            'email' => $data['email'],
            'phone' => $data['phone'],
            'hire_date' => $data['hire_date'],
            'status' => 'active'
            // internal_number is auto-generated by database
        ]);
        
        // Fire event
        event(new DriverCreated($driver));
        
        DB::commit();
        return $driver;
        
    } catch (\Exception $e) {
        DB::rollBack();
        throw $e;
    }
}
```

**7. Repository (Backend)**
```php
// Repository: DriverRepository
public function create(array $data): Driver
{
    return Driver::create($data);
}
```

**8. Database (PostgreSQL)**
```sql
INSERT INTO drivers (
    id, 
    first_name, 
    last_name, 
    birth_date, 
    citizenship, 
    email, 
    phone, 
    hire_date, 
    status,
    created_at,
    updated_at
) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Jan',
    'Novák',
    '1985-03-15',
    'CZ',
    'jan.novak@example.com',
    '+420 123 456 789',
    '2025-01-01',
    'active',
    NOW(),
    NOW()
) RETURNING *;

-- Also triggers auto-increment for internal_number
```

**9. Response (Backend)**
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "internal_number": 42,
    "first_name": "Jan",
    "last_name": "Novák",
    "full_name": "Jan Novák",
    "birth_date": "1985-03-15",
    "citizenship": "CZ",
    "email": "jan.novak@example.com",
    "phone": "+420 123 456 789",
    "hire_date": "2025-01-01",
    "status": "active",
    "readiness": {
      "is_ready": false,
      "missing_documents": [
        "passport", "visa", "drivers_licence", "chip"
      ]
    },
    "created_at": "2025-10-24T10:30:00Z",
    "updated_at": "2025-10-24T10:30:00Z"
  },
  "message": "Driver created successfully"
}
```

**10. Component Update (Frontend)**
```typescript
// Angular component receives response
next: (response) => {
  // Navigate to driver detail page
  this.router.navigate(['/drivers', response.data.id]);
  
  // Show success notification
  this.notification.success('Driver created successfully');
  
  // Update state
  this.store.addDriver(response.data);
}
```

---

## Data Flow Example 2: Document Expiry Check (Automated)

### Daily Cron Job Flow

**1. Scheduled Task (Backend)**
```php
// Console/Kernel.php
$schedule->command('drivers:check-document-expiry')
    ->dailyAt('00:00');
```

**2. Artisan Command**
```php
// Console/Commands/CheckDocumentExpiry.php
public function handle()
{
    $this->info('Checking driver document expiry...');
    
    $expiringDocuments = $this->documentService
        ->findExpiringDocuments();
    
    foreach ($expiringDocuments as $document) {
        $this->documentService
            ->sendExpiryNotification($document);
    }
    
    $this->info("Sent {$expiringDocuments->count()} notifications");
}
```

**3. Service Query (Backend)**
```php
// Service: DocumentService
public function findExpiringDocuments(): Collection
{
    // Find documents expiring in 60, 30, or 0 days
    return DriverDocument::query()
        ->whereNotNull('to')
        ->where(function($query) {
            $query->whereDate('to', '=', now()->addDays(60))
                  ->orWhereDate('to', '=', now()->addDays(30))
                  ->orWhereDate('to', '=', now())
                  ->orWhereDate('to', '<', now());
        })
        ->with(['driver', 'driver.supervisor'])
        ->get();
}
```

**4. Database Query**
```sql
SELECT 
    driver_documents.*,
    drivers.first_name,
    drivers.last_name,
    drivers.email,
    users.email as supervisor_email
FROM driver_documents
INNER JOIN drivers ON drivers.id = driver_documents.driver_id
LEFT JOIN users ON users.id = drivers.supervisor_id
WHERE driver_documents.to IS NOT NULL
AND (
    DATE(driver_documents.to) = CURRENT_DATE + INTERVAL '60 days'
    OR DATE(driver_documents.to) = CURRENT_DATE + INTERVAL '30 days'
    OR DATE(driver_documents.to) = CURRENT_DATE
    OR DATE(driver_documents.to) < CURRENT_DATE
)
ORDER BY driver_documents.to ASC;
```

**5. Notification Job (Backend)**
```php
// Jobs/SendDocumentExpiryNotification.php
public function handle()
{
    $daysLeft = $this->document->to->diffInDays(now(), false);
    
    // Determine urgency
    $urgency = match(true) {
        $daysLeft < 0 => 'overdue',
        $daysLeft <= 7 => 'critical',
        $daysLeft <= 30 => 'urgent',
        default => 'warning'
    };
    
    // Send email to HR
    Mail::to($this->document->driver->supervisor)
        ->send(new DocumentExpiryMail(
            $this->document,
            $urgency
        ));
    
    // Create in-app notification
    Notification::create([
        'user_id' => $this->document->driver->supervisor_id,
        'type' => 'document_expiry',
        'data' => [
            'driver_id' => $this->document->driver_id,
            'document_type' => $this->document->type,
            'expiry_date' => $this->document->to,
            'urgency' => $urgency
        ]
    ]);
}
```

**6. Email Sent (External Service)**
```
From: noreply@g-track.eu
To: hr.manager@company.com
Subject: ⚠️ Driver Document Expiring Soon

Driver: Jan Novák (Internal #42)
Document: Drivers Licence (Class C)
Expiry Date: 2025-11-24
Days Left: 30 days

Action Required:
Please remind the driver to renew this document.

View Driver Profile:
https://app.g-track.eu/drivers/550e8400-e29b-41d4-a716-446655440000

---
G-Track TMS - Automated Notification
```

**7. User Receives Notification (Frontend)**

When HR Manager logs in:
```typescript
// Service: notification.service.ts
fetchUnreadNotifications(): Observable<Notification[]> {
  return this.http.get<Notification[]>('/api/v0/notifications/unread');
}
```

```typescript
// Component: notification-bell.component.ts
ngOnInit() {
  this.notificationService.fetchUnreadNotifications()
    .subscribe(notifications => {
      this.unreadCount = notifications.length;
      this.notifications = notifications;
    });
}
```

UI displays badge with count: 🔔 (3)

---

## Data Flow Example 3: Order Status Transition (Automatic)

### Trigger: CMR + POD Documents Uploaded

**1. Document Upload (Frontend)**
```typescript
// Component: order-detail.component.ts
onDocumentUpload(file: File, type: 'cmr' | 'pod') {
  this.orderService.uploadDocument(this.orderId, file, type)
    .subscribe({
      next: (response) => {
        this.notification.success(`${type.toUpperCase()} uploaded`);
        this.refreshOrder();
      }
    });
}
```

**2. API Call (Backend)**
```php
// Controller: OrderDocumentController
public function upload(UploadDocumentRequest $request, string $orderId)
{
    $order = $this->orderRepository->findOrFail($orderId);
    
    // Store document
    $document = $this->documentService->uploadOrderDocument(
        $order,
        $request->file('file'),
        $request->input('type')
    );
    
    // Check if automatic status transition should happen
    $this->orderService->checkAutoTransitions($order);
    
    return response()->json([
        'data' => new DocumentResource($document),
        'order' => new OrderResource($order->fresh())
    ]);
}
```

**3. Service Logic (Backend)**
```php
// Service: OrderService
public function checkAutoTransitions(Order $order): void
{
    // Rule: Unloaded + CMR + POD → Ready for Invoice
    if ($order->status === 'unloaded') {
        $hasCmr = $order->documents()
            ->where('type', 'cmr')
            ->exists();
            
        $hasPod = $order->documents()
            ->where('type', 'pod')
            ->exists();
        
        if ($hasCmr && $hasPod) {
            $this->transitionToReadyForInvoice($order);
        }
    }
}

private function transitionToReadyForInvoice(Order $order): void
{
    DB::beginTransaction();
    
    try {
        // Change status
        $order->update(['status' => 'ready_for_invoice']);
        
        // Log status change
        $order->statusHistory()->create([
            'from_status' => 'unloaded',
            'to_status' => 'ready_for_invoice',
            'reason' => 'Automatic: CMR and POD uploaded',
            'changed_by' => 'system'
        ]);
        
        // Fire event
        event(new OrderReadyForInvoice($order));
        
        DB::commit();
        
    } catch (\Exception $e) {
        DB::rollBack();
        throw $e;
    }
}
```

**4. Event Listener (Backend)**
```php
// Listeners/NotifyAccountingOfInvoiceReady.php
public function handle(OrderReadyForInvoice $event)
{
    $accountingUsers = User::role('accounting')->get();
    
    foreach ($accountingUsers as $user) {
        Mail::to($user)->send(
            new OrderReadyForInvoiceMail($event->order)
        );
        
        Notification::create([
            'user_id' => $user->id,
            'type' => 'order_ready_for_invoice',
            'data' => [
                'order_id' => $event->order->id,
                'order_number' => $event->order->order_number,
                'customer_name' => $event->order->customer->company_name
            ]
        ]);
    }
}
```

**5. Real-time Update (Frontend via WebSocket - Future)**
```typescript
// Service: websocket.service.ts (Future implementation)
this.socket.on('order:status-changed', (data) => {
  if (data.order_id === this.currentOrderId) {
    this.store.updateOrder(data.order);
    this.notification.info(`Order status changed to: ${data.new_status}`);
  }
});
```

**Current Implementation: Polling**
```typescript
// Component periodically refreshes
refreshOrder() {
  this.orderService.getOrder(this.orderId)
    .subscribe(order => {
      if (order.status !== this.order.status) {
        this.notification.info(
          `Order status changed to: ${order.status}`
        );
      }
      this.order = order;
    });
}
```

---

## Data Flow Patterns

### Pattern 1: CRUD Operations

```
CREATE:
User Input → Validate → Service Logic → Database INSERT → Return Created Entity

READ:
Request → Auth Check → Database SELECT → Transform → Return JSON

UPDATE:
User Input → Validate → Service Logic → Database UPDATE → Audit Log → Return Updated

DELETE:
Request → Auth Check → Soft Delete (status = 'deleted') → Audit Log → Return Success
```

### Pattern 2: File Upload

```
1. User selects file (Frontend)
2. File sent as multipart/form-data (HTTP)
3. Laravel stores file temporarily
4. Service validates file (type, size, virus scan - future)
5. File moved to permanent storage
6. Database record created with file metadata
7. File URL returned to frontend
8. UI displays uploaded file
```

### Pattern 3: Background Jobs

```
1. Action triggers job (e.g., send notification)
2. Job queued in database (jobs table)
3. Laravel Horizon worker picks up job
4. Job executes (send email, process data)
5. On success: job deleted from queue
6. On failure: job retried (3 attempts) then moved to failed_jobs
7. Admin can view failed jobs in Horizon dashboard
```

### Pattern 4: Real-time Notifications

```
Current (Polling):
1. Frontend polls /api/notifications/unread every 30 seconds
2. Backend returns unread count and list
3. UI updates notification badge

Future (WebSockets):
1. Backend event fires (e.g., OrderStatusChanged)
2. Event broadcast via Laravel Echo + Pusher
3. Frontend listens on channel
4. Notification appears instantly
5. No polling needed
```

---

## Database Transaction Patterns

### Pattern: Atomic Operations

```php
DB::beginTransaction();

try {
    // Multiple related operations
    $order = Order::create($orderData);
    $order->addresses()->createMany($addresses);
    $order->documents()->create($documentData);
    
    // Update related entities
    $customer->decrement('available_credit_limit', $order->price);
    
    // Audit log
    AuditLog::create([/* ... */]);
    
    DB::commit();
    
} catch (\Exception $e) {
    DB::rollBack();
    throw $e;
}
```

### Pattern: Optimistic Locking

```php
// Prevent concurrent updates
$driver = Driver::lockForUpdate()->find($id);
$driver->update($newData);
```

---

## Security Data Flow

### Authentication Flow

```
1. User enters credentials at auth0.com
2. Auth0 validates credentials
3. Auth0 generates JWT (signed with private key)
4. Browser receives JWT
5. Angular stores JWT in memory (not localStorage/cookies)
6. Every API request: attach JWT in Authorization header
7. Laravel verifies JWT signature with Auth0 public key
8. If valid: extract user_id, roles
9. If invalid: return 401 Unauthorized
```

### Authorization Flow

```
1. Request reaches Laravel
2. Middleware extracts user from JWT
3. Load user's roles and permissions from database
4. Policy checks permission for requested action
5. If allowed: continue to controller
6. If denied: return 403 Forbidden
```

---

## Performance Optimizations

### Caching Layers

```
1. Browser Cache (Frontend)
   - Static assets (JS, CSS, images)
   - Service worker cache (future)

2. CDN Cache (Vercel)
   - Global edge caching
   - Automatic cache invalidation

3. Application Cache (Backend)
   - Redis cache for frequent queries
   - Cache tags for granular invalidation

4. Database Query Cache (PostgreSQL)
   - Internal PostgreSQL query cache
   - Materialized views (future)
```

### Eager Loading

```php
// Avoid N+1 queries
$drivers = Driver::with([
    'documents',
    'documents.files',
    'comments.author'
])->get();

// Instead of:
// 1 query for drivers
// N queries for documents (one per driver)
// M queries for files (one per document)
// → Total: 1 + N + M queries

// With eager loading:
// 1 query for drivers
// 1 query for all documents
// 1 query for all files
// → Total: 3 queries
```

---

## Related Documentation

- **[System Overview](system-overview.md)** - High-level architecture
- **[Business Processes](business-processes.md)** - Business workflows
- **[API Reference](../api/index.md)** - Detailed API specifications
- **[Technology Stack ADR](adr/2025-10-24-v2-technology-stack.md)** - Tech stack rationale

---

**Status:** ✅ Current  
**Next Review:** After V2 migration complete
