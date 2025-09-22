# ENV Matrix

| Env     | Service | Var                    | Meaning                      | Example                                                                                             |
| ------- | ------- | ---------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------- |
| preview | app     | NEXT_PUBLIC_API_URL    | Base URL API (preview)       | [https://...railway.app](https://...railway.app)                                                    |
| prod    | app     | NEXT_PUBLIC_API_URL    | Base URL API (prod)          | [https://...railway.app](https://...railway.app)                                                    |
| prod    | backend | PORT                   | HTTP port                    | 8080                                                                                                |
| prod    | backend | ALLOWED_ORIGINS        | CSV CORS origins (prod only) | [https://drivers.g-track.eu,https://*.vercel.app](https://drivers.g-track.eu,https://*.vercel.app) |
| prod    | backend | AUTH_SECRET            | Session/JWT secret           | (set in Railway)                                                                                    |
