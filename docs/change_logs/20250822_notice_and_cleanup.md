# Global notice include + SCSS backup removal — 2025-08-22

## Global notice placeholder
- before: no include point in `base.html` for site-wide banners; changes required edits to multiple templates
- after: added `{% include "coresite/partials/global/notice.html" %}` immediately inside `<main>` before the page `{% block content %}` so notices appear early in reading order without affecting page titles
- file added: `coresite/templates/coresite/partials/global/notice.html` (renders empty by default; commented example shows token-only pattern)

## SCSS backup removal
- before: legacy backup file `coresite/static/scss/main.scss.bak` present in repo
- after: removed the file; verified no build references to it

## Verification notes
- rendered `/` and `/about/` — notice include produces no output in default state
- keyboard order unchanged; headings unaffected; one `<h1>` per page maintained
- build compiles without referencing `main.scss.bak`

## Next candidates (tracked elsewhere)
- if a banner is approved, fill the notice partial using `.section`/`.wrap` with `_variables.scss` tokens
- if additional backups exist, remove them via separate housekeeping PR

