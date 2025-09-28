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

## UI Overview (2025-09 refresh)
- **Screenshots & Flow:** The demo home state matches the reference mockups shared in Figma (`G-Track / Drivers Demo v3`). The screen opens with a responsive two-pane layout (drivers table + quick badges). Screen captures for release notes are stored in the shared Drive folder `Demo Assets/Drivers/2025-09`.
- **Drawer Interaction:** Selecting a table row or avatar badge opens the right-side drawer with driver details, document indicators, and admin actions.

## Filters & Search
- Global search filters by full name, email or RČ and updates both the table and badge grid in real time.
- Status dropdown limits results to `Active`, `OnLeave`, or `Inactive` records.
- Document status dropdown matches the colour indicator logic: green = `ok` (≥31 days), yellow = `warn` (1–30 days), red = `bad` (expired).
- Pagination controls at the bottom of the table paginate the filtered list in sync with the badge grid.

## Data Persistence
- State lives entirely in the browser via `localStorage` under the key `gtrack_demo_drivers_v1`.
- Removing/adding drivers or editing via drawer actions persists immediately and survives page reloads.

## Add Driver Behaviour
- "＋ Добавить водителя" seeds a new driver with a random Czech/Slovak name, generated RC, email slug, phone number, and randomised document expirations.
- The new driver is prepended to the dataset, the list is re-rendered on page 1, and doc indicators auto-recalculate.
- Drivers created through the button are stored in `localStorage` until manually removed or storage is cleared.
