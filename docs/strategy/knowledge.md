# Technofatty Knowledge Strategy

This document defines how **Knowledge** (articles, guides, glossary, signals) must function on the site.  
It is internal-facing, guiding editorial, technical, and business directions.

---

## Purpose of Knowledge

Knowledge is the **trust engine** of the site:
- Provides authoritative, structured answers to business challenges.  
- Builds topical authority across categories.  
- Serves as the contextual layer linking to Tools and Blog.  
- Captures organic traffic at scale via evergreen content.  

---

## Mandates

1. **Authority-first**  
   Every article must demonstrate expertise, clarity, and utility.  

2. **Content Types**  
   Knowledge comprises:  
   - **Articles** – deep dives into concepts.  
   - **Guides** – structured, step-by-step practical instructions.  
   - **Glossary** – precise definitions of terms.  
   - **Signals** – short, timely notes on shifts and changes in business/tech.  

3. **Structured Data & SEO**  
   - Every article must render Schema.org JSON-LD (BlogPosting, BreadcrumbList).  
   - Canonical URLs must be clean and correct.  
   - Robots meta must adapt: noindex filtered results.  

4. **Editorial Standards**  
   - No article may be published without a **published_at** date.  
   - All images must have alt text.  
   - Meta title + description must be set, or auto-generated.  
   - Blurb is mandatory.  

5. **Interconnection**  
   - Every article must link out to at least one related Tool (application).  
   - Every article must link to at least one BlogPost (narrative).  
   - Categories must connect horizontally: “see also” patterns.  

---

## Technical Implementation

### Django Model
- `KnowledgeArticle` includes fields for:  
  - `status` (draft, published, archived)  
  - `subtype` (guide, glossary, signal)  
  - `published_at` (required for published)  
  - `meta_title`, `meta_description`, `canonical_url`  
  - `tags` (for flexible cross-linking)  

### Validations
- Image requires alt text.  
- Published requires published_at.  
- Slug must be unique + non-empty.  

### Views
- Filtered results must emit `X-Robots-Tag: noindex,follow`.  
- Canonical must adapt to filters + pagination.  

---

## UX / Design

- Article pages must show:  
  - Title, blurb, structured content.  
  - CTA to related Tools + BlogPosts.  
  - Breadcrumbs for navigation.  
- Guides should use distinct formatting to stand apart.  
- Glossary entries should be lightweight and fast-loading.  
- Signals should feel ephemeral, but archived for reference.  

---

## Developer Mandate

Every PR affecting Knowledge must:  
- Pass model validations.  
- Render structured data correctly.  
- Ensure interconnection with Tools + Blog.  
- Update documentation if new subtypes are introduced.  

---

⚡ **This document is binding for Ged and contributors. No Knowledge content goes live without meeting these requirements.**
