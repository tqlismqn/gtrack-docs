# Drivers Module - History & Logs | Модуль водителей - История и логи

---

## 🇬🇧 English

> **Status:** 🔄 Content being filled based on user requirements

### Overview

Every driver record includes a **History/Logs tab** that displays complete audit trail of all changes made to the driver and their documents.

### Purpose

1. **Transparency** - See who made what changes and when
2. **Quality Control** - Monitor employee work and identify mistakes
3. **Compliance** - Track document uploads and status changes for regulatory requirements
4. **Error Recovery** - Ability to see what was changed and potentially revert

### What is Logged

**Driver Profile Changes:**
- Field modifications (e.g., passport number changed from X to Y)
- Status changes (active → on_leave → inactive)
- Contact information updates
- Bank details modifications

**Document Operations:**
- Document uploads (file name, upload date, uploader)
- Document deletions (who deleted, when, reason if provided)
- Document expiration date changes
- Document status transitions (valid → expiring → expired)

**Comments:**
- Who added comment
- Comment content
- Timestamp

### Log Entry Format

Each log entry includes:
- **User:** Who made the change (name + role)
- **Timestamp:** When the change occurred (date + time)
- **Action:** What was done (created, updated, deleted, uploaded, etc.)
- **Old Value → New Value:** What changed (if applicable)

### UI/UX Design

**Tab Location:** In driver detail page, alongside Documents, Comments, Finance tabs

**Display Format:**
```
📋 History & Logs Tab

┌─────────────────────────────────────────────────────────┐
│ Filter: [All Actions ▼] [All Users ▼] [Last 30 days ▼] │
└─────────────────────────────────────────────────────────┘

2025-10-29 14:32:15
👤 Anna Kowalska (HR Manager)
📄 Uploaded: Passport (PL-ABC123456) - expires 2030-05-15
File: passport_PL-ABC123456.pdf (2.3 MB)

2025-10-28 11:20:03
👤 Jan Novák (Admin)
✏️ Updated: Email address
Old: driver@oldmail.com → New: driver@newmail.com

2025-10-27 09:45:22
👤 System (Automated)
⚠️ Status Change: Driver's License status changed
Valid → Expiring Soon (expires in 28 days)
```

### Database Implementation

**Table:** `audit_logs`

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    user_id UUID REFERENCES users(id),  -- NULL for system actions
    auditable_type VARCHAR(255) NOT NULL,  -- 'Driver', 'DriverDocument', etc.
    auditable_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,  -- 'created', 'updated', 'deleted', 'uploaded'
    old_values JSONB,
    new_values JSONB,
    metadata JSONB,  -- Additional context (IP, user agent, etc.)
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for fast queries
CREATE INDEX idx_audit_logs_auditable ON audit_logs(auditable_type, auditable_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_company ON audit_logs(company_id);
```

### API Endpoint

**GET** `/api/v0/drivers/{id}/history`

**Query Parameters:**
- `action` - Filter by action type (created, updated, deleted, etc.)
- `user_id` - Filter by specific user
- `from_date` - Start date for logs
- `to_date` - End date for logs
- `page` - Pagination
- `per_page` - Results per page (default: 20)

**Response:**
```json
{
  "current_page": 1,
  "data": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "name": "Anna Kowalska",
        "role": "HR Manager"
      },
      "action": "updated",
      "auditable_type": "Driver",
      "auditable_id": "uuid",
      "old_values": {
        "email": "driver@oldmail.com"
      },
      "new_values": {
        "email": "driver@newmail.com"
      },
      "created_at": "2025-10-28T11:20:03Z"
    }
  ],
  "total": 45,
  "per_page": 20,
  "last_page": 3
}
```

---

## 🇷🇺 Русский

> **Статус:** 🔄 Содержимое заполняется на основе требований пользователя

### Обзор

Каждая запись водителя включает вкладку **История/Логи**, которая отображает полный аудит всех изменений, внесенных в водителя и его документы.

### Назначение

1. **Прозрачность** - Видеть, кто, что и когда изменил
2. **Контроль качества** - Мониторинг работы сотрудников и выявление ошибок
3. **Соответствие нормам** - Отслеживание загрузок документов и изменений статуса для нормативных требований
4. **Восстановление после ошибок** - Возможность увидеть, что было изменено, и потенциально отменить

### Что логируется

**Изменения профиля водителя:**
- Изменения полей (например, номер паспорта изменен с X на Y)
- Изменения статуса (активный → в отпуске → неактивный)
- Обновления контактной информации
- Изменения банковских реквизитов

**Операции с документами:**
- Загрузка документов (имя файла, дата загрузки, загрузчик)
- Удаление документов (кто удалил, когда, причина если указана)
- Изменения даты окончания срока действия документа
- Переходы статуса документа (действителен → истекает → просрочен)

**Комментарии:**
- Кто добавил комментарий
- Содержание комментария
- Временная метка

### Формат записи лога

Каждая запись лога включает:
- **Пользователь:** Кто внес изменение (имя + роль)
- **Временная метка:** Когда произошло изменение (дата + время)
- **Действие:** Что было сделано (создано, обновлено, удалено, загружено и т.д.)
- **Старое значение → Новое значение:** Что изменилось (если применимо)

### UI/UX дизайн

**Расположение вкладки:** На странице детального просмотра водителя, рядом с вкладками Документы, Комментарии, Финансы

**Формат отображения:**
```
📋 Вкладка История и Логи

┌───────────────────────────────────────────────────────────┐
│ Фильтр: [Все действия ▼] [Все пользователи ▼] [Последние 30 дней ▼] │
└───────────────────────────────────────────────────────────┘

2025-10-29 14:32:15
👤 Anna Kowalska (HR Менеджер)
📄 Загружено: Паспорт (PL-ABC123456) - истекает 2030-05-15
Файл: passport_PL-ABC123456.pdf (2.3 МБ)

2025-10-28 11:20:03
👤 Jan Novák (Администратор)
✏️ Обновлено: Email адрес
Старый: driver@oldmail.com → Новый: driver@newmail.com

2025-10-27 09:45:22
👤 Система (Автоматически)
⚠️ Изменение статуса: Статус водительского удостоверения изменен
Действителен → Скоро истекает (истекает через 28 дней)
```

### Реализация в базе данных

**Таблица:** `audit_logs`

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    user_id UUID REFERENCES users(id),  -- NULL для системных действий
    auditable_type VARCHAR(255) NOT NULL,  -- 'Driver', 'DriverDocument', и т.д.
    auditable_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,  -- 'created', 'updated', 'deleted', 'uploaded'
    old_values JSONB,
    new_values JSONB,
    metadata JSONB,  -- Дополнительный контекст (IP, user agent, и т.д.)
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Индексы для быстрых запросов
CREATE INDEX idx_audit_logs_auditable ON audit_logs(auditable_type, auditable_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_company ON audit_logs(company_id);
```

### API Endpoint

**GET** `/api/v0/drivers/{id}/history`

**Параметры запроса:**
- `action` - Фильтр по типу действия (created, updated, deleted, и т.д.)
- `user_id` - Фильтр по конкретному пользователю
- `from_date` - Начальная дата для логов
- `to_date` - Конечная дата для логов
- `page` - Пагинация
- `per_page` - Результатов на страницу (по умолчанию: 20)

**Ответ:**
```json
{
  "current_page": 1,
  "data": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "name": "Anna Kowalska",
        "role": "HR Менеджер"
      },
      "action": "updated",
      "auditable_type": "Driver",
      "auditable_id": "uuid",
      "old_values": {
        "email": "driver@oldmail.com"
      },
      "new_values": {
        "email": "driver@newmail.com"
      },
      "created_at": "2025-10-28T11:20:03Z"
    }
  ],
  "total": 45,
  "per_page": 20,
  "last_page": 3
}
```

---

**Last Updated:** October 29, 2025
**Version:** 2.0.0
**Source:** User Requirements + Master Specification v3.1 (audit_logs table)
