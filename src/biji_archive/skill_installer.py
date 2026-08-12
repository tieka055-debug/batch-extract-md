from __future__ import annotations

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_SOURCE = PROJECT_ROOT / "skills" / "batch-extract-md"


def default_skill_root(agent: str) -> Path:
    roots = {"codex": Path.home() / ".codex" / "skills", "claude": Path.home() / ".claude" / "skills"}
    return roots[agent]


def install_skill(destination_root: Path, command: str) -> Path:
    if not SKILL_SOURCE.is_dir():
        raise RuntimeError(f"Skill source is missing: {SKILL_SOURCE}")
    target = destination_root / "batch-extract-md"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(SKILL_SOURCE, target)
    skill_file = target / "SKILL.md"
    skill_file.write_text(skill_file.read_text(encoding="utf-8").replace("{{CLI_COMMAND}}", command), encoding="utf-8")
    return target
