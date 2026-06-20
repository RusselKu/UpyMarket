# UpyStoreMarketplace

A static, modular student e-commerce prototype designed to collect click and dwell telemetry tied to onboarding attributes.

## Structure

- `/index.html` landing page with catalog, onboarding modal, and analytics canvas
- `/assets/style.css` responsive base styles
- `/assets/catalog.json` product metadata by category
- `/scripts/onboarding.js` captures and stores career + gender
- `/scripts/telemetry.js` click + dwell telemetry stubs
- `/scripts/supabaseClient.js` Supabase client and insert helper
- `/charts/analytics.js` Chart.js placeholder dashboard

## Local usage

Because this is a static GitHub Pages-style project, open `index.html` in a browser (or run any static file server).

To connect telemetry inserts to Supabase in production, expose:

- `window.UPYSTORE_SUPABASE_URL`
- `window.UPYSTORE_SUPABASE_ANON_KEY`

.