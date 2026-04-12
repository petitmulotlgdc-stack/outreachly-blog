import json
import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from pathlib import Path

@pytest.fixture
def setup_dirs(tmp_path):
    # keywords.json
    keywords_data = {
        "templates": ["best {tool_category} for {niche}"],
        "variables": {
            "tool_category": ["CRM"],
            "niche": ["coaches"]
        },
        "used": []
    }
    keywords_path = tmp_path / "keywords.json"
    keywords_path.write_text(json.dumps(keywords_data), encoding="utf-8")

    # affiliates.json
    affiliates_data = {"Brevo": "https://brevo.com/?via=outreachly"}
    affiliates_path = tmp_path / "affiliates.json"
    affiliates_path.write_text(json.dumps(affiliates_data), encoding="utf-8")

    # posts dir
    posts_dir = tmp_path / "site" / "_posts"
    posts_dir.mkdir(parents=True)

    return {
        "keywords_path": str(keywords_path),
        "affiliates_path": str(affiliates_path),
        "posts_dir": str(posts_dir),
    }

def test_run_creates_markdown_file(setup_dirs):
    from generator.generate import run
    from generator.article import Article

    mock_article = Article(
        keyword="best CRM for coaches",
        title="Best CRM for Coaches",
        slug="best-crm-for-coaches",
        body="# Best CRM for Coaches\n\nGreat article.",
        date=date.today(),
    )

    with patch("generator.generate.write_article", return_value=mock_article):
        run(
            keywords_path=setup_dirs["keywords_path"],
            affiliates_path=setup_dirs["affiliates_path"],
            posts_dir=setup_dirs["posts_dir"],
            api_key="fake-key",
        )

    posts = list(Path(setup_dirs["posts_dir"]).glob("*.md"))
    assert len(posts) == 1
    content = posts[0].read_text(encoding="utf-8")
    assert "Best CRM for Coaches" in content
    assert "---" in content  # front matter
