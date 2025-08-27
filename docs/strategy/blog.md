# Technofatty Blog Strategy

Internal mandate for how **Blog** supports growth, authority, and revenue.  
This guides editorial choices, IA, UX, and implementation.

---

## Purpose of the Blog

The Blog is the **narrative engine**:
- Explains the “why now” behind our Knowledge and Tools.
- Tells case studies, product updates, partner stories, and opinion.
- Drives distribution (email, social, syndication) and captures demand.
- Warms leads into trials, downloads, and consultations.

---

## Mandates

1) **Audience-first clarity**  
   Posts must address business readers (operators, founders, marketing/sales leaders).  
2) **Tight linkage**  
   Every post links to at least one relevant Knowledge entry and one Tool.  
3) **Distribution-ready**  
   Titles, abstracts, and OG assets must be optimized for sharing.  
4) **Sustainable cadence**  
   Publish on a predictable rhythm; keep an editorial calendar in-repo.  
5) **Measurable outcomes**  
   Each post declares a primary conversion (newsletter, tool trial, contact, download).

---

## Content Types

- **Announce**: product/feature updates, roadmap notes.  
- **Case Study**: before/after outcomes with metrics and proof.  
- **Playbook**: action-oriented, lighter than a Guide but practical.  
- **Opinion / Signal**: contrarian takes, market shifts tied to action.  
- **Roundup / Benchmark**: curated datasets, comparisons, scorecards.

Mark type via a `category_*` pair or tags to support surfacing and feeds.

---

## Editorial Standards

- Clear, declarative headline; informative dek (excerpt).  
- Mandatory **excerpt** and **featured image** (with alt text).  
- At least 2 deep links: one **Knowledge** item, one **Tool** page.  
- Evidence/attribution for claims (links, charts, or footnotes).  
- A single, explicit CTA near the top and another at the end.  
- No wall-of-text: use subheads, lists, pull-quotes, and diagrams where valuable.

---

## SEO / Structured Data

- Render Schema.org **BlogPosting** and **BreadcrumbList** via JSON-LD.  
- `meta_title` and `meta_description` must be set or smart-fallback.  
- Canonical URLs must be stable; respect pagination/campaign params.  
- Open Graph / Twitter Card images defined per post when possible.  
- RSS + Atom feeds remain accurate and limited to published posts.

---

## Interconnection Rules

- From Blog → **Knowledge**: link deeply into concepts referenced.  
- From Blog → **Tools**: if a post teaches a workflow, surface the tool used.  
- From Knowledge/Tools → **Blog**: show “From the Blog” sidebar cards (contextual).  
- Use tags to form cross-type clusters (e.g., `pricing`, `automation`, `salesops`).

---

## IA / Navigation

- Blog index is filterable by category/tag/time to value; filtered views use `noindex,follow`.  
- Show featured story at top of page 1; subsequent pages list-only.  
- Per-post breadcrumbs: Home → Blog → Category → Post Title.

---

## Analytics & Goals

- Each post declares a **Primary Goal** (front-matter or DB field):  
  `newsletter_sub`, `tool_trial`, `consultation`, `download`, `signup`.  
- Fire analytics events: `blog_post_view`, `blog_cta_click`, `blog_related_click`.  
- Capture UTM params on entry; persist to the CTA destination when relevant.

---

## Technical Implementation (Django)

### Model (BlogPost)
- Required: `title`, unique `slug`, `status` (`draft/published/archived`), `published_at` for published.  
- Optional metadata: `excerpt`, `content`, `category_slug/title`, `tags` (JSON).  
- SEO: `meta_title`, `meta_description`, `canonical_url`, `og_*`, `twitter_*`.  
- Media: `image` (featured) + `image_alt`.  
- Validation: if `image` then `image_alt` required; if `status=published` then timezone-aware `published_at`.  
- Helpers: `get_absolute_url()`, `reading_time` auto-calc.

### Admin UX
- Rich text (CKEditor/Markdown) widget for `content`.  
- Prepopulated slug from title; preview link (`?preview=1` for staff).  
- Bulk actions: publish now (set `published_at` if missing), archive.  
- Filter and search by `status`, `category`, `tag`.

### Views
- Index: paginate with featured post on page 1; order by `-published_at`.  
- Detail: published only, unless staff preview param present.  
- Feeds: RSS + Atom serve top `n` published posts with excerpt + link.  
- Filtered index: inject `X-Robots-Tag: noindex,follow` and set `meta_robots` in context.

### Templating
- Meta head via shared partial; structured data in `structured_data` block.  
- Consistent CTA component using declared Primary Goal.  
- “Related” section with 2 cards from Knowledge and 1 from Tools (or vice versa).

---

## Distribution Pipeline

- Newsletter snippet auto-generated from title + excerpt + hero image.  
- Social share image rendered (if missing) via template → static asset.  
- Syndication map (optional): Medium/Substack/LinkedIn—respect canonical.

---

## Editorial Workflow

1) Draft in admin → assign type, tags, Primary Goal.  
2) Internal review: accuracy, links, claims substantiated, CTA placed.  
3) SEO pass: title, URL, meta, OG image ok; structured data validates.  
4) Publish or schedule; changes after publish preserve original `published_at`.  
5) Post-publication check: analytics firing, CTA tracking, feed update.

---

## Developer Mandate

Any Blog-affecting PR must:  
- Preserve validations and structured data output.  
- Maintain cross-link rules to Knowledge and Tools.  
- Honor preview behavior and filtered `noindex` policy.  
- Update this doc if introducing new content types or fields.

