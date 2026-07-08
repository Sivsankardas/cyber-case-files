"""
Resolves a real image URL to attach to posts. Checks the RSS entry itself
first (media:content / media:thumbnail / image enclosure -- free, no extra
request), and only falls back to fetching the article page and reading its
og:image meta tag if the feed didn't include one.
"""
import re
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CyberCaseFilesBot/1.0)"}

OG_IMAGE_PATTERNS = [
    re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', re.IGNORECASE),
    re.compile(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE),
]


def image_from_entry(entry) -> str | None:
    """Pulls an image straight from RSS/Atom entry metadata, if present."""
    media = entry.get("media_content") or entry.get("media_thumbnail")
    if media:
        url = media[0].get("url")
        if url:
            return url

    for link in entry.get("links", []) or []:
        if str(link.get("type", "")).startswith("image"):
            href = link.get("href")
            if href:
                return href

    return None


def fetch_og_image(url: str, timeout: int = 10) -> str | None:
    """Fetches the article page and reads its og:image / twitter:image tag."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        html = resp.text[:250000]
        for pattern in OG_IMAGE_PATTERNS:
            match = pattern.search(html)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"[Image fetch error] {url}: {e}")
    return None


def resolve_image(entry=None, url: str = None) -> str | None:
    """Best-effort image resolution: entry metadata first, then og:image."""
    if entry is not None:
        img = image_from_entry(entry)
        if img:
            return img
    if url:
        return fetch_og_image(url)
    return None
