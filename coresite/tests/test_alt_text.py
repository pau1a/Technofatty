from pathlib import Path
import re

IMG_TAG = re.compile(r"<img[^>]*>", re.IGNORECASE)
ALT_ATTR = re.compile(r'''alt=(?:"[^"]+"|'[^']+')''')


def test_all_imgs_have_alt_text():
    templates_dir = Path(__file__).resolve().parents[1] / "templates"
    for path in templates_dir.rglob("*.html"):
        html = path.read_text()
        for tag in IMG_TAG.findall(html):
            assert ALT_ATTR.search(tag), f"Missing alt text in {path}: {tag}"


