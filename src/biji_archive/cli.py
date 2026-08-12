from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .exporter import export_url
from .naming import collection_name
from .skill_installer import default_skill_root, install_skill

def export_command(args: argparse.Namespace) -> None:
    destination = args.output / collection_name(args.url)
    result = export_url(args.url, destination, args.profile, args.max)
    print(json.dumps({"ok": True, "output_dir": str(result.output_dir), "exported": result.exported}, ensure_ascii=False))

def install_command(args: argparse.Namespace) -> None:
    root = args.dir or default_skill_root(args.agent)
    command = 'batch-extract-md export-url'
    target = install_skill(root, command)
    print(json.dumps({"ok": True, "skill_dir": str(target)}, ensure_ascii=False))

def main() -> None:
    parser=argparse.ArgumentParser(prog="batch-extract-md", description="批量提取文案md：将 Get笔记知识库内容导出为 Markdown。")
    subs=parser.add_subparsers(dest="command", required=True)
    export=subs.add_parser("export-url", help="Export one knowledge-base URL")
    export.add_argument("url"); export.add_argument("--output",type=Path,default=Path("exports")); export.add_argument("--profile",type=Path,default=Path.home()/".batch-extract-md"/"chrome-profile"); export.add_argument("--max",type=int,default=0); export.set_defaults(handler=export_command)
    install=subs.add_parser("install-skill", help="Install the bundled Agent Skill")
    install.add_argument("--agent",choices=("codex","claude"),default="codex"); install.add_argument("--dir",type=Path); install.set_defaults(handler=install_command)
    args=parser.parse_args()
    try: args.handler(args)
    except Exception as exc:
        print(json.dumps({"ok":False,"error":f"{type(exc).__name__}: {exc}"},ensure_ascii=False)); sys.exit(1)
if __name__ == "__main__": main()
