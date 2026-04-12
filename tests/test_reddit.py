from datetime import date
from unittest.mock import MagicMock, patch

from distributor.post_reader import PostInfo


def make_post(day=12):
    return PostInfo(
        title="Best CRM for Coaches",
        slug="best-crm-for-coaches",
        date=date(2026, 4, day),
        url="https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/",
        summary="Great article about CRM tools.",
        body_md="# Best CRM\n\nBody here.",
    )


def test_post_to_reddit_returns_url():
    from distributor.reddit import post_to_reddit

    with patch("distributor.reddit.praw.Reddit") as MockReddit:
        mock_reddit = MagicMock()
        MockReddit.return_value = mock_reddit
        mock_sub = MagicMock()
        mock_reddit.subreddit.return_value = mock_sub
        mock_sub.submit.return_value.permalink = "/r/entrepreneur/comments/abc/best_crm/"

        result = post_to_reddit(make_post(), "id", "secret", "user", "pass")

    assert result == "https://reddit.com/r/entrepreneur/comments/abc/best_crm/"


def test_post_to_reddit_rotates_subreddits():
    from distributor.reddit import post_to_reddit, SUBREDDITS

    used_subreddits = set()
    for day in range(1, len(SUBREDDITS) + 1):
        with patch("distributor.reddit.praw.Reddit") as MockReddit:
            mock_reddit = MagicMock()
            MockReddit.return_value = mock_reddit
            mock_reddit.subreddit.return_value.submit.return_value.permalink = "/r/test/abc"

            post_to_reddit(make_post(day=day), "id", "secret", "user", "pass")
            used_subreddits.add(mock_reddit.subreddit.call_args[0][0])

    assert len(used_subreddits) > 1


def test_post_to_reddit_submits_with_url():
    from distributor.reddit import post_to_reddit

    with patch("distributor.reddit.praw.Reddit") as MockReddit:
        mock_reddit = MagicMock()
        MockReddit.return_value = mock_reddit
        mock_sub = MagicMock()
        mock_reddit.subreddit.return_value = mock_sub
        mock_sub.submit.return_value.permalink = "/r/entrepreneur/comments/abc/"

        post_to_reddit(make_post(), "id", "secret", "user", "pass")

        _, kwargs = mock_sub.submit.call_args

    assert kwargs["url"] == "https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/"
    assert "Best CRM for Coaches" in mock_sub.submit.call_args[0][0]
