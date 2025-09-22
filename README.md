# G-Track Docs (MkDocs + GitHub Pages)

Единый портал документации проекта G-Track: **https://docs.g-track.eu**.

## Что внутри
- Архитектура и решения (ADR)
- Спецификации API и UX
- Операции: ENV, CI/CD, домены, правила репозиториев
- Импортируемые доки из кодовых репозиториев (`import/gtrack-app`, `import/gtrack-backend`)

## Локальный запуск
```bash
python -m venv .venv
source ./.venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve   # http://127.0.0.1:8000
```
