# Матрица переменных окружения

| Платформа | Переменная            | Назначение                                         | Значение (пример)                          |
| --------- | --------------------- | -------------------------------------------------- | ------------------------------------------ |
| Vercel    | `NEXT_PUBLIC_API_URL` | URL публичного API, доступный в браузере           | `https://staging-api.gtrack.io`            |
| Vercel    | `PORT`                | Порт запуска Next.js на сервер-сайд рендеринге     | `3000`                                     |
| Vercel    | `ALLOWED_ORIGINS`     | Список доменов, с которых разрешены запросы (CSV)  | `https://gtrack.io,https://app.gtrack.io`  |
| Railway   | `NEXT_PUBLIC_API_URL` | URL API для фронтенда (staging/preprod)            | `https://railway-api.gtrack.io`            |
| Railway   | `PORT`                | Порт Node.js сервера                               | `8080`                                     |
| Railway   | `ALLOWED_ORIGINS`     | Origins для CORS и websocket-подключений           | `https://railway.gtrack.io`                |

> Значения уточняются в Secret Manager. Для локальной разработки используйте `.env.local` с аналогичными ключами.
