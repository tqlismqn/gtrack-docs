# G-Track Backend — актуальное состояние (обновлено 2025-10-05)

**Laravel:** 10.x (framework обновлён до актуальных security-патчей)
**PHP runtime:** 8.3 (Laravel Cloud)
**База данных:** PostgreSQL 16 (Serverless, управляется Laravel Cloud)
**Хостинг:** Laravel Cloud (production/staging), fallback отсутствует
**Мониторинг:** Nightwatch + GitHub Actions health checks

## Ключевые обновления 2025
- Репозиторий переехал в [`tqlismqn/gtrack-backend`](https://github.com/tqlismqn/gtrack-backend).
- Развернут Laravel Cloud с автоматическими деплоями и миграциями (`php artisan migrate --force`).
- В `.env` стандартизированы переменные: `APP_URL`, блок `DB_*`, `SANCTUM_STATEFUL_DOMAINS`, `SESSION_DOMAIN`, `FRONTEND_URL`.
- Конфигурированы CORS для доменов `*.vercel.app` и production хоста G-Track.
- Добавлены post-deploy команды: `config:cache`, `route:cache`, `view:cache`, `event:cache`.

## Как синхронизировать README
1. Клонируйте backend: `git clone https://github.com/tqlismqn/gtrack-backend.git`.
2. Скопируйте свежий `README.md` в `docs/import/gtrack-backend/README.legacy.md`.
3. Обновите сводку выше, если поменялись версии PHP/Laravel или процедуры деплоя.
4. Запустите `mkdocs build --strict` и создайте PR `docs: sync backend readme`.

---

## Legacy README (архив)
> Историческая копия README из `gtrack-backend` хранится ниже.

```markdown
# G-Track Backend — README Snapshot

Здесь размещена копия `README.md` из репозитория [tqlismqn/gtrack-backend](https://github.com/tqlismqn/gtrack-backend).

## Содержание оригинального README
- требования к окружению (PHP 8.3, Composer, Laravel Sail/Artisan);
- пошаговый запуск API локально и в Docker;
- описание пайплайнов Laravel Cloud и Nightwatch мониторинга;
- таблица ENV-переменных и их источников.

## Инструкция по синхронизации
1. Клонируйте репозиторий backend: `git clone https://github.com/tqlismqn/gtrack-backend.git`.
2. Скопируйте `README.md` в `docs/import/gtrack-backend/README.legacy.md`.
3. Убедитесь, что `mkdocs build --strict` завершается успешно.
4. Откройте PR с заголовком `docs: sync backend readme` в `gtrack-docs`.

> ℹ️ После каждого релиза backend обновляйте данный snapshot, чтобы документация и кодовая база оставались согласованными.
```
