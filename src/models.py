from dataclasses import dataclass
from typing import Optional

@dataclass
class Article:
    id: str
    url: str
    title: str
    author: Optional[str]
    published_at: Optional[str]
    text: str