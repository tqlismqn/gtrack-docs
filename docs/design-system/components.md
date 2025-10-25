# Components

## Buttons

### Primary Button

**Appearance:**
- Background: `--primary-500`
- Text: `--text-on-primary` (white)
- Padding: `12px 24px`
- Border-radius: `--radius-md` (8px)
- Font-weight: `--font-medium` (500)
- Shadow: Level 1
- Hover: Background `--primary-600`, Shadow Level 2
- Active: Background `--primary-700`

**Usage:**
- Main actions (Save, Create, Confirm)
- One primary button per section
- Call-to-action buttons

**Example:**
```html
<button class="btn btn-primary">Save Changes</button>
```

### Secondary Button

**Appearance:**
- Background: transparent
- Border: 1px solid `--primary-500`
- Text: `--primary-500`
- Padding: `11px 23px` (1px less for border)
- Hover: Background `--primary-50`

**Usage:**
- Alternative actions
- Cancel buttons
- Less important actions

### Icon Button

**Appearance:**
- Size: 40×40px
- Background: transparent
- Icon: Material Icons, 24px
- Hover: Background `--bg-hover`
- Radius: `--radius-md`

**Usage:**
- Actions in table rows (Edit, Delete, View)
- Toolbar actions
- Navigation controls

## Inputs

### Text Input

**Appearance:**
- Height: 48px (default), 40px (dense), 56px (large)
- Padding: `12px 16px`
- Border: 1px solid `--gray-300`
- Border-radius: `--radius-md`
- Font-size: `--text-base`
- Focus: Border `--primary-500`, shadow with primary color

**States:**
- Default: Border gray-300
- Focus: Border primary-500, shadow
- Error: Border error, helper text red
- Disabled: Background gray-100, text gray-500

**Example:**
```html
<mat-form-field appearance="outline">
  <mat-label>Driver Name</mat-label>
  <input matInput type="text" />
  <mat-hint>Enter first and last name</mat-hint>
  <mat-error>This field is required</mat-error>
</mat-form-field>
```

### Select Dropdown

**Appearance:**
- Same as text input
- Dropdown arrow icon (chevron-down)
- Dropdown panel: Shadow level 2
- Options: Hover background gray-100
- Selected: Background primary-50

### Date Picker

**Appearance:**
- Input with calendar icon
- Calendar dialog: Shadow level 3
- Today: Border primary-500
- Selected: Background primary-500, text white

### Checkbox

**Size:** 20×20px  
**Checked:** Background primary-500, white checkmark  
**Unchecked:** Border gray-400  
**Disabled:** Background gray-200

### Radio Button

**Size:** 20×20px  
**Selected:** Outer circle primary-500, inner dot primary-700  
**Unselected:** Border gray-400

## Cards

### Default Card

**Appearance:**
- Background: `--bg-card` (white)
- Border-radius: `--radius-md` (8px)
- Shadow: Level 1
- Padding: `--space-6` (24px)

**Structure:**
```html
<mat-card>
  <mat-card-header>
    <mat-card-title>Card Title</mat-card-title>
    <mat-card-subtitle>Subtitle</mat-card-subtitle>
  </mat-card-header>
  <mat-card-content>
    <!-- Content here -->
  </mat-card-content>
  <mat-card-actions>
    <button mat-button>Action</button>
  </mat-card-actions>
</mat-card>
```

### Status Card (Dashboard)

**Appearance:**
- Background: gradient or solid color
- Large number display (text-3xl, font-bold)
- Icon in top-right corner
- No shadow by default
- Hover: Shadow level 2

**Example:**
```html
<div class="status-card status-card--success">
  <div class="status-card__icon">
    <mat-icon>check_circle</mat-icon>
  </div>
  <div class="status-card__value">25</div>
  <div class="status-card__label">Active Drivers</div>
</div>
```

## Tables

### Data Table

**Structure:**
- Fixed header (sticky)
- Zebra striping (optional): Odd rows white, even rows gray-50
- Row hover: Background gray-100
- Row selected: Background primary-50
- Cell padding: `12px 16px`

**Header:**
- Background: `--gray-100`
- Font-weight: `--font-semibold`
- Font-size: `--text-sm`
- Text-transform: uppercase
- Letter-spacing: `--tracking-wide`

**Cells:**
- Font-size: `--text-sm`
- Vertical-align: middle
- Border-bottom: 1px solid gray-200

**Actions Column:**
- Fixed width: 120px
- Right-aligned
- Icon buttons for Edit, View, Delete

**Example:**
```html
<table mat-table [dataSource]="dataSource">
  <ng-container matColumnDef="name">
    <th mat-header-cell *matHeaderCellDef>Driver Name</th>
    <td mat-cell *matCellDef="let driver">{{driver.name}}</td>
  </ng-container>
  
  <ng-container matColumnDef="actions">
    <th mat-header-cell *matHeaderCellDef></th>
    <td mat-cell *matCellDef="let driver">
      <button mat-icon-button (click)="edit(driver)">
        <mat-icon>edit</mat-icon>
      </button>
      <button mat-icon-button (click)="delete(driver)">
        <mat-icon>delete</mat-icon>
      </button>
    </td>
  </ng-container>
  
  <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
  <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
</table>
```

### Pagination

**Appearance:**
- Bottom of table
- Items per page selector: 10, 20, 50, 100
- Page numbers with arrows
- Current page: Background primary-500, text white
- Other pages: Background transparent, text primary-500

## Chips (Tags)

### Status Chip

**Sizes:**
- Default: `24px` height
- Small: `20px` height

**Colors (based on status):**
- **Success** (Green): Background `--success-light`, text `--success-dark`
- **Warning** (Orange): Background `--warning-light`, text `--warning-dark`
- **Error** (Red): Background `--error-light`, text `--error-dark`
- **Info** (Blue): Background `--info-light`, text `--info-dark`
- **Default** (Gray): Background `--gray-200`, text `--gray-800`

**Example:**
```html
<mat-chip class="status-chip status-chip--success">Active</mat-chip>
<mat-chip class="status-chip status-chip--warning">Expiring Soon</mat-chip>
<mat-chip class="status-chip status-chip--error">Expired</mat-chip>
```

## Tabs

**Appearance:**
- Underline style (Material Design)
- Active tab: Underline `--primary-500`, text `--text-primary`
- Inactive tab: Text `--text-secondary`
- Hover: Text `--text-primary`
- Ink bar animation: 200ms ease-in-out

**Example:**
```html
<mat-tab-group>
  <mat-tab label="Overview">Content 1</mat-tab>
  <mat-tab label="Documents">Content 2</mat-tab>
  <mat-tab label="History">Content 3</mat-tab>
</mat-tab-group>
```

## Dialogs (Modals)

**Appearance:**
- Background: White
- Shadow: Level 4
- Border-radius: `--radius-lg` (12px)
- Max-width: 600px (small), 800px (medium), 1200px (large)
- Overlay: rgba(0, 0, 0, 0.5)

**Structure:**
```html
<mat-dialog-content>
  <h2 mat-dialog-title>Dialog Title</h2>
  <mat-dialog-content>
    <!-- Content -->
  </mat-dialog-content>
  <mat-dialog-actions align="end">
    <button mat-button mat-dialog-close>Cancel</button>
    <button mat-raised-button color="primary">Confirm</button>
  </mat-dialog-actions>
</mat-dialog-content>
```

## Notifications (Snackbar/Toast)

**Appearance:**
- Background: Based on type (success, error, info, warning)
- Text: White
- Position: Bottom-center or top-right
- Duration: 3-5 seconds
- Shadow: Level 3
- Radius: `--radius-md`

**Types:**
- **Success**: Background `--success`, icon "check_circle"
- **Error**: Background `--error`, icon "error"
- **Warning**: Background `--warning`, icon "warning"
- **Info**: Background `--info`, icon "info"

## Loading States

### Spinner

**Sizes:**
- Small: 20px
- Default: 40px
- Large: 60px

**Colors:**
- Primary: `--primary-500`
- On white background: Primary
- On colored background: White

### Skeleton Loader

**Appearance:**
- Background: Linear gradient animation
- Base color: `--gray-200`
- Shine color: `--gray-100`
- Animation: 1.5s ease-in-out infinite
- Border-radius: Match component

**Usage:**
- Loading tables: Show skeleton rows
- Loading cards: Show skeleton content blocks
- Loading text: Show skeleton lines

## Icon Buttons in Tables

**Standard Actions:**
- **Edit**: `edit` icon, color primary-500
- **View**: `visibility` icon, color gray-600
- **Delete**: `delete` icon, color error-500
- **Download**: `download` icon, color gray-600
- **More**: `more_vert` icon, color gray-600

**Hover States:**
- Circular background: gray-100
- Icon stays same color

## Progress Indicators

### Linear Progress

**Appearance:**
- Height: 4px
- Background: `--gray-200`
- Fill: `--primary-500`
- Animation: Indeterminate or determinate

**Usage:**
- Top of page for loading
- Inside cards for progress tracking

### Circular Progress

**Sizes:**
- Small: 20px
- Default: 40px
- Large: 60px

**Usage:**
- Button loading states
- Center of empty states
- Inline with text ("Loading...")
