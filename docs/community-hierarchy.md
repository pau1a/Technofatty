# Technofatty Community – Visual Content Hierarchy

This document specifies the required content hierarchy for all Community pages.  
Ged must implement layouts according to this hierarchy, ensuring brand fidelity, accessibility, and conversion alignment.  
Above the fold = visible without scrolling on a standard mobile viewport (375×667).

---

## 1. Hub Page (`/community/`)

**Above the Fold**  
1. Global header (consistent with sitewide design).  
2. H1: “Technofatty Community.”  
3. Tagline (one sentence: purpose of the community).  
4. Primary CTA button: **Ask a Question** (brand accent color).  
5. Secondary CTA button/link: **Subscribe to Updates**.  
6. Filter tabs: Latest | Unanswered | Tags.  
7. First 2–3 thread cards (title, tags, author, reply count, last updated).

**Below the Fold**  
8. Remaining paginated thread cards.  
9. Related content block: Knowledge, Tools, Case Studies, Blog (cross-linked by tags).  
10. Footer: Code of Conduct link, navigation links.

---

## 2. Thread Page (`/community/q/<slug>/` or `/community/t/<slug>/`)

**Above the Fold**  
1. Global header.  
2. H1: thread title.  
3. Thread metadata (author, created date, tags).  
4. Primary CTA: **Subscribe to Updates** (inline, below metadata).  
5. Original post body.  

**Below the Fold**  
6. Replies list (paginated, ordered by time; accepted answer pinned at top if present).  
7. Accepted answer highlighted (distinct background + label).  
8. Inline related content: Knowledge, Tools, Case Studies tagged identically.  
9. Reply form (with email verification flow).  
10. Bottom CTA: **Ask Your Own Question**.  
11. Footer: Code of Conduct link.

---

## 3. Tag Page (`/community/tag/<slug>/`)

**Above the Fold**  
1. Global header.  
2. H1: “Discussions on <Tag>.”  
3. Primary CTA: **Subscribe to <Tag> Updates**.  
4. First 2–3 thread cards (title, reply count, last updated).  

**Below the Fold**  
5. Remaining thread cards (paginated).  
6. Crosslink block: related Knowledge Articles, Tools, Case Studies with same tag.  
7. Footer: Code of Conduct link.

---

## 4. Post Flow (Ask a Question / Start a Discussion)

**Above the Fold**  
1. Global header.  
2. H1: “Ask a Question” (or “Start a Discussion”).  
3. Privacy note: “Your email is never shown publicly.”  
4. Primary CTA: **Submit Your Question** (disabled until form valid).  
5. Form fields:  
   - Title  
   - Body  
   - Tags (with autocomplete from existing tags)  
   - Email  

**Below the Fold**  
6. Guidelines block: Community Code of Conduct.  
7. Post-submission confirmation: “Check your inbox to confirm” (if double opt-in).  
8. Footer navigation.

---

## Layout Standards

- **Above-the-fold CTAs** must be unmissable (brand accent color, consistent button style).  
- **Related content blocks** must use consistent visual patterns across all page types.  
- **Pagination controls** must be visible at both top and bottom of lists.  
- **Accessibility**: all CTAs must have `aria-labels`; headings must follow logical nesting.  
- **Performance**: hero sections must not include videos or heavy media. Text-first priority.

---

## Enforcement

- Any deviation in hierarchy requires stakeholder approval.  
- Ged must implement layouts mobile-first, scaling up to desktop.  
- QA must confirm: above-fold content matches this order exactly on standard mobile viewport.  
- Hierarchy violations are blockers for release.
