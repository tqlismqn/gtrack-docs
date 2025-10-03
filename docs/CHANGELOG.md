# Документация — Changelog

## docs-v2.9.0 — 2025-10-03
- ADR-STACK-0001: переход на Angular 17 + Laravel 10 + PostgreSQL 16
- Обновлены SPEC: DATA_MODEL, API, UX
- Обновлены OPS: ENV_MATRIX, CI_CD, DEPLOYMENT, DOMAINS_DNS
- Добавлены домены api.g-track.eu и app.g-track.eu

## docs-v2.8.3 — Enforce offline install + awesome-pages check
- CI: офлайн только по lock + wheelhouse (запрет на install из .in)
- Wheelhouse включает setuptools/wheel для сборки sdist офлайн
- Пин mkdocs-awesome-pages-plugin==2.9.2 и self-check импорта
- Автонавигация для docs/import/**

## docs-v2.8.2 — Offline PyPI + Auto-Nav for /import
- CI: офлайн-установка зависимостей из `docs/vendor/wheels`
- Новый чек `check-docs` с выводом версий плагинов
- Автонавигация для `docs/import/**` (awesome-pages + .pages)
- Добавлена страница `ops/CI/offline-pip.md`, обновлён `mkdocs.yml`

## docs-v2.8.1 — Offline PyPI for Docs (wheelhouse)
- CI: офлайн-установка зависимостей из `docs/vendor/wheels`
- Новый workflow `Docs - Refresh Wheels` (ручной + ежемесячный)
- Переименован required check в `check-docs`
- Добавлена страница: `ops/CI/offline-pip.md`

## 0.3.0 — 2025-09-23

* Security Pack для модуля «Водители»: ADR, спецификации, операционные инструкции.
* Обновлена навигация MkDocs и добавлен Update Pack v0.3.0.
