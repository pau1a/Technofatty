# Rollout Checklist

- [ ] Run full test suite.
- [ ] Verify legacy redirects in the staging environment before deploying to production.
- [ ] Confirm critical pages respond with expected status codes.
- [ ] Configure monitoring probes: GET /health/live/ (liveness) and /health/db/, /health/cache/ (readiness) every 10s with 2s timeout.
