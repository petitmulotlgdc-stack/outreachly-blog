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
        body_md="# Best CRM for Coaches\n\nBody here.",
    )


def test_post_to_medium_returns_url():
    from distributor.medium import post_to_medium

    with patch("distributor.medium.requests.get") as mock_get, \
         patch("distributor.medium.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"data": {"id": "user123"}}
        mock_get.return_value.raise_for_status = MagicMock()

        mock_post.return_value.json.return_value = {
            "data": {"url": "https://medium.com/@outreachly/best-crm-abc123"}
        }
        mock_post.return_value.raise_for_status = MagicMock()

        result = post_to_medium(make_post(), token="fake-token")

    assert result == "https://medium.com/@outreachly/best-crm-abc123"


def test_post_to_medium_sets_canonical_url():
    from distributor.medium import post_to_medium

    with patch("distributor.medium.requests.get") as mock_get, \
         patch("distributor.medium.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"data": {"id": "user123"}}
        mock_get.return_value.raise_for_status = MagicMock()
        mock_post.return_value.json.return_value = {"data": {"url": "https://medium.com/p/abc"}}
        mock_post.return_value.raise_for_status = MagicMock()

        post_to_medium(make_post(), token="fake-token")

        _, kwargs = mock_post.call_args

    assert kwargs["json"]["canonicalUrl"] == "https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/"
    assert kwargs["json"]["contentFormat"] == "markdown"
    assert "business" in kwargs["json"]["tags"]
