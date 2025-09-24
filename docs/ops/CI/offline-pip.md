# Offline PyPI + автонавигация для `import/`

## Зачем
PyPI/CDN могут быть заблокированы. Мы ставим зависимости **офлайн** из `docs/vendor/wheels/`, а раздел `import/` автоматически попадает в меню.

## Как работает
- `docs/requirements.in` → `docs/requirements.lock.txt` (точные версии с hashes)
- Колёса: `docs/vendor/wheels/*.whl` (+ bootstrap-инструменты `setuptools`, `wheel`)
- В CI: `pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt`
- `mkdocs-awesome-pages-plugin==2.9.2` гарантирует корректную автонавигацию
- Workflow проверяет, что плагины реально ставятся (self-check после `pip install`)
- Навигацию для `docs/import/**` строит **awesome-pages** (файл `.pages` управляет заголовком/сортировкой).

## Обновление зависимостей
Запускайте **Docs - Refresh Wheels** (ручной/ежемесячный). Он пересобирает lock, скачивает колёса, валидирует офлайн-сборку и открывает PR.

## Локально
```bash
python -m venv .venv && source .venv/bin/activate
pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt
python -m mkdocs serve
```

## Примечание по `import/`

Новые файлы в `docs/import/` автоматически появятся в меню без правки `mkdocs.yml`. Для тонкой настройки структуры используйте `docs/import/.pages`.
