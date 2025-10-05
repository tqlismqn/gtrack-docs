# G-Track — Prompt Playbook (Codex + PR SOP)

Единый шаблон промптов для Codex и правила прохождения цикла **PROMPT → PR → Merge → Deploy**.  
Применимо для репозиториев: `gtrack-docs`, `gtrack-frontend`, `gtrack-backend`.

---

## 0) SOP: как правильно вести PR

1. **Новая ветка от HEAD `origin/main`**: `codex/<short-task>-<yyyymmddHHMM>`.  
2. **Минимальный дифф** — трогаем только явно разрешённые файлы.  
3. **Проверки зелёные** → **Squash & Merge** → **Delete branch**.  
4. **Никаких ручных конфликтов**. Если PR «красный»/конфликтный → закрыть и пересоздать от свежего `main`.  
5. README в код-репо не правим (только через `chore(readme):` и когда политика позволяет). Главные тексты — в `gtrack-docs`.

Required checks (по проекту):  
- `gtrack-docs`: **Docs - Preview** (PR), **Docs - Deploy** (main)  
- `gtrack-frontend` / `gtrack-backend`: **build**, **lint**, **check-docs**, **guard-readme**, **fresh-branch**, **branch-name**

---

## 1) Универсальный шаблон промпта (для любого репозитория)

```text
[Repo Hygiene — MUST FOLLOW]
- Create a NEW branch from HEAD of origin/main: codex/<short-task>-<yyyymmddHHMM>.
- Do NOT reuse older codex/* branches.
- Keep scope minimal. Touch only allowed paths below.
- Open a PR to main with a clear title: <feat|fix|chore|docs>: <short summary>.
- After PR is green, use Squash & Merge, then delete the branch.

[Repo]
- name: <gtrack-docs | gtrack-frontend | gtrack-backend>

[Allowed paths]
- <list files/dirs you allow to change exactly>
  e.g. docs/**, mkdocs.yml
       app/**, public/**, .github/workflows/**
       server.mjs, package.json, .github/workflows/**

[Task]
- Goal: <1–3 sentences, what and why>.
- Details:
  1) <file change #1>
  2) <file change #2>
  3) <...>
- Constraints:
  - Do not modify README.md unless PR title starts with `chore(readme):`.
  - No unrelated refactors or formatting-only changes.

[Testing / Local steps to include in PR description]
- <how to test locally>
  e.g. mkdocs build --strict
       npm run build && npm run start
       curl $API/health -> {"status":"ok"}

[CI Acceptance — must be green]
- <list required checks for this repo>

[Deliverables]
- PR title: <type>: <short summary>
- Only the files under "Allowed paths" changed.
- PR description: what changed, why, and how to test (copy “Testing” block).
