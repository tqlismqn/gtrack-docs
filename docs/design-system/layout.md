# Layout Patterns

## Application Shell

### Overall Structure

```
┌─────────────────────────────────────────────┐
│              Header (64px fixed)            │
├──────┬──────────────────────────────────────┤
│      │                                      │
│ Side │         Main Content Area            │
│ Nav  │                                      │
│(240px│                                      │
│ or   │                                      │
│ 60px)│                                      │
│      │                                      │
└──────┴──────────────────────────────────────┘
```

### Header

**Height:** 64px (fixed)  
**Background:** White  
**Shadow:** Level 1  
**z-index:** `--z-fixed` (1030)

**Structure:**
```
┌─[Logo]─[Module Title]───────[Search]─[Notifications]─[Profile]─┐
```

**Components:**
- **Logo**: 40×40px, left-aligned, padding-left 16px
- **Module Title**: text-lg, font-semibold, gray-900
- **Search**: Expandable input, icon-only when collapsed
- **Notifications**: Icon button with badge (unread count)
- **Profile**: Avatar + dropdown menu

### Sidebar Navigation

**Width:** 
- Expanded: 240px
- Collapsed: 60px

**Background:** White  
**Border-right:** 1px solid gray-300  
**z-index:** `--z-drawer` (1040)

**Toggle:**
- Hamburger menu icon in top-left
- Smooth transition (300ms)
- Save state in localStorage

**Navigation Items:**

**Expanded State:**
```
┌─[Icon]─[Label]─────────►┐
│  🏠    Dashboard         │
│  👤    Drivers       [>] │ ← Expandable
│  🚚    Vehicles          │
│  📋    Orders            │
└──────────────────────────┘
```

**Collapsed State:**
```
┌─[Icon]─┐
│   🏠   │ ← Tooltip on hover
│   👤   │
│   🚚   │
│   📋   │
└────────┘
```

**Item States:**
- **Default**: Gray-600 icon, gray-700 text
- **Hover**: Gray-100 background
- **Active**: Primary-700 background, white text/icon
- **Disabled**: Gray-400 icon/text

**"Coming Soon" Badge:**
```html
<div class="nav-item">
  <mat-icon>folder</mat-icon>
  <span>Invoices</span>
  <span class="badge badge--warning">Soon</span>
</div>
```

### Main Content Area

**Padding:** `--space-6` (24px)  
**Background:** `--bg-page` (gray-50)  
**Max-width:** 1600px (centered for ultra-wide screens)

**Typical Layout:**
```
┌─────────────────────────────────────┐
│ [Breadcrumbs]                       │
│ [Page Title] ────────────── [Action]│
├─────────────────────────────────────┤
│                                     │
│  [Statistics Cards Row]             │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  [Filters Bar]                      │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  [Main Content / Table]             │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

## Module Layout Patterns

### List View (e.g., Drivers List)

**Components:**
1. **Page Header**
   - Title (text-2xl, font-bold)
   - Action buttons (Add New, Export, etc.)
2. **Statistics Cards Row**
   - 4 cards showing key metrics
   - Equal width, responsive (stack on mobile)
3. **Filters Bar**
   - Quick filters as chips/buttons
   - Advanced filter collapse/expand
4. **Data Table**
   - Sticky header
   - Pagination at bottom
5. **Empty State** (when no data)
   - Illustration + message + primary action

### Split View (e.g., Driver Detail)

**Layout:**
```
┌──────────┬──────────────────────────┐
│   List   │      Detail Panel       │
│  (30%)   │        (70%)            │
│          │                         │
│  Item 1  │  ┌──────────────────┐  │
│  Item 2  │  │ Tabs             │  │
│  Item 3  │  ├──────────────────┤  │
│  Item 4  │  │                  │  │
│  Item 5  │  │  Tab Content     │  │
│          │  │                  │  │
└──────────┴──────────────────────────┘
```

**Behavior:**
- List on left (scrollable)
- Detail on right (scrollable independently)
- Selected item highlighted in list
- Detail panel tabs for different sections
- Responsive: Stack vertically on tablet/mobile

### Form Layout

**Single Column (Simple Forms):**
- Max-width: 600px
- Centered or left-aligned
- Field spacing: `--space-4` between fields
- Section spacing: `--space-8`

**Two Column (Complex Forms):**
- Use CSS Grid: `grid-template-columns: 1fr 1fr`
- Gap: `--space-6`
- Full-width fields span both columns
- Responsive: Single column on mobile

**Form Sections:**
```html
<div class="form-section">
  <h3 class="form-section__title">Personal Information</h3>
  <div class="form-section__content">
    <!-- Fields -->
  </div>
</div>
```

## Responsive Breakpoints

### Mobile (< 600px)
- Sidebar: Hidden by default, overlay when opened
- Header: Hamburger menu + logo only
- Tables: Horizontal scroll or card view
- Forms: Single column
- Statistics cards: Single column stack

### Tablet (600px - 960px)
- Sidebar: Collapsed by default (60px)
- Header: All elements visible
- Tables: Horizontal scroll if needed
- Forms: Single or two columns
- Statistics cards: 2 columns

### Desktop (960px - 1280px)
- Sidebar: Expanded (240px)
- Full table view
- Two-column forms
- Statistics cards: 4 columns

### Large Desktop (> 1280px)
- Same as desktop
- Main content max-width to prevent excessive line length

## Spacing Guidelines

### Component Spacing

**Inside Cards:**
- Padding: `--space-6` (24px)
- Between sections: `--space-4` (16px)

**Between Cards:**
- Vertical gap: `--space-6` (24px)
- Horizontal gap: `--space-6` (24px)

**Form Fields:**
- Between fields: `--space-4` (16px)
- Between sections: `--space-8` (32px)

**Table:**
- Cell padding: `12px 16px`
- Row height: 48px (default), 40px (dense)

### Page Spacing

- Page padding: `--space-6` (24px)
- Section margins: `--space-8` to `--space-12`
- Content max-width: 1600px
