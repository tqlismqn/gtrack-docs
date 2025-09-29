# Модуль «Водители (Driver)» — API v0 (GET-only)

База: `/api/v0`

## Общие
- Форматы дат: **ISO-8601** в API; UI/импорт — `DD.MM.YYYY` (конвертация на сервере)
- Идентификаторы: ULID; маскирование полей — по RBAC
- Ошибки: единый формат (см. ниже)

## GET `/drivers`
**Параметры**
- `page` (int≥1=1), `limit` (1..200=25)
- `search` (по driverNumber, code, ФИО)
- `status` (`draft|active|suspended|archived`), `hasBlockingIssues` (bool)
- `tags`, `language` (ISO 639-1)
- `euResident` (bool — по `nationality`/`nationalities` пересечению с EU)
- `adrRequired` (bool)
- `documentType`, `documentState` (`pending_approval|valid|expired|rejected` — действует только с `documentType`)
- `expiringWithinDays` (int≥0)
- `sort` (`driverNumber|lastName|status|nextExpiryOn|createdAt`), `order` (`asc|desc`)
- `include` (`documents,assignments,notes`)

**200 OK (фрагмент)** — см. пример в VALIDATION

## GET `/drivers/{id}`
- `id`: ULID; `include` как выше
- Возвращает полную карточку с учетом RBAC/масок

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

**Design notes**

* Пороги и включённость нотификаций настраиваются per-type и влияют на признак `expiring`, но не на фильтр `expiringWithinDays` (он использует фактические даты)

---
