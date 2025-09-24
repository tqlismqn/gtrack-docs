# Update Pack — docs-vX.Y.(Z+1)

## Что изменилось
- ReDoc теперь использует абсолютные URL к YAML (устранён 404).
- Перезаписан `spec/api/gtrack-v0.yaml`:
  - UTF-8, без повреждённых символов.
  - Схемы и поля приведены в соответствие с backend v0 (firstName/lastName/status и т.д.).

## Как проверить
- Открыть Specs → **API v0 (ReDoc)** — страница рендерится, без ошибки 404.
- Прямая ссылка на YAML: `/spec/api/gtrack-v0.yaml` — отдаёт файл.
- MkDocs build: `mkdocs build --strict` — зелёный.

## Примечания
- Любые будущие изменения API сопровождать обновлением OpenAPI YAML + Update Pack.
