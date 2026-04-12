# tests/test_article.py
from datetime import date
from generator.article import Article


def make_article(**kwargs):
    defaults = dict(
        keyword="best CRM for coaches",
        title="Best CRM for Coaches",
        slug="best-crm-for-coaches",
        body="# Best CRM for Coaches\n\nGreat article body.",
        date=date(2026, 4, 12),
    )
    defaults.update(kwargs)
    return Article(**defaults)


def test_filename_format():
    article = make_article()
    assert article.filename() == "2026-04-12-best-crm-for-coaches.md"


def test_to_markdown_has_front_matter():
    article = make_article()
    md = article.to_markdown()
    assert md.startswith("---\n")
    assert "layout: post" in md
    assert 'title: "Best CRM for Coaches"' in md
    assert "date: 2026-04-12" in md
    assert "---" in md


def test_to_markdown_contains_body():
    article = make_article()
    md = article.to_markdown()
    assert "# Best CRM for Coaches" in md
    assert "Great article body." in md


def test_to_markdown_escapes_quotes_in_title():
    article = make_article(title='Best "Free" CRM')
    md = article.to_markdown()
    # The title in YAML must have the double-quote escaped
    assert 'title: "Best \\"Free\\" CRM"' in md
