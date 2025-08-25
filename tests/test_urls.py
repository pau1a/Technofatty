import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from utils.urls import ensure_absolute


def test_ensure_absolute_returns_input_if_already_absolute():
    url = "https://example.com/path"
    assert ensure_absolute(url, "https://base.com") == url


def test_ensure_absolute_joins_relative_with_base():
    assert (
        ensure_absolute("/foo", "https://example.com")
        == "https://example.com/foo"
    )


def test_ensure_absolute_returns_none_without_base():
    assert ensure_absolute("/foo", "") is None


def test_ensure_absolute_handles_protocol_relative():
    assert (
        ensure_absolute("//example.com/foo", "https://base.com")
        == "https://example.com/foo"
    )
