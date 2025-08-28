# Telemetry & Data Layer

We measure only what helps improve user value or decisions. Events are human-readable, payloads are minimal and typed.

## Data layer shape
```js
window.tf = window.tf || {};
tf.build = { branch: "{{ BUILD_BRANCH }}", sha: "{{ BUILD_COMMIT }}", at: "{{ BUILD_DATETIME }}" };
tf.identity = { uid: "<anon-or-user-id>", role: "{{ user.is_staff|yesno:'staff,guest' }}" };
tf.page = { kind: "tool|knowledge|blog|home", id: "{{ page_id }}", title: "{{ page_title }}" };
```

## Event naming
`<surface>_<verb>[_<detail>]` e.g. `tool_run`, `tool_result_export`, `blog_read_50`, `knowledge_filter_apply`.

## Canonical payloads
Tool run:
```json
{ "tool": "pricing-calibrator", "capability": "pricing", "variant": "v1", "inputs_hash": "sha256:...", "duration_ms": 1240, "ok": true }
```

Knowledge filter:
```json
{ "category": "pricing", "tag": "estimation", "subtype": "guide", "query": "value-based" }
```

Blog CTA:
```json
{ "post": "the-case-for-interval-forecasting", "cta": "tool", "target": "forecast-interval-builder" }
```

## Implementation note
Emit events with a thin wrapper that no-ops if network is unavailable. Batch where possible. Respect consent flags from `coresite.context_processors.analytics_flags`.

## Current events

These events support upcoming filtering and pagination features:

- `cta.newsletter.subscribe` – click on the newsletter subscribe button. Meta `{ "form": "newsletter" }`
- `form.newsletter.start` – email field focused.
- `form.newsletter.submit` – newsletter form submitted. Meta `{ "form": "newsletter" }`
- `cta.tools.signup` – click on the Tools page signup CTA.
- `cta.tools.open` – open a tool from the Tools page. Meta `{ "tool": "<slug>" }`

## KPIs and how to compute
Time-to-first-value: difference between `tool_run` and `tool_result_render`. Completion rate: `tool_result_render / tool_run` per tool. Assisted conversions: number of sessions that include a `tool_*` event and end with `form_submit` or `booking_start` within 7 days.
