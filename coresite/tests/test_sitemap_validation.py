import os
import gzip
import random
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

import unittest

# Configuration via environment variables
MODE = os.environ.get("SITEMAP_VALIDATE_MODE", "artifact")
ENV = os.environ.get("ENV", "development")
CANONICAL_HOST = os.environ.get("CANONICAL_HOST", "technofatty.com")
SITEMAP_PATH = os.environ.get("SITEMAP_VALIDATE_PATH", "build/sitemap.xml")
PORT = os.environ.get("SITEMAP_VALIDATE_PORT", "8000")
HEAD_SAMPLE = int(os.environ.get("SITEMAP_VALIDATE_HEAD_SAMPLE", "0"))

TRAILING_SLASH = True
QUERY_ALLOWLIST = {"page"}
RETIRED_PATHS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "seo", "retired_endpoints.txt")
RETIRED_PATHS_FILE = os.path.normpath(RETIRED_PATHS_FILE)


def _load_retired_paths():
    paths = set()
    if os.path.exists(RETIRED_PATHS_FILE):
        with open(RETIRED_PATHS_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                paths.add(line.lstrip("/"))
    return paths


class SitemapValidationTest(unittest.TestCase):
    maxDiff = None

    def _fetch(self, path):
        if MODE == "server":
            try:
                from django.test import Client
            except Exception as exc:  # pragma: no cover
                self.fail(f"Django required for server mode: {exc}")
            client = Client()
            resp = client.get(path)
            self.assertEqual(resp.status_code, 200, f"GET {path} returned {resp.status_code}")
            content = resp.content
            content_type = resp["Content-Type"]
        else:
            with open(path, "rb") as f:
                content = f.read()
            content_type = "application/xml"
        if path.endswith(".gz") or "gzip" in content_type:
            content = gzip.decompress(content)
        return content

    def _parse(self, content):
        root = ET.fromstring(content)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = []
        sitemaps = []
        if root.tag == f"{ns}urlset":
            for url_el in root.findall(f"{ns}url"):
                loc = url_el.findtext(f"{ns}loc")
                lastmod = url_el.findtext(f"{ns}lastmod")
                urls.append((loc, lastmod))
        elif root.tag == f"{ns}sitemapindex":
            for sm in root.findall(f"{ns}sitemap"):
                loc = sm.findtext(f"{ns}loc")
                sitemaps.append(loc)
        else:
            self.fail("Unknown sitemap root tag")
        return urls, sitemaps

    def _validate_url(self, url, retired_paths, seen, problems):
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            problems.append(f"Not absolute URL: {url}")
            return
        if ENV == "production":
            if parsed.scheme != "https":
                problems.append(f"Non-https URL in production: {url}")
            if parsed.netloc != CANONICAL_HOST:
                problems.append(f"Non-canonical host: {url}")
        if TRAILING_SLASH and not parsed.path.endswith("/"):
            problems.append(f"Missing trailing slash: {url}")
        if parsed.query:
            qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            if not set(qs).issubset(QUERY_ALLOWLIST):
                problems.append(f"Query string not allowed: {url}")
        if parsed.fragment:
            problems.append(f"Fragment not allowed: {url}")
        path = parsed.path.lstrip("/")
        if path in retired_paths:
            problems.append(f"Retired path present: {url}")
        if url in seen:
            problems.append(f"Duplicate URL: {url}")
        seen.add(url)

    def _validate_lastmod(self, lastmod, url, problems):
        if lastmod is None:
            return  # optional
        try:
            datetime.fromisoformat(lastmod.replace("Z", "+00:00"))
        except ValueError:
            problems.append(f"Invalid lastmod for {url}: {lastmod}")

    def _head_check(self, urls):
        if MODE != "server" or HEAD_SAMPLE <= 0:
            return
        try:
            from django.test import Client
        except Exception:
            return
        client = Client()
        rnd = random.Random(0)
        sample_size = min(HEAD_SAMPLE, len(urls), 25)
        for url in rnd.sample(list(urls), sample_size):
            path = urllib.parse.urlparse(url).path
            resp = client.head(path)
            if resp.status_code != 200:
                self.fail(f"HEAD {path} returned {resp.status_code}")

    def test_sitemap(self):
        retired_paths = _load_retired_paths()
        urls_to_process = [SITEMAP_PATH] if MODE != "server" else [f"/sitemap.xml"]
        all_urls = []
        sitemap_count = 0
        problems = []
        seen = set()
        while urls_to_process:
            current = urls_to_process.pop()
            content = self._fetch(current)
            urls, sitemaps = self._parse(content)
            sitemap_count += 1
            for loc, lastmod in urls:
                self._validate_url(loc, retired_paths, seen, problems)
                self._validate_lastmod(lastmod, loc, problems)
                all_urls.append(loc)
            for sm in sitemaps:
                urls_to_process.append(sm if MODE != "server" else urllib.parse.urlparse(sm).path)
        self._head_check(all_urls)
        sample = all_urls[:10]
        print(f"Sitemap validation mode: {MODE}, canonical host: {CANONICAL_HOST}")
        print("Sample URLs:")
        for u in sample:
            print(" ", u)
        print(f"Total sitemaps: {sitemap_count}; URLs: {len(all_urls)}; Duplicates: {len(all_urls)-len(seen)}")
        if problems:
            self.fail("; ".join(problems))
