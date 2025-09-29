# Модуль «Водители (Driver)» — API v0 (GET-only)

## База

- Префикс: `/api/v0`.
- Форматы дат: ISO-8601 в API; UI/импорт — `DD.MM.YYYY` (конвертация на сервере).
- Идентификаторы: ULID; маскирование полей — по `RBAC.md`.
- Ошибки: единый формат (см. ниже).

## GET /drivers

### Параметры

- `page` (`int ≥ 1`, по умолчанию `1`).
- `limit` (`1..200`, по умолчанию `25`).
- `search` (по `driverNumber`, `code`, ФИО).
- `status` (`draft|active|suspended|archived`).
- `hasBlockingIssues` (`bool`).
- `tags` (множественный фильтр).
- `language` (ISO 639-1).
- `euResident` (`bool` — определяется по пересечению `nationality`/`nationalities` с EU).
- `adrRequired` (`bool`).
- `documentType`.
- `documentState` (`pending_approval|valid|expired|rejected`, действует только совместно с `documentType`).
- `expiringWithinDays` (`int ≥ 0`).
- `sort` (`driverNumber|lastName|status|nextExpiryOn|createdAt`).
- `order` (`asc|desc`).
- `include` (`documents`, `assignments`, `notes`).

### Ответ 200 OK (фрагмент)

См. пример в разделе 5; включает `documents[].expiring` и `daysToExpiry` (вычисляемые поля).

## GET /drivers/{id}

- `id`: ULID.
- `include` как выше.
- Возвращает полную карточку с учетом RBAC/масок.

## Формат ошибок

```json
{
  "error": {
    "code": "VALIDATION_ERROR|NOT_FOUND|FORBIDDEN|CONFLICT|INTERNAL",
    "message": "…",
    "details": { "fieldErrors": [ { "field": "…", "reason": "…" } ] },
    "requestId": "01REQ…",
    "timestamp": "2025-09-29T19:20:10Z"
  }
}
```

Примеры ошибок см. `VALIDATION.md`.

## Design notes

- Нотификационные пороги/включённость настраиваются в админке per-тип и влияют на признак `expiring`, но не на фильтр `expiringWithinDays` (тот использует фактические даты).
