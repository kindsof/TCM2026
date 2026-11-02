#!/usr/bin/env python3
"""Analyse PubMed counts and title samples, write CSVs and SVG figures.

Pure standard library: no matplotlib required (SVG is written directly so the
figures render on GitHub without extra dependencies).
"""
import csv
import math
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")

STOPWORDS = set("""
a an and are as at be been being by for from has have had in into is it its
of on or that the their there these this those to was were with without we our
using use used can could may might not no than then than via among between
study studies review reviews analysis effect effects role roles based new
results clinical trial trials patients patient treatment treatments therapy
therapies medicine medicines chinese traditional integrative complementary
alternative health care disease diseases syndrome syndromes
""".split())

TERMS = {
    "network pharmacology": r"network pharmacolog",
    "meta-analysis / systematic review": r"meta-?analy|systematic review",
    "randomized controlled trial": r"randomi[sz]ed",
    "COVID-19": r"covid|sars-cov-2",
    "mechanism": r"mechanism",
    "acupuncture": r"acupunctur",
    "gut microbiota": r"microbio(ta|me)|gut flora",
    "quality control": r"quality control",
    "machine learning / AI": r"machine learning|artificial intelligence|deep learning",
    "syndrome differentiation": r"syndrome differentiation|pattern differentiation|zheng",
}


def read_counts():
    counts = defaultdict(dict)
    with open(os.path.join(DATA, "pubmed_counts.csv"), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            counts[row["corpus"]][int(row["year"])] = int(row["count"])
    return counts


def read_titles(corpus):
    rows = []
    path = os.path.join(DATA, f"titles_{corpus}.csv")
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)
    return rows


def words(title):
    title = title.lower()
    title = re.sub(r"<[^>]+>", " ", title)
    return re.findall(r"[a-z][a-z-]{2,}", title)


def ngrams(tokens, n):
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def title_segments(title):
    """Token lists split on punctuation so bigrams never straddle a colon etc."""
    title = re.sub(r"<[^>]+>", " ", title.lower())
    out = []
    for seg in re.split(r"[:;?!.,()\[\]/]", title):
        toks = re.findall(r"[a-z][a-z-]{2,}", seg)
        if toks:
            out.append(toks)
    return out


def term_series(rows):
    series = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for row in rows:
        year = int(row["year"])
        title = row["title"].lower()
        series[year]["n"][0] += 1
        for name, pattern in TERMS.items():
            if re.search(pattern, title):
                series[year][name][0] += 1
    out = {}
    for year, terms in series.items():
        n = terms["n"][0]
        out[year] = {"n": n}
        for name in TERMS:
            out[year][name] = 100.0 * terms[name][0] / n if n else 0.0
    return out


def title_style(rows):
    out = defaultdict(lambda: {"n": 0, "words": 0, "colon": 0, "question": 0})
    for row in rows:
        year = int(row["year"])
        title = row["title"]
        out[year]["n"] += 1
        out[year]["words"] += len(words(title))
        out[year]["colon"] += ":" in title
        out[year]["question"] += "?" in title
    for year, d in out.items():
        n = d["n"] or 1
        d["mean_words"] = d["words"] / n
        d["colon_pct"] = 100.0 * d["colon"] / n
        d["question_pct"] = 100.0 * d["question"] / n
    return out


def top_terms(rows, start, end, top=25):
    uni, bi = Counter(), Counter()
    for row in rows:
        if not (start <= int(row["year"]) <= end):
            continue
        for toks in title_segments(row["title"]):
            toks = [w for w in toks if w not in STOPWORDS]
            uni.update(toks)
            bi.update(ngrams(toks, 2))
    return uni, bi


def write_term_csv(series, path):
    years = sorted(series)
    names = list(TERMS)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["year", "n_titles"] + names)
        for year in years:
            writer.writerow([year, series[year]["n"]] + [round(series[year][k], 2) for k in names])


def write_style_csv(style, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["year", "n_titles", "mean_words", "colon_pct", "question_pct"])
        for year in sorted(style):
            d = style[year]
            writer.writerow([year, d["n"], round(d["mean_words"], 2),
                             round(d["colon_pct"], 2), round(d["question_pct"], 2)])


def rising_terms(rows, top=12):
    """Rate-based rising/falling bigrams, robust to the overall growth in output."""
    early, late = Counter(), Counter()
    n_early = n_late = 0
    for row in rows:
        year = int(row["year"])
        grams = []
        for toks in title_segments(row["title"]):
            grams.extend(ngrams([w for w in toks if w not in STOPWORDS], 2))
        if 2000 <= year <= 2009:
            early.update(grams)
            n_early += len(grams)
        elif 2021 <= year <= 2025:
            late.update(grams)
            n_late += len(grams)

    def reverse_dup(term, counts):
        rev = " ".join(reversed(term.split()))
        if rev == term:
            return False
        if counts.get(rev, 0) > counts.get(term, 0):
            return True
        if counts.get(rev, 0) == counts.get(term, 0) and rev < term:
            return True
        return False

    scored = []
    for term in set(early) | set(late):
        c_e, c_l = early.get(term, 0), late.get(term, 0)
        if c_l < 40 and c_e < 40:
            continue
        rate_e = (c_e + 0.5) / n_early * 10000
        rate_l = (c_l + 0.5) / n_late * 10000
        score = math.log(rate_l / rate_e)
        scored.append((score, term, c_e, c_l))
    up = sorted([s for s in scored if s[0] > 0 and s[3] >= 40], reverse=True)
    down = sorted([s for s in scored if s[0] < 0 and s[2] >= 40])
    noise = {"pharmacology molecular", "protocol systematic", "report cases",
             "observation therapeutic", "integrated western"}
    up = [s for s in up if s[1] not in noise and not reverse_dup(s[1], late)][:top]
    down = [s for s in down if s[1] not in noise and not reverse_dup(s[1], early)][:top]
    return up, down


# ---------------------------------------------------------------- SVG helpers

def esc(text):
    text = str(text)
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Chart:
    def __init__(self, width=960, height=520, title="", subtitle=""):
        self.w, self.h = width, height
        self.parts = []
        self.title = title
        self.subtitle = subtitle

    def line(self, x1, y1, x2, y2, color="#333", width=1, dash=None, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"{d}/>'
        )

    def rect(self, x, y, w, h, fill, opacity=1):
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" opacity="{opacity}"/>'
        )

    def text(self, x, y, text, size=13, anchor="start", color="#222", weight="normal", rotate=None):
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{tr}>{esc(text)}</text>'
        )

    def polyline(self, pts, color, width=2.4, dash=None):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<polyline points="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{da}/>'
        )

    def circle(self, x, y, r, fill, stroke="#fff"):
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )

    def render(self):
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
        )
        body = "".join(self.parts)
        title = ""
        if self.title:
            title += f'<text x="48" y="38" font-family="Helvetica, Arial, sans-serif" font-size="19" font-weight="bold" fill="#111">{esc(self.title)}</text>'
        if self.subtitle:
            title += f'<text x="48" y="60" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="#666">{esc(self.subtitle)}</text>'
        return head + title + body + "</svg>"


def nice_ticks(vmax, n=5):
    if vmax <= 0:
        return [0], 1
    raw = vmax / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), default=10 * mag)
    top = math.ceil(vmax / step) * step
    ticks = [i * step for i in range(int(top / step) + 1)]
    return ticks, step


def axes(chart, x0, y0, w, h, years, ymax, ylabel, color="#333", fmt=int):
    ticks, step = nice_ticks(ymax)
    top = ticks[-1]
    for t in ticks:
        y = y0 + h - (t / top) * h
        chart.line(x0, y, x0 + w, y, "#e6e6e6", 1)
        chart.text(x0 - 8, y + 4, fmt(t), size=11, anchor="end", color="#555")
    for year in years:
        if (year - years[0]) % 5 == 0 or year == years[-1]:
            x = x0 + (year - years[0]) / (years[-1] - years[0]) * w
            chart.line(x, y0, x, y0 + h, "#eeeeee", 1)
            chart.text(x, y0 + h + 18, str(year), size=11, anchor="middle", color="#555")
    chart.line(x0, y0 + h, x0 + w, y0 + h, color, 1.2)
    chart.line(x0, y0, x0, y0 + h, color, 1.2)
    chart.text(x0, y0 - 14, ylabel, size=11.5, color="#555")
    return top


def map_points(years, values, x0, y0, w, h, top):
    pts = []
    for year, value in zip(years, values):
        x = x0 + (year - years[0]) / (years[-1] - years[0]) * w
        y = y0 + h - (value / top) * h
        pts.append((x, y))
    return pts


COLORS = ["#1f6fb2", "#d1495b", "#2a9d8f", "#e9a03b", "#7b5ea7", "#6a994e", "#bc6c25", "#4d908e"]


def fig_counts(counts):
    years = list(range(2000, 2026))
    chart = Chart(1000, 560,
                  "PubMed 年发文量：中医药与结合医学",
                  "检索日期 2026-11-01；按 PubMed 出版年统计，含所有文献类型")
    panels = [
        ("tcm", "中医药相关（TCM）", 48, 96, 420, 360),
        ("integrative", "结合医学（integrative medicine）", 540, 96, 420, 360),
    ]
    for corpus, label, x0, y0, w, h in panels:
        vals = [counts[corpus].get(y, 0) for y in years]
        top = axes(chart, x0, y0, w, h, years, max(vals) * 1.08, label)
        pts = map_points(years, vals, x0, y0, w, h, top)
        chart.polyline(pts, COLORS[0], 2.6)
        for year, value, (x, y) in zip(years, vals, pts):
            if year in (2000, 2010, 2015, 2020, 2025):
                chart.circle(x, y, 3.2, COLORS[0])
                chart.text(x, y - 9, f"{value:,}", size=10, anchor="middle", color="#1f6fb2")
        chart.text(x0 + w, y0 + h + 36, "数据：NCBI PubMed E-utilities", size=10.5, anchor="end", color="#888")
    path = os.path.join(FIG, "fig1_pubmed_counts.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def fig_counts2(counts):
    years = list(range(2000, 2026))
    chart = Chart(1000, 460,
                  "PubMed 年发文量：核心结合医学期刊与针灸",
                  "核心期刊 = Chin J Integr Med / J Integr Med / 中国中西医结合杂志 / Integr Med Res（ISSN 检索）")
    for idx, (corpus, label) in enumerate([
        ("acupuncture", "针灸（acupuncture）"),
        ("im_journals", "核心中西医结合期刊"),
    ]):
        vals = [counts[corpus].get(y, 0) for y in years]
        top = axes(chart, 70 + idx * 480, 96, 400, 300, years, max(vals) * 1.1, label)
        pts = map_points(years, vals, 70 + idx * 480, 96, 400, 300, top)
        chart.polyline(pts, COLORS[idx + 1], 2.6)
        for year, value, (x, y) in zip(years, vals, pts):
            if year in (2000, 2010, 2015, 2020, 2025):
                chart.circle(x, y, 3.2, COLORS[idx + 1])
                chart.text(x, y - 9, f"{value:,}", size=10, anchor="middle", color=COLORS[idx + 1])
    path = os.path.join(FIG, "fig2_journals_acupuncture.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def fig_terms(series):
    years = sorted(series)
    chart = Chart(1000, 560,
                  "中医药论文标题中的方法学与研究主题（占当年抽样标题的比例）",
                  "每篇标题命中即计一次；分母为当年 PubMed 抽样标题数（每年最多 1000 条）")
    keys = ["network pharmacology", "meta-analysis / systematic review",
            "randomized controlled trial", "COVID-19", "mechanism", "gut microbiota"]
    top = axes(chart, 80, 96, 860, 380, years, 60, "占当年标题百分比 (%)")
    for i, key in enumerate(keys):
        pts = map_points(years, [series[y][key] for y in years], 80, 96, 860, 380, top)
        chart.polyline(pts, COLORS[i], 2.2)
        lx = 92 + (i % 3) * 290
        ly = 96 + 380 + 34 + (i // 3) * 22
        chart.line(lx, ly - 4, lx + 22, ly - 4, COLORS[i], 3)
        chart.text(lx + 28, ly, key, size=11.5, color="#333")
    path = os.path.join(FIG, "fig3_title_terms.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def fig_style(style):
    years = sorted(style)
    chart = Chart(1000, 480,
                  "中医药论文标题的形式变化",
                  "平均标题词数（左轴）与含冒号、含问号的标题比例（右轴）")
    x0, y0, w, h = 80, 100, 760, 300
    left_top = axes(chart, x0, y0, w, h, years, 22, "平均标题词数", fmt=lambda v: f"{v:g}")
    ticks, _ = nice_ticks(60)
    right_top = ticks[-1]
    for t in ticks:
        y = y0 + h - (t / right_top) * h
        chart.text(x0 + w + 10, y + 4, f"{t:g}%", size=11, color="#555")
    chart.text(x0 + w + 10, y0 - 14, "标题占比", size=11.5, color="#555")

    pts = map_points(years, [style[y]["mean_words"] for y in years], x0, y0, w, h, left_top)
    chart.polyline(pts, COLORS[0], 2.6)
    for year, (x, y) in zip(years, pts):
        if year in (2000, 2010, 2015, 2020, 2025):
            chart.circle(x, y, 3, COLORS[0])
            chart.text(x, y - 8, f"{style[year]['mean_words']:.1f}", size=10,
                       anchor="middle", color=COLORS[0])
    for key, color in [("colon_pct", COLORS[1]), ("question_pct", COLORS[2])]:
        pts = map_points(years, [style[y][key] for y in years], x0, y0, w, h, right_top)
        chart.polyline(pts, color, 2.2, dash="5,4")
    chart.line(100, 442, 122, 442, COLORS[0], 3)
    chart.text(130, 446, "平均标题词数（左轴）", size=11.5)
    chart.line(330, 442, 352, 442, COLORS[1], 3)
    chart.text(360, 446, "含冒号标题比例（右轴）", size=11.5)
    chart.line(600, 442, 622, 442, COLORS[2], 3)
    chart.text(630, 446, "含问号标题比例（右轴）", size=11.5)
    path = os.path.join(FIG, "fig4_title_style.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def fig_rising(rising, falling):
    chart = Chart(1000, 560,
                  "中医药论文标题词组的升降（2021–2025 对比 2000–2009）",
                  "按每万条标题出现频次的对数比排序；条形数字为对应时段出现次数（上升=2021–2025，下降=2000–2009）")
    panels = [("上升", rising, 60, 0), ("下降", falling, 520, 1)]
    row = 26
    for title, items, x0, kind in panels:
        chart.text(x0, 86, title, size=14, weight="bold",
                   color=COLORS[0] if kind == 0 else COLORS[1])
        counts = [(c_late if kind == 0 else c_early) for _, _, c_early, c_late in items]
        max_count = max(counts, default=1)
        for i, ((score, term, c_early, c_late), c_now) in enumerate(zip(items, counts)):
            y = 112 + i * row
            bar_w = 190 * (c_now / max_count)
            chart.text(x0 + 240, y + 4, term, size=11.5, anchor="end", color="#333")
            chart.rect(x0 + 250, y - 9, max(bar_w, 2), 15,
                       COLORS[0] if kind == 0 else COLORS[1], 0.85)
            chart.text(x0 + 256 + max(bar_w, 2), y + 4, f"{c_now}", size=10.5, color="#666")
    path = os.path.join(FIG, "fig5_rising_terms.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(chart.render())
    return path


def main():
    os.makedirs(FIG, exist_ok=True)
    counts = read_counts()
    tcm_rows = read_titles("tcm")
    im_rows = read_titles("integrative")

    tcm_series = term_series(tcm_rows)
    write_term_csv(tcm_series, os.path.join(DATA, "title_terms_tcm.csv"))
    write_term_csv(term_series(im_rows), os.path.join(DATA, "title_terms_integrative.csv"))
    write_style_csv(title_style(tcm_rows), os.path.join(DATA, "title_style_tcm.csv"))
    write_style_csv(title_style(im_rows), os.path.join(DATA, "title_style_integrative.csv"))

    rising, falling = rising_terms(tcm_rows)
    with open(os.path.join(DATA, "rising_terms.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["direction", "bigram", "count_2000_2009", "count_2021_2025", "log_ratio"])
        for score, term, c_early, c_late in rising:
            writer.writerow(["up", term, c_early, c_late, round(score, 3)])
        for score, term, c_early, c_late in falling:
            writer.writerow(["down", term, c_early, c_late, round(score, 3)])

    # Top bigrams by period, for the report tables.
    with open(os.path.join(DATA, "top_terms_by_period.csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["period", "rank", "bigram", "count"])
        for label, start, end in [("2000-2009", 2000, 2009), ("2010-2015", 2010, 2015),
                                  ("2016-2020", 2016, 2020), ("2021-2025", 2021, 2025)]:
            _, bi = top_terms(tcm_rows, start, end, top=15)
            for rank, (term, count) in enumerate(bi.most_common(15), 1):
                writer.writerow([label, rank, term, count])

    fig_counts(counts)
    fig_counts2(counts)
    fig_terms(tcm_series)
    fig_style(title_style(tcm_rows))
    fig_rising(rising, falling)
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
