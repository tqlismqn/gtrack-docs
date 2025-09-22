# ADR-0002: Auth Strategy (Google/MS + httpOnly session)
**Status:** proposed  
**Date:** 2025-09-22

## Context
Нужна аутентификация без тяжёлого внешнего SSO.

## Decision (draft)
- Фронт получает `id_token` от Google/Microsoft (OAuth/OIDC).
- Бэк валидирует `id_token` по JWKs провайдера.
- Выдаём httpOnly cookie-сессию (JWT или session id).
- Приватные роуты проверяют сессию; `/auth/me` отдаёт профиль.

## Env
- `AUTH_SECRET` (backend), client IDs (Google/MS) в Vercel/preview/prod.

## Open Questions
- TTL сессии и refresh-логика  
- Приватность `/drivers` (сразу/позже)
