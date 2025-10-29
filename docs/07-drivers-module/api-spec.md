# Drivers Module - API Specification | Модуль водителей - API спецификация

---

## 🇬🇧 English

> **Status:** 🔄 Content being filled from Master Specification v3.1

[Content from Master Spec section 7.1: API endpoints, request/response formats, authentication]

### RESTful Endpoints

**Base URL:** `/api/v0/drivers`

- `GET /api/v0/drivers` - List drivers (paginated)
- `GET /api/v0/drivers/{id}` - Get single driver
- `POST /api/v0/drivers` - Create driver
- `PUT /api/v0/drivers/{id}` - Update driver
- `DELETE /api/v0/drivers/{id}` - Delete driver
- `GET /api/v0/drivers/{id}/documents` - Get driver documents
- `POST /api/v0/drivers/{id}/documents` - Upload document

---

## 🇷🇺 Русский

> **Статус:** 🔄 Содержимое заполняется из Мастер-спецификации v3.1

[Содержимое из Мастер-спецификации раздел 7.1: API endpoints, форматы запроса/ответа, аутентификация]

### RESTful Endpoints

**Base URL:** `/api/v0/drivers`

- `GET /api/v0/drivers` - Список водителей (с пагинацией)
- `GET /api/v0/drivers/{id}` - Получить одного водителя
- `POST /api/v0/drivers` - Создать водителя
- `PUT /api/v0/drivers/{id}` - Обновить водителя
- `DELETE /api/v0/drivers/{id}` - Удалить водителя
- `GET /api/v0/drivers/{id}/documents` - Получить документы водителя
- `POST /api/v0/drivers/{id}/documents` - Загрузить документ

---

**Last Updated:** October 29, 2025
**Version:** 2.0.0
**Source:** Master Specification v3.1, Section 7.1 (API)
