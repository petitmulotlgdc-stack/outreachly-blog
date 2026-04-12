from typing import Optional

import requests

MEDIUM_API = "https://api.medium.com/v1"
TAGS = ["business", "productivity", "tools", "entrepreneurship", "saas"]


def post_to_medium(post, token: str) -> Optional[str]:
    """Publish full article to Medium with canonicalUrl. Returns URL of published post."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Get user ID
    me_resp = requests.get(f"{MEDIUM_API}/me", headers=headers, timeout=10)
    me_resp.raise_for_status()
    user_id = me_resp.json()["data"]["id"]

    payload = {
        "title": post.title,
        "contentFormat": "markdown",
        "content": post.body_md,
        "canonicalUrl": post.url,
        "publishStatus": "public",
        "tags": TAGS,
    }

    resp = requests.post(
        f"{MEDIUM_API}/users/{user_id}/posts",
        json=payload,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["data"]["url"]
