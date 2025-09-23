# API (Security Pack v0.3.0)

Base URL: `<RAILWAY_BASE_URL>`

## GET /health

**200** `{ "status": "ok" }`

## GET /drivers

Возвращает список водителей с маскированными чувствительными полями.

**Headers**

* `Authorization: Bearer <token>`
* `APP_ROLE_HEADER` — обязательный заголовок с ролью пользователя.

**200** `[{ DriverMasked }]`

```json
{
  "id": "drv_001",
  "full_name": "Иван Петров",
  "rc_mask": "850101/1***",
  "passport_mask": "PA******89",
  "driver_license_mask": "DL*****42",
  "iban_mask": "CZ65 **** **** 1234 56",
  "swift_mask": "KOMBCZ**",
  "tacho_card_mask": "TA****90",
  "documents": [
    { "doc_type": "driver_license", "expires_at": "2026-05-10", "status": "valid" }
  ]
}
```

Masking правила:

* RČ: оставляем первые 6 символов + последний блок из 3–4 символов, остальное `*`.
* Паспорт/Права/Тахокарта: первые 2 символа + последние 2 символа.
* IBAN: сохраняем код страны и последние 4 цифры, остальное заменяем `*` блочно по 4.
* SWIFT: первые 4 символа + последние 2 символа, остальное `*`.

**Ошибки**

* `401` — не авторизован.
* `403` — роль не разрешена (отсутствует в списке модулей Drivers).

## POST /drivers/:id/reveal

Раскрывает незашифрованные поля по отдельному водителю. Доступно только для ролей `operations.admin` и `support.senior`.

**Headers**

* `Authorization: Bearer <token>`
* `APP_ROLE_HEADER: operations.admin | support.senior`
* `Content-Type: application/json`

**Body**

```json
{ "reason": "Manual verification of tachograph" }
```

Поле `reason` обязательно, строка 10–256 символов. Сохраняется в аудит.

**200** `{ DriverRevealed }`

```json
{
  "id": "drv_001",
  "full_name": "Иван Петров",
  "national_id_rc": "850101/1234",
  "passport_no": "PA123456789",
  "driver_license_no": "DL9876542",
  "iban": "CZ6508000000001234567899",
  "swift": "KOMBCZPP",
  "tacho_card_no": "TA12345690"
}
```

**Ошибки**

* `400` — пустая или слишком короткая причина.
* `403` — роль не имеет доступа к раскрытию.
* `404` — водитель не найден или скрыт политиками RLS.
* `409` — есть активная блокировка на раскрытие (rate-limit).
* `422` — причина превышает 256 символов или содержит запрещённые символы.

Все успешные ответы инициируют запись в `audit_driver_reveals`.
