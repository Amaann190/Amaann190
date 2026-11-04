"""Builds every SVG used by the profile README.

Run:  python tools/make_svgs.py
All copy and numbers live in the CONFIG section below. Edit, re-run, commit.
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ CONFIG
C = dict(bg="#07080a", panel="#0c0d10", border="#1c1e23", ink="#f2f1ec", muted="#8d8c86",
         faint="#55565b", edge="#24262c", accent="#ff5f3a", up="#3ee08f")

SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
SANS = "'Inter Tight', 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"

TICKER = [
    ("AML", "▲ 415×", "precision lift"), ("RECON", "₹25.4L", "gaps traced"),
    ("UPI", "16.2B", "txns covered"), ("TESTS", "64+", "passing"),
    ("RECON", "10,000/10,000", "orders matched"), ("AML", "5.08M", "transfers scanned"),
    ("QUEUE", "▲ 37→57%", "top-100 precision"),
]

LOG = [  # lines that cycle under the name
    ("scan", "5.08M transfers · 515K accounts"),
    ("hit ", "AC-4471 → AC-2208 → AC-9035 → AC-6610 → AC-5524 → AC-4471"),
    ("send", "5-hop cycle, closed in 3 days → analyst queue, priority 1"),
]

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

PIPELINE = [("Inspect", "pandas · SQL"), ("Clean", "Python · pytest"), ("Model", "NetworkX · SQLite"),
            ("Verify", "pytest · ground truth"), ("Ship", "Power BI · Streamlit")]


# ------------------------------------------------------------------ helpers
def defs(extra=""):
    return f"""<defs>
  <style>
    .serif {{ font-family: {SERIF}; }}
    .sans  {{ font-family: {SANS}; }}
    .mono  {{ font-family: {MONO}; }}
    .blink {{ animation: blink 1.1s step-end infinite; }}
    .breathe {{ animation: breathe 3s ease-in-out infinite; }}
    @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
    @keyframes breathe {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .35 }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .045 0"/>
  </filter>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-opacity=".035"/>
  </pattern>
  {extra}
</defs>"""


def frame(W, H, body, extra_defs="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">\n{defs(extra_defs)}\n'
            f'<clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>\n'
            f'<g clip-path="url(#round)">\n<rect width="{W}" height="{H}" fill="{C["bg"]}"/>\n'
            f'{body}\n<rect width="{W}" height="{H}" filter="url(#grain)"/>\n</g>\n'
            f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{C["border"]}"/>\n</svg>')


_uid = [0]


def odometer(x_right, y, text, fs, family, fill, dur=10, begin=0.0, weight="400", glow=False):
    """Digits roll into place, hold, then roll again. Static fallback = the final value."""
    _uid[0] += 1
    cid = f"odo{_uid[0]}"
    cw = fs * (0.6 if family == MONO else 0.56)
    L = fs * 1.2

    def w(ch):
        return cw if ch.isdigit() else (cw * .45 if ch in ".,:" else cw * 1.05)

    total = sum(w(ch) for ch in text)
    x = x_right - total
    glow_attr = ' filter="url(#glow)"' if glow else ""
    out = [f'<clipPath id="{cid}"><rect x="{x - 8:.1f}" y="{y - fs * .92:.1f}" width="{total + 16:.1f}" '
           f'height="{fs * 1.18:.1f}"/></clipPath>',
           f'<g clip-path="url(#{cid})"><g font-family="{family}" font-size="{fs}" font-weight="{weight}" '
           f'fill="{fill}"{glow_attr}>']
    n = 0
    for ch in text:
        cx = x + w(ch) / 2
        if ch.isdigit():
            d = int(ch)
            F = (10 + d) * L
            k = min(.12 + n * .035, .4)
            out.append(f'<g transform="translate(0 -{F:.1f})"><animateTransform attributeName="transform" '
                       f'type="translate" values="0 0;0 -{F:.1f};0 -{F:.1f}" keyTimes="0;{k:.3f};1" '
                       f'calcMode="spline" keySplines=".2 .75 .25 1;0 0 1 1" dur="{dur}s" begin="{begin}s" '
                       f'repeatCount="indefinite"/>')
            for j in range(20):
                out.append(f'<text x="{cx:.1f}" y="{y + j * L:.1f}" text-anchor="middle">{j % 10}</text>')
            out.append('</g>')
            n += 1
        else:
            out.append(f'<text x="{cx:.1f}" y="{y}" text-anchor="middle">{ch}</text>')
        x += w(ch)
    out.append('</g></g>')
    return "".join(out)


FADES = f"""<linearGradient id="fadeL"><stop offset="0" stop-color="{C['panel']}"/><stop offset="1" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>
  <linearGradient id="fadeR"><stop offset="0" stop-color="{C['panel']}" stop-opacity="0"/><stop offset="1" stop-color="{C['panel']}"/></linearGradient>"""


def ticker(y0, W):
    o = [f'<rect x="0" y="{y0}" width="{W}" height="64" fill="{C["panel"]}"/>',
         f'<line x1="0" x2="{W}" y1="{y0}" y2="{y0}" stroke="{C["border"]}"/>']
    step, span = 360, 360 * len(TICKER)
    o.append(f'<g><animateTransform attributeName="transform" type="translate" from="0 0" to="-{span} 0" '
             f'dur="{len(TICKER) * 6}s" repeatCount="indefinite"/>')
    for rep in range(3):
        for i, (tag, val, lab) in enumerate(TICKER):
            x = 40 + rep * span + i * step
            col = C["up"] if "▲" in val else C["ink"]
            o.append(f'<text class="mono" x="{x}" y="{y0 + 38}" font-size="14" letter-spacing=".6">'
                     f'<tspan fill="{C["faint"]}">{tag}</tspan><tspan dx="10" fill="{col}" font-weight="700">{val}</tspan>'
                     f'<tspan dx="10" fill="{C["muted"]}">{lab}</tspan></text>'
                     f'<text class="mono" x="{x + step - 28}" y="{y0 + 38}" font-size="14" fill="{C["edge"]}">/</text>')
    o.append('</g>')
    o.append(f'<rect x="0" y="{y0 + 1}" width="120" height="63" fill="url(#fadeL)"/>'
             f'<rect x="{W - 120}" y="{y0 + 1}" width="120" height="63" fill="url(#fadeR)"/>')
    return "\n".join(o)


# ------------------------------------------------------------------ hero
NODES = {
    0: (690, 132, "AC-0193"), 1: (806, 92, "AC-3307"), 2: (934, 122, "AC-4471"), 3: (1062, 92, "AC-2208"),
    4: (1140, 186, "AC-9035"), 5: (1104, 300, "AC-6610"), 6: (988, 350, "AC-8142"), 7: (858, 392, "AC-1162"),
    8: (734, 334, "AC-7310"), 9: (668, 236, "AC-2051"), 10: (846, 232, "AC-0774"), 11: (998, 226, "AC-5524"),
    12: (1150, 392, "AC-3961"),
}
EDGES = [(0, 1), (1, 2), (0, 9), (9, 8), (8, 7), (7, 6), (6, 5), (1, 10), (10, 11), (9, 10), (10, 8),
         (10, 7), (11, 6), (6, 12), (5, 12), (0, 10)]
CYCLE = [2, 3, 4, 5, 11, 2]
SCAN_DUR = 7


def hero():
    W, H = 1200, 520
    p = lambda n: NODES[n][:2]
    cyc = " ".join(("M" if i == 0 else "L") + f" {p(n)[0]} {p(n)[1]}" for i, n in enumerate(CYCLE))
    detect = f'values="0;0;1;1;0" keyTimes="0;.6;.64;.94;1" dur="{SCAN_DUR}s" repeatCount="indefinite"'
    g = f"""<radialGradient id="halo" cx="930" cy="240" r="420" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{C['accent']}" stop-opacity=".16"/><stop offset=".55" stop-color="{C['accent']}" stop-opacity=".04"/>
    <stop offset="1" stop-color="{C['accent']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="halo2" cx="160" cy="90" r="520" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".06"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
  <linearGradient id="shine" x1="-700" y1="0" x2="0" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{C['ink']}"/><stop offset=".45" stop-color="{C['ink']}"/>
    <stop offset=".5" stop-color="#ffffff"/><stop offset=".53" stop-color="{C['accent']}"/>
    <stop offset=".58" stop-color="{C['ink']}"/><stop offset="1" stop-color="{C['ink']}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1400 0;1400 0" keyTimes="0;.45;1" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="trail"><stop offset="0" stop-color="{C['accent']}" stop-opacity="0"/><stop offset="1" stop-color="{C['accent']}" stop-opacity=".22"/></linearGradient>
  {FADES}"""
    o = [f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#halo2)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#halo)"/>']

    o.append(f'<text class="mono" x="64" y="62" font-size="12.5" letter-spacing="2.6" fill="{C["muted"]}">'
             f'FINTECH DATA ANALYST  <tspan fill="{C["faint"]}">/</tspan>  PAYMENTS · RECONCILIATION · AML  '
             f'<tspan fill="{C["faint"]}">/</tspan>  INDIA</text>')
    o.append(f'<circle cx="{W - 300}" cy="58" r="9" fill="{C["up"]}" opacity=".18" class="breathe"/>'
             f'<circle cx="{W - 300}" cy="58" r="4" fill="{C["up"]}"/>'
             f'<text class="mono" x="{W - 64}" y="62" font-size="12.5" letter-spacing="1.2" text-anchor="end" '
             f'fill="{C["ink"]}">open to analyst internships</text>')

    for u, v in EDGES:
        (x1, y1), (x2, y2) = p(u), p(v)
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C["edge"]}" stroke-width="1.2"/>')
    o.append(f'<path d="{cyc}" fill="none" stroke="{C["edge"]}" stroke-width="1.2"/>')
    # detected cycle (appears once the scan line has passed it)
    o.append(f'<g opacity="0"><animate attributeName="opacity" {detect}/>'
             f'<path d="{cyc}" fill="{C["accent"]}" fill-opacity=".06" stroke="{C["accent"]}" stroke-width="2.2" '
             f'stroke-dasharray="6 6" filter="url(#glow)"><animate attributeName="stroke-dashoffset" from="0" to="-48" dur="1.1s" repeatCount="indefinite"/></path>')
    for nd in CYCLE[:-1]:
        x, y = p(nd)
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{C["accent"]}">'
                 f'<animate attributeName="r" values="8;26" dur="1.4s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".8;0" dur="1.4s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="914" y="410" width="214" height="28" rx="5" fill="{C["bg"]}" stroke="{C["accent"]}"/>'
             f'<text class="mono" x="1021" y="428.5" font-size="11.5" font-weight="700" text-anchor="middle" '
             f'fill="{C["accent"]}" letter-spacing="1.4">CYCLE DETECTED · 5 HOPS</text></g>')
    rnd = random.Random(7)
    for i, (u, v) in enumerate(EDGES):
        (x1, y1), (x2, y2) = p(u), p(v)
        if i % 2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        d = rnd.uniform(2.2, 4.2)
        o.append(f'<circle r="2.4" fill="{C["ink"]}" opacity=".7"><animateMotion dur="{d:.1f}s" '
                 f'begin="-{rnd.uniform(0, d):.2f}s" repeatCount="indefinite" path="M {x1} {y1} L {x2} {y2}"/></circle>')
    for k in range(4):
        o.append(f'<circle r="3.6" fill="{C["accent"]}" filter="url(#glow)"><animateMotion dur="6s" '
                 f'begin="-{k * 1.5}s" repeatCount="indefinite" path="{cyc}"/></circle>')
    for key, (x, y, label) in NODES.items():
        hot = key in CYCLE
        o.append(f'<circle cx="{x}" cy="{y}" r="{7 if hot else 5}" fill="{C["bg"]}" '
                 f'stroke="{C["ink"] if hot else C["faint"]}" stroke-width="1.5"/>')
        if hot:
            o.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{C["accent"]}" opacity="0"><animate attributeName="opacity" {detect}/></circle>')
        dy = -15 if y < 200 else 25
        o.append(f'<text class="mono" x="{x}" y="{y + dy}" font-size="10" text-anchor="middle" '
                 f'fill="{C["faint"]}" letter-spacing=".6">{label}</text>')
    # scan line
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="610 0;1210 0" '
             f'dur="{SCAN_DUR}s" repeatCount="indefinite"/>'
             f'<rect x="-120" y="72" width="120" height="356" fill="url(#trail)"/>'
             f'<rect x="-1" y="72" width="2" height="356" fill="{C["accent"]}" filter="url(#glow)"/>'
             f'<text class="mono" x="-8" y="86" font-size="9.5" fill="{C["accent"]}" text-anchor="end" letter-spacing="1">SCAN</text></g>')

    o.append(f'<text class="serif" x="58" y="232" font-size="136" fill="url(#shine)" letter-spacing="-3">Amaan</text>')
    o.append(f'<text class="serif" x="58" y="352" font-size="136" font-style="italic" fill="url(#shine)" '
             f'letter-spacing="-3">Shaikh<tspan fill="{C["accent"]}">.</tspan></text>')
    n = len(LOG)
    for i, (tag, msg) in enumerate(LOG):
        a, b = i / n, (i + 1) / n
        if i == 0:
            vals, kt = "1;1;0;0", f"0;{b - .02:.3f};{b:.3f};1"
        else:
            vals, kt = "0;0;1;1;0;0", f"0;{a:.3f};{a + .02:.3f};{b - .02:.3f};{min(b, .999):.3f};1"
        col = C["accent"] if tag.strip() == "hit" else C["up"]
        o.append(f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="9s" repeatCount="indefinite"/>'
                 f'<text class="mono" x="64" y="414" font-size="14.5" fill="{C["muted"]}" xml:space="preserve">'
                 f'<tspan fill="{col}">›</tspan> <tspan fill="{col}" font-weight="700">{tag}</tspan>  '
                 f'<tspan fill="{C["ink"]}">{msg}</tspan><tspan class="blink" fill="{C["accent"]}"> ▍</tspan></text></g>')
    o.append(ticker(456, W))
    return frame(W, H, "\n".join(o), g, "Amaan Shaikh, fintech data analyst")


# ------------------------------------------------------------------ live monitor
def monitor():
    W, H = 1200, 400
    rnd = random.Random(42)
    rows = []
    flags = {2: "CYCLE", 7: "FAN-IN", 10: "CYCLE"}
    for i in range(12):
        t = f"{9 + i // 5:02d}:{rnd.randint(0, 59):02d}:{rnd.randint(0, 59):02d}"
        a, b = rnd.randint(1000, 9999), rnd.randint(1000, 9999)
        amt = f"{rnd.choice([1, 2, 4, 9, 12, 48, 75]) * rnd.randint(1000, 9000):,}.00"
        rows.append((t, f"AC-{a}", f"AC-{b}", amt, flags.get(i)))
    RH, top, n = 34, 104, len(rows)
    g = f"""<clipPath id="feed"><rect x="40" y="{top - 4}" width="690" height="268"/></clipPath>
  <linearGradient id="vfadeT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['bg']}"/><stop offset="1" stop-color="{C['bg']}" stop-opacity="0"/></linearGradient>
  <linearGradient id="vfadeB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{C['bg']}"/></linearGradient>
  <radialGradient id="mhalo" cx="980" cy="200" r="330" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{C['accent']}" stop-opacity=".09"/><stop offset="1" stop-color="{C['accent']}" stop-opacity="0"/></radialGradient>"""
    o = [f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', f'<rect width="{W}" height="{H}" fill="url(#mhalo)"/>',
         f'<circle cx="52" cy="52" r="8" fill="{C["accent"]}" opacity=".25" class="breathe"/><circle cx="52" cy="52" r="3.6" fill="{C["accent"]}"/>',
         f'<text class="mono" x="70" y="56.5" font-size="12.5" font-weight="700" letter-spacing="2.4" fill="{C["ink"]}">LIVE  '
         f'<tspan fill="{C["muted"]}" font-weight="400">TRANSACTION MONITOR</tspan></text>',
         f'<text class="mono" x="{W - 40}" y="56.5" font-size="11" letter-spacing="1.2" text-anchor="end" fill="{C["faint"]}">'
         f'simulated feed · detectors from aml-graph-intelligence</text>',
         f'<line x1="40" x2="{W - 40}" y1="76" y2="76" stroke="{C["border"]}"/>',
         f'<line x1="770" x2="770" y1="100" y2="{H - 36}" stroke="{C["border"]}"/>']
    for name, x, anchor in [("TIME", 44, "start"), ("FROM", 150, "start"), ("TO", 290, "start"),
                            ("AMOUNT ₹", 560, "end"), ("SIGNAL", 650, "start")]:
        o.append(f'<text class="mono" x="{x}" y="96" font-size="10" letter-spacing="1.6" fill="{C["faint"]}" text-anchor="{anchor}">{name}</text>')
    o.append(f'<g clip-path="url(#feed)"><g><animateTransform attributeName="transform" type="translate" '
             f'from="0 0" to="0 -{RH * n}" dur="{n * 2.2:.1f}s" repeatCount="indefinite"/>')
    for rep in range(2):
        for i, (t, a, b, amt, tag) in enumerate(rows):
            y = top + 22 + (rep * n + i) * RH
            if tag:
                o.append(f'<rect x="40" y="{y - 22}" width="690" height="{RH - 4}" rx="5" fill="{C["accent"]}" '
                         f'fill-opacity=".08" stroke="{C["accent"]}" stroke-opacity=".35"/>')
            ink = C["ink"] if tag else C["muted"]
            o.append(f'<text class="mono" font-size="13" y="{y}" fill="{ink}">'
                     f'<tspan x="44" fill="{C["faint"]}">{t}</tspan><tspan x="150">{a}</tspan>'
                     f'<tspan x="250" fill="{C["faint"]}">→</tspan><tspan x="290">{b}</tspan></text>'
                     f'<text class="mono" font-size="13" x="560" y="{y}" text-anchor="end" fill="{ink}">{amt}</text>')
            if tag:
                o.append(f'<text class="mono" font-size="11.5" x="650" y="{y}" font-weight="700" fill="{C["accent"]}" '
                         f'letter-spacing="1.2" filter="url(#glow)">● {tag}</text>')
            else:
                o.append(f'<text class="mono" font-size="11.5" x="650" y="{y}" fill="{C["faint"]}" letter-spacing="1.2">· ok</text>')
    o.append('</g></g>')
    o.append(f'<rect x="40" y="{top - 4}" width="690" height="40" fill="url(#vfadeT)"/>'
             f'<rect x="40" y="{top + 224}" width="690" height="40" fill="url(#vfadeB)"/>')
    stats = [("5.08M", "TRANSFERS SCANNED", C["ink"]), ("42.3%", "PRECISION ON GRAPH PATTERNS", C["accent"]),
             ("57%", "TOP-100 QUEUE PRECISION · WAS 37%", C["up"])]
    for i, (val, lab, col) in enumerate(stats):
        y = 150 + i * 88
        o.append(odometer(W - 48, y, val, 48, MONO, col, dur=9, begin=i * .3, weight="700", glow=col != C["ink"]))
        o.append(f'<text class="mono" x="{W - 48}" y="{y + 24}" font-size="10.5" letter-spacing="1.6" text-anchor="end" fill="{C["muted"]}">{lab}</text>')
    return frame(W, H, "\n".join(o), g, "Simulated transaction monitor flagging cycles and fan-in patterns")


# ------------------------------------------------------------------ project cards
def mini_aml(x0, y0):
    pts = [(x0 + i * 56, y0 + (12 if i % 2 else -12)) for i in range(5)]
    path = " ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(pts))
    back = f"Q {(pts[0][0] + pts[-1][0]) / 2} {y0 + 62} {pts[0][0]} {pts[0][1]}"
    o = [f'<path d="{path}" fill="none" stroke="{C["faint"]}" stroke-width="1.3"/>',
         f'<path d="M {pts[-1][0]} {pts[-1][1]} {back}" fill="none" stroke="{C["accent"]}" stroke-width="1.6" '
         f'stroke-dasharray="5 5" filter="url(#glow)"><animate attributeName="stroke-dashoffset" from="0" to="-40" dur="1.1s" repeatCount="indefinite"/></path>']
    for x, y in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{C["bg"]}" stroke="{C["ink"]}" stroke-width="1.4"/>')
    for k in range(2):
        o.append(f'<circle r="3.4" fill="{C["accent"]}" filter="url(#glow)"><animateMotion dur="4s" begin="-{k * 2}s" '
                 f'repeatCount="indefinite" path="{path} {back}"/></circle>')
    return "".join(o)


def mini_recon(x0, y0):
    cols = [("BOOKS", x0), ("GATEWAY", x0 + 112), ("BANK", x0 + 224)]
    o = [f'<text class="mono" x="{x}" y="{y0 - 16}" font-size="9.5" letter-spacing="1.2" text-anchor="middle" '
         f'fill="{C["faint"]}">{name}</text>' for name, x in cols]
    for r in range(4):
        y = y0 + r * 14
        gap = r == 2
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + 112}" y2="{y}" stroke="{C["faint"]}" stroke-opacity=".6"/>')
        if gap:
            o.append(f'<line x1="{x0 + 112}" y1="{y}" x2="{x0 + 190}" y2="{y}" stroke="{C["accent"]}" stroke-dasharray="3 3"/>'
                     f'<text class="mono breathe" x="{x0 + 224}" y="{y + 4.5}" font-size="14" font-weight="700" '
                     f'text-anchor="middle" fill="{C["accent"]}" filter="url(#glow)">×</text>')
        else:
            o.append(f'<line x1="{x0 + 112}" y1="{y}" x2="{x0 + 224}" y2="{y}" stroke="{C["faint"]}" stroke-opacity=".6"/>')
        for _, x in cols[: 2 if gap else 3]:
            o.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{C["ink"]}"/>')
        if not gap:
            o.append(f'<circle r="2.4" fill="{C["up"]}" filter="url(#glow)"><animateMotion dur="2.6s" begin="-{r * .6}s" '
                     f'repeatCount="indefinite" path="M {x0} {y} L {x0 + 224} {y}"/></circle>')
    return "".join(o)


def mini_upi(x0, y0):
    rates = [1.1, 0.8, 1.6, 0.9, 2.3, 1.2, 0.7, 5.9, 1.4, 0.6, 1.0, 1.8, 0.9, 0.57]
    o = []
    for i, r in enumerate(rates):
        h = 6 + r * 9
        x = x0 + i * 17
        col = C["accent"] if r == 5.9 else (C["ink"] if r == 0.57 else C["edge"])
        f = ' filter="url(#glow)"' if r == 5.9 else ""
        o.append(f'<rect x="{x}" y="{y0 + 58 - h}" width="10" height="{h}" rx="1.5" fill="{col}"{f}>'
                 f'<animate attributeName="height" values="0;{h};{h}" keyTimes="0;.12;1" dur="8s" begin="{i * .05:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{y0 + 58};{y0 + 58 - h};{y0 + 58 - h}" keyTimes="0;.12;1" dur="8s" begin="{i * .05:.2f}s" repeatCount="indefinite"/></rect>')
    o.append(f'<text class="mono" x="{x0 + 7 * 17 + 5}" y="{y0 - 4}" font-size="9.5" text-anchor="middle" fill="{C["accent"]}">5.89%</text>'
             f'<text class="mono" x="{x0 + 13 * 17 + 5}" y="{y0 + 40}" font-size="9.5" text-anchor="middle" fill="{C["ink"]}">SBI</text>')
    return "".join(o)


MINI = {"aml": (mini_aml, 920, 214), "recon": (mini_recon, 912, 222), "upi": (mini_upi, 916, 196)}


def card(p, i):
    W, H = 1200, 300
    g = f"""<radialGradient id="chalo" cx="1060" cy="110" r="300" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{C['accent']}" stop-opacity=".13"/><stop offset="1" stop-color="{C['accent']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['accent']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{C['accent']}"/><stop offset="1" stop-color="{C['accent']}" stop-opacity="0"/></linearGradient>"""
    fn, mx, my = MINI[p["slug"]]
    o = [f'<rect width="{W}" height="{H}" fill="url(#grid)"/>', f'<rect width="{W}" height="{H}" fill="url(#chalo)"/>',
         f'<rect x="-320" y="0" width="320" height="1.5" fill="url(#sweep)"><animate attributeName="x" values="-320;1200;1200" '
         f'keyTimes="0;.5;1" dur="8s" begin="{i * 1.2}s" repeatCount="indefinite"/></rect>',
         f'<line x1="770" x2="770" y1="40" y2="{H - 40}" stroke="{C["border"]}"/>',
         f'<text class="mono" x="48" y="62" font-size="12.5" letter-spacing="2" fill="{C["accent"]}">{p["index"]}'
         f'<tspan fill="{C["faint"]}">  /  </tspan><tspan fill="{C["muted"]}">github.com/Amaann190/{p["repo"]}</tspan>'
         f'<tspan fill="{C["accent"]}">  ↗</tspan></text>',
         f'<text class="serif" x="46" y="130" font-size="44" fill="{C["ink"]}" letter-spacing="-.5">{p["title"]}</text>',
         f'<text class="serif" x="48" y="170" font-size="23" font-style="italic" fill="{C["muted"]}">{p["tagline"]}</text>',
         f'<text class="sans" x="48" y="216" font-size="14.5" fill="{C["faint"]}">{p["note"]}</text>',
         f'<text class="mono" x="48" y="256" font-size="11.5" letter-spacing="1.6" fill="{C["muted"]}">{p["stack"]}</text>',
         odometer(1152, 124, p["metric"], 80, SANS, C["ink"], dur=10, begin=i * .4, weight="300"),
         f'<text class="mono" x="1152" y="154" font-size="11" letter-spacing="1.6" text-anchor="end" fill="{C["muted"]}">{p["label"]}</text>',
         fn(mx, my)]
    return frame(W, H, "\n".join(o), g, f'{p["title"]}: {p["tagline"]}')


# ------------------------------------------------------------------ pipeline
def pipeline():
    W, H = 1200, 210
    n, D = len(PIPELINE), 10
    x0, x1, y = 120, 1080, 96
    gap = (x1 - x0) / (n - 1)
    o = [f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="{C["edge"]}" stroke-width="2"/>',
         f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="{C["accent"]}" stroke-width="2" stroke-dasharray="{x1 - x0}" '
         f'stroke-dashoffset="{x1 - x0}" filter="url(#glow)"><animate attributeName="stroke-dashoffset" '
         f'values="{x1 - x0};0;0;{x1 - x0}" keyTimes="0;.8;.92;1" dur="{D}s" repeatCount="indefinite"/></line>']
    for i, (name, tools) in enumerate(PIPELINE):
        x = x0 + i * gap
        t = .8 * i / (n - 1)
        on = f'values="0;0;1;1;0" keyTimes="0;{max(t, .001):.3f};{t + .02:.3f};.92;1" dur="{D}s" repeatCount="indefinite"'
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{C["bg"]}" stroke="{C["faint"]}" stroke-width="1.5"/>')
        o.append(f'<g opacity="0"><animate attributeName="opacity" {on}/>'
                 f'<circle cx="{x}" cy="{y}" r="11" fill="{C["bg"]}" stroke="{C["accent"]}" stroke-width="2" filter="url(#glow)"/>'
                 f'<circle cx="{x}" cy="{y}" r="4" fill="{C["accent"]}"/></g>')
        o.append(f'<text class="mono" x="{x}" y="{y - 28}" font-size="10.5" letter-spacing="1.6" text-anchor="middle" fill="{C["faint"]}">0{i + 1}</text>'
                 f'<text class="serif" x="{x}" y="{y + 52}" font-size="30" text-anchor="middle" fill="{C["ink"]}">{name}</text>'
                 f'<text class="mono" x="{x}" y="{y + 76}" font-size="11" letter-spacing="1" text-anchor="middle" fill="{C["muted"]}">{tools}</text>')
    o.append(f'<circle r="5" fill="#fff" filter="url(#glow)"><animateMotion path="M {x0} {y} L {x1} {y}" '
             f'keyPoints="0;1;1;0" keyTimes="0;.8;.92;1" calcMode="linear" dur="{D}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.8;.86;1" dur="{D}s" repeatCount="indefinite"/></circle>')
    return frame(W, H, "\n".join(o), "", "Inspect, clean, model, verify, ship")


if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        old.unlink()
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "monitor.svg").write_text(monitor(), encoding="utf-8")
    (OUT / "pipeline.svg").write_text(pipeline(), encoding="utf-8")
    for i, p in enumerate(PROJECTS):
        (OUT / f"card-{p['slug']}.svg").write_text(card(p, i), encoding="utf-8")
    print("wrote", sorted(f.name for f in OUT.glob("*.svg")))
