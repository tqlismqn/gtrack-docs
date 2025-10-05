# SOP — Документация и версионирование
> **Назначение:** единые правила, чтобы **каждый PR/коммит** сопровождался актуализацией документации и версионированием портала `gtrack-docs`. Документ лежит в `docs/ops/DOCUMENTATION_SOP.md` и включён в навигацию «Операции».

## TL;DR
- Любая задача → вместе с кодом **обновляем документацию**.
- Изменения в **app/backend**: кладём текст в `/docs` соответствующего репо → это **автосинкнется** в `gtrack-docs/docs/import/...`.
- Общие спецификации/ADR/ops: правки делаем **в `gtrack-docs/docs/**`.
- Существенные апдейты портала — **версионируем**: обновляем `CHANGELOG.md`, создаём страницу в `ops/UPDATE_PACKS/`, ставим git-тег `docs-vX.Y.Z`.
- PR не проходит ревью без отмеченного блока «Docs updated».

## 1) Где живут документы
- **Центральные доки**: `gtrack-docs/docs/**`
  - ADR: `docs/adr/*`
  - Спеки: `docs/spec/*` (API, Data Model, UX)
  - Операции: `docs/ops/*` (ENV, CI/CD, домены, SOP)
  - Архив обновлений: `docs/ops/UPDATE_PACKS/*`
- **Локальные доки кода** (автосинк):
  - `gtrack-frontend/docs/**` → `gtrack-docs/docs/import/gtrack-frontend/**`
  - `gtrack-backend/docs/**` → `gtrack-docs/docs/import/gtrack-backend/**`

## 2) Когда обновлять
Обновлять **всегда**, если меняется:
- API/схемы/модель данных; UI/UX; ENV/CI/CD/домены; ADR; правила импорта Excel.
Идеально — в **том же PR**, что и код; иначе — отдельный PR в `gtrack-docs`.

## 3) Что обновлять (чек-лист)
- API → `docs/spec/API.md`
- Data Model → `docs/spec/DATA_MODEL.md`
- UX → `docs/spec/UX/*`
- Ops → `docs/ops/ENV_MATRIX.md`, `CI_CD.md`, `DEPLOYMENT.md`, `DOMAINS_DNS.md`, `REPO_GOVERNANCE.md`
- Архитектура → `docs/adr/ADR-XXXX-*.md`
- Локальные заметки разработки → `/docs` в соответствующем код-репо

## 4) Версионирование портала
- Семантическая версия `X.Y.Z` для `gtrack-docs`:
  - **Major** — несовместимые изменения в спеках/архитектуре
  - **Minor** — новые разделы без ломания контрактов
  - **Patch** — правки/уточнения
- Процедура:
  1) Обновить `docs/CHANGELOG.md` — `## X.Y.Z — YYYY-MM-DD`
  2) Создать страницу `docs/ops/UPDATE_PACKS/YYYY-MM-DD-docs-update-pack-vX.Y.Z.md`
  3) После merge: git-тег `docs-vX.Y.Z`
  4) Проверить деплой Pages
- (Опц.) В `mkdocs.yml`:
  ```yaml
  extra:
    version: X.Y.Z
```

и вывести её в `docs/index.md` («Версия портала: {{ config.extra.version }}»)

## 5) Definition of Done для PR

* [ ] Обновлены соответствующие разделы доков (см. §3)
* [ ] Обновлены локальные доки `/docs` в code-репо (если нужно)
* [ ] `mkdocs build --strict` зелёный (Docs-Preview)
* [ ] Для крупных апдейтов: обновлён CHANGELOG + добавлен Update Pack
* [ ] В описании PR — ссылки на изменённые страницы портала

## 6) Блок для промптов Codex (вставлять в каждую задачу)

```
[Docs — MUST UPDATE]
- If API/UX/DataModel changed: update gtrack-docs/docs/spec/* accordingly.
- If ops/ci/env changed: update gtrack-docs/docs/ops/*.
- Update or create ADR in gtrack-docs/docs/adr/* if architectural decision made.
- For local developer notes/examples: update /docs in this repository; do not touch README.md (guarded).
- Ensure mkdocs nav remains consistent (no missing pages) and “Docs - Preview” is green.
```

## 7) E2E-пример

Изменили поле в `Driver`:

1. backend PR — схема/ответ `/drivers` → обновить `gtrack-backend/docs/*`
2. frontend PR — UI → обновить `gtrack-frontend/docs/*`
3. docs PR — обновить `spec/DATA_MODEL.md`, `spec/API.md`, (при необходимости) `spec/UX/*`
4. Merge code-PR → автосинк создаст PR в `gtrack-docs/import/*` → смержить
5. В `gtrack-docs`: обновить `CHANGELOG.md`, добавить Update Pack, поставить тег

## 8) Быстрые команды

* `mkdocs build --strict` / `mkdocs serve`
* Переиздать деплой: пустой коммит в `main`
* Тег:

```bash
git tag -a docs-vX.Y.Z -m "docs: release X.Y.Z"
git push origin docs-vX.Y.Z
```

## 9) Ссылки

* Портал: [https://docs.g-track.eu](https://docs.g-track.eu)
* MkDocs/Material: [https://www.mkdocs.org](https://www.mkdocs.org) / [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
* GitHub Pages + Actions: [https://docs.github.com/pages](https://docs.github.com/pages)
