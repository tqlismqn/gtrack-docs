# Foundation

## Colors

### Primary Color Palette

**Primary Blue:**
```css
--primary-50: #E3F2FD;
--primary-100: #BBDEFB;
--primary-200: #90CAF9;
--primary-300: #64B5F6;
--primary-400: #42A5F5;
--primary-500: #2196F3;  /* Main brand color */
--primary-600: #1E88E5;
--primary-700: #1976D2;
--primary-800: #1565C0;
--primary-900: #0D47A1;
```

**Usage:**
- Primary-500: Main actions, links, active states
- Primary-700: Sidebar active item background
- Primary-100: Hover states, subtle backgrounds

### Accent Color Palette

**Accent Green:**
```css
--accent-50: #E8F5E9;
--accent-100: #C8E6C9;
--accent-500: #4CAF50;  /* Success states */
--accent-700: #388E3C;
```

**Usage:**
- Success messages
- Valid/Active status indicators
- Positive actions (Save, Confirm)

### Semantic Colors

**Success:**
```css
--success-light: #81C784;
--success: #4CAF50;
--success-dark: #388E3C;
```

**Warning:**
```css
--warning-light: #FFB74D;
--warning: #FF9800;
--warning-dark: #F57C00;
```

**Error:**
```css
--error-light: #E57373;
--error: #F44336;
--error-dark: #D32F2F;
```

**Info:**
```css
--info-light: #64B5F6;
--info: #2196F3;
--info-dark: #1976D2;
```

### Neutral Colors

**Grays:**
```css
--gray-50: #FAFAFA;
--gray-100: #F5F5F5;
--gray-200: #EEEEEE;
--gray-300: #E0E0E0;
--gray-400: #BDBDBD;
--gray-500: #9E9E9E;
--gray-600: #757575;
--gray-700: #616161;
--gray-800: #424242;
--gray-900: #212121;
```

**Usage:**
- Gray-50: Page background
- Gray-100: Card backgrounds
- Gray-300: Borders, dividers
- Gray-700: Primary text
- Gray-500: Secondary text

### Background Colors

```css
--bg-page: #FAFAFA;        /* Main page background */
--bg-card: #FFFFFF;        /* Card/Panel backgrounds */
--bg-hover: #F5F5F5;       /* Hover states */
--bg-selected: #E3F2FD;    /* Selected items */
--bg-disabled: #F5F5F5;    /* Disabled states */
```

### Text Colors

```css
--text-primary: #212121;    /* Main headings, important text */
--text-secondary: #757575;  /* Descriptive text, labels */
--text-disabled: #BDBDBD;   /* Disabled text */
--text-on-primary: #FFFFFF; /* Text on primary color */
--text-link: #2196F3;       /* Links */
```

## Typography

### Font Family

**Primary Font:**
```css
--font-family-primary: 'Roboto', 'Segoe UI', 'Arial', sans-serif;
```

**Monospace Font (for codes, numbers):**
```css
--font-family-mono: 'Roboto Mono', 'Courier New', monospace;
```

### Font Sizes

```css
--text-xs: 12px;    /* Small labels, captions */
--text-sm: 14px;    /* Body text, table cells */
--text-base: 16px;  /* Default body text */
--text-lg: 18px;    /* Subheadings */
--text-xl: 20px;    /* Section titles */
--text-2xl: 24px;   /* Page titles */
--text-3xl: 30px;   /* Large headings */
--text-4xl: 36px;   /* Hero text */
```

### Font Weights

```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

**Usage:**
- Headings: 600 (semibold) or 700 (bold)
- Body text: 400 (normal)
- Labels: 500 (medium)
- Important numbers: 600 (semibold)

### Line Heights

```css
--leading-tight: 1.25;   /* Headings */
--leading-normal: 1.5;   /* Body text */
--leading-relaxed: 1.75; /* Long-form content */
```

### Letter Spacing

```css
--tracking-tight: -0.025em;  /* Large headings */
--tracking-normal: 0;         /* Default */
--tracking-wide: 0.025em;     /* All-caps labels */
```

## Spacing

### Spacing Scale

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
```

**Usage Guidelines:**
- Component padding: space-3 to space-6
- Section spacing: space-8 to space-12
- Page margins: space-6 to space-8
- Form field gaps: space-4
- Button padding: space-3 (vertical) × space-6 (horizontal)

## Border Radius

```css
--radius-sm: 4px;    /* Small elements, chips */
--radius-md: 8px;    /* Cards, buttons */
--radius-lg: 12px;   /* Large cards, modals */
--radius-full: 9999px; /* Pills, avatars */
```

## Shadows

### Elevation Levels

**Level 1 (Subtle):**
```css
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
```
*Usage: Cards at rest*

**Level 2 (Default):**
```css
box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
```
*Usage: Raised cards, dropdowns*

**Level 3 (Emphasized):**
```css
box-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23);
```
*Usage: Modals, floating action buttons*

**Level 4 (Modal):**
```css
box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
```
*Usage: Dialogs, overlays*

## Z-Index Scale

```css
--z-base: 0;        /* Normal content */
--z-dropdown: 1000; /* Dropdowns */
--z-sticky: 1020;   /* Sticky headers */
--z-fixed: 1030;    /* Fixed headers */
--z-drawer: 1040;   /* Side drawers */
--z-modal: 1050;    /* Modal dialogs */
--z-popover: 1060;  /* Popovers */
--z-tooltip: 1070;  /* Tooltips */
--z-toast: 1080;    /* Toast notifications */
```

## Grid System

### Container Widths

```css
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;
```

### Grid Columns

Standard 12-column grid for responsive layouts:
- Mobile: 4 columns
- Tablet: 8 columns
- Desktop: 12 columns

### Breakpoints

```css
--breakpoint-xs: 0px;
--breakpoint-sm: 600px;
--breakpoint-md: 960px;
--breakpoint-lg: 1280px;
--breakpoint-xl: 1920px;
```

## Transitions

### Duration

```css
--transition-fast: 150ms;
--transition-base: 200ms;
--transition-slow: 300ms;
--transition-slower: 500ms;
```

### Easing

```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

**Default transition:**
```css
transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
```
