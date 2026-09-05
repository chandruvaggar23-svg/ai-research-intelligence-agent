import os
import time
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

MAX_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
FETCH_TIMEOUT = 8   # seconds per URL
MAX_CONTENT_CHARS = 3000


def search(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, str]]:
    """Run a DuckDuckGo text search and return results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
                "content": "",   # filled by fetch_content()
            })
    return results


def fetch_content(url: str) -> str:
    """Scrape visible text from a URL. Returns '' on failure."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchIQ/1.0)"}
        resp = requests.get(url, headers=headers, timeout=FETCH_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove scripts, styles, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Collapse blank lines
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return "\n".join(lines)[:MAX_CONTENT_CHARS]
    except Exception:
        return ""


def search_and_fetch(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, str]]:
    """Search DuckDuckGo + fetch full content for each result."""
    results = search(query, max_results)
    for r in results:
        r["content"] = fetch_content(r["url"])
        time.sleep(0.3)   # polite delay
    # Fall back to snippet if fetch failed
    for r in results:
        if not r["content"]:
            r["content"] = r["snippet"]
    return results
