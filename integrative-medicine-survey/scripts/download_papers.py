#!/usr/bin/env python3
"""Download the open-access papers listed in papers/manifest.json and build an index.

Only openly licensed articles are included (CC BY / CC BY-NC etc.); paywalled
papers are deliberately not downloaded. Crossref is used for bibliographic
metadata so the index can be checked against the DOI record.
"""
import csv
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAPERS = os.path.join(ROOT, "papers")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(url, timeout=90, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def crossref(doi):
    try:
        data = json.loads(fetch(f"https://api.crossref.org/works/{doi}", timeout=30))
    except Exception as exc:  # noqa: BLE001
        print(f"  crossref failed for {doi}: {exc}", file=sys.stderr)
        return {}
    m = data.get("message", {})
    authors = []
    for a in m.get("author", []):
        name = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        authors.append(name or a.get("name", ""))
    published = m.get("published", {}).get("date-parts", [[None]])[0]
    license_url = ""
    for lic in m.get("license", []):
        if lic.get("URL"):
            license_url = lic["URL"]
            break
    return {
        "title": (m.get("title") or [""])[0],
        "authors": "; ".join(authors),
        "journal": (m.get("container-title") or [""])[0],
        "year": published[0] if published else "",
        "volume": m.get("volume", ""),
        "issue": m.get("issue", ""),
        "page": m.get("page", ""),
        "license": license_url,
    }


def main():
    manifest = json.load(open(os.path.join(PAPERS, "manifest.json"), encoding="utf-8"))
    rows = []
    for item in manifest:
        path = os.path.join(PAPERS, item["file"])
        ok = False
        if os.path.exists(path) and os.path.getsize(path) > 20000:
            with open(path, "rb") as fh:
                ok = fh.read(5) == b"%PDF-"
        if not ok:
            print(f"downloading {item['file']}", file=sys.stderr)
            for attempt in range(3):
                try:
                    blob = fetch(item["url"])
                    if blob[:5] != b"%PDF-":
                        raise ValueError(f"not a PDF: {blob[:80]!r}")
                    with open(path, "wb") as fh:
                        fh.write(blob)
                    ok = True
                    break
                except Exception as exc:  # noqa: BLE001
                    print(f"  attempt {attempt + 1} failed: {exc}", file=sys.stderr)
                    time.sleep(3)
        if not ok:
            print(f"FAILED {item['file']}", file=sys.stderr)
            continue
        meta = crossref(item["doi"])
        rows.append({
            "file": item["file"],
            "theme": item["theme"],
            "doi": item["doi"],
            "title": meta.get("title", ""),
            "authors": meta.get("authors", ""),
            "journal": meta.get("journal", ""),
            "year": meta.get("year", ""),
            "volume": meta.get("volume", ""),
            "issue": meta.get("issue", ""),
            "page": meta.get("page", ""),
            "license": meta.get("license", ""),
            "size_kb": round(os.path.getsize(path) / 1024),
            "url": item["url"],
        })
        print(f"  ok {item['file']} ({rows[-1]['size_kb']} KB) {rows[-1]['title'][:70]}", file=sys.stderr)

    out = os.path.join(PAPERS, "index.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["file"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out} with {len(rows)} papers", file=sys.stderr)


if __name__ == "__main__":
    main()
