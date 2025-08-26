# Design Tokens

Technofatty centralizes all design tokens in [`_variables.scss`](../coresite/static/coresite/scss/abstracts/_variables.scss). Tokens are exposed as SCSS maps and mirrored to CSS custom properties for runtime use.

## Token scales
The token file defines several scales used throughout the site:

- **Colors** – brand and UI colors used for backgrounds, text, and accents.
- **Spacing** – t‑shirt‑sized spacing units (`--space-1` … `--space-8`).
- **Typography** – font sizes, families, line heights and display scales.
- **Layout & Dimensions** – container widths, component sizes and breakpoints.
- **Radii, border widths, blurs, shadows & z-index layers** – primitives for shape, depth and layering.

## Naming conventions
Token names are short, lowercase, and use hyphens only when necessary (`text-strong`, `bg-accent-light`). Each scale is namespaced in CSS with a clear prefix, e.g. `--color-blue`, `--space-4`, `--radius-sm`. Names should describe intent rather than specific values; prefer `--color-green` over `--color-00ff00`.

## Approval workflow
1. Propose additions or changes in a pull request updating `_variables.scss` and any affected documentation.
2. Design reviews ensure names, purpose, and contrast requirements fit the system.
3. Engineering reviews confirm the token doesn't duplicate an existing value and is used consistently.
4. Once approved, the token is merged and released.

## Versioning policy
Tokens follow a semver-like scheme:

- **MAJOR** – removing a token or altering its meaning.
- **MINOR** – adding a new token or deprecating an old one.
- **PATCH** – fixing values or documentation without changing intent.

Consumers should pin the token package and update only after reviewing breaking changes.

## Accessibility & contrast
Color tokens used for text or interactive elements must meet WCAG 2.1 AA contrast ratios: at least **4.5:1** for normal text and **3:1** for large text (≥24px or 19px bold). Use tools like `npm contrast` or browser inspectors to verify combinations. Avoid introducing tokens that cannot meet these thresholds in typical foreground/background pairings.
