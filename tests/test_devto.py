# tests/test_devto.py
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


def test_post_to_devto_returns_url():
    from distributor.devto import post_to_devto

    with patch("distributor.devto.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "url": "https://dev.to/outreachly/best-crm-for-coaches-abc123"
        }
        mock_post.return_value.raise_for_status = MagicMock()

        result = post_to_devto(make_post(), api_key="fake-key")

    assert result == "https://dev.to/outreachly/best-crm-for-coaches-abc123"


def test_post_to_devto_sets_canonical_url():
    from distributor.devto import post_to_devto

    with patch("distributor.devto.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"url": "https://dev.to/p/abc"}
        mock_post.return_value.raise_for_status = MagicMock()

        post_to_devto(make_post(), api_key="fake-key")

        payload = mock_post.call_args[1]["json"]

    assert payload["article"]["canonical_url"] == "https://blog.outreachly.pro/2026/04/12/best-crm-for-coaches/"
    assert payload["article"]["published"] is True
    assert "business" in payload["article"]["tags"]
