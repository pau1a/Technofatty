# Technofatty

## Configuration

The application reads configuration from environment variables.

- **Local development**: copy `.env.example` to `.env` and fill in your values. `make dev` loads this file automatically.
- **CI**: the workflow in `.github/workflows/ci.yml` injects the required environment variables.
- **Production**: variables are provided by a systemd `EnvironmentFile` outside this repository.

Required variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_CONN_MAX_AGE`
- `NEWSLETTER_PROVIDER`
- `OPT_IN_MODE`
- `NEWSLETTER_TIMEOUT_SECONDS`
- `ANALYTICS_ENABLED`
- `ANALYTICS_PROVIDER`
- `ANALYTICS_SITE_ID`
- `CONSENT_REQUIRED`

See `.env.example` for placeholder values.
