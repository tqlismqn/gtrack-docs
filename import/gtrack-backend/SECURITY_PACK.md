# Security Pack (Drivers Module)

This document describes the minimum security controls that protect personally identifiable information (PII) for the `drivers` module. The implementation combines PostgreSQL Row-Level Security (RLS), application-side encryption, blind indexes for searchable fields, and a dedicated audit trail for every privileged disclosure.

## Data Protection Overview

| Control | Description |
| --- | --- |
| TLS enforcement | The application forces `sslmode=require` when constructing the PostgreSQL connection string and enables client-side TLS for the `pg` driver. |
| Row-Level Security | RLS is enabled on `drivers`. Policies delegate filtering decisions to the `app.user_role` and `app.user_id` session parameters that are set per-request inside the API. |
| Encryption at rest | Sensitive attributes are encrypted in the application using AES-256-GCM before being persisted in columns ending with `_enc`. |
| Blind indexes | Deterministic SHA-256 hashes salted with `HASH_SALT` are stored in columns ending with `_hash` so exact-match searches can be executed without revealing the plaintext. |
| Audit log | Every successful `POST /drivers/:id/reveal` call inserts a row into `pii_access_log` capturing who accessed which driver fields and why. |

### Sensitive driver fields

The following attributes are encrypted and have blind indexes:

- `national_id_rc`
- `passport_no`
- `driving_license_no`
- `iban`
- `swift`
- `tacho_card_no`

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string. The application appends `sslmode=require` if missing. |
| `ENCRYPTION_KEY_V1` | Base64 encoded 32-byte key used for AES-256-GCM encryption. |
| `ENCRYPTION_KEY_PREV` | (Optional) Previous 32-byte base64 key kept during key rotation. |
| `HASH_SALT` | Secret salt mixed into SHA-256 blind hashes. |
| `APP_ROLE_HEADER` | Header name that contains the caller role (defaults to `X-User-Role`). |
| `APP_USER_ID_HEADER` | Header name with the driver/user identifier (defaults to `X-User-Id`). |
| `LOG_PII_REVEAL` | When set to `true`, the API writes audit records to `pii_access_log`. |

### Key management & rotation

1. Generate a new 32-byte random key and expose it as base64.
2. Set the existing `ENCRYPTION_KEY_V1` value into `ENCRYPTION_KEY_PREV`.
3. Update `ENCRYPTION_KEY_V1` with the new base64 key.
4. Deploy the application so it can decrypt using both keys. All new writes will use the new key (`v1`).
5. Re-encrypt existing records in batches if required, then unset `ENCRYPTION_KEY_PREV`.

## RLS Policies

The migration `db/migrations/2025-09-23_security_pack.sql` enables RLS and creates policies bound to `app.user_role` / `app.user_id` GUCs:

- **Admin/HR** (`FOR ALL`) – full read/write access via the `app_rw` role.
- **Dispatcher/Accounting/Admin/HR** (`FOR SELECT`) – read access when connected as `app_rw` or `app_ro`.
- **Driver** (`FOR SELECT`) – limited to the row where `drivers.id` matches `app.user_id`.

The API uses `SET LOCAL` equivalents (`set_config`) to set these GUCs at the start of every request.

## Blind index search

To search by a sensitive attribute without decrypting it, compute the blind hash inside the application (or with the same salt) and use it in the WHERE clause:

```sql
SELECT id, full_name
FROM drivers
WHERE national_id_rc_hash = '\\x' || encode(digest(CONCAT(:hash_salt, :rc_plaintext), 'sha256'), 'hex');
```

> Replace `:hash_salt` with the `HASH_SALT` secret and `:rc_plaintext` with the value you need to find. The application exposes this via `blindHash(...)` so service code should not reconstruct the SQL manually.

## Audit Trail

`pii_access_log` captures:

- `actor_role`, `actor_id`
- `driver_id`
- `fields` (text array of revealed attributes)
- Optional `request_id`, `ip_address`, `reason`
- `occurred_at` timestamp

Set `LOG_PII_REVEAL=true` in production to activate the logging. The audit log can be reviewed downstream or synced into the central observability stack.

## API Behaviour

- `GET /drivers` – returns masked values (`*_mask`) only. Optional exact-match search parameters (`rc`, `passport`, `license`, `iban`, `swift`, `tacho_card_no`) are translated into blind hash lookups.
- `POST /drivers/:id/reveal` – restricted to `Admin` and `HR`. The endpoint decrypts the requested fields, returns the plaintext, and writes to `pii_access_log`.

These endpoints always set `app.user_role` (and optionally `app.user_id`) before querying PostgreSQL so that the database policies enforce access control even if application code is compromised.
