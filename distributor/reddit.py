from typing import Optional

import praw

SUBREDDITS = ["entrepreneur", "smallbusiness", "productivity"]


def post_to_reddit(
    post,
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
) -> Optional[str]:
    """Submit article link to a rotating subreddit. Returns URL of the Reddit post."""
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="outreachly-bot/1.0",
    )

    # Rotate subreddit by day of month to avoid posting to the same one daily
    subreddit_name = SUBREDDITS[post.date.day % len(SUBREDDITS)]
    subreddit = reddit.subreddit(subreddit_name)

    submission = subreddit.submit(post.title, url=post.url)
    return f"https://reddit.com{submission.permalink}"
