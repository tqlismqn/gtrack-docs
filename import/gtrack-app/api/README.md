# API (которым пользуется фронт)

- `GET /health` → `{ "status": "ok" }`
- `GET /drivers` → массив водителей:
```json
[
  {"full_name":"...", "national_id_rc":"...", "documents":[{"doc_type":"...", "expires_at":"YYYY-MM-DD","status":"valid|expiring|expired"}]}
]
