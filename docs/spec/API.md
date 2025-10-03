# API v1 — Laravel 10 (v2.9.0)

## Аутентификация
- Laravel Sanctum (SPA cookie), CORS: app.g-track.eu, localhost:4200
- Роли/права: spatie/permission — Admin, HR, Dispatcher, Accounting, Driver

## Эндпоинты (префикс `/api/v1`)
- GET  /drivers?status=&expiresInDays=
- GET  /drivers/{id}
- POST /drivers
- PUT  /drivers/{id}
- DELETE /drivers/{id}
- GET  /drivers/{id}/documents
- POST /drivers/{id}/documents
- DELETE /drivers/{id}/documents/{docId}
- POST /import/drivers-excel  — ставит задачу в очередь (Excel → batch parse → validate → upsert)
- GET  /health  — простой healthcheck

## Коды ошибок и валидация
- FormRequest на создание/обновление Driver и DriverDocument.
- Ошибки импорта — файл отчёта с номерами строк и описанием.
