import json
import os
import pytest
import tempfile

@pytest.fixture
def keywords_file(tmp_path):
    data = {
        "templates": [
            "best {tool_category} for {niche}",
            "{tool_a} vs {tool_b} for {niche}"
        ],
        "variables": {
            "tool_category": ["CRM", "email marketing"],
            "niche": ["coaches", "consultants"],
            "tool_a": ["Brevo", "Apollo"],
            "tool_b": ["Mailchimp", "Hunter.io"]
        },
        "used": []
    }
    path = tmp_path / "keywords.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)

def test_pick_keyword_returns_string(keywords_file):
    from generator.keywords import pick_keyword
    keyword = pick_keyword(keywords_file)
    assert isinstance(keyword, str)
    assert len(keyword) > 5

def test_pick_keyword_marks_as_used(keywords_file):
    from generator.keywords import pick_keyword
    pick_keyword(keywords_file)
    data = json.loads(open(keywords_file, encoding="utf-8").read())
    assert len(data["used"]) == 1

def test_pick_keyword_avoids_duplicates(keywords_file):
    from generator.keywords import pick_keyword
    k1 = pick_keyword(keywords_file)
    k2 = pick_keyword(keywords_file)
    assert k1 != k2

def test_pick_keyword_resets_when_exhausted(keywords_file):
    from generator.keywords import pick_keyword
    # Exhaust all keywords
    seen = set()
    for _ in range(20):
        k = pick_keyword(keywords_file)
        seen.add(k)
    # Should still work (resets used list)
    k = pick_keyword(keywords_file)
    assert isinstance(k, str)
