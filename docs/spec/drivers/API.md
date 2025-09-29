# Модуль «Водители (Driver)» — API v0 (GET-only)

База: `/api/v0`

## Общие
- Даты/время: ISO-8601 в API; UI/импорт — `DD.MM.YYYY` / 24h
- Идентификаторы: ULID; маскирование — по RBAC
- Ошибки: единый формат (`VALIDATION_ERROR`, `NOT_FOUND`, `FORBIDDEN`, `CONFLICT`, `INTERNAL`)

## GET `/drivers`
**Параметры**: 
- `page`, `limit`, `search`, `status`, `hasBlockingIssues`, `tags`, `language`, `euResident`, `adrRequired`, 
- `documentType`, `documentState`, 
- `expiringWithinDays`, 
- `sort`, `order`, 
- `include` (`documents,assignments,notes`).

**200 OK (фрагмент)**
```json
{
  "page": 1,
  "limit": 50,
  "total": 123,
  "items": [
    {
      "id": "01J9…",
      "driverNumber": "DRV000123",
      "code": "EMP-2025-042",
      "person": {"firstName":"Ivan","lastName":"Petrov","dateOfBirth":"1989-12-04"},
      "rolesTags": {"tags":["ADR"],"languages":["cs","en","ru"]},
      "employment": {"employmentType":"employee","hiredOn":"2024-06-01","payrollEnabled":true},
      "compliance": {"status":"active","nextExpiryOn":"2025-11-30","hasBlockingIssues":false},
      "documents": [
        {"type":"driver_license","state":"valid","expiryDate":"2031-03-01","categories":["C","CE"],"expiring":false,"daysToExpiry":1980}
      ]
    }
  ]
}
```

## GET `/drivers/{id}`

**Query:** `include=documents,assignments,notes` (RBAC/маски применяются)

**200 OK (фрагмент)** — полный профиль водителя с маскированием по роли (см. VALIDATION/RBAC)

## Единый формат ошибок (пример)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query parameters.",
    "details": {"fieldErrors":[{"field":"limit","reason":"out_of_range","expected":"1..200","actual":250}]},
    "requestId": "01REQ…",
    "timestamp": "2025-09-29T19:20:10Z"
  }
}
```

**Design notes:** пороги уведомлений per-type влияют на `documents[].expiring`, но не на фильтр `expiringWithinDays`.
