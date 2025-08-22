# Task Spec: Header & Navigation — Global Partial and De‑duplication (Technofatty)

Objective
Unify the site header and primary navigation into a single global partial to remove duplicated link markup, add missing accessibility labels, and ensure every page consumes the same source of truth. No design changes, no JavaScript, no new dependencies.

Scope
Extract the current header and nav markup from base.html and any page‑level templates that repeat it. Create one global partial for header+nav and include it from base.html so all pages inherit it automatically. Preserve existing link order, link text, URLs, and classes. Add an explicit aria-label to the <nav> element to identify its purpose. Where both desktop and overlay menus exist, both must render from the same include so link lists are not duplicated.

Constraints
Do not alter visual styles or introduce new classes. Do not change routing or link destinations. Do not modify any SCSS tokens; if styles reference hardcoded values elsewhere, leave them for the separate SCSS tokenization task. Keep the current skip link behavior intact. No new dropdown or menu logic.

Accessibility requirements
One primary <nav> landmark with aria-label="Primary". Heading order must remain unchanged. Focus order through the header must be logical and match the visual order. If there is an overlay or secondary nav pattern, it must consume the same list of links via the global partial so screen readers encounter identical link sets.

File and path conventions
Place the new partial at coresite/templates/coresite/partials/global/header_nav.html. Reference it from coresite/templates/coresite/base.html. Remove any page‑level nav duplicates and ensure only the base template includes the header partial. If there is a separate overlay menu shell, keep its container but include the shared link list inside it rather than re‑writing the links.

Evidence handling
Before: record the template paths that currently contain header/nav markup and note any differences in link order or labels. After: list the single partial path and the pages that now inherit it through base.html. Store these notes in docs/change_logs/<YYYYMMDD>_header_nav_unify.md. If any link text differs between duplicates, flag it and resolve to the currently approved wording; note the decision in the change log.

Verification
Run the site and inspect any page. Confirm there is exactly one primary <nav> landmark, the aria-label is present, and both desktop and overlay menus show identical link lists. Use keyboard only to tab through the header; focus rings remain visible and traversal order is unchanged. View source on two different pages and confirm the header markup is identical. No console errors, no template include errors.

Acceptance
All pages render the same header from a single include. The primary <nav> has an aria-label. No visual diffs beyond the removal of duplicated markup. No broken or missing links. Skip link remains functional. Commit message: refactor(nav): centralize header+primary nav into global partial; add aria-label.

