# Security Practices (Drivers Security Pack)

## TLS и транспорт

* Все внешние соединения проходят через HTTPS (Railway + Cloudflare proxy, TLS 1.2+).
* Внутренний трафик между сервисами защищён туннелем Railway; прямой доступ к БД извне закрыт.

## Контроль доступа и RLS

* В PostgreSQL включено Row Level Security для таблиц `drivers` и `audit_driver_reveals`.
* Политики RLS проверяют `app_role` из заголовка `APP_ROLE_HEADER`.
* Роли с доступом к раскрытию: `operations.admin`, `support.senior`. Остальные получают только маскированные данные.

## Аудит и мониторинг

* Каждое обращение к `POST /drivers/:id/reveal` создаёт запись в `audit_driver_reveals` (id пользователя, роль, причина, IP, user-agent).
* Логи передаются в централизованный Logtail (30 дней хранения) и в S3-compatible архив (1 год).
* Еженедельная проверка аудита — ответственный: Security Lead.

## Бэкапы и восстановление

* Автоматические snapshot Railway PostgreSQL: каждые 24 часа, хранение 7 дней.
* Раз в неделю выполняем off-site бэкап в EU S3 (верификация checksum).
* Тест восстановления (restore drill) — ежеквартально, минимум 5 записей PII.

## Размещение данных (EU)

* Railway регион: `eu-central` (Франкфурт).
* Внешние хранилища (S3) — регион `eu-central-1`.
* Экспорт данных за пределы EU запрещён без DPA.

## Управление доступами

* Доступ к Railway project — только через SSO (Okta) с MFA.
* DBA и Security Lead имеют права на ротацию ключей; разработчики — read-only к реплике без PII.
* Каждые 90 дней проводится ревью доступов и отзыв неиспользуемых аккаунтов.
