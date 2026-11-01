#!/usr/bin/env python3
"""Analyse the AI x integrative-medicine corpus and write the chapter figures."""
import csv
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_pubmed as ap  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")

STOP = ap.STOPWORDS


def read_counts():
    ai = {int(r["year"]): int(r["count"]) for r in csv.DictReader(open(os.path.join(DATA, "ai_counts.csv"), encoding="utf-8"))}
    tcm = {int(r["year"]): int(r["count"]) for r in csv.DictReader(open(os.path.join(DATA, "pubmed_counts.csv"), encoding="utf-8"))
           if r["corpus"] == "tcm"}
    return ai, tcm


def read_titles():
    return list(csv.DictReader(open(os.path.join(DATA, "titles_ai.csv"), encoding="utf-8")))


def write_share(ai, tcm):
    path = os.path.join(DATA, "ai_share.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["year", "ai_tcm_papers", "tcm_papers", "share_pct"])
        for year in range(2000, 2026):
            writer.writerow([year, ai.get(year, 0), tcm.get(year, 0),
                             round(100 * ai.get(year, 0) / tcm.get(year, 1), 2)])
    return path


def write_journals(rows):
    counter = Counter(r["journal"] for r in rows if int(r["year"]) >= 2021 and r["journal"])
    path = os.path.join(DATA, "ai_top_journals.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["journal", "papers_2021_2025"])
        for journal, count in counter.most_common(20):
            writer.writerow([journal, count])
    return path, counter


def write_terms(rows):
    uni, bi = Counter(), Counter()
    for row in rows:
        if int(row["year"]) < 2021:
            continue
        for toks in ap.title_segments(row["title"]):
            toks = [w for w in toks if w not in STOP]
            uni.update(toks)
            bi.update(ap.ngrams(toks, 2))
    path = os.path.join(DATA, "ai_title_terms.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["kind", "term", "count"])
        for term, count in uni.most_common(30):
            writer.writerow(["unigram", term, count])
        for term, count in bi.most_common(30):
            writer.writerow(["bigram", term, count])
    return path, uni, bi


def fig_trend(ai, tcm):
    years = list(range(2000, 2026))
    chart = ap.Chart(1000, 520,
                     "AI 相关中医药论文：数量与占比（PubMed，2000–2025）",
                     "检索式：中医药语料 AND（人工智能/机器学习/深度学习/神经网络/大语言模型等）")
    # left: absolute counts
    vals = [ai.get(y, 0) for y in years]
    top = ap.axes(chart, 60, 100, 400, 320, years, max(vals) * 1.1, "AI 相关论文数（篇）")
    pts = ap.map_points(years, vals, 60, 100, 400, 320, top)
    chart.polyline(pts, ap.COLORS[0], 2.6)
    for year, value, (x, y) in zip(years, vals, pts):
        if year in (2000, 2010, 2020, 2023, 2025):
            chart.circle(x, y, 3.2, ap.COLORS[0])
            chart.text(x, y - 9, f"{value}", size=10, anchor="middle", color=ap.COLORS[0])
    # right: share of TCM corpus
    shares = [100 * ai.get(y, 0) / tcm.get(y, 1) for y in years]
    top2 = ap.axes(chart, 560, 100, 400, 320, years, max(shares) * 1.15, "占中医药论文比例（%）", fmt=lambda v: f"{v:g}")
    pts = ap.map_points(years, shares, 560, 100, 400, 320, top2)
    chart.polyline(pts, ap.COLORS[1], 2.6)
    for year, value, (x, y) in zip(years, shares, pts):
        if year in (2000, 2010, 2020, 2023, 2025):
            chart.circle(x, y, 3.2, ap.COLORS[1])
            chart.text(x, y - 9, f"{value:.1f}%", size=10, anchor="middle", color=ap.COLORS[1])
    path = os.path.join(FIG, "fig6_ai_trend.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def fig_subtopics(sub_rows):
    chart = ap.Chart(1000, 540,
                     "AI + 中医药研究的主题分布（PubMed，2000–2025）",
                     "同一论文可命中多个主题；深色部分为 2025 年论文数")
    max_total = max(r["count_2000_2025"] for r in sub_rows)
    x0, y0 = 300, 100
    row = 34
    for i, r in enumerate(sub_rows):
        y = y0 + i * row
        total, last = r["count_2000_2025"], r["count_2025"]
        w = 560 * total / max_total
        w_last = 560 * last / max_total
        chart.text(x0 - 10, y + 5, r["subtopic"], size=11.5, anchor="end", color="#333")
        chart.rect(x0, y - 10, w, 18, ap.COLORS[0], 0.35)
        chart.rect(x0, y - 10, w_last, 18, ap.COLORS[0], 0.95)
        chart.text(x0 + w + 8, y + 5, f"{total}", size=10.5, color="#555")
    chart.line(x0, y0 - 24, x0, y0 + len(sub_rows) * row - 12, "#999", 1)
    path = os.path.join(FIG, "fig7_ai_subtopics.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def main():
    ai, tcm = read_counts()
    rows = read_titles()
    write_share(ai, tcm)
    jpath, counter = write_journals(rows)
    tpath, uni, bi = write_terms(rows)
    sub = list(csv.DictReader(open(os.path.join(DATA, "ai_subtopics.csv"), encoding="utf-8")))
    sub = [{"subtopic": r["subtopic"], "count_2000_2025": int(r["count_2000_2025"]),
            "count_2025": int(r["count_2025"])} for r in sub]
    sub.sort(key=lambda r: r["count_2000_2025"], reverse=True)
    fig_trend(ai, tcm)
    fig_subtopics(sub)
    print("wrote", jpath, tpath, "and figures")


if __name__ == "__main__":
    main()
