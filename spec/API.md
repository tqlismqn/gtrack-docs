# API Specification

Версия API: v1 (черновик).

## Общие требования

- Базовый URL: `https://api.gtrack.io` (production), `https://staging-api.gtrack.io` (staging).
- Все ответы возвращаются в формате `application/json`.
- Аутентификация: httpOnly session cookie, установленная после успешного OAuth входа.

## Эндпоинты

### GET /health

Проверка готовности сервиса.

- **Auth**: не требуется.
- **Ответ 200**

```json
{
  "status": "ok",
  "version": "2025.09.21",
  "uptimeSeconds": 52342
}
```

**Схема ответа**

| Поле           | Тип     | Описание                                  |
| -------------- | ------- | ----------------------------------------- |
| `status`       | string  | `ok` при успешной работе, `degraded` иначе |
| `version`      | string  | Текущая версия сборки                      |
| `uptimeSeconds`| integer | Количество секунд работы процесса         |

### GET /drivers

Возвращает список водителей с агрегированными данными карточки.

- **Auth**: требуется активная сессия.
- **Параметры запроса**

| Параметр  | Тип     | Обязателен | Описание                                      |
| --------- | ------- | ---------- | --------------------------------------------- |
| `page`    | integer | Нет        | Номер страницы (по умолчанию `1`)             |
| `perPage` | integer | Нет        | Размер страницы (по умолчанию `25`, максимум `100`) |
| `status`  | string  | Нет        | Фильтр по статусу документов (`active`, `expired`, `pending`) |

- **Ответ 200**

```json
{
  "data": [
    {
      "id": "drv_123",
      "fullName": "Иван Петров",
      "phone": "+7 999 123-45-67",
      "vehicle": {
        "plateNumber": "A123BC77",
        "model": "Hyundai Solaris"
      },
      "documents": {
        "license": "active",
        "medicalCertificate": "pending",
        "vehicleInsurance": "expired"
      },
      "lastShiftStart": "2025-09-20T06:30:00Z",
      "assignedDispatcher": {
        "id": "usr_456",
        "fullName": "Мария Орлова"
      }
    }
  ],
  "meta": {
    "page": 1,
    "perPage": 25,
    "total": 150
  }
}
```

**Схема элемента `data[]`**

| Поле                         | Тип     | Описание                                                     |
| ---------------------------- | ------- | ------------------------------------------------------------ |
| `id`                         | string  | Уникальный идентификатор водителя                            |
| `fullName`                   | string  | ФИО                                                           |
| `phone`                      | string  | Контактный номер                                             |
| `vehicle.plateNumber`        | string  | Государственный номер                                        |
| `vehicle.model`              | string  | Марка и модель                                                |
| `documents.license`          | string  | Статус водительского удостоверения (`active`, `expired`, `pending`) |
| `documents.medicalCertificate`| string | Статус медсправки (`active`, `expired`, `pending`)            |
| `documents.vehicleInsurance` | string  | Статус страховки (`active`, `expired`, `pending`)             |
| `lastShiftStart`             | string  | ISO8601 timestamp начала последней смены                     |
| `assignedDispatcher.id`      | string  | Идентификатор диспетчера                                     |
| `assignedDispatcher.fullName`| string  | Имя диспетчера                                               |

**Схема `meta`**

| Поле    | Тип     | Описание                              |
| ------- | ------- | ------------------------------------- |
| `page`  | integer | Текущая страница                      |
| `perPage` | integer | Размер страницы                        |
| `total` | integer | Общее количество записей               |
