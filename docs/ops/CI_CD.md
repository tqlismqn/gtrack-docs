# CI/CD Overview

## gtrack-app / gtrack-backend

* Checks: build, lint, check-docs + policies (guard-readme, fresh-branch, branch-name)
* Require status checks to pass; linear history; squash merge

## gtrack-docs

* **Docs - Preview** (PR): mkdocs build --strict
* **Docs - Deploy** (main): GitHub Pages; site_url=[https://docs.g-track.eu](https://docs.g-track.eu)
* Автосинк: app/backend → import/* (PR в gtrack-docs)
