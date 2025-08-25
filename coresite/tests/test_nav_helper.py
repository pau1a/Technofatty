import pytest

from utils.nav import is_active


@pytest.mark.parametrize(
    "request_path, nav_url, expected",
    [
        ("/tools/", "/tools/", True),  # top-level
        ("/tools/sub/", "/tools/", True),  # child page
        ("/knowledge/", "/tools/", False),  # non-matching
    ],
)
def test_is_active(request_path, nav_url, expected):
    assert is_active(request_path, nav_url) is expected
