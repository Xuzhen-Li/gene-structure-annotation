"""Catalog charts from a repository SOFTWARE_AUTHORITY.tsv (paper-viz house look).
usage: python3 -B make_catalog_charts_v6.py REPO_KEY TSV OUTDIR PREFIX
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
plt.rcParams.update({"font.family": "Arial", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.8,
    "ytick.major.size": 2.8, "xtick.labelsize": 7, "ytick.labelsize": 7, "svg.fonttype": "none",
    "pdf.fonttype": 42, "axes.titleweight": "normal", "axes.labelweight": "normal"})

def _wrap_lab(s, width=28):
    if len(s) <= width:
        return s
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return chr(10).join(lines)

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
h = max(135, 5.6 * len(order) + 24)
fig, ax = plt.subplots(figsize=(135 * MM, h * MM))
ys = list(range(len(order)))[::-1]
for y, s in zip(ys, order):
    left = 0
    for t in TIERS:
        v = counts[s][t]
        if v:
            ax.barh(y, v, left=left, height=0.68, color=TCOL[t], edgecolor="white", linewidth=0.3)
            if v >= 3:
                ink = "#000000" if t in ("newer", "established", "niche", "no paper") or True else "#FFFFFF"
                # white on standard blue #1F72AE is typically >=4.5; still use black on green/gold/sky/grey
                if t == "standard":
                    ink = "#FFFFFF"
                ax.text(left + v / 2, y, str(v), ha="center", va="center", fontsize=7, color=ink, fontweight="bold")
        left += v
    ax.text(left + 0.4, y, str(left), ha="left", va="center", fontsize=7, color="#000000")
ax.set_yticks(ys)
ax.set_yticklabels([_wrap_lab(s) for s in order])
ax.set_xlabel(("Catalogue" if key == "te" else "Catalog") + " entries (n)")
mx = max(sum(counts[s].values()) for s in order)
ax.set_xlim(0, mx * (1.12 if key == "te" else 1.75) + 1)
ax.set_ylim(-0.6, len(order) - 0.4)
ax.tick_params(axis="y", length=0)
handles = [Patch(facecolor=TCOL[t], edgecolor="none", label="%s: %d" % (TLAB[t], tot_t[t])) for t in TIERS]
ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=7, handlelength=1.0, handleheight=0.8, borderaxespad=0.3, title="Citation tier (OpenAlex)", title_fontsize=7)
ax.text(0.99, 0.99, "N = %d entries" % N, transform=ax.transAxes, ha="right", va="top", fontsize=7)
fig.tight_layout(pad=0.4)
for ext in ("svg", "png"):
    fig.savefig(os.path.join(out, prefix + "_catalog_by_step_v2." + ext), dpi=600 if ext == "png" else None)
plt.close(fig)

# ---- chart 2: year vs citations ----
pts = [r for r in recs if r["yr"] and r["cit"] is not None]
fig, ax = plt.subplots(figsize=(135 * MM, 89 * MM))
for t in TIERS[:-1]:
    xs = [r["yr"] for r in pts if r["tier"] == t and not r["isdef"]]
    yv = [max(r["cit"], 0.8) for r in pts if r["tier"] == t and not r["isdef"]]
    ax.scatter(xs, yv, s=14, c=TCOL[t], edgecolors="#333333", linewidths=0.3, zorder=2, label=None)
d = [r for r in pts if r["isdef"]]
ax.scatter([r["yr"] for r in d], [max(r["cit"], 0.8) for r in d], s=30, c=[TCOL[r["tier"]] for r in d], edgecolors="#000000", linewidths=1.0, zorder=3, marker="D")
ax.set_yscale("log")
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
def _log_tick(v, pos):
    if v <= 0:
        return ""
    r = round(v)
    if abs(v - r) > 1e-8 * max(v, 1):
        return ""
    n = int(r)
    if n in (1, 10, 100, 1000, 10000, 100000, 1000000):
        return "{:,}".format(n)
    return ""
ax.yaxis.set_major_locator(LogLocator(base=10, numticks=8))
ax.yaxis.set_major_formatter(FuncFormatter(_log_tick))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=[]))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.axhline(500, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
ax.axhline(100, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
ax.axvline(2022.5, color="#757575", lw=0.5, ls=(0, (2, 2)), zorder=1)
x0 = min(r["yr"] for r in pts) - 1
x1 = max(r["yr"] for r in pts) + 2.5
ax.set_xlim(x0, x1)
ax.set_ylim(0.6, max(r["cit"] for r in pts) * 12)
ax.set_xlabel("Publication year of the cited paper")
ax.set_ylabel("OpenAlex citations")
fig.tight_layout(pad=0.4)
fig.canvas.draw()
rend = fig.canvas.get_renderer()
# reference-line labels, kept off the data cloud and off the axes frame
ref_labs = []
def _place_ref(text, xd, yd, ha, va):
    t = ax.text(xd, yd, text, fontsize=7, color="#6B6B6B", ha=ha, va=va, zorder=4)
    ref_labs.append(t)
    return t
# put 500/100 labels at the far right inside the axes, above each line
_place_ref("500 citations", x0 + 0.35, 560, "left", "bottom")
_place_ref("100 citations", x0 + 0.35, 112, "left", "bottom")
_place_ref("2023+", 2022.7, 0.72, "left", "bottom")
# collision helpers
import matplotlib.transforms as mtransforms
spines = {}
for name in ("left", "right", "top", "bottom"):
    spines[name] = ax.transData.transform(ax.spines[name].get_path().vertices) if False else None
# display coords of frame
bb_ax = ax.get_window_extent(rend)
mk = [ax.transData.transform((r["yr"], max(r["cit"], 0.8))) for r in pts]
dk = [ax.transData.transform((r["yr"], max(r["cit"], 0.8))) for r in d]
# display y of reference lines
y100 = ax.transData.transform((x0, 100))[1]
y500 = ax.transData.transform((x0, 500))[1]
x2023 = ax.transData.transform((2022.5, 1))[0]
boxes = []
# include ref labels as occupied
for t in ref_labs:
    t.update_positions(rend) if hasattr(t, "update_positions") else None
    boxes.append(t.get_window_extent(rend).expanded(1.05, 1.2))
# candidates: prefer left for late years; many offsets; no-arrow first if close
cands_right = [(8, 0), (8, 10), (8, -10), (10, 16), (10, -16), (14, 24), (14, -24), (18, 34), (18, -34), (22, 46), (22, -46), (28, 8), (28, -8), (8, 58), (8, -58)]
cands_left = [(-8, 0), (-8, 10), (-8, -10), (-10, 16), (-10, -16), (-14, 24), (-14, -24), (-18, 34), (-18, -34), (-22, 46), (-22, -46), (-28, 8), (-28, -8), (-8, 58), (-8, -58)]
def _leader_hits(px, py, bb):
    # line from point to nearest corner / mid of bbox
    cx = (bb.x0 + bb.x1) / 2
    cy = (bb.y0 + bb.y1) / 2
    for o in boxes:
        # if the segment (px,py)-(cx,cy) crosses o (and o is not this box)
        if _seg_box(px, py, cx, cy, o):
            return True
    return False
def _seg_box(x0, y0, x1, y1, bb, pad=1.0):
    # reject if the segment interior intersects bb (ignore near the point itself)
    # Liang-style clip
    dx, dy = x1 - x0, y1 - y0
    if dx == 0 and dy == 0:
        return False
    L, R, B, T = bb.x0 - pad, bb.x1 + pad, bb.y0 - pad, bb.y1 + pad
    # sample 12 points along the middle 70% of the segment
    for k in range(2, 11):
        t = k / 12.0
        x, y = x0 + t * dx, y0 + t * dy
        if L <= x <= R and B <= y <= T:
            return True
    return False
def hit(bb, px, py):
    # other labels
    for o in boxes:
        if bb.overlaps(o):
            return True
    # default diamonds
    for (qx, qy) in dk:
        if bb.x0 - 5 < qx < bb.x1 + 5 and bb.y0 - 5 < qy < bb.y1 + 5:
            return True
    # scatter points
    n = 0
    for (qx, qy) in mk:
        if bb.x0 < qx < bb.x1 and bb.y0 < qy < bb.y1:
            n += 1
    if n > 0:
        return True
    # axes frame: text may sit in the right margin, but must not sit ON the right spine
    rx = ax.transData.transform((ax.get_xlim()[1], 1))[0]
    lx = ax.transData.transform((ax.get_xlim()[0], 1))[0]
    typ = ax.transData.transform((2000, ax.get_ylim()[1]))[1]
    byp = ax.transData.transform((2000, ax.get_ylim()[0]))[1]
    # if the spine x is inside the label (not just at the edge by <1 px)
    if bb.x0 + 1.5 < rx < bb.x1 - 1.5 or bb.x0 + 1.5 < lx < bb.x1 - 1.5:
        return True
    if bb.y0 + 1.5 < typ < bb.y1 - 1.5 or bb.y0 + 1.5 < byp < bb.y1 - 1.5:
        return True
    # reference lines crossing the glyph
    if bb.y0 + 1.0 < y100 < bb.y1 - 1.0 and not (bb.x1 < lx or bb.x0 > rx):
        return True
    if bb.y0 + 1.0 < y500 < bb.y1 - 1.0 and not (bb.x1 < lx or bb.x0 > rx):
        return True
    if bb.x0 + 1.0 < x2023 < bb.x1 - 1.0 and not (bb.y1 < min(typ, byp) or bb.y0 > max(typ, byp)):
        return True
    if _leader_hits(px, py, bb):
        return True
    return False
MANUAL = {
    ("function", "DeepTMHMM"): (40, -60),
    ("function", "OrthoFinder 3"): (-30, -22),
    ("function", "TMbed"): (16, 18),
    ("te", "TEtrimmer"): (-12, -36),
    ("te", "panEDTA"): (-16, -18),
}
for r in sorted(d, key=lambda r: -r["cit"]):
    yy = max(r["cit"], 0.8)
    man = MANUAL.get((key, r["name"]))
    if man is None:
        man = MANUAL.get((prefix, r["name"]))
    if man is not None:
        dx, dy = man
        t = ax.annotate(r["name"], (r["yr"], yy), xytext=(dx, dy), textcoords="offset points", fontsize=7, color="#000000", ha="left" if dx > 0 else "right", va="center",
                        arrowprops=dict(arrowstyle="-", lw=0.4, color="#000000", shrinkA=0, shrinkB=3))
        t.update_positions(rend)
        boxes.append(matplotlib.text.Text.get_window_extent(t, rend).expanded(1.08, 1.2))
        continue
    px, py = ax.transData.transform((r["yr"], yy))
    # late years: try left first
    order_c = (cands_left + cands_right) if r["yr"] >= (x1 - 4) else (cands_right + cands_left)
    best = None
    for dx, dy in order_c:
        t = ax.annotate(r["name"], (r["yr"], yy), xytext=(dx, dy), textcoords="offset points", fontsize=7, color="#000000", ha="left" if dx > 0 else "right", va="center",
                        arrowprops=dict(arrowstyle="-", lw=0.4, color="#000000", shrinkA=0, shrinkB=3) if abs(dx) > 9 or abs(dy) > 9 else None)
        t.update_positions(rend)
        bb = matplotlib.text.Text.get_window_extent(t, rend).expanded(1.08, 1.2)
        if not hit(bb, px, py):
            best = t
            boxes.append(bb)
            break
        t.remove()
    if best is None:
        t = ax.annotate(r["name"], (r["yr"], yy), xytext=(-10, 12), textcoords="offset points", fontsize=7, color="#000000", ha="right", va="bottom")
        boxes.append(t.get_window_extent(rend))
        print("WARN label fallback", r["name"])
med = statistics.median([r["cit"] for r in pts])
nop = sum(1 for r in recs if r["tier"] == "no paper")
ax.text(0.01, 0.02, "n = %d with a paper; median %d citations; %d without a paper not shown" % (len(pts), med, nop), transform=ax.transAxes, fontsize=7, va="bottom", color="#000000")
hs = [plt.Line2D([], [], marker="o", ls="", markerfacecolor=TCOL[t], markeredgecolor="#333333", markeredgewidth=0.3, markersize=4, label=t) for t in TIERS[:-1]]
hs.append(plt.Line2D([], [], marker="D", ls="", markerfacecolor="white", markeredgecolor="#000000", markeredgewidth=1.0, markersize=4.5, label="repository default"))
ax.legend(handles=hs, loc="upper left", frameon=False, fontsize=7, handletextpad=0.2, borderaxespad=0.3, ncol=5, columnspacing=0.8)
for ext in ("svg", "png"):
    fig.savefig(os.path.join(out, prefix + "_catalog_year_citations_v2." + ext), dpi=600 if ext == "png" else None)
plt.close(fig)
print("defaults", [(r["name"], r["yr"], r["cit"]) for r in d])
