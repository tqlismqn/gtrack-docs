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
