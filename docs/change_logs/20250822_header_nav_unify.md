# Header & Navigation Global Partial Unification

## Before
- Template with header/nav markup: `coresite/templates/coresite/base.html`
- Duplicate link lists existed in desktop nav and overlay menu.
- Link order was consistent (`Home`, `About`, `Services`, `Contact`), but the "Join Us" CTA was outside the desktop list and inside the overlay list.

## After
- Single partial path: `coresite/templates/coresite/partials/global/header_nav.html`
- Pages inheriting the partial via `base.html`:
  - `coresite/templates/coresite/about.html`
  - `coresite/templates/coresite/community_join.html`
  - `coresite/templates/coresite/contact.html`
  - `coresite/templates/coresite/homepage.html`
  - `coresite/templates/coresite/legal.html`
  - `coresite/templates/coresite/services.html`
  - `coresite/templates/coresite/support.html`
  - `coresite/templates/coresite/signal_placeholder.html`
- CTA wording standardized to "Join Us".
