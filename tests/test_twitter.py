# tests/test_twitter.py
from datetime import date
from unittest.mock import MagicMock, patch

from distributor.post_reader import PostInfo


def make_post():
    return PostInfo(
        title="Best CRM for Coaches",
        slug="best-crm-for-coaches",
        date=date(2026, 4, 12),
        url="https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/",
        summary="Great article about CRM tools.",
        body_md="# Best CRM\n\nBody here.",
    )


def test_post_to_twitter_returns_url():
    from distributor.twitter import post_to_twitter

    with patch("distributor.twitter.tweepy.Client") as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        mock_client.create_tweet.return_value.data = {"id": "99887766"}

        result = post_to_twitter(make_post(), "key", "secret", "token", "token_secret")

    assert result == "https://twitter.com/i/web/status/99887766"


def test_post_to_twitter_tweet_contains_url():
    from distributor.twitter import post_to_twitter

    with patch("distributor.twitter.tweepy.Client") as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        mock_client.create_tweet.return_value.data = {"id": "123"}

        post_to_twitter(make_post(), "key", "secret", "token", "token_secret")

        tweet_text = mock_client.create_tweet.call_args[1]["text"]

    assert "blog.outreachly.pro" in tweet_text
    assert len(tweet_text) <= 280


def test_post_to_twitter_truncates_long_title():
    from distributor.twitter import post_to_twitter

    long_title_post = PostInfo(
        title="A" * 200,
        slug="test",
        date=date(2026, 4, 12),
        url="https://blog.outreachly.pro/test/",
        summary="Summary.",
        body_md="Body.",
    )

    with patch("distributor.twitter.tweepy.Client") as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        mock_client.create_tweet.return_value.data = {"id": "1"}

        post_to_twitter(long_title_post, "key", "secret", "token", "token_secret")

        tweet_text = mock_client.create_tweet.call_args[1]["text"]

    assert len(tweet_text) <= 280
