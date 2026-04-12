import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from generator.keywords import pick_keyword
from generator.writer import write_article


def _is_long_article(hour: int) -> bool:
    """Return True for hours that should generate long articles (8h and 14h UTC)."""
    return hour in (8, 14)


def run(
    keywords_path: str,
    affiliates_path: str,
    posts_dir: str,
    api_key: str,
    long: bool = False,
) -> None:
    """Generate one article and save it to posts_dir."""
    keyword = pick_keyword(keywords_path)
    article_type = "long" if long else "short"
    print(f"Generating {article_type} article for keyword: {keyword}")

    article = write_article(
        keyword=keyword,
        affiliates_path=affiliates_path,
        api_key=api_key,
        long=long,
    )
    print(f"Article generated: {article.title}")

    Path(posts_dir).mkdir(parents=True, exist_ok=True)
    post_path = Path(posts_dir) / article.filename()
    post_path.write_text(article.to_markdown(), encoding="utf-8")
    print(f"Saved to: {post_path}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Error: ANTHROPIC_API_KEY is not set. Add it to your .env file.")

    hour = datetime.now(timezone.utc).hour
    long = _is_long_article(hour)

    repo_root = Path(__file__).parent.parent
    run(
        keywords_path=str(repo_root / "keywords.json"),
        affiliates_path=str(repo_root / "affiliates.json"),
        posts_dir=str(repo_root / "docs" / "_posts"),
        api_key=api_key,
        long=long,
    )
