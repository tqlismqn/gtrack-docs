# Модуль «Водители (Driver)» — Валидация v0.1

## Общие принципы

* ISO в API; UI/импорт: `DD.MM.YYYY` / `DD.MM.YYYY HH:mm`
* Уникальность в тенанте: `driverNumber`, `code` (если задан)

## Driver

* `driverNumber`: `^DRV\d{6}$`
* `code`: `^[A-Z0-9][A-Z0-9_-]{1,31}$`
* `dateOfBirth`: обяз., возраст ≥ 18
* Contacts: e-mail/телефон ≤ 3, максимум один primary
* Banking: CZ vs non-CZ — взаимоисключающие наборы
* Employment: если `payrollEnabled=true` → обязателен блок `payrollSettings`

## Document

* `type`: из списка; `state`: `pending_approval|valid|expired|rejected`
* `expiryDate >= issueDate` (если обе заданы)
* Типоспецифичные правила (см. Data Model 3.2)
* `source=driver_bot` не может выставить `state=valid`

## Attachment

* MIME: pdf/jpg/png/heic; size ≤ 15 MB

## Кросс-проверки

* EU/non-EU + `visa_work_permit`; `suspended` блокирует новые `Assignment` (кроме override)

## Примеры ошибок

* см. JSON-примеры из основного обсуждения (VALIDATION шага)
