from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


def collection_name(url: str) -> str:
    query = parse_qs(urlparse(url).query)
    name = unquote(query.get("followName", [""])[0]).strip()
    if name:
        return safe_name(name)
    match = re.search(r"/subject/([^/?]+)", url)
    return safe_name(match.group(1) if match else "biji-export")


def safe_name(value: str, fallback: str = "untitled") -> str:
    value = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", value).strip(" .")
    return (value[:100] or fallback)


def next_path(folder: Path, position: int, title: str) -> Path:
    base = f"{position:03d}_{safe_name(title)}"
    candidate = folder / f"{base}.md"
    counter = 2
    while candidate.exists():
        candidate = folder / f"{base}_{counter}.md"
        counter += 1
    return candidate
