import hashlib
from io import BytesIO
from typing import Tuple
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageDraw, ImageFont

IMAGE_SIZE = getattr(settings, "SOCIAL_IMAGE_SIZE", (1200, 630))
BACKGROUND_COLOR = getattr(settings, "SOCIAL_BG_COLOR", (15, 23, 42))
TITLE_COLOR = getattr(settings, "SOCIAL_TITLE_COLOR", (255, 255, 255))
BRAND_COLOR = getattr(settings, "SOCIAL_BRAND_COLOR", (14, 165, 233))
BRAND_TEXT = getattr(settings, "SOCIAL_BRAND_TEXT", "Technofatty")
FONT_PATH = getattr(
    settings,
    "SOCIAL_FONT_PATH",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)

def _get_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        width = draw.textbbox((0, 0), test_line, font=font)[2]
        if width <= max_width:
            line = test_line
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def _create_image_bytes(text: str) -> bytes:
    img = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    title_font = _get_font(80)
    brand_font = _get_font(40)
    margin = 60
    max_width = IMAGE_SIZE[0] - 2 * margin
    lines = _wrap_text(draw, text, title_font, max_width)
    draw.multiline_text((margin, margin), "\n".join(lines), fill=TITLE_COLOR, font=title_font)
    brand_pos = (margin, IMAGE_SIZE[1] - margin - 40)
    draw.text(brand_pos, BRAND_TEXT, fill=BRAND_COLOR, font=brand_font)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_social_images(post, force: bool = False) -> Tuple[str, str]:
    text = getattr(post, "meta_title", None) or post.title
    slug = getattr(post, "slug", "post")
    filename_base = slug.replace("/", "-")
    title_hash = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
    filename_base = f"{filename_base}-{title_hash}"

    og_name = f"{filename_base}_og.png"
    twitter_name = f"{filename_base}_twitter.png"

    og_path = f"social/{og_name}"
    twitter_path = f"social/{twitter_name}"

    if force:
        if default_storage.exists(og_path):
            default_storage.delete(og_path)
        if default_storage.exists(twitter_path):
            default_storage.delete(twitter_path)

    og_bytes = _create_image_bytes(text)
    twitter_bytes = _create_image_bytes(text)
    og_storage_path = default_storage.save(og_path, ContentFile(og_bytes))
    twitter_storage_path = default_storage.save(twitter_path, ContentFile(twitter_bytes))

    og_url = default_storage.url(og_storage_path)
    twitter_url = default_storage.url(twitter_storage_path)

    base_url = getattr(settings, "SITE_BASE_URL", "").rstrip("/")
    if base_url:
        og_url = urljoin(base_url + "/", og_url.lstrip("/"))
        twitter_url = urljoin(base_url + "/", twitter_url.lstrip("/"))

    return og_url, twitter_url
