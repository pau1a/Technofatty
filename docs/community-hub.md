# Community Hub

## Overview

The Community Hub lists discussion threads and allows visitors to browse, ask new questions, or subscribe for updates.

### Headline & Subhead
- **Technofatty Community** (H1)
- Subhead: "Get practical answers from peers and TF staff on growth, content, analytics, and tools."

### Calls to Action
- **Ask a Question** – primary CTA directing users to create a new thread.
- **Subscribe to Updates** – secondary CTA for email notifications.

### Filters
Server‑rendered filter strip with:
- **Latest** – default view.
- **Unanswered** – shows threads without an accepted answer.
Tag filtering is available via tag pills on thread cards.

### Pagination
Top and bottom pagers navigate through thread pages.

### Thread Cards
- Title (H2) linking to the thread
- Tag pills linking to tag-filtered views
- Byline showing the author
- Reply count and updated timestamp
- Optional "✓ answered" indicator when accepted answer exists

### Related Content
A block titled **Related across TF** shows up to:
- Two Knowledge Articles
- One Tool
- One Case Study
Items render as cards with small source labels (e.g., "From Knowledge") and collapse when content is missing. Results are based on shared tags with the current filter.

### Accessibility
- Global “Skip to content” targets the thread list.
- Landmarks: `main`, `nav`, and `footer` are present.
- All controls are keyboard reachable with visible focus rings and non–color cues.

### Performance
- Minimal server rendering; no blocking scripts.
- Pagination limits payload to 10 threads per page.

### SEO
- `<title>` ≤60 chars and `<meta name="description">` ≤155 chars.
- Canonical URL points to `/community/`.
- JSON-LD: `CollectionPage` containing an `ItemList` for threads and `BreadcrumbList` for navigation.
- Robots: set `<meta name="robots">` and `X-Robots-Tag` to `index,follow` only when `COMMUNITY_INDEXABLE` is true; otherwise `noindex,nofollow`.

### Telemetry
- `community.view_hub`
- `cta.community.ask_question`
- `cta.community.subscribe_updates`
- `community.filter.latest`
- `community.filter.unanswered`
- `community.filter.tag` (includes selected tag in metadata)

All community events include payload properties:
- `surface` – always "community"
- `filter` – current filter when relevant
- `position` – location of the control (e.g., "header", "footer")
- `tag` – selected tag for tag events

Events are emitted only after consent; before consent, event senders must no-op.

### Gating & Tests
- Canonical URL and JSON-LD schema are regression-tested for stability.
- Hero copy and analytics event tokens are snapshot-tested to guard accidental changes.
- `community.view_hub` fires only when consent enables `tfSend`.
- Sitemap validation honors `ENV`/`CANONICAL_HOST` environment variables.

