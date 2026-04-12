import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import date

def make_affiliates(tmp_path):
    data = {
        "Brevo": "https://brevo.com/?via=outreachly",
        "Apollo": "https://apollo.io/?via=outreachly"
    }
    path = tmp_path / "affiliates.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)

def test_write_article_returns_article(tmp_path):
    from generator.writer import write_article
    from generator.article import Article

    affiliates_path = make_affiliates(tmp_path)
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="# Best CRM for Coaches\n\nThis is the article body about Brevo and Apollo.")]

    with patch("generator.writer.anthropic.Anthropic") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.messages.create.return_value = mock_response

        article = write_article(
            keyword="best CRM for coaches",
            affiliates_path=affiliates_path,
            api_key="fake-key"
        )

    assert isinstance(article, Article)
    assert article.keyword == "best CRM for coaches"
    assert len(article.body) > 10
    assert article.date == date.today()

def test_write_article_injects_affiliate_links(tmp_path):
    from generator.writer import write_article

    affiliates_path = make_affiliates(tmp_path)
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="# Best CRM\n\nUse Brevo for email and Apollo for leads.")]

    with patch("generator.writer.anthropic.Anthropic") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.messages.create.return_value = mock_response

        article = write_article(
            keyword="best CRM for coaches",
            affiliates_path=affiliates_path,
            api_key="fake-key"
        )

    assert "https://brevo.com/?via=outreachly" in article.body
