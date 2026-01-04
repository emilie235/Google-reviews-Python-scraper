"""
Clean legacy fields from scraped JSON files.

Usage:
  python scripts/clean_json.py

This will scan `data/*/*.json`, back up each file (timestamped),
remove `likes` and `owner_responses` keys if present, and set
`company` to the review's `restaurant` value when available.
"""
from pathlib import Path
import json
import shutil
from datetime import datetime


DATA_DIR = Path("data")


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except Exception as e:
        print(f"Skipping {path} — JSON error: {e}")
        return 0

    if not isinstance(data, list):
        print(f"Skipping {path} — expected list of reviews")
        return 0

    changed = False
    count_changed = 0
    for doc in data:
        if not isinstance(doc, dict):
            continue
        modified = False
        # Remove legacy fields
        for k in ("likes", "owner_responses"):
            if k in doc:
                del doc[k]
                modified = True

        # Ensure company matches restaurant when present
        rest = doc.get("restaurant")
        if rest and doc.get("company") != rest:
            doc["company"] = rest
            modified = True

        if modified:
            changed = True
            count_changed += 1

    if changed:
        # Backup original
        bak = path.with_suffix(path.suffix + ".bak." + datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        shutil.copy2(path, bak)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Updated {path} — modified {count_changed} reviews (backup: {bak.name})")
    else:
        print(f"No changes for {path}")

    return count_changed


def main():
    total = 0
    if not DATA_DIR.exists():
        print("No data/ directory found")
        return

    for json_file in DATA_DIR.rglob("*.json"):
        total += process_file(json_file)

    print(f"Done — total modified reviews: {total}")


if __name__ == "__main__":
    main()
