# G-Track Docs (MkDocs + GitHub Pages)

Документация проекта G-Track. Портал опубликован на **https://docs.g-track.eu** (GitHub Pages).

## Что внутри
- **MkDocs** с темой **Material**
- Автодеплой на GitHub Pages:
  - `Docs - Preview` (PR) — сборка в strict-режиме
  - `Docs - Deploy` (push в `main`) — публикация на Pages
- Кастомный домен и каноникал:
  - `docs/CNAME` → `docs.g-track.eu`
  - `site_url` в `mkdocs.yml` → `https://docs.g-track.eu/`

## Локальный запуск
```bash
python -m venv .venv
source ./.venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
# открой http://127.0.0.1:8000
```
> Убедитесь, что в requirements.txt нет CLI-флагов pip (они относятся к pip.conf/командной строке).
