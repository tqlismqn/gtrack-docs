# G-Track — Обзор

Добро пожаловать в портал документации **G-Track**: https://docs.g-track.eu

## Что внутри
- **Решения (ADR):** ключевые архитектурные решения и их последствия.
- **Спецификации:** API, модель данных и UX (карточка водителя).
- **Операции (Ops):** переменные окружения, CI/CD, деплой, домены и правила репозиториев.
- **Импорт из код-репозиториев:** разделы с /docs из `gtrack-app` и `gtrack-backend`.

## Текущее состояние (сентябрь 2025)
- Фронтенд (Next.js, Vercel): страница `/drivers` рендерит список (2 мок-водителя).
- Бэкенд (Fastify, Railway): `GET /health`, `GET /drivers`, CORS по `ALLOWED_ORIGINS`.
- Док-портал (MkDocs Material): GitHub Pages + домен `docs.g-track.eu`.
- Автосинк `/docs` из app/backend → `import/<repo>/` с авто-PR в `gtrack-docs`.

## Быстрый старт локально
```bash
python -m venv .venv
source ./.venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve  # http://127.0.0.1:8000
