# Водители

API для управления ресурсами водителей в версии **v0**.

## Получить список водителей

`GET /api/v0/drivers`

Возвращает пагинированный список водителей.

```json
{
  "items": [
    {
      "id": "drv_123",
      "firstName": "Иван",
      "lastName": "Иванов",
      "status": "active"
    }
  ],
  "nextPageToken": null
}
```

## Создать водителя

`POST /api/v0/drivers`

- Тело запроса: `firstName`, `lastName`, `phone`.
- Ответ `201 Created` с данными созданного водителя.

## Обновить статус водителя

`PATCH /api/v0/drivers/{driverId}`

- Тело запроса: поле `status` (`active`, `inactive`).
- Ответ `200 OK` с актуальными данными водителя.

## Примечания
- Требует авторизации с ролью `dispatcher` или `admin`.
- Полные детали схем доступны в OpenAPI ReDoc для v0.
