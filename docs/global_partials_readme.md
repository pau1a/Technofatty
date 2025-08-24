# Global Partials

This page outlines the shared partial templates used across Technofatty. Each entry explains the partial’s purpose, where it lives, and which templates include it.

## Conventions

### Single page-level H1
Pages use only one `<h1>`. When a design calls for a visually hidden title, the first partial renders the `<h1>` with `class="visually-hidden"` followed by a visible `<h2>`【F:coresite/templates/coresite/partials/contact/contact-intro.html†L1-L2】.

### Section wrapper pattern
Content blocks are wrapped in:

```html
<section id="section-id" class="section" role="region" aria-labelledby="section-id-heading">
  <div class="wrap">
    ...
  </div>
</section>
```
The `id` matches the heading’s `-heading` suffix. Example usage appears throughout `about.html`【F:coresite/templates/coresite/about.html†L20-L24】.

### Design tokens
All styling values come from `_variables.scss`, the single source of truth for SCSS/CSS tokens【F:coresite/static/coresite/scss/abstracts/_variables.scss†L1-L8】.

### Consent-aware analytics
Analytics is tied to the site's consent banner. Until a user grants tracking permission, the analytics partial outputs nothing and no tracking scripts run【F:coresite/templates/coresite/partials/global/analytics.html†L1-L30】.

## Partial reference

### Analytics
* **Path**: `coresite/templates/coresite/partials/global/analytics.html`
* **Purpose**: Loads the provider snippet and tiny event dispatcher only after tracking consent is granted【F:coresite/templates/coresite/partials/global/analytics.html†L1-L30】
* **Included in**: `base.html` (thus every page)【F:coresite/templates/coresite/base.html†L21-L23】

### Header and primary navigation
* **Path**: `coresite/templates/coresite/partials/global/header_nav.html`
* **Purpose**: Renders the site header, desktop navigation, and mobile menu. Pulls in navigation links and the primary call-to-action.
* **Included in**: `base.html` (thus every page)【F:coresite/templates/coresite/base.html†L18】

### Navigation links
* **Path**: `coresite/templates/coresite/partials/global/nav_links.html`
* **Purpose**: Canonical list of primary site links reused across header, mobile menu, and footer navigation.
* **Included in**: `header_nav.html`, `includes/footer_links.html`

### Navigation CTA
* **Path**: `coresite/templates/coresite/partials/global/nav_cta.html`
* **Purpose**: Renders the "Join Us" button in navigation【F:coresite/templates/coresite/partials/global/nav_cta.html†L1】
* **Included in**: `header_nav.html`【F:coresite/templates/coresite/partials/global/header_nav.html†L10-L12】

### Footer
* **Path**: `coresite/templates/coresite/partials/global/footer.html`
* **Purpose**: Site-wide footer with link groups and meta information【F:coresite/templates/coresite/partials/global/footer.html†L1-L44】
* **Included in**: `base.html` (thus every page)

### Featured grid
* **Path**: `coresite/templates/coresite/partials/featured_grid.html`
* **Purpose**: Grid of featured resources cards【F:coresite/templates/coresite/partials/featured_grid.html†L3-L18】
* **Included in**: `homepage.html`

### Newsletter sign-up block
* **Path**: `coresite/templates/coresite/partials/newsletter_block.html`
* **Purpose**: Email subscription form and status messaging【F:coresite/templates/coresite/partials/newsletter_block.html†L2-L27】
* **Included in**: `homepage.html`

### Signals block
* **Path**: `coresite/templates/coresite/partials/signals_block.html`
* **Purpose**: Grid of current signals with optional CTAs【F:coresite/templates/coresite/partials/signals_block.html†L1-L27】
* **Included in**: `homepage.html`

### Support block
* **Path**: `coresite/templates/coresite/partials/support_block.html`
* **Purpose**: Support resources grid with optional intro text【F:coresite/templates/coresite/partials/support_block.html†L1-L17】
* **Included in**: `homepage.html`

### Community block
* **Path**: `coresite/templates/coresite/partials/community_block.html`
* **Purpose**: Community call-to-action and secondary links【F:coresite/templates/coresite/partials/community_block.html†L1-L23】
* **Included in**: `homepage.html`

### Trust section
* **Path**: `coresite/templates/coresite/partials/trust.html`
* **Purpose**: Highlights benefits with icon grid and follow-up CTA【F:coresite/templates/coresite/partials/trust.html†L1-L18】
* **Included in**: `homepage.html`

### Hero section
* **Path**: `coresite/templates/coresite/partials/hero.html`
* **Purpose**: Media-rich hero banner at top of the homepage【F:coresite/templates/coresite/partials/hero.html†L1-L27】
* **Included in**: `homepage.html`

### Global notice placeholder
* **Status**: No global notice partial exists yet; site currently has no mechanism for site-wide alert banners.

## Inclusion map
- All templates → analytics
- `coresite/templates/coresite/homepage.html` → header_nav, hero, trust, featured_grid, newsletter_block, signals_block, support_block, community_block
- `coresite/templates/coresite/about.html` → header_nav
- `coresite/templates/coresite/contact.html` → header_nav
- `coresite/templates/coresite/legal.html` → header_nav
- `coresite/templates/coresite/support.html` → header_nav

Pages without additional partials are intentionally minimal; they inherit analytics, the header, and footer via `base.html`.
