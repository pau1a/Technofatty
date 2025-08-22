# Global cleanup log – 2025-08-22

## About page canonical H1
- **before**: `coresite/templates/coresite/partials/about/about-hero.html` began with an `<h2>`; page rendered with no `<h1>`.
- **after**: added `<h1 class="visually-hidden" id="about-page-heading">About</h1>` above the existing `<h2>` so the About page now exposes a single page-level heading.

## Contact section wrappers
- **before**: Sections in `coresite/templates/coresite/contact.html` lacked the standard `class="section"` and `role="region"` semantics.
- **after**: each `<section>` now includes `class="section" role="region"` with unchanged `aria-labelledby` references, restoring wrapper parity.

## Signal placeholder semantics
- **before**: `coresite/templates/coresite/signal_placeholder.html` used a visible `<h1>` and omitted `role`/`aria-labelledby` on its section wrapper.
- **after**: section now has `role="region" aria-labelledby="signal-placeholder-heading"`; inserted a hidden `<h1>` with that ID and converted the visible heading to `<h2>` to maintain hierarchy.
