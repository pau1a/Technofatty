# Technofatty

## Setup

### Requirements
- Python 3.12

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py check
```

### Run server

```bash
python manage.py runserver
```

### Tests

```bash
pytest
```

## Configuration

The application reads configuration from environment variables.

- **Local development**: copy `.env.example` to `.env` and fill in your values. `make dev` loads this file automatically.
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
- `TF_EMAIL_BACKEND`

See `.env.example` for placeholder values.

## Deployment

See `docs/deployment.md` for details on production deployment with Apache + mod_wsgi.

## Internal Strategy Docs

For collaborators:  
We maintain internal notes on site philosophy, content strategy, and revenue pathways.  
See [`docs/strategy.md`](docs/strategy.md) for the latest thinking.  

## License
MIT
