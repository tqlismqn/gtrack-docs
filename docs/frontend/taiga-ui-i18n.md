# Taiga UI Internationalization Guide

## Overview
Comprehensive internationalization (i18n) support for G-Track TMS using Taiga UI 4.60.0.

## Language Provider Setup
### Basic Configuration
```typescript
import {
  TUI_LANGUAGE,
  TUI_RUSSIAN_LANGUAGE,
  TUI_ENGLISH_LANGUAGE
} from '@taiga-ui/core';

@NgModule({
  providers: [
    {
      provide: TUI_LANGUAGE,
      useValue: TUI_RUSSIAN_LANGUAGE // Default language
    }
  ]
})
export class AppModule {}
```

## Supported Languages
- English (default)
- Russian
- German
- French
- Spanish
- Arabic (RTL support)

## Runtime Language Switching
```typescript
import { TuiLanguageSwitcher } from '@taiga-ui/core';

@Component({
  selector: 'app-language-switcher'
})
export class LanguageSwitcherComponent {
  constructor(private languageSwitcher: TuiLanguageSwitcher) {}

  changeLanguage(lang: string) {
    this.languageSwitcher.setLanguage(
      this.getLanguageToken(lang)
    );
  }

  private getLanguageToken(lang: string) {
    const languages = {
      'en': TUI_ENGLISH_LANGUAGE,
      'ru': TUI_RUSSIAN_LANGUAGE,
      // Add other languages
    };
    return languages[lang] || TUI_ENGLISH_LANGUAGE;
  }
}
```

## Custom Language Implementation
```typescript
import { TUI_LANGUAGE } from '@taiga-ui/core';

const CUSTOM_LANGUAGE = {
  months: ['Январь', 'Февраль', ...],
  days: ['Понедельник', 'Вторник', ...],
  dateFormat: 'DD.MM.YYYY',
  // Other custom translations
};

@NgModule({
  providers: [
    {
      provide: TUI_LANGUAGE,
      useValue: CUSTOM_LANGUAGE
    }
  ]
})
export class CustomLanguageModule {}
```

## RTL (Right-to-Left) Support
```typescript
import { TUI_LANGUAGE_RTL } from '@taiga-ui/core';

@NgModule({
  providers: [
    {
      provide: TUI_LANGUAGE_RTL,
      useValue: true // For Arabic, Hebrew, etc.
    }
  ]
})
export class RTLSupportModule {}
```

## Localization Best Practices
- Use language tokens consistently
- Separate translation files
- Leverage Angular's built-in i18n
- Test with multiple languages

## Performance Considerations
- Lazy load language modules
- Cache language resources
- Minimize runtime language switches

## Debugging Internationalization
- Verify language provider setup
- Check browser locale settings
- Use browser dev tools language settings

## Accessibility in Multi-Language Context
- Support screen reader translations
- Maintain consistent UI layout
- Handle text expansion/contraction

## Example Translation File Structure
```typescript
// translations.ts
export const TRANSLATIONS = {
  en: {
    welcome: 'Welcome to G-Track',
    dashboard: 'Dashboard'
  },
  ru: {
    welcome: 'Добро пожаловать в G-Track',
    dashboard: 'Панель управления'
  }
};
```

## Troubleshooting Common Issues
- Ensure correct language token import
- Verify module providers
- Check for circular dependencies
- Use Angular DevTools for language debugging