# Funnel Dashboard

This dashboard visualises user journeys across the key events defined in `analytics_events.md`.

## Data model

Each analytics event includes an `id` and optional metadata. Store events in a table with at least:

- `id` – event identifier
- `name` – event name
- `ts` – timestamp
- `meta` – JSON payload

The `id` lets you join consecutive events to reconstruct funnels.

## Looker/Metabase setup

1. Connect the events table to your BI tool.
2. Create a funnel view with steps ordered by `ts` and grouped by `id`.
3. Build visualisations for drop‑off between steps.
4. Filter by properties in `meta` (e.g. `surface`, `position`).

## Example SQL

```sql
select id, name, ts
from events
where name in ('cta.nav.join','form.newsletter.submit')
order by ts;
```

This query can be the basis for funnels tracking sign‑up journeys.
