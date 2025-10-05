# G-Track — Восстановление проекта и перенос инфраструктуры (Update Pack)

**Дата:** 2025-10-05  
**Ответственный:** Thomas Gradinar  
**Репозитории:**  
- Frontend: `tqlismqn/gtrack-frontend`  
- Backend: `tqlismqn/gtrack-backend`  
- Docs: `tqlismqn/gtrack-docs`

---

## Резюме

- Перенесли исходные проекты подрядчика в наши репозитории с сохранением истории коммитов и тегов.
- Отключили устаревшие SSH/rsync-workflow и переместили их в `.github/workflows_disabled/` с README-комментарием.
- Подняли backend на **Laravel Cloud** (PHP 8.3, PostgreSQL 16 Serverless), применили миграции и включили Nightwatch мониторинг.
- Подняли frontend на **Vercel** (Node 20.x, Angular 17), настроили сборку на `dist/gtrack-frontend` и добавили `vercel.json` для SPA-роутинга.
- Для демо-сценария временно включили `authBypass`/`menuBypass` и стартовый маршрут `/dashboard` без Auth0 редиректа.
- Обновили документацию: импортировали README фронта/бэка в `docs/import/…` и зафиксировали инфраструктурные изменения в этом пакете.

---

## Детали переноса репозиториев

**Метод:** локальный клон подрядчика → `git push --all` + `git push --tags` в наши пустые репозитории (при необходимости — `--force` после временного снятия branch protection`).  
**Что сделали:**
1. `gtrack-frontend` и `gtrack-backend` наполнили из исходников подрядчика.
2. После переноса вернули правила защиты веток на `main`.
3. Архивировали все устаревшие деплой-workflow в `.github/workflows_disabled/` и добавили пояснение.

---

## Новая инфраструктура и стек

### Backend — Laravel Cloud
- **Laravel:** 10.x  
- **PHP:** 8.3  
- **DB:** PostgreSQL 16 (Serverless)  
- **ENV (без секретов):** `APP_ENV=production|staging`, `APP_URL=<cloud-domain>`, `DB_*` (из Connection Info), `SANCTUM_STATEFUL_DOMAINS`, `SESSION_DOMAIN`.  
- **Nightwatch:** установлен `laravel/nightwatch`, мониторинг включён.  
- **Команды после деплоя:** `php artisan migrate --force`, `php artisan storage:link`, `php artisan config:cache`, `php artisan route:cache`.

### Frontend — Vercel
- **Angular:** 17  
- **Node:** 20.x  
- **Output Directory:** `dist/gtrack-frontend`  
- **ENV:** `API_BASE_URL=<laravel-cloud-domain>`  
- **SPA-роутинг:** `vercel.json` с rewrites на `/index.html`.

---

## Временный демо-режим (без Auth0)

- `src/environments/environment*.ts`:
  ```ts
  authBypass: true,
  menuBypass: true
  ```
- `app.routes.ts`: дефолтный маршрут установлен на `/dashboard`.
- В README добавлена сноска о временном обходе Auth0 для демонстрации.

---

## Что дальше

- Подготовить план обратного включения Auth0 после демо.
- Оформить ADR по переходу на новую инфраструктуру.
- Настроить автоматический синк README из новых репозиториев.
