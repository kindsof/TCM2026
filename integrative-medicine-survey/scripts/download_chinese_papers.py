#!/usr/bin/env python3
"""Download the Chinese papers listed in papers/chinese/manifest.json.

These articles are free to read on the journal website but are **not** openly
licensed (no CC BY), so the PDFs are not committed to this public repository.
Run this script locally to fetch them for personal study; files go to
papers/chinese/pdf/ (ignored by git).

Usage:
    python3 scripts/download_chinese_papers.py
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "papers", "chinese", "pdf")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def main():
    manifest = json.load(open(os.path.join(ROOT, "papers", "chinese", "manifest.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    ok = 0
    for item in manifest:
        path = os.path.join(OUT, item["file"])
        if os.path.exists(path) and os.path.getsize(path) > 20000:
            with open(path, "rb") as fh:
                if fh.read(5) == b"%PDF-":
                    print(f"skip {item['file']} (already downloaded)")
                    ok += 1
                    continue
        print(f"downloading {item['id']} {item['title'][:40]}")
        for attempt in range(3):
            try:
                req = urllib.request.Request(item["pdf_url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=120) as resp:
                    blob = resp.read()
                if blob[:5] != b"%PDF-":
                    raise ValueError("server did not return a PDF")
                with open(path, "wb") as fh:
                    fh.write(blob)
                print(f"  saved {path} ({len(blob) / 1024:.0f} KB)")
                ok += 1
                break
            except Exception as exc:  # noqa: BLE001
                print(f"  attempt {attempt + 1} failed: {exc}", file=sys.stderr)
                time.sleep(3)
        time.sleep(0.5)
    print(f"{ok}/{len(manifest)} papers available in {OUT}")


if __name__ == "__main__":
    main()
