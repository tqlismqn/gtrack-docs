# ENV Matrix

| Env | Service | Var | Meaning | Example |
| --- | --- | --- | --- | --- |
| preview | app | `NEXT_PUBLIC_API_URL` | Base URL API (preview) | `https://gtrack-preview.railway.app` |
| prod | app | `NEXT_PUBLIC_API_URL` | Base URL API (prod) | `https://drivers.g-track.eu/api` |
| prod | backend | `PORT` | HTTP port | `8080` |
| prod | backend | `ALLOWED_ORIGINS` | CSV со списком CORS | `https://drivers.g-track.eu,https://*.vercel.app` |
| preview/prod | backend | `AUTH_SECRET` | Секрет для сессий/JWT | (set in Railway) |
| preview/prod | backend | `ENCRYPTION_KEY_V1` | Активный ключ AES-256-GCM (base64) | `base64:...` |
| preview/prod | backend | `ENCRYPTION_KEY_PREV` | Предыдущий ключ для дешифрования (опционально) | `base64:...` |
| preview/prod | backend | `HASH_SALT` | Соль для blind indexes (base64) | `base64:...` |
| preview/prod | backend | `APP_ROLE_HEADER` | Название заголовка с ролью | `x-gtrack-role` |
