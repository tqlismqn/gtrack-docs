# Taiga UI Foundation Components Reference

## Overview
This document provides a comprehensive reference for Taiga UI 4.60.0 foundation components in G-Track TMS, focusing on Angular 20 standalone implementations.

## TuiRoot Component
### Purpose
The `TuiRoot` component is the primary wrapper for Taiga UI applications, providing essential configuration and global styling.

### Installation
```typescript
import { TuiRootModule } from '@taiga-ui/core';

@Component({
  standalone: true,
  imports: [TuiRootModule],
  selector: 'app-root',
  template: `
    <tui-root>
      <!-- Your app content -->
    </tui-root>
  `
})
export class AppComponent {}
```

### Configuration Options
- `appearance`: Theme configuration (light/dark)
- `language`: Default internationalization settings
- `icons`: Custom icon provider

## TuiAlerts System
### Notification Types
- `TuiNotification.Success`
- `TuiNotification.Error`
- `TuiNotification.Warning`
- `TuiNotification.Info`

### Usage Example
```typescript
import { TuiAlertModule, TuiAlertService } from '@taiga-ui/core';

@Component({
  standalone: true,
  imports: [TuiAlertModule],
})
export class AlertDemoComponent {
  constructor(private alerts: TuiAlertService) {}

  showSuccessAlert() {
    this.alerts
      .open('Operation successful', { status: TuiNotification.Success })
      .subscribe();
  }
}
```

## TuiDialogs System
### Dialog Types
- Modal Dialogs
- Confirmation Dialogs
- Custom Dynamic Dialogs

### Usage Example
```typescript
import { TuiDialogModule, TuiDialogService } from '@taiga-ui/core';

@Component({
  standalone: true,
  imports: [TuiDialogModule],
})
export class DialogDemoComponent {
  constructor(private dialogs: TuiDialogService) {}

  openConfirmDialog() {
    this.dialogs
      .open('Confirm Action', {
        label: 'Are you sure?',
        size: 'auto'
      })
      .subscribe();
  }
}
```

## TuiDropdown System
### Dropdown Types
- Standard Dropdown
- Contextual Menus
- Hints and Popovers

### Usage Example
```typescript
import { TuiDropdownModule } from '@taiga-ui/core';

@Component({
  standalone: true,
  imports: [TuiDropdownModule],
  template: `
    <button
      tuiButton
      [tuiDropdown]="dropdown">
      Open Dropdown
    </button>
    <ng-template #dropdown>
      <!-- Dropdown content -->
    </ng-template>
  `
})
export class DropdownDemoComponent {}
```

## Best Practices
- Always wrap application in `<tui-root>`
- Use standalone components for better tree-shaking
- Leverage dependency injection for services
- Configure global theme in app module

## Performance Tips
- Lazy load dialog and dropdown modules
- Use `ChangeDetectionStrategy.OnPush`
- Minimize DOM manipulation in templates

## Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast modes supported

## Troubleshooting
- Ensure `@taiga-ui/core` is correctly imported
- Check peer dependencies
- Verify Angular version compatibility