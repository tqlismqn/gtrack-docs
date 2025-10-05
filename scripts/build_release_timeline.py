#!/usr/bin/env python3
import re, os, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACK = ROOT / "docs/import/backend/CHANGELOG.md"
FRNT = ROOT / "docs/import/frontend/CHANGELOG.md"
OUT  = ROOT / "docs/releases/timeline.md"

header = """---
title: Releases — Combined Timeline
---
_This page is auto-generated. Source: root CHANGELOG.md in backend/frontend._
"""

VERSION_RE = re.compile(r"^##\s*\[?([vV]?\d+\.\d+\.\d+)\]?\s*-\s*(\d{4}-\d{2}-\d{2})\s*$")
SECTION_RE = re.compile(r"^###\s+(Added|Changed|Deprecated|Removed|Fixed|Security)\s*$")

def parse_changelog(path, repo_label):
    items = []  # list of dicts: {date, version, label, body}
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        m = VERSION_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        version, date_s = m.groups()
        # collect until next "##"
        j = i + 1
        body = []
        while j < len(lines) and not lines[j].startswith("## "):
            body.append(lines[j])
            j += 1
        items.append({
            "date": datetime.date.fromisoformat(date_s),
            "version": version,
            "label": repo_label,
            "body": "".join(body).strip()
        })
        i = j
    return items

def build():
    items = []
    items += parse_changelog(BACK, "Backend")
    items += parse_changelog(FRNT, "Frontend")
    items.sort(key=lambda x: (x["date"], x["label"], x["version"]), reverse=True)

    with OUT.open("w", encoding="utf-8") as f:
        f.write(header)
        if not items:
            f.write("\n_No releases found yet._\n")
            return
        # grouped by date
        cur_date = None
        for it in items:
            if it["date"] != cur_date:
                cur_date = it["date"]
                f.write(f"\n## {cur_date.isoformat()}\n")
            f.write(f"\n### {it['label']} — {it['version']}\n\n")
            if it["body"]:
                f.write(it["body"] + "\n")
            else:
                f.write("_No details._\n")

if __name__ == "__main__":
    build()
