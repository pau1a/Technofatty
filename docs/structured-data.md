# Partial context keys

This document lists required and optional context dictionary keys for each template partial.

<a id="about-about-cta"></a>
### about/about-cta.html
- Required: None
- Optional: None

<a id="about-about-hero"></a>
### about/about-hero.html
- Required: None
- Optional: None

<a id="about-about-milestones"></a>
### about/about-milestones.html
- Required: None
- Optional: None

<a id="about-about-principles"></a>
### about/about-principles.html
- Required: None
- Optional: None

<a id="about-about-story"></a>
### about/about-story.html
- Required: None
- Optional: None

<a id="about-about-team"></a>
### about/about-team.html
- Required: None
- Optional: None

<a id="about-about-trust"></a>
### about/about-trust.html
- Required: None
- Optional: None

<a id="community_block"></a>
### community_block.html
- Required: community.headline, community.messages.empty
- Optional: community.heading_level, community.intro, community.primary_cta (url,label), community.secondary_links (slug,url,label,description)

<a id="consent_banner"></a>
### consent_banner.html
- Required: None
- Optional: None

<a id="contact-contact-cta"></a>
### contact/contact-cta.html
- Required: None
- Optional: None

<a id="contact-contact-form"></a>
### contact/contact-form.html
- Required: form
- Optional: None

<a id="contact-contact-info"></a>
### contact/contact-info.html
- Required: None
- Optional: None

<a id="contact-contact-intro"></a>
### contact/contact-intro.html
- Required: None
- Optional: None

<a id="contact-contact-social"></a>
### contact/contact-social.html
- Required: None
- Optional: None

<a id="contact-contact-trust"></a>
### contact/contact-trust.html
- Required: None
- Optional: None

<a id="featured_grid"></a>
### featured_grid.html
- Required: resources (list of {title, blurb, url})
- Optional: case_studies (list of CaseStudy objects)

<a id="knowledge-featured"></a>
### knowledge/_featured.html
- Required: featured.image.url, featured.heading, featured.excerpt, featured.cta.url, featured.cta.label
- Optional: featured.image.alt, featured.image.width, featured.image.height

<a id="global-analytics"></a>
### global/analytics.html
- Required: ANALYTICS_PROVIDER, ANALYTICS_SITE_ID
- Optional: None

<a id="global-build_banner"></a>
### global/build_banner.html
- Required: None
- Optional: build_branch, build_commit, build_datetime

<a id="global-footer"></a>
### global/footer.html
- Required: footer (headline, optional heading_level, intro, meta)
- Optional: footer.heading_level, footer.intro, footer.meta.copyright, footer.meta.made_in, footer.meta.email

<a id="global-header_nav"></a>
### global/header_nav.html
- Required: request.path (from context)
- Optional: None

<a id="global-nav_cta"></a>
### global/nav_cta.html
- Required: user.is_authenticated (from context)
- Optional: None

<a id="global-nav_links"></a>
### global/nav_links.html
- Required: nav_links
- Optional: id_prefix (default "nav"), location (default "header")

<a id="global-notice"></a>
### global/notice.html
- Required: None
- Optional: None

<a id="global-status_placeholder"></a>
### global/status_placeholder.html
- Required: None
- Optional: None

<a id="hero"></a>
### hero.html
- Required: site_images.hero1.image or site_images.hero1.video
- Optional: site_images.hero1.alt_text

<a id="legal-legal-accessibility"></a>
### legal/legal-accessibility.html
- Required: None
- Optional: None

<a id="legal-legal-compliance"></a>
### legal/legal-compliance.html
- Required: None
- Optional: None

<a id="legal-legal-contact"></a>
### legal/legal-contact.html
- Required: None
- Optional: None

<a id="legal-legal-cookies"></a>
### legal/legal-cookies.html
- Required: None
- Optional: None

<a id="legal-legal-intro"></a>
### legal/legal-intro.html
- Required: None
- Optional: None

<a id="legal-legal-licensing"></a>
### legal/legal-licensing.html
- Required: None
- Optional: None

<a id="legal-legal-privacy"></a>
### legal/legal-privacy.html
- Required: None
- Optional: None

<a id="legal-legal-terms"></a>
### legal/legal-terms.html
- Required: None
- Optional: None

<a id="newsletter_block"></a>
### newsletter_block.html
- Required: None
- Optional: messages, APPROVED_CTA

<a id="seo-meta_head"></a>
### seo/meta_head.html
- Required: canonical_url
- Optional: page_title, meta_description, og_type, og_image_url

<a id="seo-blog_post_jsonld"></a>
### seo/blog_post_jsonld.html
- Required: post, canonical_url
- Optional: None

<a id="seo-structured_data"></a>
### seo/structured_data.html
- Required: None
- Optional: None

<a id="signals_block"></a>
### signals_block.html
- Required: signals.headline, signals.cards
- Optional: signals.heading_level, signals.intro, cards.kicker, cards.title, cards.problem, cards.approach, cards.evidence, cards.cta_text

<a id="support-support-accessibility"></a>
### support/support-accessibility.html
- Required: None
- Optional: None

<a id="support-support-account-billing"></a>
### support/support-account-billing.html
- Required: None
- Optional: None

<a id="support-support-contact"></a>
### support/support-contact.html
- Required: None
- Optional: None

<a id="support-support-faqs"></a>
### support/support-faqs.html
- Required: None
- Optional: None

<a id="support-support-guides"></a>
### support/support-guides.html
- Required: None
- Optional: None

<a id="support-support-intro"></a>
### support/support-intro.html
- Required: None
- Optional: None

<a id="support-support-privacy-security"></a>
### support/support-privacy-security.html
- Required: None
- Optional: None

<a id="support-support-status"></a>
### support/support-status.html
- Required: None
- Optional: None

<a id="support-support-troubleshooting"></a>
### support/support-troubleshooting.html
- Required: None
- Optional: None

<a id="support_block"></a>
### support_block.html
- Required: support.headline, support.messages.empty
- Optional: support.heading_level, support.intro, support.links (slug,url,label,description)

<a id="trust"></a>
### trust.html
- Required: None
- Optional: None

