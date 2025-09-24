# Offline PyPI для документации (wheelhouse)

## Зачем
CI/окружения иногда блокируют PyPI/CDN. Чтобы сборка доков не падала, зависимости ставим офлайн из `docs/vendor/wheels/`.

## Как работает
- Декларации: `docs/requirements.in`
- Лок: `docs/requirements.lock.txt` (с hash)
- Колёса: `docs/vendor/wheels/`
- В CI: `pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt`

## Обновление зависимостей
Запусти workflow **Docs - Refresh Wheels** (ручной/по расписанию) — он:
1) пересоберёт lock с hash,
2) скачает колёса в `docs/vendor/wheels/`,
3) проверит офлайн-установку и `mkdocs build --strict`,
4) создаст PR.

## Локально
```bash
python -m venv .venv && source .venv/bin/activate
pip install --no-index --find-links=docs/vendor/wheels -r docs/requirements.lock.txt
python -m mkdocs serve
```

Политика
- Любое изменение mkdocs.yml/плагинов → запуск Docs - Refresh Wheels.
- В PR — блок “Docs updated”.
