import os
from pathlib import Path
from typing import Dict, Optional

from distributor.linkedin import post_to_linkedin
from distributor.medium import post_to_medium
from distributor.post_reader import read_latest_post
from distributor.reddit import post_to_reddit
from distributor.twitter import post_to_twitter


def distribute(posts_dir: str) -> Dict[str, str]:
    """Distribute latest post to all configured platforms. Returns dict of platform -> url."""
    post = read_latest_post(posts_dir)
    if post is None:
        print("No posts found. Skipping distribution.")
        return {}

    print(f"Distributing: {post.title} ({post.url})")
    results: Dict[str, str] = {}

    # Medium
    medium_token = os.environ.get("MEDIUM_TOKEN")
    if medium_token:
        try:
            url = post_to_medium(post, token=medium_token)
            results["medium"] = url
            print(f"✓ Medium: {url}")
        except Exception as e:
            print(f"✗ Medium failed: {e}")

    # Reddit
    reddit_id = os.environ.get("REDDIT_CLIENT_ID")
    reddit_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    reddit_user = os.environ.get("REDDIT_USERNAME")
    reddit_pass = os.environ.get("REDDIT_PASSWORD")
    if all([reddit_id, reddit_secret, reddit_user, reddit_pass]):
        try:
            url = post_to_reddit(
                post, client_id=reddit_id, client_secret=reddit_secret,
                username=reddit_user, password=reddit_pass,
            )
            results["reddit"] = url
            print(f"✓ Reddit: {url}")
        except Exception as e:
            print(f"✗ Reddit failed: {e}")

    # Twitter
    tw_key = os.environ.get("TWITTER_API_KEY")
    tw_secret = os.environ.get("TWITTER_API_SECRET")
    tw_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    tw_secret2 = os.environ.get("TWITTER_ACCESS_SECRET")
    if all([tw_key, tw_secret, tw_token, tw_secret2]):
        try:
            url = post_to_twitter(
                post, api_key=tw_key, api_secret=tw_secret,
                access_token=tw_token, access_secret=tw_secret2,
            )
            results["twitter"] = url
            print(f"✓ Twitter: {url}")
        except Exception as e:
            print(f"✗ Twitter failed: {e}")

    # LinkedIn
    linkedin_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if linkedin_token:
        try:
            url = post_to_linkedin(post, access_token=linkedin_token)
            results["linkedin"] = url
            print(f"✓ LinkedIn: {url}")
        except Exception as e:
            print(f"✗ LinkedIn failed: {e}")

    print(f"Distribution complete. {len(results)}/4 platforms succeeded.")
    return results


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    repo_root = Path(__file__).parent.parent
    distribute(posts_dir=str(repo_root / "docs" / "_posts"))
