#!/usr/bin/env python3
"""Collect PubMed data for the AI x integrative-medicine chapter.

Outputs:
  data/ai_counts.csv       TCM+AI publications per year, 2000-2025
  data/ai_subtopics.csv    subtopic counts within TCM+AI, 2021-2025
  data/titles_ai.csv       all TCM+AI titles (journal, year, pmid, title)
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

TCM = ('("Medicine, Chinese Traditional"[MeSH Terms] OR "traditional Chinese medicine"[tiab] '
       'OR "Chinese herbal medicine"[tiab] OR "Chinese medicine"[tiab])')
AI = ('("Artificial Intelligence"[MeSH Terms] OR "Machine Learning"[MeSH Terms] '
      'OR "Deep Learning"[MeSH Terms] OR "artificial intelligence"[tiab] '
      'OR "machine learning"[tiab] OR "deep learning"[tiab] OR "neural network"[tiab] '
      'OR "large language model"[tiab] OR "generative AI"[tiab] OR ChatGPT[tiab])')

SUBTOPICS = {
    "machine learning": '"machine learning"[tiab]',
    "deep learning": '"deep learning"[tiab]',
    "neural network": '"neural network"[tiab] OR "neural networks"[tiab]',
    "large language model / ChatGPT": '"large language model"[tiab] OR "large language models"[tiab] OR ChatGPT[tiab] OR GPT[tiab]',
    "knowledge graph": '"knowledge graph"[tiab]',
    "data mining": '"data mining"[tiab]',
    "medical imaging / radiomics": 'radiomics[tiab] OR "medical imaging"[tiab] OR "image recognition"[tiab]',
    "tongue diagnosis": '"tongue diagnosis"[tiab] OR "tongue image"[tiab]',
    "pulse diagnosis": '"pulse diagnosis"[tiab] OR "pulse wave"[tiab]',
    "syndrome differentiation": '"syndrome differentiation"[tiab] OR "pattern differentiation"[tiab]',
    "drug discovery": '"drug discovery"[tiab]',
}


def get(url, data=None, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data)
            req.add_header("User-Agent", "tcm-survey/1.0 (research script)")
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            print(f"retry {attempt + 1}: {exc}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))


def esearch(term, **params):
    query = {"db": "pubmed", "term": term, "retmode": "json"}
    query.update(params)
    return json.loads(get(f"{BASE}/esearch.fcgi?" + urllib.parse.urlencode(query)))


def esummary(ids):
    if not ids:
        return {}
    data = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"}).encode()
    return json.loads(get(f"{BASE}/esummary.fcgi", data=data)).get("result", {})


def main():
    combined = f"({TCM}) AND ({AI})"

    rows = []
    for year in range(2000, 2026):
        res = esearch(combined, retmax=0, datetype="pdat", mindate=str(year), maxdate=str(year))
        count = int(res["esearchresult"]["count"])
        rows.append({"year": year, "count": count})
        print(f"{year}: {count}", file=sys.stderr)
        time.sleep(0.4)
    with open(os.path.join(DATA, "ai_counts.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["year", "count"])
        writer.writeheader()
        writer.writerows(rows)

    sub_rows = []
    for name, term in SUBTOPICS.items():
        total = int(esearch(f"({combined}) AND ({term})", retmax=0)["esearchresult"]["count"])
        last = int(esearch(f"({combined}) AND ({term})", retmax=0, datetype="pdat",
                           mindate="2025", maxdate="2025")["esearchresult"]["count"])
        sub_rows.append({"subtopic": name, "count_2000_2025": total, "count_2025": last})
        print(f"{name}: {total} (2025: {last})", file=sys.stderr)
        time.sleep(0.4)
    with open(os.path.join(DATA, "ai_subtopics.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["subtopic", "count_2000_2025", "count_2025"])
        writer.writeheader()
        writer.writerows(sub_rows)

    titles = []
    for year in range(2000, 2026):
        res = esearch(combined, retmax=2000, datetype="pdat", mindate=str(year), maxdate=str(year))
        ids = res["esearchresult"].get("idlist", [])
        print(f"{year}: {len(ids)} titles", file=sys.stderr)
        for start in range(0, len(ids), 100):
            batch = ids[start:start + 100]
            summary = esummary(batch)
            for pmid in batch:
                item = summary.get(pmid, {})
                title = (item.get("title") or "").strip()
                journal = (item.get("fulljournalname") or item.get("source") or "").strip()
                if title:
                    titles.append({"year": year, "pmid": pmid, "title": title,
                                   "journal": journal, "pubdate": item.get("pubdate", "")})
            time.sleep(0.4)
        time.sleep(0.4)
    with open(os.path.join(DATA, "titles_ai.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["year", "pmid", "title", "journal", "pubdate"])
        writer.writeheader()
        writer.writerows(titles)
    print(f"wrote {len(titles)} AI titles", file=sys.stderr)


if __name__ == "__main__":
    main()
