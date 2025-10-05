# G-Track Frontend — актуальное состояние (обновлено 2025-10-05)

**Фреймворк:** Angular 17 (Standalone, Angular CLI)
**Node.js (Vercel runtime):** 20.x
**Сборка:** `dist/gtrack-frontend`
**Хостинг:** Vercel (SPA с `vercel.json`)
**API:** Laravel Cloud (`API_BASE_URL` в `.env`, fallback на staging backend)

## Ключевые обновления 2025
- Репозиторий переименован в [`tqlismqn/gtrack-frontend`](https://github.com/tqlismqn/gtrack-frontend).
- Удалены устаревшие SSH/rsync воркфлоу; деплой управляется Vercel через Production/Preview environments.
- Добавлен demo-режим для презентаций: флаги `authBypass` и `menuBypass` в `environment*.ts`, стартовый маршрут `/dashboard`.
- CI/CD закреплён на `npm ci` → `npm run build`; превью проверяется пайплайном `build` + `lint` + `check-docs`.
- API-коммуникация через `API_BASE_URL`; CORS у backend настроен на `https://*.vercel.app` и основной домен.

## Как синхронизировать README
1. Склонируйте фронтенд-репозиторий: `git clone https://github.com/tqlismqn/gtrack-frontend.git`.
2. Скопируйте актуальный `README.md` в `docs/import/gtrack-frontend/README.legacy.md` (этот файл хранит исходник).
3. При необходимости обновите верхний блок выше (стек, ключевые изменения, пайплайны).
4. Выполните `mkdocs build --strict` и откройте PR `docs: sync frontend readme`.

---

## Legacy README (архив)
> Ниже хранится последняя сохранённая копия из репозитория `gtrack-frontend`.

```markdown
# G-Track Frontend — README Snapshot

Этот раздел хранит актуальную копию `README.md` из репозитория [tqlismqn/gtrack-frontend](https://github.com/tqlismqn/gtrack-frontend).

## Что внутри оригинального README
- требования окружения (Node 20.x, Angular CLI 17);
- инструкции по локальному запуску и тестированию;
- описание CI-пайплайнов и переменных окружения для Vercel;
- чек-лист деплоя и гайд по подключению к backend-API.

## Как обновлять snapshot
1. Склонируйте репозиторий фронтенда: `git clone https://github.com/tqlismqn/gtrack-frontend.git`.
2. Скопируйте файл `README.md` в `docs/import/gtrack-frontend/README.legacy.md`.
3. Проверьте `mkdocs build --strict`.
4. Создайте PR в `gtrack-docs` с пометкой `docs: sync frontend readme`.

> ℹ️ Если README фронтенда обновился, синхронизируйте данный snapshot, чтобы документация оставалась в едином источнике правды.
```
