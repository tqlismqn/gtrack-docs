# Модуль «Водители (Driver)» — Data Model v0.1

**Назначение:** зафиксировать модель данных и защиту ПДн (GDPR) для реализации по принципу contracts-first.

**Ключевые решения:**
- Идентификаторы: ULID; человекочитаемый номер: **`driverNumber` = `DRV` + 6 цифр (без дефиса)**, уникален в тенанте; внешний ключ импорта **`code`**.
- Сущности: `Driver`, `Document`, `Attachment`, `Assignment`, `Note`, `Compliance`, `AuditLog`, `AccessRequest` (временный аппрув просмотра).
- Для документов: **1 актуальный файл**, без версияции (замена → запись в AuditLog).
- Форматы дат/времени: **ISO-8601** в API; **UI/Import: DD.MM.YYYY / 24h** (конвертация на сервере).
- Retention: **5 лет** после архивации; **Legal Hold** — блокирует удаление.

## 1. Сущности и связи

### 1.1. Driver
- 1—M → `Document`, `Assignment`, `Note`, `AuditLog`
- 1—1 → `Compliance`

### 1.2. Document
- M—1 → `Driver`; 1—M → `Attachment` *(MVP: держим ровно 1 актуальный)*
- `state`: `pending_approval` | `valid` | `expired` | `rejected`

### 1.3. Attachment
- M—1 → `Document`; MIME: `application/pdf`, `image/jpeg`, `image/png`, `image/heic`; Size ≤ 15 MB

### 1.4. Assignment
- Ссылки: `vehicleId`, `tripId` (строки/ULID); запрещено при `suspended` (если нет override)

### 1.5. Note
- Видимость: `private`, `internal`, `public_to_driver` (для бота и ЛК водителя)

### 1.6. Compliance
- `status`, `blockingReason`, `nextExpiryOn`, `hasBlockingIssues`

### 1.7. AuditLog
- Все операции + скачивания; учитывает Legal Hold; retention 5 лет

### 1.8. AccessRequest
- Временный доступ к немаскированным полям на конкретного водителя; `scopes`: `bank_full`, `doc_numbers_full`; аппрувер: `hr_lead|admin`; срок (по умолчанию) 8 часов

## 2. Поля `Driver`

### 2.1. person
| Ключ | Тип | Формат | Обязат. | GDPR | Шифр/маска | Пример |
|---|---|---|---|---|---|---|
| id | string | ULID | да | none | — | `01J9X4…` |
| driverNumber | string | `^DRV\d{6}$` | да | none | — | `DRV000123` |
| code | string | `^[A-Z0-9][A-Z0-9_-]{1,31}$` | нет | none | — | `EMP-2025-042` |
| firstName | string | 1..100 | да | moderate | — | `Ivan` |
| lastName | string | 1..100 | да | moderate | — | `Petrov` |
| middleName | string | 0..100 | нет | moderate | — | `Sergeevich` |
| dateOfBirth | date | ISO; **UI: DD.MM.YYYY** | да | critical | шифр+маска | `1989-12-04` |
| gender | enum | male/female/other/unspecified | нет | moderate | — | `male` |
| countryOfBirth | string | ISO-3166-1 alpha-2 | нет | moderate | — | `CZ` |
| nationality | string | ISO-3166-1 alpha-2 | нет | moderate | — | `CZ` |
| nationalities | array<string> | ISO-3166-1, ≤4 | нет | moderate | — | `["CZ","PL"]` |
| placeOfBirth | string | 0..120 | нет | moderate | — | `Praha, CZ` |
| nationalId | string | 0..64 | нет | critical | шифр+маска | `850412/1234` |

### 2.2. contacts (≤3 e-mail/телефона)
- `emails[] { address, label: primary|other, isPrimary }` (≤1 primary)
- `phones[] { number (E.164), label: mobile|other, isPrimary }` (≤1 primary)
- Адресные поля — опциональны

### 2.3. employment/payroll
- `employmentType: employee|contractor` (обяз.)
- `hiredOn`, `terminatedOn` — ISO (UI: DD.MM.YYYY)
- `payrollEnabled: boolean` → при `true` объект `payrollSettings` (ставка/валюта/суточные/штрафы)

### 2.4. roles/tags
- `tags[]` (≤20), `languages[]` (ISO 639-1, ≤5)

### 2.5. banking
- Если `bankCountry=CZ` → `czAccountNumber` (+`czBankCode`), **запрещены** `iban/swiftBic/bankName`
- Если `bankCountry!=CZ` → обязательны `iban/swiftBic/bankName`, **запрещены** `czAccountNumber/czBankCode`
- Банковские номера — GDPR: **critical** (шифр + маска по ролям)

### 2.6. compliance (агрегат)
- `status: draft|active|suspended|archived`; `blockingReason`; `nextExpiryOn`; `hasBlockingIssues`

### 2.7. meta
- `tenantId`, `createdAt`, `updatedAt`, `archivedAt?`, `legalHold`, `extRefs{}`

## 3. Документы (`Document`) и вложения (`Attachment`)

### 3.1. Общие поля `Document`
- `type`, `state`; даты `issueDate?`, `expiryDate?` (если истекаемые — обяз.)
- Узкоспец. поля: `number`, `categories[]`, `classes[]`, `cardNumber`, `visaType`, `countryReceived`, `a1SwitzerlandExtension`, `policyNumber`, `declarationType`
- `review{…}`; `source: hr|driver_bot|import|api`; `attachmentId?`

### 3.2. Типы (MVP)
- `passport` — номер, страна выдачи, **expiry** — обяз.
- `driver_license` — номер, **expiry**, `categories` ∈ {C, CE, C1, C1E, D, DE, D1, D1E}
- `cpc_dqc` — `countryReceived`, **expiry**; номер — опц.
- `tachograph_card` — `cardNumber`, **expiry**
- `medical_certificate` — **issue/expiry**
- `psychotest` — **issue/expiry** (интервалы зависят от DOB/политики)
- `visa_work_permit` — номер, тип, страна EC, **expiry** (для non-EU)
- `adr_permit` — `classes[]` из "1".."9", **expiry**
- `certificate_a1` — **issue/expiry**, `a1SwitzerlandExtension: boolean`
- `insurance` — `policyNumber`, **expiry**
- `declaration` — `declarationType` ∈ enum (настройка)

### 3.3. Attachment
- MIME: pdf/jpg/png/heic; Size ≤ 15 MB; 1 актуальный файл; замена → AuditLog

## 4. Бизнес-правила допуска
- Статусы: `draft → active → suspended → archived`
- Критичные документы (дефолт): `driver_license`, `cpc_dqc`, `tachograph_card`, `medical_certificate`, `visa_work_permit` (для non-EU), `adr_permit` (если требуется), `psychotest` *(ASSUMPTION: критичен)*
- Override: временный допуск `{ enabled, until, reason, approverId }`

## 5. Нотификации
- Каналы: e-mail, Inbox, Telegram-бот; пороги expiring **per-type** (вкл/выкл), дефолт 30/14/7; дайджест 08:00 Europe/Prague

## 6. RBAC (сводка)
- Роли: `admin`, `hr_lead`, `hr`, `dispatcher`, `accountant`, `driver(self)`; multi-role & groups (union)
- Маски: номера доков/нац. ID/банки — по матрице; AccessRequest (scopes: `bank_full`, `doc_numbers_full`)

## 7. GDPR
- Классы: `critical` (шифр+маска), `moderate`, `none`; скачивания: admin/hr/hr_lead/driver(self) (свои); всё в AuditLog; retention 5 лет; Legal Hold
