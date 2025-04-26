import json
from slugify import slugify
import hashlib

def extract_text(soup):
    # Simple extraction: get all text from <p> tags
    return "\n".join(p.get_text(strip=True) for p in soup.find_all("p"))

def to_json(article):
    return json.dumps(article.__dict__, ensure_ascii=False, indent=2)

def make_id(title):
    slug = slugify(title)
    h = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return f"{slug}-{h}"