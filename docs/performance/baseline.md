# Performance Baseline

This document records baseline performance metrics and target budgets for the project.

## Baseline Metrics
- Bootstrap CSS (`node_modules/bootstrap/dist/css/bootstrap.min.css`): 232,111 bytes (~227 KB)
- Bootstrap JS (`node_modules/bootstrap/dist/js/bootstrap.bundle.min.js`): 80,496 bytes (~79 KB)

## Target Budgets
- CSS bundle size ≤ 250 KB
- JavaScript bundle size ≤ 90 KB
- Image assets per page ≤ 300 KB total

## Asset Checklist
- Provide explicit width and height for images to avoid layout shifts.
- Use `loading="lazy"` for images below the initial viewport.
- Apply spacing using design tokens (`--space-1` … `--space-8`) instead of hard-coded values.

