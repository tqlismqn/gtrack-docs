# 2025-10-14 — Safe bootstrap & storage fallback (demo stabilization)

**Changed**
- `src/main.ts`: глобальные ловушки ошибок; `?debug=1` включает eruda (диагностика на iOS/Android).
- `src/app/demo/shared/storage.ts`: добавлен безопасный wrapper над `localStorage` с in-memory fallback.
- `src/app/drivers/data/drivers.service.ts`: отказ от прямого `localStorage`; гарантированный seed из 7 водителей.
- `src/app/drivers/drivers.routes.ts`: добавлен маршрут `:id` для прямых ссылок.
- `src/app/drivers/components/drivers-page/drivers-page.component.ts`: синхронизация выбранного водителя с URL.

**Optional**
- `vercel.json`: `Cache-Control: no-store` для `index.html`.

**Acceptance**
- Демо открывается без «белого экрана» на iOS/Android/desktop.
- При пустом хранилище появляется список из 7 водителей.
- `/drivers/:id` открывается напрямую; клик/стрелки обновляют карточку без сброса скролла списка.
- В консоли нет «null»/TypeError, bootstrap-ошибки логируются глобальными ловушками.
