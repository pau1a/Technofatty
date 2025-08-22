# Footer global partial log – 2025-08-22

## Footer deduplication
- **before**: `coresite/templates/coresite/about.html`, `community_join.html`, `contact.html`, `homepage.html`, `legal.html`, `services.html`, `signal_placeholder.html`, and `support.html` each overrode a footer block to include `coresite/partials/footer.html`; link sets and labels were identical across pages.
- **after**: the footer now lives at `coresite/templates/coresite/partials/global/footer.html` and is auto-included from `base.html`; all page-level footer overrides were removed.
