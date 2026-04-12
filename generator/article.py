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
        front_matter = f"""---
layout: post
title: "{self.title}"
date: {self.date.isoformat()}
description: "{self.title} — Expert guide for coaches and consultants."
---

"""
        return front_matter + self.body

    def filename(self) -> str:
        """Return Jekyll post filename: YYYY-MM-DD-slug.md"""
        return f"{self.date.isoformat()}-{self.slug}.md"
