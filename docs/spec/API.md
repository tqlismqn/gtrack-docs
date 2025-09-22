# API (MVP)

Base URL: `<RAILWAY_BASE_URL>`

## GET /health

**200** `{ "status": "ok" }`

## GET /drivers

**200** `[Driver]`

### Типы

```json
{
  "id": "drv_001",
  "full_name": "Иван Петров",
  "national_id_rc": "850101/1234",
  "documents": [
    { "doc_type": "driver_license", "expires_at": "2026-05-10", "status": "valid" }
  ]
}
```

### Планируемые

* **POST /auth/session** `{ provider, id_token }` → httpOnly cookie
* **GET /auth/me** → профиль при валидной сессии
