# Модуль «Водители (Driver)» — Audit & Notifications v0.1

**Назначение:** зафиксировать модель аудита и систему уведомлений для модуля «Водители». Документ дополняет спецификации `DATA_MODEL.md`, `API.md`, `VALIDATION.md`, `RBAC.md`.

**Ключевые решения:**

* **AuditLog** — централизованный журнал событий с ретеншином **5 лет**, учитывает **Legal Hold**.
* **Каналы уведомлений:** e-mail, внутренний **Inbox**, **Telegram-бот**. Локали: **ru, en, cs, uk, pl, de** (минимальные техшаблоны).
* **Настройки per-tenant:** включение/выключение каналов, пороги `daysBefore` **per document type**, получатели (HR/dispatcher + **копия accounting & security**).
* **Дайджест** ежедневно (по умолчанию 08:00 `Europe/Prague`) + **мгновенные** алерты при `expired` + **еженедельный отчёт** (по умолчанию Пн 08:30).
* **AccessRequest:** фиксирует временные раскрытия немаскированных полей; каждое такое открытие логируется.
* **Анти-спам:** дедуп за день по ключу `(driverId, documentType, daysBefore, date)`; ретраи при сбоях.

---

## 1. AuditLog — модель

### 1.1. Схема

| Ключ                | Тип                            | Обяз. | Описание                                                                                                                                           |
| ------------------- | ------------------------------ | ----: | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                  | ULID                           |    да | идентификатор события                                                                                                                              |
| tenantId            | ULID                           |    да | тенант                                                                                                                                             |
| timestamp           | datetime (ISO, UTC)            |    да | время события                                                                                                                                      |
| actorUserId         | ULID | `system` | `driver_bot` |    да | инициатор                                                                                                                                          |
| actorEffectiveRoles | string[]                       |    да | роли (union) на момент                                                                                                                             |
| source              | enum                           |    да | `ui` | `api` | `driver_bot` | `import` | `system`                                                                                                  |
| action              | enum                           |    да | см. §1.2                                                                                                                                           |
| targetType          | enum                           |    да | `driver` | `document` | `attachment` | `note` | `assignment` | `notification` | `access_request` | `settings` | `export` | `import` | `compliance` |
| targetId            | ULID | string                  |   нет | сущность/ключ                                                                                                                                      |
| targetDriverId      | ULID                           |   нет | владелец (для связанного с водителем)                                                                                                              |
| success             | boolean                        |    да | признак успеха                                                                                                                                     |
| requestId           | string                         |   нет | трассировка                                                                                                                                        |
| ip                  | string                         |   нет | IPv4/IPv6                                                                                                                                          |
| userAgent           | string                         |   нет | UA                                                                                                                                                 |
| metadata            | object                         |   нет | payload события (см. §1.3)                                                                                                                         |

**Retention:** 5 лет; **Legal Hold** блокирует удаление записей.
**Индексирование:** `(tenantId, timestamp DESC)`, `(tenantId, action)`, `(tenantId, targetDriverId, timestamp DESC)`.

### 1.2. Доступные `action`

* **Driver:** `driver.created`, `driver.updated`, `driver.archived`, `driver.status_change`.
* **Document:** `document.created`, `document.updated`, `document.state_change`, `document.replaced_attachment`.
* **Attachment:** `attachment.uploaded`, `attachment.downloaded`, `attachment.deleted`*.
* **Note:** `note.created`, `note.updated`, `note.deleted` (visibility: `private|internal|public_to_driver`).
* **Assignment:** `assignment.created`, `assignment.updated`, `assignment.deleted`.
* **AccessRequest:** `access_request.created|approved|denied|revoked|expired`, `data_view_unmasked`.
* **Notifications:** `notification_settings.updated`, `notification.sent`, `notification.failed`, `notification.digest_sent`, `notification.weekly_report_sent`.
* **Import/Export:** `import.started|finished`, `export.started|finished`.
* **Compliance:** `compliance.recomputed`.

* *Удаление вложений в MVP не используется, оставлено для будущих политик хранения.*

### 1.3. Примеры `metadata`

* `attachment.downloaded` → `{ "documentId":"01DOC…", "attachmentId":"01ATT…", "filename":"passport.pdf" }`
* `access_request.approved` → `{ "requestId":"01AR…", "scopes":["doc_numbers_full"], "validUntil":"2025-10-01T16:00:00Z" }`
* `notification.sent` → `{ "channel":"email", "template":"doc_expiring", "locale":"ru", "driverId":"01DRV…", "documentType":"passport", "daysBefore":14, "recipients":["hr@…","acc@…","sec@…"] }`

---

## 2. RBAC на журнал

| Роль         | Доступ к AuditLog                                                       |
| ------------ | ----------------------------------------------------------------------- |
| admin        | Полный доступ, экспорт                                                  |
| hr_lead      | Все события по driver/document/note/attachment/notifications            |
| hr           | То же, что hr_lead, но без админ-операций                               |
| dispatcher   | События по driver/compliance/notifications (без содержимого документов) |
| accountant   | События по banking/billing/notifications (без бинарников)               |
| driver(self) | Только собственные события                                              |

---

## 3. NotificationSettings — модель per-tenant

### 3.1. Схема (верхний уровень)

| Ключ            | Тип    | Описание                                                                |
| --------------- | ------ | ----------------------------------------------------------------------- |
| timezone        | string | дефолт `Europe/Prague`                                                  |
| dailyDigestTime | string | время локали, напр. `08:00`                                             |
| weeklyReport    | object | `{ "enabled": true, "weekday": "MON", "time": "08:30" }` *(ASSUMPTION)* |
| channels        | object | `{ "email": true, "inbox": true, "telegram": true }`                    |
| perDocumentType | map    | ключ = тип (`passport`, `driver_license`, …), значение см. ниже         |

### 3.2. per-document config

```json
{
  "enabled": true,
  "daysBefore": [30, 14, 7, 0],
  "instantOnExpired": true,
  "recipients": {
    "hr": true,
    "dispatcher": true,
    "accounting": true,
    "security": true
  },
  "extraEmails": ["custom@tenant.cz"],
  "includeDriver": false,
  "snoozeDays": 0
}
```

> По умолчанию **включены** копии в **accounting** и **security** для всех документов (требование бизнеса). Админ/HR могут поменять.

---

## 4. Триггеры и поведение

### 4.1. Daily job (per-tenant)

1. Пересчёт `Compliance` и `nextExpiryOn`.
2. Отправка персональных уведомлений по `daysBefore`, приходящихся на сегодня.
3. Отправка **ежедневного дайджеста**.

### 4.2. Instant triggers

* При `document.state_change → expired` — мгновенное уведомление.
* Изменение настроек — не шлёт писем; логируется `notification_settings.updated`.

### 4.3. Weekly report

* По умолчанию Пн 08:30 (*ASSUMPTION*). Получатели: HR, hr_lead, accounting, security (при включенных флагах).

### 4.4. Дедуп/ретраи

* Ключ дедупликации за календарный день: `(driverId, documentType, daysBefore, date)`.
* Ретраи 3× с экспоненциальной задержкой при `notification.failed`.

---

## 5. Шаблоны уведомлений (минимальные)

### 5.1. Общие переменные

`{{tenant.name}}`, `{{driver.fullName}}`, `{{driver.driverNumber}}`,
`{{document.type}}`, `{{document.expiryDate}}`, `{{daysBefore}}`,
`{{link.driverProfile}}`, `{{link.document}}`.

### 5.2. Истечение документа (RU)

**Subject:** `[G-Track] Истекает {{document.type}} у {{driver.fullName}} через {{daysBefore}} дн.`
**Body (text):**

```
Водитель: {{driver.fullName}} ({{driver.driverNumber}})
Документ: {{document.type}}
Истекает: {{document.expiryDate}}
Дней до истечения: {{daysBefore}}

Профиль: {{link.driverProfile}}
Документ: {{link.document}}
```

*EN/CZ/UK/PL/DE — аналогичные тексты с соответствующей локалью.*

### 5.3. Ежедневный дайджест

```
Дата: {{today}}  •  Часовой пояс: {{tenant.timezone}} ({{dailyDigestTime}})

Просрочки: {{expiredCount}}
Истекают сегодня/завтра/7/14/30: {{t0}} / {{t1}} / {{t7}} / {{t14}} / {{t30}}

Топ-риски:
- {{driver1}} — {{docType}} (expires {{date}})
- …
```

### 5.4. Telegram/Inbox

* Используют те же переменные; добавляются CTA: «Открыть профиль», «Запросить у водителя».

---

## 6. Weekly Report — структура письма

**Секции:**

* **A. Документы** — новые/апрув/реджект/истёкшие, по типам.
* **B. Активность сотрудников** — счётчики `driver.*`, `document.*`, `note.*`, `access_request.*` по пользователям.
* **C. Оценка времени** *(ASSUMPTION)* — «активное время» = интервал между первой и последней операцией пользователя с отсечкой простоя > 30 мин.
* **D. Риски** — список водителей с `hasBlockingIssues=true`.

**Приложения:** CSV-вложения по секциям A/B/D.
**Аудит:** `notification.weekly_report_sent`.

---

## 7. API (admin/hr_lead)

### 7.1. GET `/notification-settings`

Возвращает текущие настройки.

**200 OK**

```json
{
  "timezone": "Europe/Prague",
  "dailyDigestTime": "08:00",
  "weeklyReport": { "enabled": true, "weekday": "MON", "time": "08:30" },
  "channels": { "email": true, "inbox": true, "telegram": true },
  "perDocumentType": {
    "passport": { "enabled": true, "daysBefore": [30,14,7,0], "instantOnExpired": true,
      "recipients": { "hr": true, "dispatcher": true, "accounting": true, "security": true },
      "extraEmails": [], "includeDriver": false, "snoozeDays": 0
    }
  }
}
```

### 7.2. PUT `/notification-settings`

**Роли:** `admin` или `hr_lead`. При изменении создаётся `notification_settings.updated`.

**400 VALIDATION_ERROR** — при неизвестном `documentType` или некорректном времени/таймзоне.

### 7.3. POST `/notifications/test`

Отправляет тестовое сообщение указанному получателю/каналу. **Роль:** `admin`.

### 7.4. GET `/audit`

Фильтры: `action`, `actor`, `targetType`, `driverId`, `dateFrom`, `dateTo`, пагинация. RBAC: см. §2.

---

## 8. Взаимодействие с RBAC и AccessRequest

* Любые раскрытия немаскированных данных по активному AccessRequest → `data_view_unmasked` (с `accessRequestId`, `scopes`).
* Скачивания вложений — только `admin/hr/hr_lead/driver(self)` (для своих); каждое скачивание = `attachment.downloaded`.
* Настройки уведомлений доступны `admin` (R/W) и `hr_lead` (R/W), `hr` — R-only.

---

## 9. Примеры событий (JSON)

### 9.1. `notification.sent`

```json
{
  "id": "01LOGABC...",
  "timestamp": "2025-09-30T06:00:00Z",
  "tenantId": "01TEN...",
  "actorUserId": "system",
  "actorEffectiveRoles": ["system"],
  "source": "system",
  "action": "notification.sent",
  "targetType": "notification",
  "targetId": "doc_expiring:passport:14",
  "targetDriverId": "01DRV...",
  "success": true,
  "metadata": {
    "channel": "email",
    "template": "doc_expiring",
    "locale": "ru",
    "driverId": "01DRV...",
    "documentType": "passport",
    "daysBefore": 14,
    "recipients": ["hr@tenant.cz","security@tenant.cz","accounting@tenant.cz"]
  }
}
```

### 9.2. `attachment.downloaded`

```json
{
  "timestamp": "2025-09-30T10:15:41Z",
  "tenantId": "01TEN...",
  "actorUserId": "01USR...",
  "actorEffectiveRoles": ["hr"],
  "source": "ui",
  "action": "attachment.downloaded",
  "targetType": "attachment",
  "targetId": "01ATT...",
  "targetDriverId": "01DRV...",
  "success": true,
  "ip": "203.0.113.5",
  "userAgent": "Firefox/...",
  "metadata": { "documentId": "01DOC...", "filename": "passport.pdf" }
}
```

### 9.3. `access_request.approved`

```json
{
  "timestamp": "2025-09-30T08:30:00Z",
  "actorUserId": "01HRLEAD...",
  "source": "ui",
  "action": "access_request.approved",
  "targetType": "access_request",
  "targetId": "01AR...",
  "success": true,
  "metadata": { "requestId": "01AR...", "scopes": ["doc_numbers_full"], "validUntil": "2025-10-01T16:00:00Z" }
}
```

---

## 10. Анти-спам и защита

* **Дедуп:** по `(driverId, documentType, daysBefore, date)`; повтор за день не отправляется.
* **Rate-limit:** системные ограничения очереди отправок per-tenant (например, 60 msg/мин; политика уточняется).
* **Отказоустойчивость:** ретраи 3×; после неудачи — запись `notification.failed` с кодом ошибки.
* **Приватность:** минимизация PII в шаблонах; ссылки ведут в защищённый UI (авторизация обязательна).

---

## 11. Связанные документы

* [`DATA_MODEL.md`](./DATA_MODEL.md) — сущности и поля
* [`API.md`](./API.md) — контракты чтения
* [`VALIDATION.md`](./VALIDATION.md) — правила валидации
* [`RBAC.md`](./RBAC.md) — роли, маскирование, AccessRequest

---

# Изменения против v0.1

* Добавлен полноценный раздел **Audit & Notifications** (данный файл).
* Определены настройки per-tenant, получатели, локали, шаблоны, триггеры, weekly-report.
* Уточнены события журнала и RBAC на просмотр.

---

# Допущения (ASSUMPTIONS)

1. Weekly report — Пн 08:30; можно перенастроить.
2. «Активное время» в отчётах считается эвристикой (см. §6C).
3. Rate-limit рассылок — 60 msg/мин per-tenant (уточняется в реализации).

---

# Контрольный список внедрения

* [ ] Создать таблицу/коллекцию `NotificationSettings` (per-tenant).
* [ ] Реализовать daily-job и instant-triggers.
* [ ] Подключить очередь отправки (email/Inbox/Telegram).
* [ ] Записывать все события в AuditLog.
* [ ] Добавить API: GET/PUT `/notification-settings`, GET `/audit`, POST `/notifications/test`.
* [ ] Покрыть RBAC и дедуп/ретраи.

---

## Версии и ретеншин

* Retention AuditLog: **5 лет** (единый для метаданных и вложений).
* Legal Hold: блокирует удаления, видимость событий — по RBAC.

---
