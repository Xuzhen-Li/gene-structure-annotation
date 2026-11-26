"""Small SVG builder for editable schematics (live text, no external deps beyond matplotlib for text metrics)."""
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import html

FONT = "Arial, Liberation Sans, Helvetica, sans-serif"
_FP = {False: FontProperties(family="Arial"), True: FontProperties(family="Arial", weight="bold")}
PAL = {"blue": "#1F72AE", "orange": "#F77E12", "green": "#119B76", "red": "#CC312C",
       "purple": "#595594", "sky": "#62B4E7", "gold": "#E6C32A", "magenta": "#A8127F",
       "brown": "#8A4C38", "grey": "#6B6B6B", "dark": "#333333"}

def tint(hexc, f):
    h = hexc.lstrip("#"); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * f); g = int(g + (255 - g) * f); b = int(b + (255 - b) * f)
    return "#%02X%02X%02X" % (r, g, b)

def tw(s, size, bold=False):
    if not s:
        return 0.0
    return TextPath((0, 0), s, size=size, prop=_FP[bold]).get_extents().x1 + 0.5

def wrap(s, size, width, bold=False):
    words = s.split(" "); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size, bold) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

class SVG:
    def __init__(self, w, h, title=""):
        self.w, self.h = w, h; self.title = title; self.body = []; self.grads = {}; self.markers = {}
        self.overflow = []

    def _grad(self, color):
        gid = "g" + color.lstrip("#")
        if gid not in self.grads:
            self.grads[gid] = (tint(color, 0.93), tint(color, 0.82))
        return gid

    def _marker(self, color):
        mid = "m" + color.lstrip("#")
        self.markers[mid] = color
        return mid

    def rect(self, x, y, w, h, color, rx=8, fill=None, stroke_w=1.4, dash=None, shadow=True, grad=True, sfill=None):
        f = fill if fill else ("url(#%s)" % self._grad(color) if grad else tint(color, 0.9))
        d = " stroke-dasharray=\"%s\"" % dash if dash else ""
        s = " filter=\"url(#shadow)\"" if shadow else ""
        self.body.append("<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%.1f\" rx=\"%g\" fill=\"%s\" stroke=\"%s\" stroke-width=\"%g\"%s%s/>" % (x, y, w, h, rx, f, color, stroke_w, d, s))

    def text(self, x, y, s, size=14, bold=False, color="#000000", anchor="start", italic=False, maxw=None):
        if maxw is not None and tw(s, size, bold) > maxw + 0.5:
            self.overflow.append((s, round(tw(s, size, bold), 1), maxw))
        st = " font-style=\"italic\"" if italic else ""
        self.body.append("<text x=\"%.1f\" y=\"%.1f\" font-family=\"%s\" font-size=\"%g\" font-weight=\"%s\" fill=\"%s\" text-anchor=\"%s\"%s>%s</text>" % (x, y, FONT, size, "bold" if bold else "normal", color, anchor, st, html.escape(s)))

    def line(self, pts, color="#333333", w=1.6, arrow=True, dash=None):
        p = " ".join("%.1f,%.1f" % q for q in pts)
        m = " marker-end=\"url(#%s)\"" % self._marker(color) if arrow else ""
        d = " stroke-dasharray=\"%s\"" % dash if dash else ""
        self.body.append("<polyline points=\"%s\" fill=\"none\" stroke=\"%s\" stroke-width=\"%g\" stroke-linejoin=\"round\"%s%s/>" % (p, color, w, d, m))

    def raw(self, s):
        self.body.append(s)

    def node(self, x, y, w, title, lines=(), color="#1F72AE", tsize=15, bsize=12.5, pad=10, dash=None, align="middle", title_color=None, body_color="#333333", min_h=0, bold_first=False):
        tl = wrap(title, tsize, w - 2 * pad, True) if title else []
        bl = []
        for ln in lines:
            bl += wrap(ln, bsize, w - 2 * pad)
        h = pad + len(tl) * tsize * 1.22 + (4 if tl and bl else 0) + len(bl) * bsize * 1.32 + pad - 2
        h = max(h, min_h)
        self.rect(x, y, w, h, color, dash=dash)
        cx = x + w / 2 if align == "middle" else x + pad
        yy = y + pad + tsize * 0.92
        for t in tl:
            self.text(cx, yy, t, tsize, True, title_color or color, align, maxw=w - 2 * pad); yy += tsize * 1.22
        yy += (4 if tl and bl else 0) - tsize * 0.22 + bsize * 0.98 if tl else 0
        if not tl:
            yy = y + pad + bsize * 0.95
        for b in bl:
            self.text(cx, yy, b, bsize, False, body_color, align, maxw=w - 2 * pad); yy += bsize * 1.32
        return h

    def save(self, path):
        defs = ["<filter id=\"shadow\" x=\"-10%\" y=\"-10%\" width=\"130%\" height=\"140%\"><feDropShadow dx=\"0\" dy=\"1.5\" stdDeviation=\"1.6\" flood-color=\"#000000\" flood-opacity=\"0.16\"/></filter>"]
        for gid, (a, b) in self.grads.items():
            defs.append("<linearGradient id=\"%s\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"%s\"/><stop offset=\"1\" stop-color=\"%s\"/></linearGradient>" % (gid, a, b))
        for mid, c in self.markers.items():
            defs.append("<marker id=\"%s\" viewBox=\"0 0 12 10\" refX=\"10\" refY=\"5\" markerWidth=\"9\" markerHeight=\"7.5\" markerUnits=\"userSpaceOnUse\" orient=\"auto\"><path d=\"M0,0 L12,5 L0,10 L3,5 z\" fill=\"%s\"/></marker>" % (mid, c))
        out = ["<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"%d\" height=\"%d\" viewBox=\"0 0 %d %d\">" % (self.w, self.h, self.w, self.h)]
        if self.title:
            out.append("<title>%s</title>" % html.escape(self.title))
        out.append("<defs>" + "".join(defs) + "</defs>")
        out.append("<rect x=\"0\" y=\"0\" width=\"%d\" height=\"%d\" fill=\"#FFFFFF\"/>" % (self.w, self.h))
        out += self.body
        out.append("</svg>")
        with open(path, "x", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")
        return self.overflow
