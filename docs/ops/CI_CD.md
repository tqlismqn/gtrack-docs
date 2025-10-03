# CI/CD (v2.9.0)

## gtrack-docs
- Build: `mkdocs build --strict`
- Checks: Docs - Preview (PR), Docs - Deploy (main)

## gtrack-app (Angular 17)
- Node ≥18.13
- Steps: `npm ci` → `npm run build`
- Artifact: dist/
- Deploy: static host/Vercel

## gtrack-backend (Laravel 10)
- PHP ≥8.1, Composer ≥2.2
- Steps: `composer install --no-dev --optimize-autoloader` → `php artisan key:generate` → `php artisan migrate --force` → `php artisan test`
- Deploy: Laravel Cloud (primary) или Railway (fallback)
