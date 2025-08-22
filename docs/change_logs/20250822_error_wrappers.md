# Standardize error page section wrappers

- `coresite/templates/404.html`: replaced `<section class="error">` with `<section id="error-404" class="section" role="region" aria-labelledby="error-404-heading">; the page `<h1>` now carries `id="error-404-heading"`.
- `coresite/templates/500.html`: replaced `<section class="error">` with `<section id="error-500" class="section" role="region" aria-labelledby="error-500-heading">; the page `<h1>` now carries `id="error-500-heading"`.
