### `docs/adr/ADR-0001-app-shell-first.md`
```markdown
# ADR-0001: App Shell First
**Status:** accepted  
**Date:** 2025-09-21

## Context
Нужно быстро показать работающий каркас, параллельно выстраивая CI/CD и доки.

## Decision
Сначала собираем **App Shell** (роутинг, навигация, страницы, деплой), затем наращиваем модули: Drivers, Import, Auth и т.д.

## Consequences
+ Быстрый E2E-цикл (UI ↔ API ↔ Docs)  
+ Итеративные поставки без «больших взрывов»  
− Требуется дисциплина PR/CI, чтобы не копить долг
