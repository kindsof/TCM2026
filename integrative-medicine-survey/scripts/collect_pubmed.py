#!/usr/bin/env python3
"""Collect PubMed publication counts and title samples for the integrative-medicine survey.

Outputs (written next to this script's parent directory):
  data/pubmed_counts.csv   yearly PubMed counts for four query corpora, 2000-2025
  data/titles_<corpus>.csv sampled titles per year for corpus A (integrative) and B (TCM)

Uses only the public NCBI E-utilities API, no key, <=3 requests/second.
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
YEARS = range(2000, 2026)

CORPORA = {
    # Broad "integrative medicine" literature.
    "integrative": '("integrative medicine"[MeSH Terms] OR "integrative medicine"[tiab] '
                   'OR "integrative health"[tiab] OR "integrative oncology"[tiab])',
    # Traditional Chinese medicine / Chinese herbal medicine.
    "tcm": '("Medicine, Chinese Traditional"[MeSH Terms] OR "traditional Chinese medicine"[tiab] '
           'OR "Chinese herbal medicine"[tiab] OR "Chinese medicine"[tiab])',
    # Acupuncture.
    "acupuncture": '("Acupuncture Therapy"[MeSH Terms] OR acupuncture[tiab])',
    # Core integrative-medicine journals indexed in PubMed (ISSN based).
    "im_journals": '("2095-4964"[ISSN] OR "1672-0415"[ISSN] OR "1003-5370"[ISSN] OR "2213-4220"[ISSN])',
}


def get(url, data=None, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data)
            req.add_header("User-Agent", "tcm-survey/1.0 (research script)")
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            print(f"retry {attempt + 1}: {exc}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("unreachable")


def esearch(term, **params):
    query = {"db": "pubmed", "term": term, "retmode": "json"}
    query.update(params)
    url = f"{BASE}/esearch.fcgi?" + urllib.parse.urlencode(query)
    return json.loads(get(url))


def esummary(ids):
    if not ids:
        return {}
    data = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    ).encode()
    url = f"{BASE}/esummary.fcgi"
    payload = json.loads(get(url, data=data))
    return payload.get("result", {})


def collect_counts():
    rows = []
    for corpus, term in CORPORA.items():
        print(f"counting {corpus}", file=sys.stderr)
        total = int(esearch(term, retmax=0)["esearchresult"]["count"])
        for year in YEARS:
            res = esearch(term, retmax=0, datetype="pdat",
                          mindate=str(year), maxdate=str(year))
            count = int(res["esearchresult"]["count"])
            rows.append({"corpus": corpus, "year": year, "count": count})
            print(f"  {corpus} {year}: {count}", file=sys.stderr)
            time.sleep(0.4)
        print(f"  {corpus} total (all years): {total}", file=sys.stderr)
    path = os.path.join(OUT, "pubmed_counts.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["corpus", "year", "count"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path}", file=sys.stderr)


def collect_titles(corpus, term, per_year=1000):
    rows = []
    for year in YEARS:
        res = esearch(term, retmax=per_year, datetype="pdat",
                      mindate=str(year), maxdate=str(year), sort="relevance")
        ids = res["esearchresult"].get("idlist", [])
        print(f"{corpus} {year}: {len(ids)} titles", file=sys.stderr)
        for start in range(0, len(ids), 100):
            batch = ids[start:start + 100]
            summary = esummary(batch)
            for pmid in batch:
                item = summary.get(pmid, {})
                title = (item.get("title") or "").strip()
                journal = (item.get("fulljournalname") or item.get("source") or "").strip()
                pubdate = item.get("pubdate", "")
                if title:
                    rows.append({"corpus": corpus, "year": year, "pmid": pmid,
                                 "title": title, "journal": journal, "pubdate": pubdate})
            time.sleep(0.4)
        time.sleep(0.4)
    path = os.path.join(OUT, f"titles_{corpus}.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["corpus", "year", "pmid", "title", "journal", "pubdate"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)", file=sys.stderr)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    collect_counts()
    collect_titles("integrative", CORPORA["integrative"])
    collect_titles("tcm", CORPORA["tcm"])
