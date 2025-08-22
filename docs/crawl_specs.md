# Crawl & Indexation Baseline

Canonical routes and indexation intent:

| Route | Intent | Rationale |
| ----- | ------ | --------- |
| `/` | index | Primary homepage |
| `/about/` | index | Company overview |
| `/contact/` | index | Contact information |
| `/support/` | index | Help resources |
| `/legal/` | index | Policies and legal notes |

Verification checks (to be run after deployment):

```
$ curl -I https://technofatty.com/
$ curl -I https://technofatty.com/about/
$ curl -I https://technofatty.com/contact/
$ curl -I https://technofatty.com/support/
$ curl -I https://technofatty.com/legal/
$ curl -I https://technofatty.com/robots.txt
$ curl -I https://technofatty.com/sitemap.xml
```

Each command should return a single redirect (if any) to the canonical URL and a `200 OK` status. Pages should include a matching `<link rel="canonical">` tag and no `X-Robots-Tag` headers unless explicitly added for temporary exclusion.

> **Note:** Runtime verification could not be executed in this development container because the Django framework and related dependencies were unavailable. Install requirements and rerun the above commands after deployment.

