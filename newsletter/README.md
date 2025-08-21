# Newsletter

Django app handling newsletter subscriptions for the `#signup` block.

## Configuration

- `NEWSLETTER_PROVIDER` – backend adapter to use (`stub` by default).
- `OPT_IN_MODE` – `single` or `double` opt-in. Selects the success copy.
- `NEWSLETTER_TIMEOUT_SECONDS` – provider timeout (default 3).
- `NEWSLETTER_RATE_LIMITS` – dict with `ip_per_hour` and `email_per_hour` limits.
