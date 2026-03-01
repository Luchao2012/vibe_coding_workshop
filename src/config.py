"""Simple configuration for the ACC chatbot demo.

Keep this file easy to read and edit for students.
"""

from __future__ import annotations

# List the ACC pages you want to crawl.
# Replace these with real ACC URLs for your workshop.
ACC_URLS: list[str] = [
    "https://asianchamber-hou.org/",
    "https://asianchamber-hou.org/the-chamber/",
    "https://asianchamber-hou.org/membership-info/",
    "https://asianchamber-hou.org/programs/",
    "https://asianchamber-hou.org/around-the-chamber/",
    "https://asianchamber-hou.org/business-resources/",
    "https://asianchamber-hou.org/bid-opportunities/",
    "https://asianchamber-hou.org/contact/",
]

# Where to save crawled markdown files
RAW_DATA_DIR = "data/raw"

# How long to wait between requests (be polite to websites)
REQUEST_DELAY_SECONDS = 1.0

# User-Agent string to identify this crawler
USER_AGENT = "ACC-Workshop-Crawler/1.0"
