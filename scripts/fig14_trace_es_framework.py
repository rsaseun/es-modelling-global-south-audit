"""Fig. 14. The TRACE-ES framework.

Reproduces Fig. 14 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

The diagram is drawn as SVG at its printed size (6.3 in = full text width), so the
type sizes are true point sizes in the article: main themes 14 pt, sub-themes 11 pt.
Flow arrows run Drivers -> Evidence -> Pillars -> Deliverables -> Outcomes; the four
coloured arrows carry the deliverable of each pillar.

Output: outputs/figures/Fig14_TRACE-ES_framework.svg (editable), .pdf (vector, fonts
embedded) and .png (1200 dpi).
Requires: cairosvg (pip) with the Cairo library, and the Liberation Sans font.
Icons: Lucide (ISC licence), vendored in data/icons/.
Run from the repository root:  python scripts/fig14_trace_es_framework.py
"""
import re
from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg
from PIL import Image, ImageFont

REPO = Path(__file__).resolve().parents[1]
ICONS = REPO / "data" / "icons"
OUT = REPO / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
NAME = "Fig14_TRACE-ES_framework"
DPI = 1200

FONT = "Liberation Sans"
TTF = {False: "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
       True: "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"}
MAIN, SUB = 14, 11                     # point sizes: main themes / sub-themes
W = 6.3 * 72                           # 453.6 pt = full text width of the article
M = 6                                  # outer margin
INK, INK2, MUTED = "#0b0b0b", "#3f3e3b", "#8a8984"
COL = dict(T="#2a78d6", R="#eb6834", A="#1baf7a", CE="#6250d6", drv="#7a5c3e", evi="#c98a00",
           gain="#1a8f4f", gap="#d23b37", out="#0b7a3e", navy="#0f2a4a")
TINT = dict(T="#eaf2fc", R="#fdf0ea", A="#e6f6ef", CE="#efedfb", drv="#f4efe8", evi="#fff6dd", out="#e6f4ea")

_fonts = {}


def text_w(s, size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(TTF[bold], size * 20)
    return _fonts[key].getlength(s) / 20


def wrap(s, width, size, bold=False):
    lines, cur = [], ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(trial, size, bold) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    lines.append(cur)
    for ln in lines:
        assert text_w(ln, size, bold) <= width + 0.5, f"text too wide: {ln!r}"
    return lines


def text(x, y, lines, size, bold=False, color=INK, anchor="start", lh=1.18, italic=False):
    if isinstance(lines, str):
        lines = [lines]
    out = [f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" '
           f'font-weight="{"bold" if bold else "normal"}"{" font-style=\"italic\"" if italic else ""} '
           f'fill="{color}" text-anchor="{anchor}">']
    for i, ln in enumerate(lines):
        out.append(f'<tspan x="{x:.2f}" dy="{0 if i == 0 else size * lh:.2f}">{escape(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)


def icon(name, cx, cy, size, color, sw=2.0):
    s = (ICONS / f"{name}.svg").read_text()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S)
    k = size / 24
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) scale({k:.4f})" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')


def badge(name, cx, cy, r, fill, fg="white"):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{fill}"/>' + icon(name, cx, cy, r * 1.25, fg, 2.2)


def rrect(x, y, w, h, fill, stroke, sw=1.2, r=7):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def flow_arrow(cx, y, h, w, color, label=None):
    """Down-pointing block arrow (flow direction) with an optional label on its right."""
    hw, head = w / 2, min(h * 0.55, 9)
    pts = [(cx - hw * 0.45, y), (cx + hw * 0.45, y), (cx + hw * 0.45, y + h - head), (cx + hw, y + h - head),
           (cx, y + h), (cx - hw, y + h - head), (cx - hw * 0.45, y + h - head)]
    s = f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="{color}"/>'
    if label:
        s += text(cx + hw + 6, y + h / 2 + SUB * 0.36, label, SUB, italic=True, color=INK2)
    return s


def heading(x, y, icon_name, color, title, width):
    """Main-theme heading: icon badge + 14-pt bold title (wrapped)."""
    lines = wrap(title, width - 26, MAIN, True)
    s = badge(icon_name, x + 9, y + 8, 9, color) + text(x + 24, y + 13, lines, MAIN, True, INK)
    return s, 8 + 13 + (len(lines) - 1) * MAIN * 1.18


def build():
    svg, y = [], M
    iw = W - 2 * M

    # ---------- title band ----------
    sub = wrap("Translating Regional Analytics into Credible, Equitable ES evidence",
               iw - 46, SUB)
    th = 10 + MAIN + 3 + len(sub) * SUB * 1.18 + 1
    svg.append(rrect(M, y, iw, th, COL["navy"], COL["navy"], 0, 8))
    svg.append(text(M + 10, y + 5 + MAIN, "TRACE-ES framework for the Global South", MAIN, True, "white"))
    svg.append(text(M + 10, y + 8 + MAIN + SUB, sub, SUB, False, "#dbe6f3"))
    svg.append(icon("globe", W - M - 18, y + th / 2, 22, "white", 1.6))
    y += th + 6

    # ---------- 1. drivers ----------
    drivers = [("thermometer-sun", "Warming (SSP–RCP)"), ("tractor", "Land-use change"),
               ("building-2", "Urban, cropland"), ("waves", "Sea-level rise"),
               ("sun", "Drought, aridity"), ("trees", "Restoration, zoning")]
    pad, gap, cols = 7, 5, 3
    cw = (iw - 2 * pad - (cols - 1) * gap) / cols
    wrapped = [wrap(t, cw - 27, SUB) for _, t in drivers]
    ch = max(len(w_) for w_ in wrapped) * SUB * 1.18 + 7
    head, hh = heading(M + pad, y + 5, "thermometer-sun", COL["drv"], "Drivers: climate and environmental change", iw - 2 * pad)
    bh = 5 + hh + 7 + 2 * ch + gap + pad
    svg.append(rrect(M, y, iw, bh, TINT["drv"], COL["drv"]))
    svg.append(head)
    cy0 = y + 5 + hh + 7
    for i, ((ic, _), lines) in enumerate(zip(drivers, wrapped)):
        cx, cy = M + pad + (i % cols) * (cw + gap), cy0 + (i // cols) * (ch + gap)
        svg.append(rrect(cx, cy, cw, ch, "white", "#d9cfc2", 0.8, 5))
        svg.append(icon(ic, cx + 12, cy + ch / 2, 15, COL["drv"], 2.2))
        ty = cy + ch / 2 - (len(lines) - 1) * SUB * 1.18 / 2 + SUB * 0.36
        svg.append(text(cx + 24, ty, lines, SUB, False, INK))
    y += bh
    svg.append(flow_arrow(W / 2, y + 2, 15, 26, MUTED, "alter ES supply and demand"))
    y += 19

    # ---------- 2. evidence from the review ----------
    gains = ["≈25% growth per year; doubling 3.2 yr",
             "Land-change × climate scenarios",
             "New services: cooling, flood, marine"]
    gaps = ["Validation reported in <10% of studies",
            "25–38% of regional studies led abroad",
            "48.9% China; South–South links 8.0%"]
    colw = (iw - 2 * pad - 10) / 2
    head, hh = heading(M + pad, y + 5, "database", COL["evi"], "Evidence from this review (1990–2025, n = 7,972)", iw - 2 * pad)
    gl = [wrap(t, colw - 18, SUB) for t in gains]; pl = [wrap(t, colw - 18, SUB) for t in gaps]
    rows_h = [max(len(a), len(b)) * SUB * 1.18 + 3 for a, b in zip(gl, pl)]
    bh = 5 + hh + 7 + SUB + 5 + sum(rows_h) + pad - 3
    svg.append(rrect(M, y, iw, bh, TINT["evi"], COL["evi"]))
    svg.append(head)
    ly = y + 5 + hh + 7 + SUB
    for k, (lab, items, ic, col) in enumerate([("Gains", gl, "circle-check", COL["gain"]), ("Gaps", pl, "triangle-alert", COL["gap"])]):
        x0 = M + pad + k * (colw + 10)
        svg.append(text(x0, ly, lab, SUB, True, col))
        yy = ly + 5
        for lines, rh in zip(items, rows_h):
            svg.append(icon(ic, x0 + 6, yy + SUB * 0.55, 11, col, 2.4))
            svg.append(text(x0 + 16, yy + SUB * 0.9, lines, SUB, False, INK))
            yy += rh
    svg.append(f'<line x1="{W / 2:.2f}" y1="{ly - SUB:.2f}" x2="{W / 2:.2f}" y2="{y + bh - pad:.2f}" stroke="#e3cf9a" stroke-width="0.8"/>')
    y += bh
    svg.append(flow_arrow(W / 2, y + 2, 15, 26, MUTED, "gaps motivate four pillars"))
    y += 19

    # ---------- 3. four pillars ----------
    P = [("T", "layers", "Transferable quantification", ["Tier 1: coefficients, screening only",
          "Tier 2: InVEST, SWAT, RUSLE", "Tier 3: process–ML hybrids", "Regional parameter libraries"]),
         ("R", "shield-check", "Robustness & credibility", ["Ensembles; uncertainty propagation",
          "In-situ validation, field data", "Model cards and reporting", "Context-sensitive ESV coefficients"]),
         ("A", "git-merge", "Analytical integration", ["Land change (PLUS/FLUS) × climate",
          "ES supply–demand flows", "Trade-offs and synergies", "Attribution (Geodetector, MGWR)"]),
         ("CE", "users", "Co-production & equity", ["Global South-led teams", "Data sovereignty (CARE)",
          "Participatory, cultural NCP", "South–South hubs; open outlets"])]
    pw = (iw - 6) / 2
    letters = {"T": "T", "R": "R", "A": "A", "CE": "C/E"}
    heads = [wrap(t, pw - 58, MAIN, True) for _, _, t, _ in P]
    items = [[wrap(s, pw - 26, SUB) for s in it] for *_, it in P]
    pos = [(M, 0), (M + pw + 6, 0), (M, 1), (M + pw + 6, 1)]
    row_head = [max(len(heads[0]), len(heads[1])), max(len(heads[2]), len(heads[3]))]
    row_body = [max(sum(len(l) for l in items[0]), sum(len(l) for l in items[1])),
                max(sum(len(l) for l in items[2]), sum(len(l) for l in items[3]))]
    hdr_h = [7 + n * MAIN * 1.18 + 1 for n in row_head]
    box_h = [hdr_h[r] + 5 + row_body[r] * SUB * 1.18 + 4 * 2.5 + 4 for r in (0, 1)]
    ys = [y, y + box_h[0] + 6]
    for (key, ic, title, _), hl, it, (px, r) in zip(P, heads, items, pos):
        py, bh, hh = ys[r], box_h[r], hdr_h[r]
        svg.append(rrect(px, py, pw, bh, TINT[key], COL[key], 1.4))
        svg.append(f'<path d="M{px:.2f},{py + hh:.2f} V{py + 7:.2f} Q{px:.2f},{py:.2f} {px + 7:.2f},{py:.2f} '
                   f'H{px + pw - 7:.2f} Q{px + pw:.2f},{py:.2f} {px + pw:.2f},{py + 7:.2f} V{py + hh:.2f} Z" fill="{COL[key]}"/>')
        lt = letters[key]
        svg.append(f'<circle cx="{px + 15:.2f}" cy="{py + hh / 2:.2f}" r="11.8" fill="white"/>')
        svg.append(text(px + 15, py + hh / 2 + (4.9 if len(lt) == 1 else 3.9), lt, MAIN if len(lt) == 1 else SUB, True, COL[key], "middle"))
        svg.append(icon(ic, px + pw - 14, py + hh / 2, 15, "white", 2.2))
        svg.append(text(px + 31, py + hh / 2 - (len(hl) - 1) * MAIN * 1.18 / 2 + MAIN * 0.36, hl, MAIN, True, "white"))
        yy = py + hh + 5
        for lines in it:
            svg.append(f'<circle cx="{px + 11:.2f}" cy="{yy + SUB * 0.5:.2f}" r="2.6" fill="{COL[key]}"/>')
            svg.append(text(px + 19, yy + SUB * 0.86, lines, SUB, False, INK))
            yy += len(lines) * SUB * 1.18 + 2.5
    y = ys[1] + box_h[1] + 4

    # ---------- deliverables: four coloured flow arrows ----------
    dl = [("T", "Calibrated models"), ("R", "Validated estimates"),
          ("A", "Planning-ready scenarios"), ("CE", "Locally owned evidence")]
    dw = (iw - 3 * 5) / 4
    dlines = [wrap(f"{letters[k]}: {t}", dw - 10, SUB, True) for k, t in dl]
    body = max(len(l) for l in dlines) * SUB * 1.18 + 6
    tip = 8
    svg.append(text(M, y + SUB, "Deliverables", SUB, True, INK2))
    y += SUB + 3.5
    for i, ((key, _), lines) in enumerate(zip(dl, dlines)):
        x = M + i * (dw + 5)
        pts = [(x, y), (x + dw, y), (x + dw, y + body), (x + dw / 2, y + body + tip), (x, y + body)]
        svg.append(f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="{COL[key]}"/>')
        ty = y + body / 2 - (len(lines) - 1) * SUB * 1.18 / 2 + SUB * 0.36
        svg.append(text(x + dw / 2, ty, lines, SUB, True, "white", "middle"))
    y += body + tip + 5

    # ---------- 4. outcomes ----------
    outs = [("landmark", "Ecosystem accounts (SEEA-EA)"), ("sprout", "Nature-based solutions targeting"),
            ("wheat", "Food–water–carbon planning"), ("target", "GBF and SDG 2, 6, 11, 13–15")]
    tw = (iw - 2 * pad - gap) / 2
    olines = [wrap(t, tw - 32, SUB) for _, t in outs]
    tile_h = max(len(l) for l in olines) * SUB * 1.18 + 9
    head, hh = heading(M + pad, y + 5, "badge-check", COL["out"], "Outcomes 2026–2035: decision-grade ES intelligence", iw - 2 * pad)
    bh = 5 + hh + 7 + 2 * tile_h + gap + pad
    svg.append(rrect(M, y, iw, bh, TINT["out"], COL["out"], 1.4))
    svg.append(head)
    ty0 = y + 5 + hh + 7
    for i, ((ic, _), lines) in enumerate(zip(outs, olines)):
        x, ty = M + pad + (i % 2) * (tw + gap), ty0 + (i // 2) * (tile_h + gap)
        svg.append(rrect(x, ty, tw, tile_h, "white", "#b8dcc4", 0.8, 5))
        svg.append(badge(ic, x + 13, ty + tile_h / 2, 8.5, COL["out"]))
        svg.append(text(x + 28, ty + tile_h / 2 - (len(lines) - 1) * SUB * 1.18 / 2 + SUB * 0.36, lines, SUB, False, INK))
    y += bh + M

    H = y
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.1f}pt" height="{H:.1f}pt" viewBox="0 0 {W:.1f} {H:.1f}">'
            f'<rect width="100%" height="100%" fill="white"/>' + "".join(svg) + "</svg>"), H


def fig_framework():
    svg, H = build()
    (OUT / f"{NAME}.svg").write_text(svg, encoding="utf-8")
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT / f"{NAME}.pdf"))
    png = OUT / f"{NAME}.png"
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(png), output_width=round(W / 72 * DPI), background_color="white")
    im = Image.open(png).convert("RGB")
    im.save(png, dpi=(DPI, DPI), optimize=True)
    print(f"{NAME}: {W / 72:.2f} x {H / 72:.2f} in, {im.width} x {im.height} px at {DPI} dpi")


if __name__ == "__main__":
    fig_framework()
