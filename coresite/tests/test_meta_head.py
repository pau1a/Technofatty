import re
from django.template import Template, Context
from django.test import RequestFactory, override_settings


def render_meta(context):
    tpl = Template("{% include 'coresite/partials/seo/meta_head.html' %}")
    return tpl.render(Context(context))


def test_meta_title_description_truncated():
    long_title = 'T' * 80
    long_desc = 'D' * 200
    html = render_meta({'meta_title': long_title, 'meta_description': long_desc, 'canonical_url': '/foo/'})
    title_match = re.search(r"<title>(.*?)</title>", html)
    assert title_match
    assert len(title_match.group(1)) <= 60
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html)
    assert desc_match
    assert len(desc_match.group(1)) <= 155


@override_settings(SITE_BASE_URL="https://technofatty.com")
def test_canonical_matches_request():
    rf = RequestFactory()
    request = rf.get('/foo/', secure=True, HTTP_HOST='technofatty.com')
    html = render_meta({'canonical_url': '/foo/', 'request': request})
    assert '<link rel="canonical" href="https://technofatty.com/foo/">' in html
    assert '<!-- canonical-mismatch -->' not in html


@override_settings(SITE_BASE_URL="https://technofatty.com")
def test_canonical_mismatch_emits_comment():
    rf = RequestFactory()
    request = rf.get('/foo/', secure=True, HTTP_HOST='technofatty.com')
    html = render_meta({'canonical_url': '/bar/', 'request': request})
    assert '<link rel="canonical" href="https://technofatty.com/bar/">' in html
    assert '<!-- canonical-mismatch -->' in html
