# Deployment Profiles (v2.9.0)

## Laravel Cloud (primary)
- Managed-хостинг под Laravel: проекты/окружения, переменные, SSL, домены, DB/Cache.
- Deploy: push/CI → Cloud; миграции — через CI.
- Подключение PostgreSQL 16: через панель, ENV — как в ENV Matrix.

## Railway (fallback)
- Buildpacks/Nixpacks (PHP 8.2), ENV по матрице.
- Health: `/health`.
- CORS/COOKIE домены — как в ENV Matrix.

## Домены
- api.g-track.eu → backend
- app.g-track.eu → frontend
