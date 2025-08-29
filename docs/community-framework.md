# Technofatty Community Section – Strategic Framework

This document defines the approved strategic framework for the `/community/` section of the Technofatty website.  
Ged is responsible for implementing this framework in code. No deviations are permitted without stakeholder approval.

---

## Purpose

The Community is not a bolt-on forum. It is a growth engine node in the Technofatty neural net architecture, tightly integrated with Knowledge Articles, Tools, Case Studies, and Blog. Its roles are:

- **SEO**: create indexable, schema-rich long-tail landing pages (when COMMUNITY_INDEXABLE flag is true).  
- **CRO**: funnel users into newsletter subscription via verified email and surface CTAs consistently.  
- **Trust**: demonstrate moderation, accessibility, and brand fidelity.  
- **Authority**: reinforce Technofatty as the professional, trusted choice in its space.

---

## Page Types and Strategic Roles

### 1. Hub Page (`/community/`)

**Purpose**  
Entry point for all community activity. Distributes authority and sets expectations.

**SEO**  
- Indexable overview (when enabled).  
- Meta title ≤60 chars: *Technofatty Community – Questions & Discussions*.  
- Meta description ≤155 chars: *Join the Technofatty Community to ask questions, share experiences, and get answers from peers and experts.*  
- Schema: `ItemList` of featured threads + `BreadcrumbList`.

**CRO**  
- Primary CTA: **Ask a Question** (above fold).  
- Secondary CTA: **Subscribe to Updates** (newsletter).  
- Trust: **Code of Conduct** link visible.

**UX**  
- Filters: Latest | Unanswered | Tags.  
- Paginated thread list (cards with title, author, tags, reply count, last updated).  
- Mobile-first readable layout.  
- Accessibility: thread list is semantic `<ul>/<li>`.

---

### 2. Thread Page (`/community/q/<slug>/` or `/community/t/<slug>/`)

**Purpose**  
Long-tail informational match. Builds authority and engagement.

**SEO**  
- Schema: `QAPage` (questions) or `DiscussionForumPosting` (discussions).  
- Title tag = thread title (≤60 chars).  
- Meta description from accepted answer or excerpt (≤155 chars).  
- Canonical: self-referencing.

**CRO**  
- Inline CTA: **Subscribe to Updates** (between first post and first answer).  
- Bottom CTA: **Ask your own question**.  
- Newsletter opt-in integrated into posting (verified email).  

**UX**  
- H1 = thread title.  
- Accepted answer visually distinct.  
- Staff replies flagged.  
- Pagination for long threads.  
- Accessibility: ARIA roles, labeled forms, “Jump to accepted answer” link.

**Trust**  
- Staff replies marked.  
- Code of Conduct linked in footer.

---

### 3. Tag Page (`/community/tag/<slug>/`)

**Purpose**  
Topical hub tying Community into Knowledge, Tools, and Case Studies.

**SEO**  
- Meta title: *Technofatty Community – <Tag> Discussions*.  
- Schema: `ItemList`.  
- Indexable topical landing page.

**CRO**  
- CTA: **Subscribe to <Tag> updates**.  
- Crosslink to Knowledge, Tools, and Case Studies with same tag.

**UX**  
- Clear H1 = tag name.  
- Thread list (same design as hub).  
- Breadcrumbs: Home → Community → Tag.

**Trust**  
- Staff-monitored tags labeled.

---

### 4. Post Flow (Ask/Start)

**Purpose**  
Conversion funnel entry point. Grows subscriber base.

**SEO**  
- Always `noindex`.  

**CRO**  
- Primary CTA: **Submit your question**.  
- Email verification tied to newsletter list.  
- Copy: “By asking, you’ll also get community updates.”

**UX**  
- Fields: title, body, tags, email.  
- Server-side validation.  
- Post-submission confirmation: “Check your inbox to confirm.”  

**Trust**  
- “Your email is never shown publicly.”  
- Link to guidelines inline.

---

## Horizontal Integration (Neural Net)

All community pages must surface related content:  
- Knowledge Articles with matching tags.  
- Tools pages discussed in threads.  
- Case Studies relevant to discussions.  
- Blog posts with “Join the conversation in Community.”

Crosslinks must be **bidirectional** (e.g. Knowledge → Community, Community → Knowledge).  
Tagging taxonomy must be consistent across all content types.

---

## Acceptance Criteria

Ged must implement these criteria without exception:

- **UX**: clear purpose, mobile-first readability, server-side pagination, WCAG AA compliance.  
- **SEO**: clean URL scheme, canonical tags, meta title/desc constraints, schema.org integration, indexability toggle.  
- **CRO**: primary and secondary CTAs only, integrated newsletter opt-in, explicit trust signals, analytics events gated by consent.  
- **Trust**: Code of Conduct visible, moderation markers, privacy assurances.  

Any build that fails these criteria is non-compliant and cannot be released.

---

## Governance

- All design tokens must derive from `_variables.scss`.  
- All CTAs must match sitewide button styles.  
- Accessibility reviews are required at each milestone.  
- No JavaScript beyond Bootstrap dependencies without stakeholder approval.  
- COMMUNITY_INDEXABLE must remain `false` in production until authorized.

---

*This document is binding. It operationalizes Technofatty’s doctrine: clarity, authority, accessibility, performance, and conversion. Ged is tasked with implementing it in code, Paula with reviewing it for strategic alignment, and deviations require stakeholder sign-off.*
