# Drivers Demo Scaffold

## Purpose
- Provide a static, host-routed demo environment for showcasing the Drivers experience without backend dependencies.
- Enable the `demo.g-track.eu` domain to serve a curated build of drivers-related assets from within the main Next.js project.

## Scope
- Covers static assets, routing, and baseline documentation necessary to host the Drivers demo.
- Excludes dynamic data integrations, authentication, or production telemetry.

## Information Architecture
- **Layout:** Single page with hero banner and contextual copy.
- **Navigation:** Left-side table of contents for feature highlights.
- **Status Badges:** Right-aligned badges summarising release state and availability windows.
- **Drawer:** Collapsible drawer for supplementary references and download links.

## Routing
- All demo assets are hosted under `/demo/drivers/` and are served when requests originate from `demo.g-track.eu`.
- Internal links must remain within the `/demo/drivers/` namespace.

## Limitations
- No backend or API connectivity; data shown must be static.
- No authenticated features; user flows are limited to unauthenticated browsing.
- No analytics or tracking scripts beyond essential platform instrumentation.

## Acceptance Criteria
- Visiting `/demo/drivers/` returns the static scaffold page without Next.js errors.
- Requests sent to `demo.g-track.eu` are rewritten to the `/demo/drivers/` assets.
- Documentation is updated to include UX scope, routing rules, and DNS instructions.
