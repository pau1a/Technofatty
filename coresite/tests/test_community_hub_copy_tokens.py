from pathlib import Path


def test_community_hub_copy_and_tokens_guarded():
    template = Path(__file__).resolve().parents[1] / "templates/coresite/community.html"
    text = template.read_text()
    assert "Technofatty Community" in text
    assert (
        "Get practical answers from peers and TF staff on growth, content, analytics, and tools." in text
    )
    tokens = [
        "community.view_hub",
        "cta.community.ask_question",
        "cta.community.subscribe_updates",
        "community.filter.latest",
        "community.filter.unanswered",
        "community.filter.tag",
    ]
    for tok in tokens:
        assert tok in text
