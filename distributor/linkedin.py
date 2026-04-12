from typing import Optional

import requests

LINKEDIN_API = "https://api.linkedin.com/v2"
HASHTAGS = "#entrepreneur #smallbusiness #coaches"


def post_to_linkedin(post, access_token: str) -> Optional[str]:
    """Post article to LinkedIn as a UGC share. Returns post URL."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    # Get the authenticated person's URN
    me_resp = requests.get(f"{LINKEDIN_API}/me", headers=headers, timeout=10)
    me_resp.raise_for_status()
    person_id = me_resp.json()["id"]
    author_urn = f"urn:li:person:{person_id}"

    commentary = (
        f"{post.title}\n\n"
        f"{post.summary[:200]}\n\n"
        f"Read the full article: {post.url}\n\n"
        f"{HASHTAGS}"
    )

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": commentary},
                "shareMediaCategory": "ARTICLE",
                "media": [{
                    "status": "READY",
                    "description": {"text": post.summary[:200]},
                    "originalUrl": post.url,
                    "title": {"text": post.title},
                }],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp = requests.post(f"{LINKEDIN_API}/ugcPosts", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    post_id = resp.headers.get("x-restli-id", "unknown")
    return f"https://www.linkedin.com/feed/update/{post_id}/"
