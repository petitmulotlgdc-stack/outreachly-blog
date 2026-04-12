# distributor/devto.py
from typing import Optional

import requests

DEVTO_API = "https://dev.to/api"
TAGS = ["business", "productivity", "tools", "entrepreneur"]


def post_to_devto(post, api_key: str) -> Optional[str]:
    """Publish full article to Dev.to with canonical_url. Returns URL of published article."""
    payload = {
        "article": {
            "title": post.title,
            "body_markdown": post.body_md,
            "published": True,
            "canonical_url": post.url,
            "tags": TAGS,
        }
    }

    resp = requests.post(
        f"{DEVTO_API}/articles",
        json=payload,
        headers={"api-key": api_key},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["url"]
