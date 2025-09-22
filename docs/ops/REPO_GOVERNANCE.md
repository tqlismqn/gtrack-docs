# Repo Governance

## Ветвление

* Ветка задачи: `codex/<task>-<yyyymmddHHMM>` от HEAD `origin/main`
* После merge — удалять ветку (включено auto-delete)

## Политики

* Нельзя править README в код-репо (guard-readme)
* PR «чистый»: только файлы из Allowed paths

## PR SOP

1. Новая ветка от актуального main
2. Маленький дифф
3. Checks зелёные → Squash & Merge → Delete branch
4. Конфликт? Закрыть PR, пересоздать от HEAD main
