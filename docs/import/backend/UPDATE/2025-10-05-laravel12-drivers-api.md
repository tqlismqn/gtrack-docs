# Laravel 12 Upgrade & Drivers API

## Overview
- Migrated the backend from Laravel 10 to Laravel 12 with PHP 8.2+ support and the slim bootstrap configuration.
- Introduced a dedicated `/api/drivers` REST API for managing demo driver records.
- Seeded 9 demo drivers mirroring the public demo data set.
- Hardened CORS configuration for demo domains and aligned automated tests.

## Framework Changes
- Composer dependencies upgraded to target `laravel/framework ^12.0`, Sanctum 4.x, PHPUnit 11, and supporting packages.
- Removed legacy Kernel bindings in favour of the Laravel 12 `bootstrap/app.php` slim skeleton.
- Routing definitions consolidated into the new bootstrap configuration while retaining the existing `api/v1` module routes.

## Drivers Domain
### Database
- New `drivers` table (UUID PK) with personal data, employment fields, document JSON payloads, salary breakdown, and indexes on status/citizenship/workplace.
- Seeder `DemoDriversSeeder` truncates and populates 9 demo driver rows with realistic passports, permits, and salary data.

### API Endpoints (`/api/drivers`)
| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/drivers/` | List drivers with document expirations converted to `days` remaining. |
| POST | `/api/drivers/` | Create a driver; UUID generated server-side. |
| PUT | `/api/drivers/` | Bulk replace driver list (transactional). |
| PUT | `/api/drivers/{id}` | Partially update an existing driver. |
| DELETE | `/api/drivers/` | Bulk delete by driver IDs. |

### Payload Notes
- `status`: `Active`, `OnLeave`, `Inactive`.
- `citizenship`: `CZ`, `EU`, `Non-EU`.
- `contract_type`: `Срочный`, `Бессрочный`.
- `docs` entries accept either `expires_at` (ISO date) or pre-calculated `days`. Server responses always include `days` when `expires_at` provided.
- `salary` JSON supports keys: `base`, `bonus`, `deductions`, `trips`, `perDiem`.

## Configuration
- `config/cors.php` restricts exposure to API routes and consumes `CORS_ORIGINS` from environment (`.env.example` updated).
- `DatabaseSeeder` executes the driver seeder alongside existing seed routines.

## Testing & Deployment
- Feature tests cover CRUD, bulk replace/delete, and seeded driver expectations (`phpunit`).
- Run migrations and seeders post-deploy: `php artisan migrate --seed`.
- Validate CORS headers for `https://demo.g-track.eu` via automated or manual smoke tests before promoting to Laravel Cloud demo environment.
