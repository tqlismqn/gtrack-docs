# G-Track — Модуль «Водители»: Спецификация для разработчиков (Dev Spec v1.5)

Дата: 2025-10-03

## 1) Архитектура/окружения
Frontend: Next.js (Vercel) · Backend: Fastify (Railway) · DB: PostgreSQL · Docs: MkDocs (GitHub Pages).
ENV: NEXT_PUBLIC_API_URL; PORT; ALLOWED_ORIGINS.

## 2) API (REST v1.5)
Базовый URL: /api · JWT · RFC7807.
Drivers: GET /drivers (search/status/docStatus/euOnly/limit/offset) → {items,total}; GET /drivers/{id}; POST /drivers; PATCH /drivers/{id}.
Documents: GET /drivers/{id}/documents; POST /drivers/{id}/documents; POST /drivers/{id}/documents/{docId}/files.
Comments: GET/POST /drivers/{id}/comments (1 вложение опц.).
Reminders: POST /reminders/preview; POST /reminders/send.
Meta: GET /lookups (страны, типы документов, статусы, адреса Praha/Kladno, категории прав).

## 3) JSON Schemas (фрагменты)
— driver.read.v1 (id, internal_number, full_name, names, birth_date, citizenship, rodne_cislo?, email/phone, адреса, status, hire/fire, contract, work_location, bank, flags, doc_summary)
— driver.document.v1 (type: passport|visa_or_residence|driver_license|tachograph_card|code95|adr_certificate|medical_check|psychotest|insurance|travel_insurance|a1|a1_switzerland|declaration; number/country/from/to/categories/files)
— driver.file.v1 (id, filename, size, mime, hash, uploaded_at, uploaded_by)

## 4) БД (PostgreSQL v1.5)
Таблицы: drivers, driver_documents, driver_files, driver_comments, per_diems, audit_log. Индексы по status/citizenship/doc(to)/fts(full_name,email,phone). Ограничения: банк-правила, даты, RČ-условия, психотест age-rule.

## 5) RBAC
Admin=Full; HR=CRUD/Upload/Reminders; Dispatcher=Read/Upload/Comments; Accounting=Read/Salary CRUD; Driver=Self.

## 6) Агенты
Notification Agent (cron 03:00 UTC, локали, каналы); Excel Import Agent (dry-run, отчёт CSV/HTML); Telegram Mini App (WebApp, статусы, upload).

## 7) Ошибки
400/validation_error; 401/403; 404/409; 413/415; 429; 500 — в формате Problem+JSON.

## 8) CI/CD и доки
Backend: npm ci && npm start + curl $PORT/health; checks: build/lint/check-docs/guard-readme/fresh-branch/branch-name.
Frontend: npm ci && npm run build && npm run start (Vercel preview). Docs: mkdocs build --strict; Pages deploy.
Автосинк /docs из app/backend в gtrack-docs/import/...; версионирование портала: docs-vX.Y.Z + CHANGELOG + Update Pack.

## 9) Roadmap
Auth (OIDC Google/MS, httpOnly-сессии); Импорт v1.1 (улучшенный парсер ФИО, справочники стран, кат. прав); Уведомления v1.1 (групповые дайджесты, пороги per-tenant в UI); Link-checker для док-портала.

## 10) DoD по задачам модуля
Обновлены /docs в код-репо и центральные доки (gtrack-docs); CI зелёный; ветка codex/<task>-<yyyymmddHHMM>; Squash & Merge; навигация MkDocs консистентна; CHANGELOG/Update Pack при изменениях.
