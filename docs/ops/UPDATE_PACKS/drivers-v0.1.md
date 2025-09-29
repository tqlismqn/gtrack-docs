# Update Pack — Drivers Module v0.1

## Изменения

- Добавлены страницы спецификаций драйвер-модуля:
  - `DATA_MODEL`
  - `API`
  - `VALIDATION`
  - `RBAC`
  - `OPEN_QUESTIONS_AND_ASSUMPTIONS`

## Влияние

- Реализация API чтения: `GET /drivers`, `GET /drivers/{id}`.
- Подготовка импорт/экспорт шаблонов (Шаг 8) — подлежит реализации в приложении.
- Роли и маскирование — требуются в бэкенде/фронтенде для корректной видимости.

## Тесты/проверки

- `mkdocs build --strict` должен проходить.
- Проверить внутренние ссылки и таблицы.

## Post-merge действия

- Проставить git-тег: `docs-v2.9.0` (или актуальную версию).
- Актуализировать настройки политики нотификаций per-тип в админке.

---

**Примечание о Billing/Trial (Phase B, черновик)**

- Отдельная страница: `docs/spec/billing/PHASE_B.md` (создать в следующем PR).
- Содержит модели `Plan`, `TenantBilling`, `Invoice`; API `/api/billing/v0`; статусы `trial|active|past_due|cancelled`; webhook для Stripe/Chargebee.
