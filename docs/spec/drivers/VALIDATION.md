# Модуль «Водители (Driver)» — Валидация v0.1

## Общие принципы

- Форматы дат: ISO в API; UI/импорт `DD.MM.YYYY` / `DD.MM.YYYY HH:mm`.
- Уникальность в пределах арендатора: `driverNumber`, `code` (если задан).

## Driver — ключевые правила

- `driverNumber`: `^DRV\d{6}$` (генерируется системой).
- `code`: `^[A-Z0-9][A-Z0-9_-]{1,31}$`; уникален, если указан.
- `dateOfBirth`: обязательна, возраст ≥ 18 лет.
- Контакты: `emails[]`, `phones[]` ≤ 3; максимум один `isPrimary=true` в каждом списке.
- Банкинг: наборы полей для CZ vs non-CZ взаимоисключающие.
- Employment: если `payrollEnabled=true` → обязательный блок `payrollSettings`.

## Documents — общие правила

- `type` из разрешенного списка; `state` из `pending_approval|valid|expired|rejected`.
- `expiryDate ≥ issueDate` (если обе даты заданы).
- Типоспецифичные правила — см. таблицу в `DATA_MODEL.md` (повтор: `passport`, `driver_license`, ...).
- `source = driver_bot` не может переводить `state` в `valid`.

## Attachment

- MIME из белого списка.
- Размер ≤ 15 MB.

## Кросс-проверки

- EU/non-EU + валидный `visa_work_permit` → влияет на `Compliance`.
- При `suspended` запрет на новые `Assignment` (кроме override).

## Ошибки — примеры

- `PLAN_LIMIT_EXCEEDED`, `FORBIDDEN_FEATURE` — зарезервированы для Billing (Phase B).
- См. раздел примеров (JSON-фрагменты) в шаге 6 спецификации.
