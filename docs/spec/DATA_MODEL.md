# Data Model (MVP)

## Driver

* `id: string`
* `full_name: string`
* `national_id_rc: string`
* `documents: Document[]`

## Document

* `doc_type: enum("driver_license","medical","tachograph","other")`
* `expires_at: date(YYYY-MM-DD)`
* `status: enum("valid","expiring","expired")`
