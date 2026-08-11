from __future__ import annotations
import argparse, json
from pathlib import Path
from .exporter import export_url
from .naming import collection_name

def main() -> None:
    parser = argparse.ArgumentParser(prog="biji-archive")
    parser.add_argument("url", help="完整的 biji.com 知识库 URL")
    parser.add_argument("--output", type=Path, default=Path("exports"))
    parser.add_argument("--profile", type=Path, default=Path.home()/".biji-archive"/"chrome-profile")
    parser.add_argument("--max", type=int, default=0)
    args = parser.parse_args()
    destination = args.output / collection_name(args.url)
    result = export_url(args.url, destination, args.profile, args.max)
    print(json.dumps({"output_dir": str(result.output_dir), "exported": result.exported}, ensure_ascii=False))

if __name__ == "__main__":
    main()
