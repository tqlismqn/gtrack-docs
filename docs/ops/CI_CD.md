# CI/CD (v2.9.0)

## gtrack-docs
- Build: `mkdocs build --strict`
- Checks: Docs - Preview (PR), Docs - Deploy (main)

## gtrack-frontend (Angular 17)
- Node 20.x (Vercel runtime)
- Steps: `npm ci` → `npm run build`
- Artifact: `dist/gtrack-frontend`
- Deploy: Vercel (Production / Preview environments)

## gtrack-backend (Laravel 10)
- PHP 8.3, Composer ≥2.2
- Steps: `composer install --no-dev --optimize-autoloader` → `php artisan migrate --force` → `php artisan test`
- Deploy: Laravel Cloud (auto post-deploy: `config:cache`, `route:cache`, `view:cache`, `event:cache`)
