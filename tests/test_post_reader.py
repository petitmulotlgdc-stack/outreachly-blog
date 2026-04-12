from datetime import date
from pathlib import Path
import pytest


def make_post_file(tmp_path, filename, title, body):
    content = f'---\nlayout: post\ntitle: "{title}"\ndate: 2026-04-12\n---\n\n{body}'
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


def test_read_latest_post_returns_post_info(tmp_path):
    from distributor.post_reader import read_latest_post, PostInfo
    make_post_file(tmp_path, "2026-04-12-best-crm-for-coaches.md",
                   "Best CRM for Coaches", "# Best CRM\n\nGreat article about Brevo.")

    post = read_latest_post(str(tmp_path))
    assert isinstance(post, PostInfo)
    assert post.title == "Best CRM for Coaches"
    assert post.slug == "best-crm-for-coaches"
    assert post.date == date(2026, 4, 12)
    assert "blog.outreachly.pro" in post.url
    assert "2026/04/12" in post.url


def test_read_latest_post_returns_most_recent(tmp_path):
    from distributor.post_reader import read_latest_post
    make_post_file(tmp_path, "2026-04-10-older-article.md", "Older", "Old body.")
    make_post_file(tmp_path, "2026-04-12-newer-article.md", "Newer", "New body.")

    post = read_latest_post(str(tmp_path))
    assert post.slug == "newer-article"


def test_read_latest_post_returns_none_when_empty(tmp_path):
    from distributor.post_reader import read_latest_post
    assert read_latest_post(str(tmp_path)) is None


def test_summary_strips_markdown(tmp_path):
    from distributor.post_reader import read_latest_post
    make_post_file(tmp_path, "2026-04-12-test.md", "Test",
                   "# Heading\n\nNormal text with **bold** and [link](http://example.com).")

    post = read_latest_post(str(tmp_path))
    assert "**" not in post.summary
    assert "http://" not in post.summary
    assert "Heading" in post.summary
    assert "Normal text" in post.summary
