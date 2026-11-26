"""Catalog charts from a repository SOFTWARE_AUTHORITY.tsv (paper-viz house look).
usage: python3 -B make_catalog_charts_v1.py REPO_KEY TSV OUTDIR PREFIX
REPO_KEY: te | structure | function
"""
import sys, os, csv, math, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text
from matplotlib.patches import Patch

key, tsv, out, prefix = sys.argv[1:5]
MM = 1 / 25.4
plt.rcParams.update({"font.family": "Arial", "font.size": 7, "axes.titlesize": 8, "axes.labelsize": 8,
    "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.8,
    "ytick.major.size": 2.8, "xtick.labelsize": 7, "ytick.labelsize": 7, "svg.fonttype": "none",
    "pdf.fonttype": 42, "axes.titleweight": "normal", "axes.labelweight": "normal"})
TIERS = ["standard", "established", "newer", "niche", "no paper"]
TCOL = {"standard": "#1F72AE", "established": "#62B4E7", "newer": "#119B76", "niche": "#E6C32A", "no paper": "#BFBFBF"}
TLAB = {"standard": "standard (\u2265500)", "established": "established (100\u2013499)", "newer": "newer (<100, 2023+)", "niche": "niche (<100, pre-2023)", "no paper": "no paper"}

rows = list(csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"))
recs = []
for r in rows:
    if key == "te":
        sec, sk, role, yr, cit = r["step_section"], None, r["role"], r["paper_year"], r["citations_openalex"]
        isdef = role == "repository default"
    else:
        sec, role, yr, cit = r["section_title"], r["role"], r["year"], r["openalex_citations"]
        sk = 99 if r["section"] == "viz" else int(r["section"])
        isdef = role.startswith("default")
    recs.append(dict(name=r["name"], sec=sec, sk=sk, tier=r["tier"], isdef=isdef,
                     yr=int(yr) if yr else None, cit=int(cit) if cit else None, typ=r["type"]))
N = len(recs)
# section order
order = []
if key == "te":
    for r in recs:
        if r["sec"] not in order:
            order.append(r["sec"])
else:
    seen = {}
    for r in recs:
        seen.setdefault(r["sec"], r["sk"])
    order = sorted(seen, key=lambda s: seen[s])
counts = {s: {t: 0 for t in TIERS} for s in order}
for r in recs:
    counts[r["sec"]][r["tier"]] += 1
tot_t = {t: sum(counts[s][t] for s in order) for t in TIERS}
print("N", N, "tiers", tot_t)

# ---- chart 1: entries per section by tier ----
h = max(70, 5.2 * len(order) + 22)
fig, ax = plt.subplots(figsize=(135 * MM, h * MM))
ys = list(range(len(order)))[::-1]
for y, s in zip(ys, order):
    left = 0
    for t in TIERS:
        v = counts[s][t]
        if v:
            ax.barh(y, v, left=left, height=0.68, color=TCOL[t], edgecolor="white", linewidth=0.3)
            if v >= 3:
                ax.text(left + v / 2, y, str(v), ha="center", va="center", fontsize=6, color="white" if t in ("standard", "newer") else "#000000")
        left += v
    ax.text(left + 0.4, y, str(left), ha="left", va="center", fontsize=7)
ax.set_yticks(ys)
ax.set_yticklabels(order)
ax.set_xlabel(("Catalogue" if key == "te" else "Catalog") + " entries (n)")
mx = max(sum(counts[s].values()) for s in order)
ax.set_xlim(0, mx * (1.12 if key == "te" else 1.75) + 1)
ax.set_ylim(-0.6, len(order) - 0.4)
ax.tick_params(axis="y", length=0)
handles = [Patch(facecolor=TCOL[t], edgecolor="none", label="%s: %d" % (TLAB[t], tot_t[t])) for t in TIERS]
ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=6.5, handlelength=1.0, handleheight=0.8, borderaxespad=0.3, title="Citation tier (OpenAlex)", title_fontsize=6.5)
ax.text(0.99, 0.99, "N = %d entries" % N, transform=ax.transAxes, ha="right", va="top", fontsize=7)
fig.tight_layout(pad=0.4)
for ext in ("svg", "png"):
    fig.savefig(os.path.join(out, prefix + "_catalog_by_step." + ext), dpi=600 if ext == "png" else None)
plt.close(fig)

# ---- chart 2: year vs citations ----
pts = [r for r in recs if r["yr"] and r["cit"] is not None]
fig, ax = plt.subplots(figsize=(135 * MM, 80 * MM))
for t in TIERS[:-1]:
    xs = [r["yr"] for r in pts if r["tier"] == t and not r["isdef"]]
    yv = [max(r["cit"], 0.8) for r in pts if r["tier"] == t and not r["isdef"]]
    ax.scatter(xs, yv, s=14, c=TCOL[t], edgecolors="#333333", linewidths=0.3, zorder=2, label=None)
d = [r for r in pts if r["isdef"]]
ax.scatter([r["yr"] for r in d], [max(r["cit"], 0.8) for r in d], s=30, c=[TCOL[r["tier"]] for r in d], edgecolors="#000000", linewidths=1.0, zorder=3, marker="D")
ax.set_yscale("log")
ax.axhline(500, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
ax.axhline(100, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
ax.axvline(2022.5, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
x0 = min(r["yr"] for r in pts) - 1; x1 = max(r["yr"] for r in pts) + 1
ax.set_xlim(x0, x1)
ax.set_ylim(0.6, max(r["cit"] for r in pts) * 12)
ax.text(x0 + 0.4, 560, "500 citations", fontsize=6, color="#6B6B6B", va="bottom")
ax.text(x0 + 0.4, 112, "100 citations", fontsize=6, color="#6B6B6B", va="bottom")
ax.text(2022.7, ax.get_ylim()[1] if False else 1.0, "2023+", fontsize=6, color="#6B6B6B", va="bottom")
ax.set_xlabel("Publication year of the cited paper")
ax.set_ylabel("OpenAlex citations")
# label defaults with simple collision avoidance in display space
fig.canvas.draw()
rend = fig.canvas.get_renderer()
mk = [ax.transData.transform((r["yr"], max(r["cit"], 0.8))) for r in pts]
dk = [ax.transData.transform((r["yr"], max(r["cit"], 0.8))) for r in d]
boxes = []
cands = [(8, 0), (-8, 0), (7, 9), (7, -9), (-7, 9), (-7, -9)] + [(sx * dx, dy) for dx, dy in [(12, 18), (12, -18), (18, 30), (18, -30), (26, 44), (26, -44), (30, 0), (34, 60), (34, -60)] for sx in (1, -1)]
def hit(bb):
    for o in boxes:
        if bb.overlaps(o):
            return True
    for (px, py) in dk:
        if bb.x0 - 4 < px < bb.x1 + 4 and bb.y0 - 4 < py < bb.y1 + 4:
            return True
    n = 0
    for (px, py) in mk:
        if bb.x0 < px < bb.x1 and bb.y0 < py < bb.y1:
            n += 1
    return n > 0
for r in sorted(d, key=lambda r: -r["cit"]):
    yy = max(r["cit"], 0.8)
    best = None
    for dx, dy in cands:
        t = ax.annotate(r["name"], (r["yr"], yy), xytext=(dx, dy), textcoords="offset points", fontsize=6.5, ha="left" if dx > 0 else "right", va="center",
                        arrowprops=dict(arrowstyle="-", lw=0.4, color="#333333", shrinkA=0, shrinkB=3))
        t.update_positions(rend)
        bb = matplotlib.text.Text.get_window_extent(t, rend).expanded(1.05, 1.15)
        if not hit(bb):
            best = t; boxes.append(bb); break
        t.remove()
    if best is None:
        t = ax.annotate(r["name"], (r["yr"], yy), xytext=(7, 7), textcoords="offset points", fontsize=6.5, ha="left", va="center")
        boxes.append(t.get_window_extent(rend)); print("WARN label fallback", r["name"])
med = statistics.median([r["cit"] for r in pts])
nop = sum(1 for r in recs if r["tier"] == "no paper")
ax.text(0.01, 0.02, "n = %d with a paper; median %d citations; %d without a paper not shown" % (len(pts), med, nop), transform=ax.transAxes, fontsize=6.5, va="bottom")
hs = [plt.Line2D([], [], marker="o", ls="", markerfacecolor=TCOL[t], markeredgecolor="#333333", markeredgewidth=0.3, markersize=4, label=t) for t in TIERS[:-1]]
hs.append(plt.Line2D([], [], marker="D", ls="", markerfacecolor="white", markeredgecolor="#000000", markeredgewidth=1.0, markersize=4.5, label="repository default"))
ax.legend(handles=hs, loc="upper left", frameon=False, fontsize=6.5, handletextpad=0.2, borderaxespad=0.3, ncol=5, columnspacing=0.8)
fig.tight_layout(pad=0.4)
for ext in ("svg", "png"):
    fig.savefig(os.path.join(out, prefix + "_catalog_year_citations." + ext), dpi=600 if ext == "png" else None)
plt.close(fig)
print("defaults", [(r["name"], r["yr"], r["cit"]) for r in d])
