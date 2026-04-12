import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

import frontmatter


@dataclass
class PostInfo:
    title: str
    slug: str
    date: date
    url: str       # https://blog.outreachly.pro/YYYY/MM/DD/slug/
    summary: str   # first 150 words, plain text (no markdown)
    body_md: str   # full markdown body (no front matter)


def _strip_markdown(md: str, word_limit: int = 150) -> str:
    """Strip markdown formatting and return first word_limit words as plain text."""
    text = re.sub(r"```.*?```", "", md, flags=re.DOTALL)
    text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"\|[^\n]+\|", "", text)
    words = text.split()
    return " ".join(words[:word_limit])


def read_latest_post(
    posts_dir: str,
    base_url: str = "https://blog.outreachly.pro",
) -> Optional[PostInfo]:
    """Read the most recent Jekyll post from posts_dir. Returns None if no posts exist."""
    posts = sorted(Path(posts_dir).glob("????-??-??-*.md"), reverse=True)
    if not posts:
        return None

    post_path = posts[0]
    # Filename: YYYY-MM-DD-slug.md
    stem_parts = post_path.stem.split("-", 3)  # ['2026', '04', '12', 'slug']
    year, month, day, slug = stem_parts
    post_date = date(int(year), int(month), int(day))

    post = frontmatter.load(str(post_path))
    title = str(post.get("title", slug.replace("-", " ").title()))
    url = f"{base_url}/{year}/{month}/{day}/{slug}/"

    return PostInfo(
        title=title,
        slug=slug,
        date=post_date,
        url=url,
        summary=_strip_markdown(post.content),
        body_md=post.content,
    )
