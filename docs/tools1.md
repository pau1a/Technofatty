# Tools Strategy & Implementation Blueprint (internal)

> This is the internal mandate for how the **Tools** segment of Technofatty will exist, behave, evolve, and make money. It ties Tools to Knowledge and Blog, encodes how we’ll ship, how we’ll measure success, and what “good” looks like across engineering, UX, growth, compliance, and ops. Treat this as the source of truth for GED when building and for reviewers when approving.

---

## 1) Why Tools exist (objectives that won’t change)

Technofatty Tools exist to:

- Solve concrete, repeatable business problems fast enough to feel like magic;
- Generate qualified demand for consulting and productized services;
- Convert operating value into revenue through freemium → pro → enterprise paths;
- Feed and be fed by our Knowledge and Blog layers so the site feels like an integrated neural network rather than islands;
- Showcase our engineering quality: speed, reliability, privacy, and tasteful UX.

**Non‑goals:** vanity gadgets, SEO-only toys, or anything that compromises user trust or data protection.

---

## 2) The user journey (how Tools knit into the whole site)

**Entry points:** tools hub, deep links from Knowledge articles, tool cards embedded in Blog posts, and category pages (e.g., “Pricing & Forecasting”, “Sales Ops”, “Content Ops”, “Finance Ops”).

**Activation:** a tool runs in under 10 seconds with sane defaults; the first run never asks for sign‑up unless an external API key is required. When a run completes, we surface a concise result + one or two contextual calls to action: save/share/export, “explain the result”, “diagnose anomalies”, and a single related Knowledge/Blog pointer.

**Retention:** saved runs (local or account‑tied), email me updates, browser extension parity for the top tools, and gentle “next best action” prompts (e.g., “Turn this into a one‑pager for your client?”).

**Conversion:** pro gates on volume, export formats, batch mode, scheduled runs, and team sharing. Enterprise adds SSO, audit, DPA/SCCs, and support SLAs.

---

## 3) Information architecture & routing

- A dedicated Django app: `tools`.
- Public URLs: `/tools/` (hub), `/tools/<tool-slug>/` (detail/runner), `/tools/<tool-slug>/runs/<id>/` (saved run – private or share‑key), `/tools/categories/<slug>/` (filtered hub).
- Tools, like Knowledge & Blog, adopt our `StatusChoices` and `PublishedManager` semantics (draft/published/archived + `published_at` ≤ now).
- Canonicals & sitemaps: only the hub, categories, published tool detail pages, and optionally public run pages with a share key are indexed. Filtered lists emit `noindex,follow` (header + meta) like Knowledge.

---

## 4) Data model blueprint (reference scaffold)

This is the minimal shape GED should implement. Extend incrementally.

```python
# apps/tools/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from coresite.models import StatusChoices, PublishedManager

class ToolCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

class Tool(models.Model):
    category = models.ForeignKey(ToolCategory, related_name="tools", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT, db_index=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    blurb = models.TextField(blank=True)
    description_md = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="tools/", blank=True, null=True)
    hero_alt = models.CharField(max_length=255, blank=True)

    # Monetization flags
    free = models.BooleanField(default=True)
    pro_required = models.BooleanField(default=False)
    enterprise_capable = models.BooleanField(default=False)

    # SEO meta
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tool_detail", kwargs={"slug": self.slug})

class ToolRun(models.Model):
    tool = models.ForeignKey(Tool, related_name="runs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)

    # request/response envelopes; small inputs can be JSON, larger handled via file upload
    input = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="ok")  # ok|error|rate_limited|timeout

    # shareable by opaque token (optional)
    share_token = models.CharField(max_length=40, blank=True, db_index=True)
    is_public = models.BooleanField(default=False)

    # cost + telemetry
    exec_ms = models.PositiveIntegerField(default=0)
    tokens_in = models.IntegerField(default=0)
    tokens_out = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    class Meta:
        indexes = [
            models.Index(fields=["tool", "created_at"]),
            models.Index(fields=["share_token"]),
        ]
```

**Notes:**
- We persist enough telemetry to price runs, detect abuse, and tell a compelling ROI story.
- Large attachments (CSVs, PDFs) are uploaded to `MEDIA_ROOT/tools_uploads/<tool>/...` and tied via a `ToolRunFile` table later if needed.

---

## 5) Views, templates, and admin essentials

- Hub view with server‑side filters: category, time‑to‑value, “AI‑powered” flag, and a query string search across `title`, `blurb`, `description_md` and tags.
- Tool detail/runner view accepts `?preview=1` for staff, mirroring Knowledge behaviour. First render shows the runner UI above the fold and “how it works” below.
- Saved run view requires `is_public` + `share_token` or an authenticated owner.
- Admin: inline Markdown editor (keep CKEditor for Knowledge, but default to Markdown for Tools), quick publish/unpublish, and a “Run smoke test” admin action that executes a canned input and records latency.

Example URLconf:

```python
# apps/tools/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.tools_hub, name="tools_hub"),
    path("categories/<slug:slug>/", views.tools_category, name="tools_category"),
    path("<slug:slug>/", views.tool_detail, name="tool_detail"),
    path("<slug:slug>/runs/<str:share_token>/", views.tool_run_public, name="tool_run_public"),
]
```

---

## 6) Cross‑linking that feels like a neural net (not tags for tags’ sake)

**Motifs**
We reuse the `motif` concept across Knowledge and Tools to create subtle, opinionated pathways. A tool declares a `motif` or two. Knowledge articles with the same motif show up as “Deepen understanding” callouts. Blog posts tagged with that motif become “Field notes”.

**Embeddings for relatedness**
A weekly job creates vector embeddings for Tools, Knowledge, and Blog. We store the vectors in Postgres using `cube` or in a tiny SQLite sidecar if simpler. Related items are selected by cosine similarity with editorial overrides. This keeps recommendations relevant without adding a full vector DB dependency.

**Contextual recipes**
Each tool ships with one to three “recipes” (short, skimmable playbooks) stored as Markdown franchise files in `apps/tools/content/recipes/<tool-slug>/`. Recipes can be linked from tool UIs and cross‑referenced from Knowledge. They are versioned alongside code.

---

## 7) Monetization model and gates

**Freemium:** one‑off runs with small inputs, lightweight exports (PNG, TXT), no batch/scheduling.

**Pro:** higher limits, CSV/XLSX/PDF export, batch mode, saved runs with history, priority queueing, and private share links.

**Enterprise:** SSO, audit logs, DPA/SCCs, dedicated rate limits, custom models or on‑prem endpoints, support SLAs.

**How we nudge:** finish a run → show value → allow one export → explain the next level. Pricing copy remains quiet and specific: what you unlock, not just a price grid. Stripe links live under `/account/billing/` and are only mentioned at the moment of need.

---

## 8) Measurement without creepiness

We log only what we need to improve the tools and price fairly.

**Event envelope (server‑side preferred):**

```json
{
  "ts": "2025-08-27T12:00:00Z",
  "user_id": 123,              // optional anon key if not logged in
  "ip_hash": "sha256:...",    // align with ContactEvent approach
  "event": "tool_run_completed",
  "tool": "proposal-summariser",
  "properties": {
    "exec_ms": 2480,
    "status": "ok",
    "cost_usd": 0.0019,
    "tokens_in": 612,
    "tokens_out": 220,
    "input_bytes": 43810,
    "origin": "web|ext|api",
    "plan": "free|pro|enterprise"
  }
}
```

We emit `X-Robots-Tag: noindex,follow` on filtered listings, and we already set `<meta name="robots" content="noindex,follow">` in the template when filters are active. This keeps crawl budget where it matters.

**Success leading indicators:** time‑to‑first‑value < 10s; repeat runs per user ≥ 2; export rate; recipe clicks.
**Lagging indicators:** pro upgrades, enterprise leads, consulting requests from tool pages, churn on saved runs.

---

## 9) Security, privacy, and compliance

- Inputs stay in the region we deploy to; we do not retain raw user content longer than necessary. Default retention for ToolRun.input/result is 30 days for free, 90 for pro, configurable for enterprise.
- Redaction policy for uploads (PII, secrets) enforced client‑side and server‑side; show a brief nudging banner: “Don’t paste secrets. Use the redactor.”
- Rate limits per IP and per account; back‑pressure with honest UI messages, not silent failures.
- Model and API providers are abstracted behind a small service layer so we can move between providers without touching view code. Secrets live in environment variables; never in the DB.

---

## 10) Performance & accessibility checklist (baked into Definition of Done)

- First interactive under 2s on the detail page for an empty form; typical run under 10s wall‑clock.
- No layout shifts when results stream in; use reserved space or skeletons.
- Keyboard only, proper labels, and colour contrast meet WCAG AA.
- Dark mode respects system pref; charts and code blocks remain legible.

---

## 11) Apache + Django notes (how we serve Tools safely)

- Static build artefacts for the tools UI (JS/CSS) are collected via `collectstatic` as usual.
- Long‑running jobs are decoupled from request/response; we do not rely on mod_wsgi request threads for heavy lifting. If streaming is needed, prefer polling or short‑lived Ajax to avoid WebSocket complexity under Apache. If we must use SSE, place them behind an event endpoint with appropriate timeouts.
- CSP: allow `script-src` from self and the specific CDN(s) used for code highlighting or charts. Inline JSON‑LD is whitelisted via `script-src 'self' 'unsafe-inline'` only for `type="application/ld+json"` using a hash/nonce in future; start pragmatic, harden iteratively.

Example vhost fragment:

```apache
# /etc/apache2/sites-available/technofatty.conf (fragment)
Alias /static/ /var/www/technofatty_com/static/
Alias /media/  /var/djangoproj/technofatty_com/media/

<Directory /var/www/technofatty_com/static>
  Require all granted
</Directory>
<Directory /var/djangoproj/technofatty_com/media>
  Require all granted
</Directory>

WSGIDaemonProcess technofatty processes=4 threads=8 python-path=/var/djangoproj/technofatty_com:/home/technofatty/.virtualenvs/technofatty_env/lib/python3.8/site-packages
WSGIProcessGroup technofatty
WSGIScriptAlias / /var/djangoproj/technofatty_com/technofatty_com/wsgi.py

# Conservative timeouts; tools perform work server-side or async, not in-request.
WSGIApplicationGroup %{GLOBAL}
WSGIScriptReloading On
Timeout 60
```

---

## 12) Shipping discipline (GED mandate)

Everything ships through PRs with tests and a migration plan, the way we just did for Knowledge.

**Branch naming:** `codex/tools/<scope>` for feature work, `hotfix/tools/<scope>` for urgent fixes.

**Migrations:** follow the `000x_` sequence within the `tools` app. Name them descriptively. Pre‑migration checks in PR description: duplicates, null slugs, published without published_at, etc.

**Tests to include:** model constraints, manager semantics (future‑dated hidden), hub filters, `noindex` headers on filtered pages, preview mode for staff, basic rate‑limit path, and one golden‑path tool run.

**Definition of Done:**
- Passing tests;
- Admin forms usable;
- Hub and detail templates responsive;
- Analytics events emitted;
- Docs updated (this file, plus the top‑level README hook below).

**Roll‑out:** ship the hub and one anchor tool first; follow with two supporting tools in the same category to form a coherent cluster.

---

## 13) Content model and editorial rhythm

Each tool has: title, blurb, short how‑it‑works, inputs cheat‑sheet, and one to three recipes. When a tool ships, a Knowledge article publishes within 48 hours that explains the underlying method, with examples and caveats. A Blog post follows with a real‑world story using the tool. This pattern gives us three internal links and a strong topical cluster.

We keep tone practical, sceptical, and slightly playful. Screenshots are captioned with the “why”, not just the “what”.

---

## 14) Backlog seeds (business‑useful, AI‑assisted)

We keep this short and tangible. Build what we can maintain.

- **Client Brief → Proposal Outliner**: paste brief, pick scope, get a structured outline, risk list, and pricing levers. Export to DOCX.
- **Sales Call Synthesiser**: drop a transcript, get next steps, objection map, and follow‑up email drafts.
- **Pricing Scenario Model**: small CSV in, margin targets and sensitivity out with a clean chart. Batch mode = pro.
- **Policy Summariser (UK/EU)**: paste a policy update link, get a two‑minute brief and a “what changes tomorrow” section; stores citations.
- **Vendor DPIA Helper**: upload vendor features; get questions to ask and a draft DPIA section; never stores uploads by default.

---

## 15) Top‑level README hook (paste‑ready)

Add this section to the repo root `README.md` under “Product Areas”.

```md
### Tools
Business‑first micro‑apps that turn messy inputs into decisions. Start at `/tools/` for the hub. Each tool has a short blurb, a runnable UI, and a few recipes. We ship freemium by default, with pro features behind auth. The hub, detail pages, and saved runs follow the same publish/preview rules as Knowledge.

Internal blueprint: see `docs/tools/BLUEPRINT.md`.
```

---

## 16) File layout (where these docs live)

Place this file at `docs/tools/BLUEPRINT.md` and link it from the top‑level README as above. Recipes live next to code under `apps/tools/content/recipes/<tool-slug>/`. Any internal diagrams can go in `docs/tools/diagrams/`.

---

## 17) Risks & mitigations

- **Over‑building v1** → One anchor tool first, prove adoption, add two in the same cluster; keep scope tight.
- **Model/provider churn** → thin service layer; feature flags by provider; golden‑path tests.
- **Privacy blowback** → default non‑retention, clear redaction, data processing summary in the UI; enterprise‑grade DPA when asked.
- **Ops overload** → asynchronous jobs for heavy work; budgets on tokens/time; scheduled jobs spaced sensibly.

---

## 18) Appendix: skeleton templates

Tool hub template skeleton:

```html
<!-- templates/tools/hub.html -->
<section class="section section--scaffold" aria-labelledby="tools-heading">
  <div class="wrap">
    <h1 id="tools-heading">Tools</h1>
    <form class="tools-filter" method="get">
      <!-- category, q, time, ai-only toggles; mirrors Knowledge filterbar style -->
    </form>
    <div class="tools-grid">
      {% for tool in page_obj.object_list %}
        <article class="tool-card">
          <a href="{{ tool.get_absolute_url }}">
            <h2>{{ tool.title }}</h2>
            <p>{{ tool.blurb }}</p>
          </a>
        </article>
      {% empty %}
        <p>No tools published yet.</p>
      {% endfor %}
    </div>
    {% include "coresite/partials/pagination.html" %}
  </div>
</section>
```

Detail/runner skeleton:

```html
<!-- templates/tools/detail.html -->
<section class="section section--scaffold" aria-labelledby="tool-heading">
  <div class="wrap">
    <h1 id="tool-heading">{{ tool.title }}</h1>
    <p class="lede">{{ tool.blurb }}</p>
    <div id="runner">
      <!-- GED implements the actual UI elements per tool; keep fast and minimal. -->
    </div>
    <aside class="recipes">
      <h2>Recipes</h2>
      <!-- Render short, actionable playbooks -->
    </aside>
    <hr>
    <section class="how-it-works">
      {{ tool.description_md|markdown }}
    </section>
  </div>
</section>
```

---

## 19) Final word

Keep the bar high: instant usefulness, beautiful restraint in the UI, and privacy by default. If a tool doesn’t save someone time or money in its first minute, we rethink it. This is how Tools pays for the rest of the site—and earns trust while doing it.

