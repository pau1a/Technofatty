import pytest


def build_breadcrumbs(pages):
    """Build a JSON-LD BreadcrumbList from ``pages``.

    Each page is a mapping with ``name`` and ``url`` keys.  The function
    enumerates the list and assigns sequential ``position`` values starting at
    1 for each ListItem.
    """
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": page["name"],
                "item": page["url"],
            }
            for idx, page in enumerate(pages)
        ],
    }


def assert_sequential_positions(breadcrumbs):
    items = breadcrumbs["itemListElement"]
    for idx, item in enumerate(items):
        assert item["position"] == idx + 1


def test_multilevel_breadcrumb_positions():
    pages = [
        {"name": "Home", "url": "/"},
        {"name": "Section", "url": "/section/"},
        {"name": "Subsection", "url": "/section/sub/"},
    ]
    breadcrumbs = build_breadcrumbs(pages)
    assert_sequential_positions(breadcrumbs)


def test_single_item_breadcrumb():
    pages = [{"name": "Home", "url": "/"}]
    breadcrumbs = build_breadcrumbs(pages)
    assert_sequential_positions(breadcrumbs)
    assert len(breadcrumbs["itemListElement"]) == 1


def test_deeply_nested_breadcrumb():
    pages = [
        {"name": f"Level {i}", "url": f"/level-{i}/"}
        for i in range(1, 11)
    ]
    breadcrumbs = build_breadcrumbs(pages)
    assert_sequential_positions(breadcrumbs)
    assert breadcrumbs["itemListElement"][-1]["position"] == len(pages)
