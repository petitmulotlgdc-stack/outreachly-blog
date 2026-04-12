import json
import random
import re


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _fill_template(template: str, variables: dict) -> str:
    """Fill a template string with random values from variables dict."""
    result = template
    for key, values in variables.items():
        placeholder = "{" + key + "}"
        if placeholder in result:
            result = result.replace(placeholder, str(random.choice(values)))
    return result


def _to_slug(keyword: str) -> str:
    """Convert keyword to URL-safe slug."""
    import unicodedata
    slug = unicodedata.normalize("NFKD", keyword).encode("ascii", "ignore").decode("ascii")
    slug = slug.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug or "article"


def pick_keyword(keywords_path: str) -> str:
    """Pick an unused keyword, mark it as used, return it."""
    while True:
        data = _load(keywords_path)
        templates = data["templates"]
        variables = data["variables"]
        used = set(data.get("used", []))

        # Generate up to 20 candidate keywords from 200 random attempts
        candidates = []
        for _ in range(200):
            template = random.choice(templates)
            keyword = _fill_template(template, variables)
            if keyword not in used:
                candidates.append(keyword)
            if len(candidates) >= 20:
                break

        # If exhausted, reset used list and retry
        if not candidates:
            data["used"] = []
            _save(keywords_path, data)
            continue

        keyword = random.choice(candidates)
        data["used"] = list(used) + [keyword]
        _save(keywords_path, data)
        return keyword


def keyword_to_slug(keyword: str) -> str:
    return _to_slug(keyword)
