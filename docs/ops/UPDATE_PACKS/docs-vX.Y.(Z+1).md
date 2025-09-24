# Update Pack — docs-vX.Y.(Z+1)

## Что изменилось

* Подключён ReDoc через **CDN-встраивание** (без Python-плагинов).
* Добавлены страницы: Specs → Обзор, Specs → **API v0 (ReDoc)**, Specs → **API v1 (ReDoc, DRAFT)**.
* Зафиксированы версии инструментов: `mkdocs==1.5.3`, `mkdocs-material==9.5.17`.

## Как обновиться

* Сборка:

  ```bash
  python -m pip install -r requirements.txt
  mkdocs build --strict
  ```
* API не менялось; это инфраструктурные улучшения документации.

## Проверка

* `mkdocs build --strict` проходит без ошибок.
