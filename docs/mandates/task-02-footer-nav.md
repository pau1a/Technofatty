Mandate: Task 2 — Unify Footer Navigation
=========================================

**Objective**
The footer must not have its own hard-coded link set. It must consume the canonical `coresite/templates/coresite/partials/global/nav_links.html` partial that is already used for the header. This ensures a single source of truth for navigation, consistent link copy, and a DRY structure.

**Constraints**
- No hard-coded anchors in the footer template.
- The only include call-sites for navigation are the header and footer.
- ARIA labels present in the partial must be preserved and surfaced into both header and footer.
- Link copy in footer must match header unless specifically extended.
- Styling must use SCSS tokens defined in `_variables.scss`, not inline classes.
- Mobile-first design intent is to be respected.

**Footer-only items**
Where footer requires additional links (e.g., Legal, Privacy, Terms), these are to be passed as parameters to `nav_links.html`, or by introducing a lightweight footer extension partial that delegates to `nav_links.html`. No second canonical link source is permitted.

**Definition of Done**
- Header and footer render the same canonical link set.
- Footer-only items are passed via parameters or extension partial, not re-defined.
- Exactly two include call-sites exist across the repo: one in the header, one in the footer.
- No direct anchors to the five pillars or secondary pages exist outside `nav_links.html`.
- Header/footer parity confirmed visually on desktop and mobile viewports.
- Accessibility landmarks (ARIA labels) validated in both places.
- Styling confirmed to use only SCSS tokens, not hard-coded inline rules.

**Verification Artefacts**
- Repo `grep` output showing two include call-sites only.
- Repo `grep` output showing no direct anchors to pillars/secondary pages outside the partial.
- Screenshots of header/footer on mobile and desktop proving parity.
- Confirmation note that aria-labels pass automated checks (e.g. WAVE/AXE).
- Optional: attach Lighthouse/Performance snippet proving no regressions introduced.

**Guidance to Ged where uncertain**
- If the canonical path of the partial differs (e.g. casing, folder structure), resolve to the actual repo location and confirm.
- If footer requires analytics data-attributes, extend via parameters, not by forking.
- If SCSS tokens appear missing for footer layout, escalate to Paula for definition rather than inventing ad-hoc classes.
- If ambiguity arises between cloning for mobile vs including twice, defer to Paula’s instruction; default is two canonical include call-sites only.
