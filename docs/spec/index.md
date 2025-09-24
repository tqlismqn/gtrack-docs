# API Specifications (OpenAPI)

Здесь опубликованы спецификации API проекта **G-Track**. Рендер выполняется клиентским **ReDoc CDN** — сборка MkDocs не требует Python-плагинов.

## Текущие спецификации
- **API v0** — мок-сервис (без БД): `/health`, `/drivers`, `/drivers/{id}`. Рендер: _Specs → API v0 (ReDoc)_.

## Будущие спецификации
- **API v1 (DRAFT)** — заготовка для следующих релизов. Рендер: _Specs → API v1 (ReDoc, DRAFT)_.

---

## Как обновлять спеку (runbook)
1. Изменили поведение API в `gtrack-backend` → сначала обновите **OpenAPI YAML** в `gtrack-docs/spec/api/…`.
2. Минорные правки v0 вносим в `docs/spec/api/gtrack-v0.yaml` + при необходимости обновляем страницы `docs/api/v0/*`.
3. Несовместимые изменения → новый файл `docs/spec/api/gtrack-v1.yaml` (или следующая версия) и страница `docs/spec/redoc/v1.md`.
4. Всегда делайте **Update Pack** и **CHANGELOG** (patch-bump).
5. Проверка локально/в CI: 
   ```bash
   python -m pip install -r requirements.txt
   mkdocs build --strict
````
