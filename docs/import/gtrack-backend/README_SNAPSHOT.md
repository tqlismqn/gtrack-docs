# G-Track Backend — README Snapshot

Здесь размещена копия `README.md` из репозитория [tqlismqn/gtrack-backend](https://github.com/tqlismqn/gtrack-backend).

## Содержание оригинального README
- требования к окружению (PHP 8.3, Composer, Laravel Sail/Artisan);
- пошаговый запуск API локально и в Docker;
- описание пайплайнов Laravel Cloud и Nightwatch мониторинга;
- таблица ENV-переменных и их источников.

## Инструкция по синхронизации
1. Клонируйте репозиторий backend: `git clone https://github.com/tqlismqn/gtrack-backend.git`.
2. Скопируйте `README.md` в `docs/import/gtrack-backend/README_SNAPSHOT.md`.
3. Убедитесь, что `mkdocs build --strict` завершается успешно.
4. Откройте PR с заголовком `docs: sync backend readme` в `gtrack-docs`.

> ℹ️ После каждого релиза backend обновляйте данный snapshot, чтобы документация и кодовая база оставались согласованными.
