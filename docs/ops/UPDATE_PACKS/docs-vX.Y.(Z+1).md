# Update Pack — docs-vX.Y.(Z+1)

## Что изменилось
- Перевели ReDoc на CDN-встраивание (без `mkdocs-redoc-plugin`), чтобы сборка не зависела от доступа к PyPI.
- Страницы: `Specs → API v0 (ReDoc)`, `Specs → API v1 (ReDoc, DRAFT)` обновлены.
- Nav и ссылки сохранены.

## Как обновиться
- Ничего — API неизменён.
- Если позже вернёмся к плагину, просто добавьте его в `requirements.txt` и `plugins:` в `mkdocs.yml`.

## Проверка
- `mkdocs build --strict` — успешно.
