# Python Runtime Strategy

## Current Version
- Production runtime: **Python 3.8**
- Official end-of-life: **October 2024** (per [PEP 569](https://peps.python.org/pep-0569/))

## Rationale for Deferral
- Key dependencies have not yet released Python 3.12–compatible versions.
- Upgrade would require coordinated testing across multiple services.
- Available engineering time is prioritized for feature delivery until EOL nears.

## Recurring Review
A scheduled GitHub Action creates an issue on the first of each month reminding the team to revisit the upgrade plan. The reminder continues until Python 3.8 reaches end-of-life.

## Path to Python 3.12
1. **Dependency Audit** – catalog all runtime and build dependencies and confirm 3.12 support.
2. **Staging Validation** – deploy the upgraded stack to staging with representative data and traffic.
3. **Rollback Preparedness** – document and test procedures to revert to 3.8 if critical regressions surface.

## Next Steps
- Monitor dependency roadmaps and unblock upgrades as 3.12 compatibility lands.
- Follow reminders to reassess readiness at least monthly.
- Target production rollout ahead of the October 2024 EOL to retain support coverage.

- Capture lessons learned after the upgrade to inform future runtime transitions.
