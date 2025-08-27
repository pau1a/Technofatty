# Blog: Opinion with Handrails

The blog is where we take positions, challenge assumptions, and point to what to do next.

## Purpose
Articulate why a capability or pattern matters, when to use it, and what trade-offs to accept. Each post should route to one tool and one knowledge article.

## Shape of a post
Headline that carries a claim. One strong counter-example. A section called “When not to use this”. End with two routes: do it now (tool) or learn deeper (article).

## Linking discipline
Link once, early. Repeat links only if the reader has earned them with new context (e.g. after results screenshots).

## Editorial integrity
If a sponsor is mentioned, disclose at the point of mention. If we include benchmark numbers, link to the runbook or notebook. If it’s a hunch, label it as such.

## Reusables
– Post-footer partial that accepts `tool_slug` and `article_slug`.  
– “How this was tested” expandable to keep the body lean.

## Telemetry hooks
`blog_read_start`, `blog_read_50`, `blog_read_95`, `blog_click_tool`, `blog_click_article`. See `telemetry.md` for payload shapes.
