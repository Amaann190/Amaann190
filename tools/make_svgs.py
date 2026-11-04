"""Builds the SVGs used by the profile README (dark + light variants).

Run:  python tools/make_svgs.py
Edit the numbers / copy in PROJECTS and TICKER below, then re-run.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg="#0b0b0b", ink="#f4f3ee", muted="#8b8a84", faint="#5a5955",
                 rule="#191919", edge="#2e2e2c", accent="#ff6a3d", up="#4ade80",
                 card="#101010", border="#232322", grain=".07"),
    "light": dict(bg="#f6f4ee", ink="#141413", muted="#6d6b64", faint="#a3a097",
                  rule="#e6e1d3", edge="#cfcabb", accent="#d8492a", up="#15803d",
                  card="#fbfaf6", border="#e0dbcc", grain=".05"),
}

SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
SANS = "'Inter Tight', 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"


def base_style(t):
    return f"""
  <style>
    .serif {{ font-family: {SERIF}; }}
    .sans  {{ font-family: {SANS}; }}
    .mono  {{ font-family: {MONO}; }}
    .blink {{ animation: blink 1.6s ease-in-out infinite; }}
    .pulse {{ animation: pulse 6s ease-in-out infinite; }}
        @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
    @keyframes pulse {{ 0%,35% {{ opacity: .0 }} 50%,85% {{ opacity: 1 }} 100% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
  </style>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 {t['grain']} 0"/>
  </filter>"""


# ---------------------------------------------------------------- header
NODES = {  # account graph on the right of the header
    "a": (812, 128, "AC-0193"), "b": (962, 96, "AC-4471"), "c": (1110, 146, "AC-2208"),
    "d": (1082, 268, "AC-9035"), "e": (930, 292, "AC-1162"), "f": (800, 246, "AC-7310"),
    "g": (958, 196, "AC-5524"),
}
EDGES = [("a", "b"), ("a", "f"), ("f", "e"), ("e", "d"), ("a", "g"), ("f", "g"), ("g", "e")]
CYCLE = ["b", "c", "d", "g", "b"]  # the laundering loop that lights up

TICKER = [
    ("AML", "▲ 415×", "precision lift"),
    ("RECON", "₹25.4L", "gaps traced"),
    ("UPI", "16.2B", "txns covered"),
    ("TESTS", "64+", "passing"),
    ("RECON", "10,000/10,000", "orders matched"),
    ("AML", "5.07M", "transfers scanned"),
    ("QUEUE", "▲ 37→57%", "top-100 precision"),
]


def header(t):
    W, H = 1200, 440
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'role="img" aria-label="Amaan Shaikh, fintech data analyst">')
    o.append("<defs>" + base_style(t) + "</defs>")
    o.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    # ledger rules + double margin line
    for y in range(110, 372, 28):
        o.append(f'<line x1="0" x2="{W}" y1="{y}" y2="{y}" stroke="{t["rule"]}" stroke-width="1"/>')
    o.append(f'<line x1="40" x2="40" y1="0" y2="372" stroke="{t["accent"]}" stroke-opacity=".35"/>')
    o.append(f'<line x1="44" x2="44" y1="0" y2="372" stroke="{t["accent"]}" stroke-opacity=".35"/>')

    # top strip
    o.append(f'<text class="mono" x="64" y="62" font-size="12.5" letter-spacing="2.4" fill="{t["muted"]}">'
             f'STATEMENT OF WORK  /  FINTECH DATA ANALYST  /  INDIA</text>')
    o.append(f'<circle class="blink" cx="{W-64-262}" cy="58" r="4.5" fill="{t["up"]}"/>')
    o.append(f'<text class="mono" x="{W-64}" y="62" font-size="12.5" letter-spacing="1.2" text-anchor="end" '
             f'fill="{t["ink"]}">open to analyst internships</text>')

    # name
    o.append(f'<g class="rise" style="animation-delay:.05s"><text class="serif" x="60" y="200" font-size="112" '
             f'fill="{t["ink"]}" letter-spacing="-2">Amaan</text></g>')
    o.append(f'<g class="rise" style="animation-delay:.2s"><text class="serif" x="60" y="300" font-size="112" '
             f'font-style="italic" fill="{t["ink"]}" letter-spacing="-2">Shaikh<tspan fill="{t["accent"]}">.</tspan></text></g>')
    o.append(f'<g class="rise" style="animation-delay:.4s"><text class="sans" x="64" y="346" font-size="18" fill="{t["muted"]}">'
             f'I follow money through payment systems until every rupee is accounted for.</text></g>')

    # graph: plain edges
    for u, v in EDGES:
        (x1, y1, _), (x2, y2, _) = NODES[u], NODES[v]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["edge"]}" stroke-width="1.2"/>')
    # cycle edges (base + pulsing highlight)
    cyc = " ".join(("M" if i == 0 else "L") + f" {NODES[n][0]} {NODES[n][1]}" for i, n in enumerate(CYCLE))
    o.append(f'<path d="{cyc}" fill="none" stroke="{t["edge"]}" stroke-width="1.2"/>')
    o.append(f'<path class="pulse" d="{cyc}" fill="none" stroke="{t["accent"]}" stroke-width="2" '
             f'stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" from="0" to="-40" dur="1.2s" repeatCount="indefinite"/></path>')
    # money moving along ordinary edges
    for i, (u, v) in enumerate(EDGES):
        (x1, y1, _), (x2, y2, _) = NODES[u], NODES[v]
        if i % 2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        o.append(f'<circle r="2.6" fill="{t["muted"]}"><animateMotion dur="{2.2 + (i % 3) * .7:.1f}s" '
                 f'begin="-{i * .45:.2f}s" repeatCount="indefinite" path="M {x1} {y1} L {x2} {y2}"/></circle>')
    # money going round the cycle
    for k in range(3):
        o.append(f'<circle r="3.4" fill="{t["accent"]}"><animateMotion dur="6s" begin="-{k * 2}s" '
                 f'repeatCount="indefinite" path="{cyc}"/></circle>')
    # nodes
    for key, (x, y, label) in NODES.items():
        hot = key in CYCLE
        o.append(f'<circle cx="{x}" cy="{y}" r="{7 if hot else 5.5}" fill="{t["bg"]}" '
                 f'stroke="{t["ink"] if hot else t["faint"]}" stroke-width="1.4"/>')
        dy = -16 if y < 200 else 26
        o.append(f'<text class="mono" x="{x}" y="{y + dy}" font-size="10.5" text-anchor="middle" '
                 f'fill="{t["faint"]}" letter-spacing=".5">{label}</text>')
    # detection tag
    o.append(f'<g class="pulse"><rect x="1000" y="318" width="150" height="26" rx="4" fill="none" stroke="{t["accent"]}"/>'
             f'<text class="mono" x="1075" y="335" font-size="11" text-anchor="middle" fill="{t["accent"]}" '
             f'letter-spacing="1">CYCLE · 4 HOPS · 3D</text></g>')

    # ticker
    o.append(f'<rect x="0" y="372" width="{W}" height="68" fill="{t["card"]}"/>')
    o.append(f'<line x1="0" x2="{W}" y1="372" y2="372" stroke="{t["border"]}"/>')
    step = 360
    span = step * len(TICKER)
    o.append('<g><animateTransform attributeName="transform" type="translate" from="0 0" '
             f'to="-{span} 0" dur="{len(TICKER) * 6}s" repeatCount="indefinite"/>')
    for rep in range(3):
        for i, (tag, val, lab) in enumerate(TICKER):
            x = 40 + rep * span + i * step
            col = t["up"] if "▲" in val else t["ink"]
            o.append(f'<text class="mono" x="{x}" y="412" font-size="14" letter-spacing=".6">'
                     f'<tspan fill="{t["faint"]}">{tag}</tspan>'
                     f'<tspan dx="10" fill="{col}" font-weight="600">{val}</tspan>'
                     f'<tspan dx="10" fill="{t["muted"]}">{lab}</tspan></text>')
            o.append(f'<text class="mono" x="{x + step - 28}" y="412" font-size="14" fill="{t["edge"]}">/</text>')
    o.append("</g>")
    o.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" pointer-events="none"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- project cards
PROJECTS = [
    dict(slug="aml", index="01", title="AML Graph Intelligence",
         tagline="Following money between accounts, not just counting transfers.",
         stack="PYTHON · NETWORKX · PANDAS · POWER BI · PYTEST",
         metric="415×", label="PRECISION LIFT OVER BASE RATE",
         note="5.08M synthetic transfers · 42.3% precision vs 0.17% for daily rules",
         repo="aml-graph-intelligence"),
    dict(slug="recon", index="02", title="Merchant Settlement Reconciliation",
         tagline="Did every rupee we sold actually reach the bank?",
         stack="PYTHON · SQLITE · POWER BI · PYTEST",
         metric="₹25.4L", label="RECOVERABLE GAPS TRACED",
         note="books → gateway → bank · 10,000/10,000 orders verified to the paisa",
         repo="merchant-settlement-reconciliation"),
    dict(slug="upi", index="03", title="UPI Reliability Intelligence",
         tagline="Which banks fail most, and which fail the most people.",
         stack="PYTHON · SQL · POWER BI · DAX · STREAMLIT",
         metric="16.2B", label="UPI TRANSACTIONS COVERED",
         note="59 banks · Jan 2022 to Nov 2024 · NPCI published statistics",
         repo="upi-reliability-intelligence"),
]


def mini_aml(t, x0, y0):
    pts = [(x0 + i * 52, y0 + (10 if i % 2 else -10)) for i in range(5)]
    path = " ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(pts))
    back = f"M {pts[-1][0]} {pts[-1][1]} Q {(pts[0][0] + pts[-1][0]) / 2} {y0 + 52} {pts[0][0]} {pts[0][1]}"
    o = [f'<path d="{path}" fill="none" stroke="{t["faint"]}" stroke-width="1.3"/>',
         f'<path d="{back}" fill="none" stroke="{t["accent"]}" stroke-width="1.4" stroke-dasharray="4 4">'
         f'<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.2s" repeatCount="indefinite"/></path>']
    for x, y in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{t["card"]}" stroke="{t["ink"]}" stroke-width="1.3"/>')
    o.append(f'<circle r="3" fill="{t["accent"]}"><animateMotion dur="4s" repeatCount="indefinite" path="{path} {back[back.index("Q"):]}"/></circle>')
    return "".join(o)


def mini_recon(t, x0, y0):
    cols = [("BOOKS", x0), ("GATEWAY", x0 + 104), ("BANK", x0 + 208)]
    o = []
    for name, x in cols:
        o.append(f'<text class="mono" x="{x}" y="{y0 - 14}" font-size="9.5" letter-spacing="1" '
                 f'text-anchor="middle" fill="{t["faint"]}">{name}</text>')
    for r in range(4):
        y = y0 + r * 13
        gap = r == 2
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + 104}" y2="{y}" stroke="{t["faint"]}" stroke-opacity=".6"/>')
        o.append(f'<line x1="{x0 + 104}" y1="{y}" x2="{x0 + 208 - (60 if gap else 0)}" y2="{y}" '
                 f'stroke="{t["accent"] if gap else t["faint"]}" stroke-opacity="{1 if gap else .6}" {"stroke-dasharray=\"3 3\"" if gap else ""}/>')
        for _, x in cols[: 2 if gap else 3]:
            o.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{t["ink"]}"/>')
        if gap:
            o.append(f'<text class="mono blink" x="{x0 + 208}" y="{y + 4}" font-size="12" text-anchor="middle" '
                     f'fill="{t["accent"]}">×</text>')
        else:
            o.append(f'<circle r="2.2" fill="{t["up"]}"><animateMotion dur="2.6s" begin="-{r * .5}s" '
                     f'repeatCount="indefinite" path="M {x0} {y} L {x0 + 208} {y}"/></circle>')
    return "".join(o)


def mini_upi(t, x0, y0):
    rates = [1.1, 0.8, 1.6, 0.9, 2.3, 1.2, 0.7, 5.9, 1.4, 0.6, 1.0, 1.8, 0.9, 0.57]
    o = []
    for i, r in enumerate(rates):
        h = 6 + r * 9
        x = x0 + i * 17
        hot = r == 5.9
        sbi = r == 0.57
        col = t["accent"] if hot else (t["ink"] if sbi else t["edge"])
        o.append(f'<rect x="{x}" y="{y0 + 58 - h}" width="10" height="{h}" fill="{col}">'
                 f'<animate attributeName="height" values="0;{h}" dur=".9s" begin="{i * .05:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="y" values="{y0 + 58};{y0 + 58 - h}" dur=".9s" begin="{i * .05:.2f}s" fill="freeze"/></rect>')
    o.append(f'<text class="mono" x="{x0 + 7 * 17 + 5}" y="{y0 - 3}" font-size="9.5" text-anchor="middle" fill="{t["accent"]}">5.89%</text>')
    o.append(f'<text class="mono" x="{x0 + 13 * 17 + 5}" y="{y0 + 40}" font-size="9.5" text-anchor="middle" fill="{t["ink"]}">SBI</text>')
    return "".join(o)


MINI = {"aml": mini_aml, "recon": mini_recon, "upi": mini_upi}


def card(t, p):
    W, H = 1200, 290
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="{p["title"]}: {p["tagline"]}">',
         "<defs>" + base_style(t) + "</defs>",
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>',
         f'<line x1="760" x2="760" y1="36" y2="{H - 36}" stroke="{t["border"]}"/>',
         # left column
         f'<text class="mono" x="48" y="62" font-size="12.5" letter-spacing="2" fill="{t["faint"]}">'
         f'{p["index"]}  <tspan fill="{t["muted"]}">/ github.com/Amaann190/{p["repo"]}</tspan></text>',
         f'<g class="rise"><text class="serif" x="46" y="128" font-size="42" fill="{t["ink"]}" letter-spacing="-.5">{p["title"]}</text></g>',
         f'<g class="rise" style="animation-delay:.15s"><text class="serif" x="48" y="166" font-size="23" font-style="italic" '
         f'fill="{t["muted"]}">{p["tagline"]}</text></g>',
         f'<text class="sans" x="48" y="212" font-size="14.5" fill="{t["faint"]}">{p["note"]}</text>',
         f'<text class="mono" x="48" y="252" font-size="11.5" letter-spacing="1.6" fill="{t["muted"]}">{p["stack"]}</text>',
         # right column
         f'<text class="serif" x="1152" y="118" font-size="78" text-anchor="end" fill="{t["ink"]}" letter-spacing="-1">{p["metric"]}</text>',
         f'<text class="mono" x="1152" y="146" font-size="11" letter-spacing="1.6" text-anchor="end" fill="{t["muted"]}">{p["label"]}</text>',
         MINI[p["slug"]](t, 900 if p["slug"] != "upi" else 912, 196),
         f'<rect width="{W}" height="{H}" rx="16" filter="url(#grain)" pointer-events="none"/>',
         "</svg>"]
    return "\n".join(o)


if __name__ == "__main__":
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f"{p['slug']}-{name}.svg").write_text(card(t, p), encoding="utf-8")
    print("wrote", sorted(f.name for f in OUT.glob("*.svg")))
