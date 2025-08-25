import pytest


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/signup/", "https://technofatty.com/#signup"),
        ("/services/", "https://technofatty.com/about/"),
        (
            "/signals/alpha/",
            "https://technofatty.com/knowledge/signals/#signal-alpha",
        ),
        ("/community/join/", "https://technofatty.com/community/"),
    ],
)
@pytest.mark.django_db
def test_legacy_redirects(client, path, expected):
    response = client.get(path, follow=False)
    assert response.status_code == 301
    assert response["Location"] == expected


def test_signup_query_string_preserved(client):
    response = client.get("/signup/?ref=newsletter", follow=False)
    assert response.status_code == 301
    assert (
        response["Location"]
        == "https://technofatty.com/?ref=newsletter#signup"
    )
