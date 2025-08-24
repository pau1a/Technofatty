# Production-safe settings & static pipeline

- Introduced a single `ENV` flag controlling debug, hosts and analytics.
- Hardened production security with SSL redirects, secure cookies and HSTS.
- Static collection now targets `static_collected` with hashed filenames and offline compilation.
- Added logging filter to skip static requests and optional Sentry wiring.
- Updated robots.txt view to rely on environment flag.
- Documented default environment values in `.env.example` for deterministic deploys.
