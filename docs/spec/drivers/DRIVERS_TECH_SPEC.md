# G-Track — Модуль «Водители»: Техническое задание (v2.9)

Дата: 2025-10-03

## 1) Цели, ценность, границы
Цель: реализовать единый модуль управления водителями (Driver): карточка, статусы документов, напоминания, файлы, импорт из Excel, роли и аудит.
Бизнес-ценность: снижение штрафов и простоев за счёт контроля сроков; прозрачность для HR/диспетчеров/бухгалтерии; единая база данных по персоналу и документам.
Границы MVP: без расчёта зарплат/суточных (только учёт), без маршрутизации рейсов, без интеграции с тахографами/трекерами.

## 2) UX и сценарии
Split-layout: слева таблица (список), справа карточка. На мобиле — карточка под таблицей/во вкладке.
Таблица: ФИО; контакты; статус; бейджи документов. Фильтры: search/status/docStatus/euOnly.
Карточка: Персональные → Рабочая инфо → Банковские → Документы → Зарплата/командировочные (учёт) → Файлы → Комментарии → История (AuditLog).
Индикаторы документов: expired (красн.), soon ≤30 (алый), warning 31–60 (оранж.), valid (зел.), unknown (сер.).

## 3) Модель данных (бизнес-уровень)
**Driver:** internal_number, ФИО, birth_date, citizenship, rodne_cislo (условный показ), email, phone, адреса, status (Active|OnLeave|Inactive|Terminated), hire/fire, contract (from/to/indefinite/signed_by), work_location (praha|kladno), bank (CZ: account; non-CZ: IBAN+SWIFT), flags (pas_souhlas, propiska_cz).
**Document:** passport, visa_or_residence, driver_license, tachograph_card, code95, adr_certificate, medical_check, psychotest, insurance, travel_insurance, a1, a1_switzerland, declaration — поля number/country/from/to/categories/files по типу.
Файлы: последняя версия + история загрузок.

## 4) Правила и валидации
rodne_cislo показывать только для CZ граждан или при визе CZ. Банки: CZ→account, иначе→IBAN+SWIFT. Даты from ≤ to (где применимо). Психотест: до 60 — каждые 3 года, после — ежегодно (next due рассчитывает агент).

## 5) Напоминания
Ежедневный cron (UTC 03:00) по документам со статусами expired/soon/warning. Каналы: e-mail, in-app; опц. Telegram/webhook. Настройки per-tenant: включение каналов, пороги daysBefore per document type, получатели; digest-режим.

## 6) Аудит
AuditLog: CRUD по водителям/докам/файлам, входы, рассылки, импорт. Ретеншн 5 лет + Legal Hold.

## 7) Импорт из Excel (MVP v1)
Источник: единый XLSX с листами viza, EU, STL SK, Уволенные, Propiska CZ, UP Prihlashka, UP Odhlasky, e-mail.
Поток: загрузка → парсинг → валидация → предпросмотр → запись. Ошибки: строка/лист/поле + рекомендация.
Ключевой маппинг (лист viza):
- Příjmení a jméno → full_name (сплит в first/last)
- Datum (narození) → birth_date
- Smlouva od/do (+ neurcita) → contract_from/contract_to/contract_indefinite
- Licence od/do → driver_license.from/to (+ number)
- Certifikát A1 od/do → a1.from/to
- Declaration (do) → declaration.to
- Pojištění (do) → insurance.to
- VIZA/BIO / Vizum/Povolení k pobytu → visa_or_residence
- Propiska (+ .1) → propiska_cz + адреса
- PAS / N PAS → passport.number + сроки
- PRAVA / N PRAVA → driver_license.number + сроки
- ADR → adr_certificate
- CHIP / N CHIP → tachograph_card.number + сроки
- 95 KOD (do) → code95.to
- Med prohlídka od/do → medical_check
- Psihotest (date) → psychotest.date (next due по правилу возраста)
- Bank / IBAN/SCET → bank_country+account или IBAN+SWIFT
- Cest. pojištění (do) → travel_insurance.to
- Telefon → phone
Доп. листы: Propiska CZ (адреса/флаг), UP Prihlashka/Odhlasky (история/флаги; Místo výkonu práce Praha/Kladno), e-mail (email/phone + pas_souhlas).

## 8) Роли и права
Admin — Full; HR — CRUD/Upload/Reminders; Dispatcher — Read/Upload/Comments; Accounting — Read/Salary CRUD; Driver — Self-service.

## 9) Нефункциональные
Производительность: 10k записей ≤1.5s (бэк); пагинация/индексы. Безопасность: JWT, CORS, маскирование RČ, лимиты upload. Хранилище: S3-совместимое с версиями. Локали шаблонов: ru, en, cs, uk, pl, de.

## 10) Acceptance
UI split-layout с фильтрами; API базовые ручки; уведомления и импорт XLSX работают; аудит пишет события.
