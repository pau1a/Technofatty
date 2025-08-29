import importlib


def test_sitemap_env_rules_respect_canonical_host(monkeypatch):
    import coresite.tests.test_sitemap_validation as sm
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("CANONICAL_HOST", "example.com")
    sm = importlib.reload(sm)
    t = sm.SitemapValidationTest()
    problems = []
    t._validate_url("https://wrong.com/page/", set(), set(), problems)
    assert any("Non-canonical host" in p for p in problems)
    monkeypatch.setenv("ENV", "development")
    monkeypatch.setenv("CANONICAL_HOST", "technofatty.com")
    importlib.reload(sm)
