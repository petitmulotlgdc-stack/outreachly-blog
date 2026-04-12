import os
import sys
from pathlib import Path


from generator.keywords import pick_keyword
from generator.writer import write_article


def run(
    keywords_path: str,
    affiliates_path: str,
    posts_dir: str,
    api_key: str,
) -> None:
    """Generate one article and save it to posts_dir."""
    keyword = pick_keyword(keywords_path)
    print(f"Generating article for keyword: {keyword}")

    article = write_article(
        keyword=keyword,
        affiliates_path=affiliates_path,
        api_key=api_key,
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

    repo_root = Path(__file__).parent.parent
    run(
        keywords_path=str(repo_root / "keywords.json"),
        affiliates_path=str(repo_root / "affiliates.json"),
        posts_dir=str(repo_root / "docs" / "_posts"),
        api_key=api_key,
    )
