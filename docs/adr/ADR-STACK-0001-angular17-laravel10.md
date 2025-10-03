# ADR-STACK-0001 — Переход на Angular 17 + Laravel 10 + PostgreSQL 16

**Статус:** accepted (2025-10-03)  
**Контекст:** Требуется ускорить разработку CRUD/админки, унифицировать валидацию/уведомления/очереди, и получить предсказуемый DX.  
**Решение:** 
- Frontend: Angular 17 (standalone) + Angular Material
- Backend: Laravel 10 (Sanctum, Queues, Notifications)
- DB: PostgreSQL 16
- Admin: Nova 5 (опц.) / Filament v3 (альтернатива)
- Deploy: Laravel Cloud (primary), Railway (fallback)
**Альтернативы, которые рассматривались:** 
- Оставить Next.js + Fastify (отклонено: дольше CRUD/админка)
- Laravel 11/12 (отложено: мигрируем позже)
- Только Railway (отклонено как primary: меньше managed-возможностей)
- Vapor (serverless) (не требуется сейчас)
**Последствия:**
- Обновить API-контракты и модель данных под Laravel.
- Обновить UX-спеки под Angular Material.
- Обновить OPS: ENV, CI/CD, DEPLOYMENT, DNS.
**Ссылки:** см. соответствующие разделы SPEC и OPS.
