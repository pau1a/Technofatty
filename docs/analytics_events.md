# Analytics Events

Event Name | Location | Business Goal
--- | --- | ---
`cta.nav.join` | Header primary CTA "Join Us" | Grow community membership
`cta.hero.signup` | Hero section CTA "Get AI Growth Tips" | Capture newsletter leads
`cta.trust.case_studies` | Trust block link to case studies | Drive case study exploration
`cta.case_studies.open` | Featured grid CTA to case studies | Drive case study exploration
`cta.community.primary` | Community section primary CTA | Encourage community engagement
`cta.support.<slug>` | Support cards on homepage (slug varies) | Route visitors to help resources
`form.newsletter.start` | Newsletter email field focus | Measure newsletter form engagement
`form.newsletter.submit` | Newsletter form submit | Track newsletter signups
`link.support.email` | Support email link on contact page | Facilitate support requests
`link.contact.email` | General contact email fallback | Allow direct outreach
`link.legal.email` | Legal email link on contact/legal pages | Enable legal notices
`share.twitter` | Twitter share button on articles | Encourage content sharing
`share.linkedin` | LinkedIn share button on articles | Encourage professional engagement
`case_study_card_click` | Case study card links | Explore individual case studies
`community.view_hub` | Community hub page load | Measure community page visits
`cta.community.ask_question` | "Ask a Question" CTA | Encourage new thread creation
`cta.community.subscribe_updates` | "Subscribe to Updates" CTA | Grow community subscribers
`community.filter.latest` | Filter strip: Latest | Understand filter preference
`community.filter.unanswered` | Filter strip: Unanswered | Track interest in unanswered threads
`community.filter.tag` | Tag pill selection | Gauge tag-based navigation

All `community.*` and `cta.community.*` events include payload properties:
- `surface`: "community"
- `filter`: current filter when relevant
- `position`: location of the control (e.g., "header", "footer")
- `tag`: selected tag for tag filter events

Events are emitted only after consent; before consent, event senders must no-op.
