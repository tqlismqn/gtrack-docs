# Data Model (Security Pack v0.3.0)

## Driver

| Column | Type | Description |
| --- | --- | --- |
| `id` | `text` | Уникальный идентификатор `drv_xxx`. |
| `full_name` | `text` | Полное имя водителя. |
| `national_id_rc_enc` | `bytea` | Зашифрованный RČ (AES-256-GCM). |
| `national_id_rc_hash` | `bytea` | Blind index для точного поиска по RČ (HMAC-SHA-256). |
| `passport_no_enc` | `bytea` | Зашифрованный номер паспорта. |
| `passport_no_hash` | `bytea` | Blind index для паспорта. |
| `driver_license_no_enc` | `bytea` | Зашифрованный номер водительского удостоверения. |
| `driver_license_no_hash` | `bytea` | Blind index для прав. |
| `iban_enc` | `bytea` | Зашифрованный IBAN. |
| `iban_hash` | `bytea` | Blind index для IBAN. |
| `swift_enc` | `bytea` | Зашифрованный SWIFT/BIC. |
| `swift_hash` | `bytea` | Blind index для SWIFT/BIC. |
| `tacho_card_no_enc` | `bytea` | Зашифрованный номер тахографической карты. |
| `tacho_card_no_hash` | `bytea` | Blind index для тахокарты. |
| `documents` | `jsonb` | Массив документов (структура ниже), хранится без PII. |
| `created_at` | `timestamptz` | Время создания. |
| `updated_at` | `timestamptz` | Время последнего изменения. |

### JSONB `documents`

| Field | Type | Description |
| --- | --- | --- |
| `doc_type` | enum(`driver_license`,`medical`,`tachograph`,`other`) | Тип документа. |
| `expires_at` | `date` | Дата истечения (YYYY-MM-DD). |
| `status` | enum(`valid`,`expiring`,`expired`) | Расчёт по правилам UI. |

### Индексы

* `idx_drivers_rc_hash` — B-tree по `national_id_rc_hash`.
* `idx_drivers_passport_hash` — B-tree по `passport_no_hash`.
* `idx_drivers_license_hash` — B-tree по `driver_license_no_hash`.
* `idx_drivers_iban_hash` — B-tree по `iban_hash`.
* `idx_drivers_swift_hash` — B-tree по `swift_hash`.
* `idx_drivers_tacho_hash` — B-tree по `tacho_card_no_hash`.

Blind index = `HMAC_SHA256(value, HASH_SALT)` → первые 32 байта.
