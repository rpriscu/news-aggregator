import sys
from .models import Article
from .utils import extract_text, to_json, make_id

def fetch_with_playwright(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000)
        html = page.content()
        browser.close()
    return html

def fetch_with_requests(url):
    import requests
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_article(url, html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title else "Untitled"
    author = None
    published_at = None
    # Try to extract author and published date from meta tags
    if soup.find("meta", attrs={"name": "author"}):
        author = soup.find("meta", attrs={"name": "author"}).get("content")
    if soup.find("meta", attrs={"property": "article:published_time"}):
        published_at = soup.find("meta", attrs={"property": "article:published_time"}).get("content")
    text = extract_text(soup)
    id_ = make_id(title)
    return Article(id=id_, url=url, title=title, author=author, published_at=published_at, text=text)

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src.fetch <url>", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    try:
        html = fetch_with_playwright(url)
    except Exception:
        try:
            html = fetch_with_requests(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}", file=sys.stderr)
            sys.exit(2)
    article = parse_article(url, html)
    print(to_json(article))

if __name__ == "__main__":
    main()