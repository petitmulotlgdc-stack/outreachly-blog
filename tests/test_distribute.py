# tests/test_distribute.py
import os
from pathlib import Path
from unittest.mock import patch

import pytest


def make_post_file(tmp_path):
    content = '---\nlayout: post\ntitle: "Best CRM"\ndate: 2026-04-12\n---\n\n# Best CRM\n\nBody.'
    (tmp_path / "2026-04-12-best-crm.md").write_text(content, encoding="utf-8")
    return str(tmp_path)


def test_distribute_calls_all_platforms(tmp_path):
    from distributor.distribute import distribute

    posts_dir = make_post_file(tmp_path)
    env = {
        "DEVTO_API_KEY": "dk",
        "REDDIT_CLIENT_ID": "ri", "REDDIT_CLIENT_SECRET": "rs",
        "REDDIT_USERNAME": "ru", "REDDIT_PASSWORD": "rp",
        "TWITTER_API_KEY": "tk", "TWITTER_API_SECRET": "ts",
        "TWITTER_ACCESS_TOKEN": "tat", "TWITTER_ACCESS_SECRET": "tas",
        "LINKEDIN_ACCESS_TOKEN": "lt",
    }

    with patch.dict(os.environ, env, clear=True), \
         patch("distributor.distribute.post_to_devto", return_value="https://dev.to/p/abc") as m_devto, \
         patch("distributor.distribute.post_to_reddit", return_value="https://reddit.com/r/abc") as m_reddit, \
         patch("distributor.distribute.post_to_twitter", return_value="https://twitter.com/i/1") as m_twitter, \
         patch("distributor.distribute.post_to_linkedin", return_value="https://linkedin.com/abc") as m_linkedin:

        results = distribute(posts_dir)

    assert m_devto.called
    assert m_reddit.called
    assert m_twitter.called
    assert m_linkedin.called
    assert len(results) == 4


def test_distribute_skips_platform_when_env_missing(tmp_path):
    from distributor.distribute import distribute

    posts_dir = make_post_file(tmp_path)

    with patch.dict(os.environ, {"DEVTO_API_KEY": "dk"}, clear=True), \
         patch("distributor.distribute.post_to_devto", return_value="https://dev.to/p/abc") as m_devto, \
         patch("distributor.distribute.post_to_reddit") as m_reddit:

        distribute(posts_dir)

    assert m_devto.called
    assert not m_reddit.called


def test_distribute_continues_when_platform_fails(tmp_path):
    from distributor.distribute import distribute

    posts_dir = make_post_file(tmp_path)
    env = {
        "DEVTO_API_KEY": "dk",
        "REDDIT_CLIENT_ID": "ri", "REDDIT_CLIENT_SECRET": "rs",
        "REDDIT_USERNAME": "ru", "REDDIT_PASSWORD": "rp",
    }

    with patch.dict(os.environ, env, clear=True), \
         patch("distributor.distribute.post_to_devto", side_effect=Exception("API error")), \
         patch("distributor.distribute.post_to_reddit", return_value="https://reddit.com/r/abc") as m_reddit:

        results = distribute(posts_dir)

    assert m_reddit.called
    assert "reddit" in results
    assert "devto" not in results


def test_distribute_returns_empty_when_no_posts(tmp_path):
    from distributor.distribute import distribute

    results = distribute(str(tmp_path))
    assert results == {}
