import json
import re
from datetime import date

import anthropic

from generator.article import Article
from generator.keywords import keyword_to_slug

SYSTEM_PROMPT = """You are an expert SEO content writer specializing in business tools and productivity software.
Write helpful, practical articles for coaches, consultants, and entrepreneurs.
Rules:
- Always write in English
- Include practical tips and real comparisons
- Structure with clear H2 and H3 headings
- Include a comparison table when comparing tools
- End with a clear recommendation
- Do NOT include the affiliate links in the text — just mention tool names naturally
- Return only the article content in Markdown (no front matter)
"""


def _load_affiliates(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _inject_affiliate_links(body: str, affiliates: dict) -> str:
    """Replace first mention of each tool name with an affiliate link."""
    for tool, url in affiliates.items():
        # Only replace the first occurrence, only if not already a link
        pattern = rf"(?<!\[)(?<!\()({re.escape(tool)})(?!\]|\))"
        replacement = f"[{tool}]({url})"
        body = re.sub(pattern, replacement, body, count=1)
    return body


def _extract_title(body: str, fallback: str = "Article") -> str:
    """Extract H1 title from markdown body."""
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def write_article(keyword: str, affiliates_path: str, api_key: str) -> Article:
    affiliates = _load_affiliates(affiliates_path)

    # Find which tools are relevant to this keyword
    relevant_tools = [tool for tool in affiliates if tool.lower() in keyword.lower()]
    tools_hint = f"Relevant tools to mention: {', '.join(relevant_tools)}" if relevant_tools else ""

    user_prompt = f"""Write a 1500-2000 word SEO-optimized blog post about: "{keyword}"

Target audience: coaches, consultants, and small business owners.

Requirements:
- H1 title (include the keyword naturally)
- Engaging introduction (hook + problem statement)
- 3-5 H2 sections with practical content
- Comparison table if comparing tools
- Conclusion with clear recommendation
{tools_hint}

Return only the Markdown content, no front matter."""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    if not response.content or not response.content[0].text:
        raise ValueError(f"Empty response from Claude API for keyword: {keyword!r}")
    body = response.content[0].text
    body = _inject_affiliate_links(body, affiliates)
    title = _extract_title(body, fallback=keyword.title())
    slug = keyword_to_slug(keyword)

    return Article(
        keyword=keyword,
        title=title,
        slug=slug,
        body=body,
        date=date.today(),
    )
