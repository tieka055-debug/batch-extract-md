from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from playwright.sync_api import BrowserContext, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

from .naming import next_path

LIST = ".min-w-0.flex-1.text-left"
TITLE = ".web-title"
JUMP = "div.cursor-pointer:has(svg.lucide-link)"

@dataclass(frozen=True)
class ExportResult:
    output_dir: Path
    exported: int
    skipped: int


def article_text(page: Page) -> tuple[str, str]:
    title = page.locator(TITLE).inner_text().strip()
    content = page.locator(TITLE).evaluate("""el => {
      const parts = [];
      for (let node = el.nextElementSibling; node; node = node.nextElementSibling) {
        const paragraphs = [...node.querySelectorAll('p')];
        const texts = paragraphs.length ? paragraphs.map(p => p.innerText) : [node.innerText];
        texts.map(t => t.trim()).filter(Boolean).forEach(t => parts.push(t));
      }
      return parts.join('\\n\\n');
    }""")
    return title, content.strip()


def export_url(url: str, output_dir: Path, profile_dir: Path, max_articles: int = 0) -> ExportResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        context: BrowserContext = pw.chromium.launch_persistent_context(
            str(profile_dir), headless=False, viewport={"width": 1440, "height": 1000}
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            # A first-time login is intentionally performed by the user in this window.
            page.locator(LIST).first.wait_for(timeout=180_000)
            total = page.locator(LIST).count()
            if max_articles:
                total = min(total, max_articles)
            exported = skipped = 0
            for index in range(total):
                item = page.locator(LIST).nth(index)
                item.scroll_into_view_if_needed()
                item.click()
                page.locator(JUMP).first.wait_for(state="visible", timeout=15_000)
                try:
                    with context.expect_page(timeout=5_000) as event:
                        page.locator(JUMP).first.click(force=True)
                    target = event.value
                except PlaywrightTimeoutError:
                    # Some SPA versions reuse the current tab instead of opening one.
                    target = page
                target.locator(TITLE).wait_for(timeout=15_000)
                title, content = article_text(target)
                path = next_path(output_dir, index + 1, title)
                path.write_text(f"# {title}\n\n来源：{target.url}\n\n{content}\n", encoding="utf-8")
                exported += 1
                if target is not page:
                    target.close()
                else:
                    page.go_back(wait_until="domcontentloaded")
            return ExportResult(output_dir, exported, skipped)
        finally:
            context.close()
