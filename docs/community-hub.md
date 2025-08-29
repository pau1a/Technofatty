# Mandate for Ged — Deliverables for `/community/`

This is a **strategy + design directive**. Ged’s job is to implement it faithfully, with no improvisation. It will live in `docs/community-hub.md` so that all contributors treat it as source-of-truth.

---

## 1. Page Identity

* **H1:** `Technofatty Community`
* **Subhead:** one crisp sentence: *“Get practical answers from peers and TF staff on growth, content, analytics, and tools.”*
* **Primary CTA (accent button):** “Ask a Question”
* **Secondary CTA (secondary button):** “Subscribe to Updates”
* **Meta title (≤60 chars):** `Technofatty Community — Questions & Discussions`
* **Meta description (≤155 chars):** `Ask questions, get practical answers, and learn from peers and TF staff across growth, content, analytics, and tools.`

---

## 2. Above-the-Fold Layout

* Global header remains intact (nav + logo).
* Beneath header: H1, subhead, two CTAs.
* **Filter strip** below CTAs: [Latest] [Unanswered] [Tags] — must be server-rendered (progressive enhancement), not JS-only.
* First two–three thread cards visible immediately (mobile-first viewport).

---

## 3. Thread Card Contract

Each card is an H2 link. Must include:

* Title (full, wrap lines).
* 2–3 tags (max).
* Reply count + “last updated” timestamp.
* Optional: small byline for human flavor.
* If answered: muted ✓ marker, visually distinct but not dominant.

Accessibility rules:

* Semantic headings (H2).
* Focus outlines and labels enforced via SCSS tokens.
* Contrast at WCAG AA minimum.

---

## 4. List & Pagination

* List is paginated, not infinite scroll.
* Page numbers + prev/next at top and bottom.
* Empty states: friendly message + CTA to create thread.

---

## 5. Related Across TF Block

* Appears after thread list.
* Pulls in: 2 Knowledge Articles, 1 Tool, 1 Case Study, based on tag overlap.
* Uses existing card pattern with a label (“From Knowledge / Tools / Case Studies”).
* If no matches, block collapses — no filler.

---

## 6. Footer Anchors

* Always includes link to **Community Code of Conduct**.
* Newsletter signup repeats gently (a second chance).

---

## 7. Structured Data

Emit JSON-LD:

```json
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Technofatty Community — Questions & Discussions",
  "url": "https://technofatty.com/community/",
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type":"ListItem","position":1,"name":"Home","item":"https://technofatty.com/"},
      {"@type":"ListItem","position":2,"name":"Community","item":"https://technofatty.com/community/"}
    ]
  },
  "mainEntity": {
    "@type": "ItemList",
    "itemListOrder": "https://schema.org/ItemListOrderDescending",
    "numberOfItems": 10,
    "itemListElement": []
  }
}
```

Ged must populate `itemListElement` with thread links dynamically.

---

## 8. Telemetry & Consent

* Fire only after consent cookie is present (ConsentMiddleware).
* Events:

  * `community.view_hub` (on load)
  * `community.filter_change` (with `filter=latest|unanswered|tags`)
  * `community.cta_click` (with `cta=ask|subscribe`)
* Namespace: `surface=community`

---

## 9. Performance & Assets

* Text-first: no hero video.
* Thumbnails only if strictly necessary; if so, must declare width/height + lazyload.
* CSS critical path only; Bootstrap + SCSS tokens; no ad-hoc hex.

---

## 10. Accessibility Enforcement

* “Skip to content” link must land on list.
* Proper landmarks (`<main>`, `<nav>`, `<footer>`).
* Focus outlines visible.
* Tokens control spacing, colors, focus states.

---

## 11. Crosslinks & Neural Net Philosophy

* Hub is not siloed. It links sideways into Knowledge, Tools, Case Studies, Blog.
* Every thread card page must also link back into Hub (“Return to Community”).
* Tag taxonomy must be consistent across all sections.

---

This page is therefore:

* The **indexable doorway** to community (with env flag controlling robots.txt).
* A **subscription driver** (Pulizzi’s content marketing doctrine).
* A **trust anchor** (conduct + governance visible).
* A **lateral node** in the TF neural net.

