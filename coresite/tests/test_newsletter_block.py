from django.urls import reverse


def test_newsletter_button_has_analytics(client):
    res = client.get(reverse("home"))
    html = res.content.decode()
    assert 'data-analytics-event="cta.newsletter.subscribe"' in html
    assert 'data-analytics-meta="{\"form\":\"newsletter\"}"' in html

