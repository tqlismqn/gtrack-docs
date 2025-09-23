# Update Pack — docs-v0.3.2

## Что изменилось
- Подключён **ReDoc** в MkDocs (рендер OpenAPI).
- Добавлена страница **Specs → API v0 (ReDoc)**.
- Добавлена посадочная **Specs → Обзор** и runbook по обновлению спек.

## Как обновиться
- Ничего не требуется: API не менялось, только способ рендера.
- Для будущих версий добавляйте `docs/spec/api/gtrack-v1.yaml` и страницу `docs/spec/redoc/v1.md`.

## Проверка
- `mkdocs build --strict` — успешно.
