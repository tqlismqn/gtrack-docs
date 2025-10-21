# DEV NOTES (v2 bootstrap)
- Workflow contexts reset to gtrack-ci-v2 and gtrack-policy-v2 only.
- Adapter branch-name policy allows codex/<task> or codex/<task>-<yyyymmddHHMM> during bootstrap.

## Vercel (bootstrap)
- Используем `vercel.json` с `"framework": null` и `npm run build`.
- Сборка создаёт минимальный `dist/index.html`, чтобы превью было зелёным до Angular v2 скелета.

## Sync probe (202510192224)
- Minor touch to trigger portal auto-sync & automerge.

## Sync probe (20251020091913)
- Autosync+automerge drill from gtrack-app.
- Docs updated
  - Compliance fix: added required block to satisfy guard-readme check.

## Sync probe (20251020145107)
- Backend: push-to-main triggers repository_dispatch to portal.

## Sync probe (20251021071808)
- Touch from reset workflow to exercise autosync.

## PR body policy quick-reference (20251021)
- Каждое открытие PR проверяется guard, что тело начинается с блока "Docs updated".
- Шаблон лежит в `.github/PULL_REQUEST_TEMPLATE.md` и должен использоваться без сокращений.
- Если нет изменений в `/docs/**`, опиши причину прямо в этом блоке.
