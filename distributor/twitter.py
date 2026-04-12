# distributor/twitter.py
from typing import Optional

import tweepy

MAX_TWEET_LENGTH = 280
HASHTAGS = "#entrepreneur #smallbusiness #productivity"


def post_to_twitter(
    post,
    api_key: str,
    api_secret: str,
    access_token: str,
    access_secret: str,
) -> Optional[str]:
    """Post a tweet with title + link. Returns URL of the tweet."""
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

    base = f"\n\n{post.url}\n\n{HASHTAGS}"
    max_title = MAX_TWEET_LENGTH - len(base) - 3  # 3 for "..."
    title = post.title if len(post.title) <= max_title else post.title[:max_title] + "..."
    text = f"{title}{base}"

    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    return f"https://twitter.com/i/web/status/{tweet_id}"
