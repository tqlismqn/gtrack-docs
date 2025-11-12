# Frontend Development Documentation

This section contains technical documentation specific to the G-Track frontend application built with Angular 20 and Taiga UI 4.60.0.

---

## 📚 Taiga UI Integration

**Migration Date:** November 9-11, 2025
**Status:** ✅ Complete

### Core Guides

- [**Taiga UI Migration Guide**](taiga-ui-migration-guide.md)
  - Step-by-step migration from Material Design 3
  - Component mapping reference
  - Common issues and solutions
  - Bundle size comparison

- [**Taiga UI Theme System**](taiga-ui-theme-system.md)
  - Dark mode implementation
  - CSS variables customization
  - Brand color configuration
  - Theme switching patterns

- [**Taiga UI i18n**](taiga-ui-i18n.md)
  - Transloco integration
  - Language switcher implementation
  - RTL support (future)
  - Date/number formatting

- [**Taiga UI Foundation**](taiga-ui-foundation.md)
  - Architecture overview
  - CDK utilities
  - Reactive forms integration
  - Performance best practices

---

## 🎨 Component Library

G-Track uses Taiga UI 4.60.0 for all UI components.

### Available Components (120+)

**Form Controls:**
- `TuiInputModule` - Text input with validation
- `TuiSelectModule` - Dropdown select
- `TuiCheckboxModule` - Checkbox control
- `TuiRadioModule` - Radio buttons
- `TuiTextAreaModule` - Multi-line text input
- `TuiInputDateModule` - Date picker
- `TuiInputPhoneModule` - Phone number input
- `TuiInputPasswordModule` - Password with toggle

**Navigation:**
- `TuiTabsModule` - Tab navigation
- `TuiStepperModule` - Multi-step forms
- `TuiBreadcrumbsModule` - Breadcrumb navigation
- `TuiPaginationModule` - Pagination controls

**Data Display:**
- `TuiTableModule` - Data tables
- `TuiCardModule` - Card containers
- `TuiBadgeModule` - Status badges
- `TuiAvatarModule` - User avatars
- `TuiTagModule` - Tags/labels

**Feedback:**
- `TuiAlertModule` - Alert messages
- `TuiDialogModule` - Modal dialogs
- `TuiNotificationModule` - Toast notifications
- `TuiLoaderModule` - Loading indicators

**Layout:**
- `TuiSidebarModule` - Sidebar navigation
- `TuiHeaderModule` - Page headers
- `TuiFooterModule` - Page footers
- `TuiAppBarModule` - Application bar

---

## 🏗️ Architecture Patterns

### Component Structure

```typescript
// G-Track component pattern
@Component({
  selector: 'app-driver-list',
  standalone: true,
  imports: [
    CommonModule,
    TuiTableModule,
    TuiInputModule,
    TuiButtonModule,
  ],
  templateUrl: './driver-list.component.html',
  styleUrls: ['./driver-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DriverListComponent {
  // Use Angular Signals for state
  drivers = signal<Driver[]>([]);
  loading = signal<boolean>(false);

  // Reactive forms with Taiga UI
  searchForm = new FormGroup({
    query: new FormControl(''),
    status: new FormControl('all'),
  });

  constructor(
    private driverService: DriverService,
    private cdr: ChangeDetectorRef,
  ) {}
}
```

### State Management

G-Track uses **Angular Signals** (no NgRx/Akita needed):

```typescript
// Signal-based state
export class DriverStore {
  // Writeable signals
  private drivers$ = signal<Driver[]>([]);
  private loading$ = signal<boolean>(false);
  private error$ = signal<Error | null>(null);

  // Computed signals
  activeDrivers = computed(() =>
    this.drivers$().filter(d => d.status === 'active')
  );

  readyDrivers = computed(() =>
    this.drivers$().filter(d => d.readiness === 'ready')
  );

  // Public readonly signals
  drivers = this.drivers$.asReadonly();
  loading = this.loading$.asReadonly();
  error = this.error$.asReadonly();
}
```

### Internationalization

G-Track uses **Transloco** (modern alternative to ngx-translate):

```typescript
// Translation usage
@Component({
  imports: [TranslocoModule],
  template: `
    <h1>{{ 'drivers.title' | transloco }}</h1>
    <p>{{ 'drivers.count' | transloco: { count: drivers().length } }}</p>
  `
})
export class DriverListComponent {}
```

---

## 🎯 Best Practices

### 1. Always Use OnPush Change Detection

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MyComponent {}
```

### 2. Prefer Signals Over Observables for State

```typescript
// ✅ Good - Signal-based
count = signal(0);
increment() { this.count.update(v => v + 1); }

// ⚠️ Old pattern - Observable-based
count$ = new BehaviorSubject(0);
increment() { this.count$.next(this.count$.value + 1); }
```

### 3. Use Taiga UI Form Controls

```typescript
// ✅ Good - Taiga UI
<tui-input formControlName="email">
  Email Address
  <input tuiTextfield type="email" />
</tui-input>

// ❌ Avoid - Plain HTML
<input type="email" formControlName="email" />
```

### 4. Leverage Taiga UI Theme System

```scss
// Use CSS variables from Taiga UI
.my-component {
  background: var(--tui-base-01);
  color: var(--tui-text-01);
  border: 1px solid var(--tui-base-03);

  &:hover {
    background: var(--tui-base-02);
  }
}
```

---

## 📦 Bundle Size Optimization

**Current Bundle Size (November 2025):**
- Initial chunk: 247 KB (gzipped)
- Lazy routes: ~50-80 KB each
- Total production build: ~800 KB

**Optimization Techniques:**
1. Lazy loading for all routes
2. Tree-shaking of unused Taiga UI components
3. OnPush change detection everywhere
4. No Zone.js (signal-based reactivity)

---

## 🧪 Testing

### Unit Tests (Jasmine + Karma)

```typescript
describe('DriverListComponent', () => {
  let component: DriverListComponent;
  let fixture: ComponentFixture<DriverListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        DriverListComponent,
        TuiTableModule,
        TuiInputModule,
      ],
      providers: [
        { provide: DriverService, useClass: MockDriverService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DriverListComponent);
    component = fixture.componentInstance;
  });

  it('should display drivers table', () => {
    component.drivers.set(mockDrivers);
    fixture.detectChanges();

    const table = fixture.nativeElement.querySelector('tui-table');
    expect(table).toBeTruthy();
  });
});
```

### E2E Tests (Playwright)

```typescript
test('should login and view drivers list', async ({ page }) => {
  await page.goto('https://app.g-track.eu/login');

  // Login
  await page.fill('[formControlName="email"]', 'admin@test.com');
  await page.fill('[formControlName="password"]', 'password');
  await page.click('button[type="submit"]');

  // Navigate to drivers
  await page.waitForURL('**/dashboard');
  await page.click('text=Drivers');

  // Verify drivers table
  await expect(page.locator('tui-table')).toBeVisible();
});
```

---

## 📖 Additional Resources

**Taiga UI Official Docs:**
- https://taiga-ui.dev (main documentation)
- https://taiga-ui.dev/components (component showcase)
- https://github.com/taiga-family/taiga-ui (GitHub repository)

**G-Track Specific:**
- [Design System](../17-design-system.md)
- [API Integration](../15-api-specification.md)

---

**Last Updated:** November 12, 2025
**Maintainer:** Frontend Team
