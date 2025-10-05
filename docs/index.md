# G-Track — Обзор

Добро пожаловать в портал документации **G-Track**: https://docs.g-track.eu

## Что внутри
- **Решения (ADR):** ключевые архитектурные решения и их последствия.
- **Спецификации:** API, модель данных и UX (карточка водителя).
- **Операции (Ops):** переменные окружения, CI/CD, деплой, домены и правила репозиториев.
- **Импорт из код-репозиториев:** README фронтенда `gtrack-frontend` и бэкенда `gtrack-backend` (актуальный стек + архив).

## Текущее состояние (октябрь 2025)
- Фронтенд — Angular 17 на **Vercel**, сборка `dist/gtrack-frontend`, demo-режим доступен из `/dashboard`.
- Бэкенд — Laravel 10 на **Laravel Cloud** (PHP 8.3, PostgreSQL 16 serverless) с Nightwatch мониторингом.
- Док-портал — MkDocs Material (GitHub Pages) с автосинком README через GitHub Actions.

## Быстрый старт локально
```bash
python -m venv .venv
source ./.venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve  # http://127.0.0.1:8000
```
