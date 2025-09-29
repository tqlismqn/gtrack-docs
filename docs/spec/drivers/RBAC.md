# Модуль «Водители (Driver)» — RBAC & Маскирование v0.1

## Роли

* `admin` — полный доступ, override, legal hold, настройки нотификаций
* `hr_lead` — полные документы и банковские (read), скачивание
* `hr` — документы полностью; банки с маской; скачивание
* `dispatcher` — операционные данные; номера документов замаскированы; без банков/скачиваний
* `accountant` — банковские полностью (R/W); документы с маской; без скачиваний
* `driver(self)` — свой профиль полностью; загрузка документов (state = pending_approval)

## Multi-Role & Groups

* Роли выдаются пользователю и/или группе; `effectiveRoles = union(userRoles ∪ groupRoles)`
* Если хотя бы одна роль даёт право — оно разрешено (R/W/D)

## AccessRequest (временный доступ)

* `scopes`: `bank_full`, `doc_numbers_full`; `approver`: `hr_lead|admin`; срок по умолчанию 8 часов
* Раскрытия без масок логируются (`data_view_unmasked`)

## Маскирование

* Документы/нац. ID: `****1234` (последние 4); видят полностью `admin/hr/hr_lead/driver(self)`
* Банки: полностью `admin/accountant/hr_lead/driver(self)`; `hr` — маска; остальные — нет доступа

## Скачивания вложений

* `admin/hr/hr_lead/driver(self)` (свои) — разрешено; все скачивания — в AuditLog
