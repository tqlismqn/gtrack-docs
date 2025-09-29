# Модуль «Водители (Driver)» — Data Model v0.1

## Цель

Зафиксировать модель данных и требования к защите персональных данных (GDPR), чтобы реализовывать API и хранилище по подходу contracts-first.

## Кратко

- **Идентификаторы**: ULID; читаемый номер водителя `driverNumber = DRV + 6 цифр` (без дефиса), уникален в пределах арендатора; внешний импортный ключ `code` (уникален в пределах арендатора).
- **Сущности**: Driver, Document, Attachment, Assignment, Note, Compliance, AuditLog (а также AccessRequest для временных аппрувов; сервисная сущность).
- **Документы**: один актуальный файл на документ без версияции (замена файла фиксируется только в AuditLog).
- **Уведомления**: каналы e-mail, внутренний Inbox, Telegram-бот (пер-тип конфиг порогов событий; включаемость/выключаемость).
- **Retention**: 5 лет после архивации водителя; legal hold на все сущности (HR/admin).

## 1. Сущности и связи

### 1.1 Driver (ядро)

- Связи: 1—M → Document, Assignment, Note, AuditLog.
- Связь: 1—1 → Compliance.

### 1.2 Document (метаданные документа)

- Связь: M—1 → Driver.
- Связи: 1—M → Attachment (MVP: фактически один актуальный).
- Статусы: `pending_approval | valid | expired | rejected`.

### 1.3 Attachment (вложение)

- Связь: M—1 → Document.
- Ограничения: размер ≤ 15 MB; MIME: `application/pdf`, `image/jpeg`, `image/png`, `image/heic`.

### 1.4 Assignment (назначение)

- Связь: M—1 → Driver.
- Ссылки на внешние модули: `vehicleId`, `tripId` (строки/ULID).
- При `suspended` — запрещено создавать (кроме override).

### 1.5 Note (служебные заметки)

- Связь: M—1 → Driver.
- Видимость: `private`, `internal`, `public_to_driver`.

### 1.6 Compliance (агрегат допуска)

- Связь: 1—1 → Driver.
- Поля: `status`, `blockingReason`, `nextExpiryOn`, `hasBlockingIssues`.

### 1.7 AuditLog (журнал)

- Фиксирует операции по Driver/Document/Attachment/Assignment/Note и системные события (скачивания, аппрувы, настройки).
- Retention 5 лет; учитывает legal hold.

### 1.8 AccessRequest (временный аппрув просмотра)

- Связан с конкретными `driverId`, `requesterId`, `scopes`, сроком действия; аппрувер: `hr_lead` или `admin`.

## 2. Поля Driver

### 2.1 person

| Ключ           | Тип    | Формат              | Обязат. | GDPR     | Шифр/маска | Пример      |
| -------------- | ------ | ------------------- | ------- | -------- | ---------- | ----------- |
| id             | string | ULID                | да      | none     | —          | 01J9X4…     |
| driverNumber   | string | `^DRV\d{6}$`        | да      | none     | —          | DRV000123   |
| code           | string | `^[A-Z0-9][A-Z0-9_-]{1,31}$` | нет | none | — | EMP-2025-042 |
| firstName      | string | 1..100              | да      | moderate | —          | Ivan        |
| lastName       | string | 1..100              | да      | moderate | —          | Petrov      |
| middleName     | string | 0..100              | нет     | moderate | —          | Sergeevich  |
| dateOfBirth    | date   | ISO; UI: DD.MM.YYYY | да      | critical | шифр+маска | 1989-12-04  |
| gender         | enum   | male/female/other/unspecified | нет | moderate | — | male |
| countryOfBirth | string | ISO-3166-1          | нет     | moderate | —          | CZ          |
| nationality    | string | ISO-3166-1          | нет     | moderate | —          | CZ          |
| nationalities  | array  | ISO-3166-1, ≤4      | нет     | moderate | —          | ["CZ","PL"] |
| placeOfBirth   | string | 0..120              | нет     | moderate | —          | Praha, CZ   |
| nationalId     | string | 0..64               | нет     | critical | шифр+маска | 850412/1234 |

### 2.2 contacts (списки до 3 шт.)

- `emails[] { address, label: primary|other, isPrimary }` (≤3; ≤1 primary).
- `phones[] { number, label: mobile|other, isPrimary }` (≤3; ≤1 primary).
- Адресные поля — все необязательные.

### 2.3 employment/payroll

- `employmentType: employee|contractor` (обязательное).
- `hiredOn`, `terminatedOn` — даты (ISO; UI: DD.MM.YYYY).
- `payrollEnabled: boolean` — если `true`, то требуется `payrollSettings`:
  - `payRateType: hourly|daily|per_km|fixed`, `payRate`, `currency`.
  - `perDiemEnabled`, `perDiemRate`, `perDiemCurrency`.
  - `finesEnabled`.

### 2.4 roles/tags

- `tags[]` (≤20), `languages[]` (ISO 639-1, ≤5).

### 2.5 banking (CZ vs non-CZ)

- Если `bankCountry = CZ` → `czAccountNumber` (+`czBankCode`), запрещены `iban`/`swiftBic`/`bankName`.
- Если `bankCountry != CZ` → обязательны `iban`/`swiftBic`/`bankName`, запрещены `czAccountNumber`/`czBankCode`.
- Номера счетов/IBAN — критичные данные (шифрование + маска по ролям).

### 2.6 compliance (агрегат)

- `status: draft|active|suspended|archived`.
- `blockingReason: expired_license|expired_medical|expired_tachograph|expired_visa|expired_adr|manual_suspend|other`.
- `nextExpiryOn: date`, `hasBlockingIssues: boolean`.

### 2.7 meta

- `tenantId`, `createdAt`, `updatedAt`, `archivedAt?`, `legalHold`, `extRefs{}`.
- Формат даты/времени: ISO в API; UI — 24h `DD.MM.YYYY HH:mm`.

## 3. Документы (Document) и вложения (Attachment)

### 3.1 Общие поля Document

- `type` (см. ниже), `state (pending_approval|valid|expired|rejected)`.
- `number?`, `issuingCountry?`, `issueDate?`, `expiryDate?`, `categories[]?`, `classes[]?`, `cardNumber?`, `visaType?`, `countryReceived?`, `a1SwitzerlandExtension?`, `policyNumber?`, `declarationType?`.
- `review { approvedBy, approvedAt, rejectedBy, rejectedAt, rejectReason }`.
- `source: hr|driver_bot|import|api`.
- `attachmentId?`.

### 3.2 Типы и специфичные правила (MVP)

- `passport` — обяз.: `number`, `issuingCountry`, `expiryDate`.
- `driver_license` — обяз.: `number`, `expiryDate`, `categories` (из: `C`, `CE`, `C1`, `C1E`, `D`, `DE`, `D1`, `D1E`).
- `cpc_dqc` (Code95) — обяз.: `countryReceived`, `expiryDate`; `number` опционально.
- `tachograph_card` — обяз.: `cardNumber`, `expiryDate`.
- `medical_certificate` — обяз.: `issueDate`, `expiryDate`.
- `psychotest` — обяз.: `issueDate`, `expiryDate` (интервалы зависят от DOB/политики).
- `visa_work_permit` — обяз.: `number`, `visaType`, `issuingCountry`, `expiryDate`.
- `adr_permit` — обяз.: `classes` из диапазона "1".."9".
- `certificate_a1` — обяз.: `issueDate`, `expiryDate`, `a1SwitzerlandExtension: boolean`.
- `insurance` — обяз.: `policyNumber`, `expiryDate`.
- `declaration` — обяз.: `declarationType` (enum, конфиг в админке).
- `other` — свободный тип (минимум: даты + notes).

### 3.3 Attachment (ограничения)

- MIME: `application/pdf`, `image/jpeg`, `image/png`, `image/heic`.
- Размер: ≤ 15 MB.
- Только один актуальный файл на Document; замена = новая загрузка, старый файл не храним (только событие в AuditLog).

## 4. Бизнес-правила допуска

- Статусы: `draft → active → suspended → archived` (см. VALIDATION/API).
- Критичные документы по умолчанию: `driver_license`, `cpc_dqc`, `tachograph_card`, `medical_certificate`, `visa_work_permit` (для non-EU), `adr_permit` (если требуется), `psychotest` (ASSUMPTION: критичен).
- `active` разрешает назначения; `suspended` запрещает (override — временное разрешение с аудитом).

## 5. Нотификации и пороги (обзор)

- Каналы: e-mail, Inbox, Telegram-бот.
- Пороги expiring: конфиг per-тип, включаемость событий можно выключать/включать.
- Дайджест 08:00 Europe/Prague; моментальные при `expired` и входе в окно ≤ N дней.

## 6. RBAC (ссылочно) и безопасность

- Роли: `admin`, `hr_lead`, `hr`, `dispatcher`, `accountant`, `driver(self)`.
- Multi-role & Groups: `effectiveRoles = union(userRoles ∪ groupRoles)`.
- Маскирование: номера документов/нац. ID/банки по матрице (см. `RBAC.md`).
- Временные аппрувы через AccessRequest (`scopes: bank_full, doc_numbers_full`).

## 7. GDPR

- Классы: `critical` (шифрование + маска), `moderate`, `none`.
- Скачивание оригиналов: только `admin/hr/hr_lead/driver(self)` (свои); логирование в AuditLog.
- Retention: 5 лет после архивации; Legal hold — блокирует удаление.
