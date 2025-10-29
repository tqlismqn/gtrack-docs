# Onboarding & Company Setup

## Registration Flow

**Step 1: Auth0 Registration**

```
User visits: https://app.g-track.eu
  ↓
Clicks "Get Started"
  ↓
Auth0 registration form:
  - Email
  - Password
  - Accept Terms & Privacy
  ↓
Email verification
  ↓
Redirects to Company Setup
```

## Step 2: Company Setup

**Setup Form Fields:**

1. **Company Name** (required)
2. **Country/Region** (required) - Determines currency, tax rate, date format
   - 🇨🇿 Czech Republic (CZK)
   - 🇵🇱 Poland (PLN)
   - 🇩🇪 Germany (EUR)
   - 🇦🇹 Austria (EUR)
   - 🇳🇱 Netherlands (EUR)
   - 🇮🇹 Italy (EUR)
3. **Interface Language** (required)
   - 🇷🇺 Russian
   - 🇬🇧 English
   - 🇨🇿 Czech
   - 🇵🇱 Polish
   - 🇩🇪 German
4. **VAT ID** (optional) - Can be added later in Settings

**Auto-Configuration Based on Country:**

| Country | Currency | Tax Rate | Date Format | Timezone | First Day |
|---------|----------|----------|-------------|----------|-----------|
| **CZ** | CZK | 21% | DD.MM.YYYY | Europe/Prague | Monday |
| **PL** | PLN | 23% | DD.MM.YYYY | Europe/Warsaw | Monday |
| **DE** | EUR | 19% | DD.MM.YYYY | Europe/Berlin | Monday |
| **AT** | EUR | 20% | DD.MM.YYYY | Europe/Vienna | Monday |
| **NL** | EUR | 21% | DD.MM.YYYY | Europe/Amsterdam | Monday |

## Step 3: Free Trial

- **Duration:** 30 days
- **Limitations:** 5 drivers, 3 vehicles
- **Features:** Full access to all features
- **No Credit Card:** Required only for paid plan upgrade

---

**Last Updated:** October 29, 2025
**Version:** 2.0.1
**Source:** Master Specification v3.1, Section 6
