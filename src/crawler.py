"""Simple web crawler for ACC pages with recursive link following.

This script:
1) Downloads HTML from seed URLs
2) Finds all links to ACC pages
3) Recursively crawls linked pages (up to depth limit)
4) Extracts readable text (headings + paragraphs + lists)
5) Saves it as a markdown file

Keep it simple and explainable for students.
"""

from __future__ import annotations

import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from src.config import ACC_URLS, RAW_DATA_DIR, REQUEST_DELAY_SECONDS, USER_AGENT


def slug_from_url(url: str) -> str:
    """Turn a URL into a safe filename slug."""
    parsed = urlparse(url)
    # Example: https://example.com/about -> example.com_about
    path = parsed.path.strip("/") or "home"
    slug = f"{parsed.netloc}_{path}".replace("/", "_")
    return slug


def extract_text(html: str) -> str:
    """Extract readable text from HTML.

    We keep headings, paragraphs, list items, divs, and spans.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts and styles to avoid noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lines: list[str] = []

    # Extract from more element types to capture prices/tier names
    for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "div", "span"]):
        text = element.get_text(strip=True)
        if text and len(text) > 2:  # Skip very short text
            # Add markdown style for headings
            if element.name == "h1":
                lines.append(f"# {text}")
            elif element.name == "h2":
                lines.append(f"## {text}")
            elif element.name == "h3":
                lines.append(f"### {text}")
            elif element.name == "h4":
                lines.append(f"#### {text}")
            else:
                lines.append(text)

    return "\n\n".join(lines)


def extract_links(html: str, base_url: str) -> list[str]:
    """Extract all links from HTML, resolve relative URLs."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    
    for link_tag in soup.find_all("a", href=True):
        href = link_tag["href"]
        # Resolve relative URLs
        absolute_url = urljoin(base_url, href)
        # Remove fragments (#)
        absolute_url = absolute_url.split("#")[0]
        links.append(absolute_url)
    
    return links


def is_acc_url(url: str) -> bool:
    """Check if URL is within ACC domain."""
    parsed = urlparse(url)
    return "asianchamber-hou.org" in parsed.netloc


def fetch_html(url: str) -> str:
    """Download HTML from a URL."""
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(timeout=20, headers=headers) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def save_markdown(url: str, content: str, output_dir: Path) -> Path:
    """Save extracted content as a markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = slug_from_url(url)
    file_path = output_dir / f"{slug}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def crawl() -> None:
    """Recursively crawl ACC website starting from seed URLs."""
    output_dir = Path(RAW_DATA_DIR)
    visited_urls: set[str] = set()
    to_visit: list[str] = list(ACC_URLS)
    max_pages = 50  # Safety limit to avoid infinite crawls

    print(f"Starting recursive crawl (max {max_pages} pages)...\n")

    while to_visit and len(visited_urls) < max_pages:
        url = to_visit.pop(0)
        
        # Normalize URL (remove trailing slash for comparison)
        url_normalized = url.rstrip("/")
        
        # Skip if already visited
        if url_normalized in visited_urls:
            continue
        
        visited_urls.add(url_normalized)

        print(f"Crawling ({len(visited_urls)}/{max_pages}): {url}")
        
        try:
            html = fetch_html(url)
            text = extract_text(html)
            
            if not text.strip():
                print("  ⚠ No text extracted")
            else:
                path = save_markdown(url, text, output_dir)
                print(f"  ✓ Saved: {path.name}")
            
            # Extract links and add to queue
            links = extract_links(html, url)
            new_links = 0
            for link in links:
                link_normalized = link.rstrip("/")
                if is_acc_url(link) and link_normalized not in visited_urls:
                    to_visit.append(link)
                    new_links += 1
            
            if new_links > 0:
                print(f"  → Found {new_links} new links to crawl")
        
        except Exception as exc:
            print(f"  ✗ Error: {exc}")

        # Be polite to the website
        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"\n✅ Crawl complete! Downloaded {len(visited_urls)} pages.")


if __name__ == "__main__":
    crawl()
