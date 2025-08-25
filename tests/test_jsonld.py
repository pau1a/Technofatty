import json
import pathlib
import sys
from django.utils.safestring import SafeString

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from utils.jsonld import render_jsonld


def test_render_jsonld_minified_and_deterministic():
    data1 = {"b": 2, "a": 1}
    data2 = {"a": 1, "b": 2}
    out1 = render_jsonld(data1)
    out2 = render_jsonld(data2)
    expected = '<script type="application/ld+json">{"a":1,"b":2}</script>'
    assert isinstance(out1, SafeString)
    assert out1 == expected
    assert out1 == out2
    # ensure minified: no unnecessary whitespace
    inner = out1.split('>', 1)[1].rsplit('<', 1)[0]
    assert '\n' not in inner and ' ' not in inner
