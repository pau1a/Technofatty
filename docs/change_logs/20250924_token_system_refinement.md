# SCSS token system refinement

- expanded `_variables.scss` to cover fonts, spacing, radii, borders, shadows, opacity, z-index and component dimensions with CSS custom property output
- updated token helper functions to return `var()` references with fallbacks
- replaced hard-coded values across components (`hero`, `trust`, `hamburger`, `menu-overlay`, `cards`, `grid`, `home`, base styles) with design tokens
- added utility tokens for focus rings and screen-reader helpers
