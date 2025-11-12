# Taiga UI Theme System

## Overview
The Taiga UI theme system provides robust, customizable styling for G-Track TMS applications with comprehensive theming capabilities.

## CSS Variables
### Color Palette
```scss
:root {
  // Primary Colors
  --tui-primary: #2C3E50;
  --tui-secondary: #34495E;
  --tui-accent: #3498DB;

  // Semantic Colors
  --tui-success: #27AE60;
  --tui-error: #E74C3C;
  --tui-warning: #F39C12;
  --tui-info: #3498DB;
}
```

### Dark Mode Configuration
```typescript
import { TUI_THEME, TUI_DARK_THEME } from '@taiga-ui/core';

@NgModule({
  providers: [
    {
      provide: TUI_THEME,
      useValue: TUI_DARK_THEME
    }
  ]
})
export class AppModule {}
```

## Custom Theme Creation
### Step-by-Step Guide
1. Create a custom theme file
```scss
// custom-theme.scss
@import '@taiga-ui/core/styles/theme';

$custom-theme: tui-derive-theme($tui-base-theme, (
  'color-primary': #007bff,
  'color-accent': #17a2b8,
  'border-radius': 8px
));
```

2. Import in global styles
```scss
// styles.scss
@import 'custom-theme.scss';
```

## Material Icons Integration
```typescript
import { TUI_ICONS_PATH } from '@taiga-ui/core';

@NgModule({
  providers: [
    {
      provide: TUI_ICONS_PATH,
      useValue: (name: string) => `path/to/icons/${name}.svg`
    }
  ]
})
export class AppModule {}
```

## SCSS Customization
### Global Configuration
```scss
// Customize global properties
:root {
  // Spacing
  --tui-space-xs: 4px;
  --tui-space-s: 8px;
  --tui-space-m: 16px;

  // Typography
  --tui-font-heading-1: 2.5rem;
  --tui-font-text: 1rem;
}
```

## Responsive Design
### Breakpoint Variables
```scss
$tui-breakpoint-xs: 375px;
$tui-breakpoint-s: 576px;
$tui-breakpoint-m: 768px;
$tui-breakpoint-l: 992px;
$tui-breakpoint-xl: 1200px;
```

## Performance Optimization
- Use CSS variables for dynamic theming
- Minimize custom CSS overrides
- Leverage Taiga UI's built-in theme system

## Accessibility Considerations
- Maintain sufficient color contrast
- Support high contrast modes
- Ensure readability across themes

## Troubleshooting
- Verify theme imports
- Check CSS variable precedence
- Use browser dev tools to inspect theme application