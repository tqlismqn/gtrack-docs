# Offline PyPI для документации (wheelhouse)

## Зачем
CI/окружения иногда блокируют доступ к PyPI/CDN. Чтобы сборка docs не падала, мы ставим зависимости офлайн из `docs/vendor/wheels/`.

## Как это работает
- Зависимости описаны в `docs/requirements.in` (диапазоны).
- Лок-файл `docs/requirements.lock.txt` фиксирует точные версии + хэши.
- Колёса для всех зависимостей лежат в `docs/vendor/wheels/`.
- В CI используем `pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt`.

## Обновление зависимостей
1. Запусти workflow **Docs - Refresh Wheels** вручную в GitHub Actions.
2. Он:
   - пересоберёт lock,
   - скачает колёса (`*.whl`) только в виде бинарников,
   - проверит офлайн-установку и `mkdocs build --strict`,
   - откроет PR с обновлениями.
3. На ревью PR убедись, что `mkdocs build --strict` зелёный.

## Локальная разработка
```bash
python -m venv .venv && source .venv/bin/activate
pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt
mkdocs serve
```

## Политика

* Любое изменение `mkdocs.yml` / плагинов → запускаем **Docs - Refresh Wheels**.
* В PR обязательно блок *"Docs updated"*.
