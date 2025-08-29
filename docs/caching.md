# Caching Strategy

This project uses multiple caching layers to reduce response time and load on the application.

## Homepage featured grid
- The `featured_grid` template fragment is cached for one hour with a key that changes when resources or case studies are edited.
- No manual invalidation is required; updating content automatically produces a new cache key.

## Sitemap
- The `/sitemap.xml` output is cached for one hour.
- Saving a `BlogPost` or `CaseStudy` automatically clears the cache to keep listings fresh.

## JSON-LD blocks
- Rendered JSON-LD script tags are cached using a hash of their content for one hour.
- Any change to the underlying data automatically generates a new hash and refreshes the cache.

## Static assets
- Static files use hashed filenames via `ManifestStaticFilesStorage`.
- Long‑lived `Cache-Control` headers should be set by the web server or CDN (e.g. Apache `Header` directive).

## General invalidation
- Clearing the default cache clears view and fragment caches.
- Deployments that change static assets automatically bust CDN caches thanks to hashed filenames.
