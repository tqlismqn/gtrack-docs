# ENV Matrix (v2.9.0)

Компонент | Переменная | Назначение | Пример
---|---|---|---
Frontend (Angular) | NG_APP_API_URL | Базовый URL API | https://api.g-track.eu
Backend (Laravel) | APP_URL | Базовый URL приложения | https://api.g-track.eu
Backend (Laravel) | DB_CONNECTION/HOST/PORT/NAME/USER/PASS | PostgreSQL 16 | pgsql / 10.0.0.5 / 5432 / gtrack / gtrack / secret
Backend (Laravel) | SANCTUM_STATEFUL_DOMAINS | SPA-домены | app.g-track.eu,localhost:4200
Backend (Laravel) | SESSION_DOMAIN | Куки-домен | .g-track.eu
Backend (Laravel) | QUEUE_CONNECTION | Очереди | database/redis
Backend (Laravel) | LOG_CHANNEL | Логи | stack
