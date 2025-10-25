# Icons

## Icon Library

G-Track uses **Material Icons** as the primary icon library.

### Installation
Material Icons are included with Angular Material. No additional installation needed.

### Basic Usage
```html
<mat-icon>home</mat-icon>
<mat-icon>person</mat-icon>
<mat-icon>directions_car</mat-icon>
```

## Icon Sizes

### Standard Sizes

```css
.mat-icon-sm { font-size: 18px; width: 18px; height: 18px; }  /* Small */
.mat-icon    { font-size: 24px; width: 24px; height: 24px; }  /* Default */
.mat-icon-lg { font-size: 36px; width: 36px; height: 36px; }  /* Large */
.mat-icon-xl { font-size: 48px; width: 48px; height: 48px; }  /* Extra Large */
```

**Usage:**
- Buttons: 24px (default)
- Small buttons: 18px
- Large feature icons: 36px or 48px
- Sidebar navigation: 24px

## Icon Colors

### Semantic Colors

```css
.icon-primary   { color: var(--primary-500); }
.icon-success   { color: var(--success); }
.icon-warning   { color: var(--warning); }
.icon-error     { color: var(--error); }
.icon-info      { color: var(--info); }
.icon-disabled  { color: var(--gray-400); }
```

### Text Colors

```css
.icon-text-primary   { color: var(--text-primary); }
.icon-text-secondary { color: var(--text-secondary); }
```

## Module-Specific Icons

### Core Modules

| Module | Icon | Icon Name |
|--------|------|-----------|
| Dashboard | 🏠 | `dashboard` |
| Drivers | 👤 | `person` |
| Vehicles | 🚚 | `local_shipping` |
| Customers | 📇 | `contacts` |
| Orders | 📋 | `assignment` |
| Invoices | 💰 | `receipt` |
| Settings | ⚙️ | `settings` |

### Common Actions

| Action | Icon | Icon Name |
|--------|------|-----------|
| Add/Create | ➕ | `add` |
| Edit | ✏️ | `edit` |
| Delete | 🗑️ | `delete` |
| View | 👁️ | `visibility` |
| Download | ⬇️ | `download` |
| Upload | ⬆️ | `upload` |
| Search | 🔍 | `search` |
| Filter | 🔽 | `filter_list` |
| Sort | ↕️ | `sort` |
| Refresh | 🔄 | `refresh` |
| Close | ❌ | `close` |
| Check | ✅ | `check` |
| More | ⋮ | `more_vert` |
| Expand | ▼ | `expand_more` |
| Collapse | ▲ | `expand_less` |

### Status Icons

| Status | Icon | Icon Name |
|--------|------|-----------|
| Success | ✅ | `check_circle` |
| Error | ❌ | `error` |
| Warning | ⚠️ | `warning` |
| Info | ℹ️ | `info` |
| Pending | ⏳ | `schedule` |

### Document Icons

| Document Type | Icon | Icon Name |
|---------------|------|-----------|
| PDF | 📄 | `picture_as_pdf` |
| Image | 🖼️ | `image` |
| File | 📎 | `attach_file` |
| Folder | 📁 | `folder` |
| Document | 📃 | `description` |

### Navigation Icons

| Navigation | Icon | Icon Name |
|------------|------|-----------|
| Home | 🏠 | `home` |
| Back | ← | `arrow_back` |
| Forward | → | `arrow_forward` |
| Menu | ≡ | `menu` |
| Close Menu | × | `close` |

## Icon Usage Guidelines

### Do's ✅

1. **Use icons consistently** - Same action = same icon throughout app
2. **Pair with text labels** when possible for clarity
3. **Use appropriate sizes** - Don't make icons too small or too large
4. **Match icon style** - Use only Material Icons, not mixed styles
5. **Use semantic colors** - Green for success, red for error, etc.

### Don'ts ❌

1. **Don't use decorative icons** - Every icon should serve a purpose
2. **Don't use unclear icons** - If meaning isn't obvious, add a label
3. **Don't mix icon styles** - Stick to Material Icons throughout
4. **Don't overuse icons** - Too many icons = visual clutter
5. **Don't use icon-only buttons** without tooltips on desktop

## Tooltips with Icons

For icon-only buttons, always provide a tooltip:

```html
<button mat-icon-button matTooltip="Edit driver">
  <mat-icon>edit</mat-icon>
</button>
```

**Tooltip Guidelines:**
- Appear on hover (desktop) or long-press (mobile)
- Position: Below by default, adjust if near edge
- Delay: 500ms
- Clear, concise text (2-5 words)

## Custom SVG Icons

For icons not available in Material Icons, use custom SVG:

```typescript
// app.component.ts
export class AppComponent {
  constructor(private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer) {
    this.matIconRegistry.addSvgIcon(
      'custom-truck',
      this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/truck.svg')
    );
  }
}
```

```html
<mat-icon svgIcon="custom-truck"></mat-icon>
```

**Custom Icon Requirements:**
- Viewbox: 0 0 24 24
- Stroke width: 2px
- Optimized/minified SVG
- Single color (use currentColor for fill)
