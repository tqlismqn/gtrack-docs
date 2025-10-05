# Changelog

## docs-v2.9.2 — 2025-10-05
- Очистили `docs/import/` от legacy-подрядчиков (`app`, `backend`, `gtrack-app`).
- Добавили сводные README для `gtrack-frontend` и `gtrack-backend` с архивом legacy README.
- Обновили навигацию `mkdocs.yml`, индекс Import, SOP/CI/CD и корневой README под новые репозитории.
- Создали маркер `docs/_meta/redeploy.txt` для форс-ребилда портала.


Все заметные изменения в документации фиксируются в этом файле.

## docs-v2.9 — 2025-10-03
- Drivers: добавлены ТЗ v2.9 и Dev Spec v1.5, обновлена навигация и Update Pack.

### docs-v2.9.1 — Drivers: Audit & Notifications

* NEW: `spec/drivers/AUDIT_AND_NOTIFICATIONS.md` — модель аудита, каналы уведомлений, настройки, триггеры, weekly report.
* NAV: добавлена ссылка в раздел Drivers (.pages).
* PACK: обновлён Update Pack `drivers-v0.1`.

### **docs-v2.9.0** — Drivers Module v0.1

* NEW: `docs/spec/drivers/DATA_MODEL.md` — модель данных Driver/Document/Attachment/… (GDPR, retention, нотификации)
* NEW: `docs/spec/drivers/API.md` — REST v0: `GET /drivers`, `GET /drivers/{id}` (фильтры/сорт/пагинация/`include`)
* NEW: `docs/spec/drivers/VALIDATION.md` — правила валидации, примеры
* NEW: `docs/spec/drivers/RBAC.md` — роли, маскирование, AccessRequest
* NEW: `docs/spec/drivers/OPEN_QUESTIONS_AND_ASSUMPTIONS.md`

## docs-vX.Y.(Z+1) — <YYYY-MM-DD>
- UI: расширена ширина макета (1400px), ReDoc-страницы без правого TOC.
- Навигация: возвращены API v0 (Health, Водители); добавлен раздел Imported.

## docs-v2.9.0 — Drivers Module v0.1
* NEW: спецификации модуля водителей (Data Model, API v0, Validation, RBAC)
* NEW: Update Pack `drivers-v0.1`

## docs-vX.Y.(Z+1) — 2025-09-24
- Fix: ReDoc loads spec via absolute URL; v0 YAML replaced with clean, backend-aligned version (UTF-8).

## docs-vX.Y.(Z+1) — 2025-09-24

* Docs: ReDoc через CDN (без плагина); добавлены Specs-страницы для v0 и v1 (DRAFT).
* Toolchain pinned: `mkdocs==1.5.3`, `mkdocs-material==9.5.17`.

## docs-v0.3.1 — 2025-09-23
- Добавлены примечания по CI (npm install без lock; переход на npm ci при lock-файле).
- Уточнено: используется встроенный AJV Fastify; без `@fastify/ajv-compiler`.

## [0.0.1] - 2025-09-21
### Added
- Init docs structure: ADR, UX, API, OPS, импорт и README-навигация.

0.1.1 — 2025-09-22 — Added DOCUMENTATION_SOP and nav link.
