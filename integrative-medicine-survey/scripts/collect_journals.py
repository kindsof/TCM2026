#!/usr/bin/env python3
"""Count PubMed records per candidate journal (ISSN) for 2021-2025."""
import csv
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

JOURNALS = [
    ("Chinese Journal of Integrative Medicine", "1672-0415", "CJIM"),
    ("Journal of Integrative Medicine", "2095-4964", "JIM"),
    ("Zhongguo Zhong Xi Yi Jie He Za Zhi (中国中西医结合杂志)", "1003-5370", "中国中西医结合杂志"),
    ("Integrative Medicine Research", "2213-4220", "IMR"),
    ("Chinese Medicine", "1749-8546", "Chinese Medicine"),
    ("Journal of Ethnopharmacology", "0378-8741", "J Ethnopharmacol"),
    ("Phytomedicine", "0944-7113", "Phytomedicine"),
    ("Acupuncture in Medicine", "0964-5284", "Acupunct Med"),
    ("Complementary Therapies in Medicine", "0965-2299", "Complement Ther Med"),
    ("Chinese Journal of Natural Medicines", "1875-5364", "Chin J Nat Med"),
    ("Frontiers in Pharmacology", "1663-9812", "Front Pharmacol"),
    ("Integrative Cancer Therapies", "1534-7354", "Integr Cancer Ther"),
    ("Journal of Traditional Chinese Medicine", "0255-2922", "J Tradit Chin Med"),
    ("Chinese Herbal Medicines", "1674-6384", "Chin Herb Med"),
    ("World Journal of Traditional Chinese Medicine", "2311-8571", "World J Tradit Chin Med"),
]

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def count(issn, year):
    query = {"db": "pubmed", "term": f'"{issn}"[ISSN]', "retmode": "json",
             "retmax": 0, "datetype": "pdat",
             "mindate": str(year), "maxdate": str(year)}
    url = f"{BASE}/esearch.fcgi?" + urllib.parse.urlencode(query)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "tcm-survey/1.0"})
            data = json.load(urllib.request.urlopen(req, timeout=60))
            return int(data["esearchresult"]["count"])
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise
            print(f"retry {issn} {year}: {exc}")
            time.sleep(2)
    return 0


def main():
    rows = []
    for name, issn, short in JOURNALS:
        counts = {}
        for year in range(2021, 2026):
            counts[year] = count(issn, year)
            time.sleep(0.4)
        rows.append({"journal": name, "short": short, "issn": issn,
                     **{str(year): value for year, value in counts.items()}})
        print(short, counts)
    path = os.path.join(DATA, "journal_counts_2021_2025.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["journal", "short", "issn", "2021", "2022", "2023", "2024", "2025"])
        writer.writeheader()
        writer.writerows(rows)
    print("wrote", path)


if __name__ == "__main__":
    main()
