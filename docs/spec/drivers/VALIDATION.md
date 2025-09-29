# Модуль «Водители (Driver)» — Валидация v0.1

## Общие принципы

* ISO в API; UI/импорт `DD.MM.YYYY` / `DD.MM.YYYY HH:mm`
* Уникальность пер-тенант: `driverNumber`, `code` (если задан)

## Driver — ключевые правила

* `driverNumber`: `^DRV\d{6}$` (генерируется)
* `code`: `^[A-Z0-9][A-Z0-9_-]{1,31}$`; уникален, если указан
* DOB: `dateOfBirth` обяз., **возраст ≥ 18**
* Contacts: `emails[]`, `phones[]` ≤ 3; максимум один `isPrimary=true` в каждом списке
* Banking: CZ vs non-CZ наборы полей взаимоисключающие
* Employment: если `payrollEnabled=true` → обязателен блок `payrollSettings`

## Documents — общие

* `type` из списка; `state` из `pending_approval|valid|expired|rejected`
* `expiryDate >= issueDate` (если обе заданы)
* Типоспецифичные правила — см. таблицу в Data Model
* `source=driver_bot` не может переводить `state` в `valid`

## Attachment

* MIME из белого списка; size ≤ 15 MB

## Кросс-проверки

* EU/non-EU + `visa_work_permit` валидный → влияет на Compliance
* При `suspended` запрет на новые `Assignment` (кроме override)

## Ошибки — примеры

* `PLAN_LIMIT_EXCEEDED`, `FORBIDDEN_FEATURE` — зарезервированы для Billing (Phase B)
* См. JSON-фрагменты в соответствующих разделах API

---
