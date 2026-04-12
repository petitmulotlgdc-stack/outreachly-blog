from datetime import date
from unittest.mock import MagicMock, patch

from distributor.post_reader import PostInfo


def make_post():
    return PostInfo(
        title="Best CRM for Coaches",
        slug="best-crm-for-coaches",
        date=date(2026, 4, 12),
        url="https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/",
        summary="Great article about CRM tools for coaches.",
        body_md="# Best CRM\n\nBody here.",
    )


def test_post_to_linkedin_returns_url():
    from distributor.linkedin import post_to_linkedin

    with patch("distributor.linkedin.requests.get") as mock_get, \
         patch("distributor.linkedin.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"id": "person123"}
        mock_get.return_value.raise_for_status = MagicMock()

        mock_resp = MagicMock()
        mock_resp.headers = {"x-restli-id": "urn:li:ugcPost:9876"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = post_to_linkedin(make_post(), access_token="fake-token")

    assert "linkedin.com" in result


def test_post_to_linkedin_uses_correct_author_urn():
    from distributor.linkedin import post_to_linkedin

    with patch("distributor.linkedin.requests.get") as mock_get, \
         patch("distributor.linkedin.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"id": "abc123"}
        mock_get.return_value.raise_for_status = MagicMock()
        mock_post.return_value.headers = {"x-restli-id": "urn:li:ugcPost:1"}
        mock_post.return_value.raise_for_status = MagicMock()

        post_to_linkedin(make_post(), access_token="fake-token")

        payload = mock_post.call_args[1]["json"]

    assert payload["author"] == "urn:li:person:abc123"
    assert payload["lifecycleState"] == "PUBLISHED"


def test_post_to_linkedin_commentary_contains_url():
    from distributor.linkedin import post_to_linkedin

    with patch("distributor.linkedin.requests.get") as mock_get, \
         patch("distributor.linkedin.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"id": "abc"}
        mock_get.return_value.raise_for_status = MagicMock()
        mock_post.return_value.headers = {"x-restli-id": "urn:li:ugcPost:1"}
        mock_post.return_value.raise_for_status = MagicMock()

        post_to_linkedin(make_post(), access_token="fake-token")

        payload = mock_post.call_args[1]["json"]

    commentary = payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
    assert "blog.outreachly.pro" in commentary
