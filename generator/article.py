from dataclasses import dataclass
from datetime import date


@dataclass
class Article:
    keyword: str
    title: str
    slug: str
    body: str
    date: date

    def to_markdown(self) -> str:
        """Return Jekyll-compatible Markdown with front matter."""
        safe_title = self.title.replace('"', '\\"')
        front_matter = f"""---
layout: post
title: "{safe_title}"
date: {self.date.isoformat()}
description: "{safe_title} — Expert guide for coaches and consultants."
---

"""
        return front_matter + self.body

    def filename(self) -> str:
        """Return Jekyll post filename: YYYY-MM-DD-slug.md"""
        return f"{self.date.isoformat()}-{self.slug}.md"
