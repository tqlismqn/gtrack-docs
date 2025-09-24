# Проверка офлайн-сборки и автонавигации

**Как запустить:** GitHub → **Actions → Docs - Verify Offline → Run workflow**.

Проверяется:
- офлайн-установка зависимостей из `docs/vendor/wheels` по `docs/requirements.lock.txt`,
- наличие плагинов `mkdocs-material`, `mkdocs-awesome-pages-plugin`, `mkdocs-git-revision-date-localized`,
- наличие `awesome-pages` в `mkdocs.yml`,
- автонавигация для `docs/import/**`: временно создаётся файл `__autonav_smoke.md` и проверяется его появление в `site/import/__autonav_smoke/index.html`.

Если тест падает с сообщением *Offline assets missing* — сперва запустите **Docs - Refresh Wheels**.
