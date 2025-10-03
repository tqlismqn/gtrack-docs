# Data Model — Drivers (v2.9.0)

## Таблицы

### drivers
- id (PK)
- last_name (string, req)
- first_name (string, req)
- middle_name (string, nullable)
- birth_date (date, nullable)
- rc (string, nullable) — родное число (CZ)
- citizenship (string, nullable)
- gender (string(10), nullable)
- reg_address (string, nullable) — адрес регистрации
- res_address (string, nullable) — адрес проживания
- phone (string, nullable)
- email (string, nullable)
- status (enum: Active, OnLeave, Inactive, Terminated) — default Active
- hired_at (date, nullable)
- terminated_at (date, nullable)
- contract_type (string, nullable)
- contract_signed (bool, default false)
- workplace (string, nullable)
- pas_souhlas (bool, default false)
- propiska_cz (bool, default false)
- created_at, updated_at (timestamps)

### document_types
- id (PK)
- code (string, unique) — e.g. PASSPORT, VISA, DL, A1, ADR, CODE95, MEDICAL, PSYCHO, TACHO
- meta (json, nullable)
- created_at, updated_at

### driver_documents
- id (PK)
- driver_id (FK → drivers.id, on delete cascade)
- document_type_id (FK → document_types.id)
- number (string, nullable)
- issued_at (date, nullable)
- expires_at (date, nullable)
- country (string, nullable)
- file_path (string, nullable) — путь к загруженному скану
- created_at, updated_at
- INDEX(driver_id, document_type_id)

## Retention & Audit
- Audit: activity log на уровне CRUD для drivers и driver_documents.
- Retention документов: 5 лет (учёт Legal Hold).
