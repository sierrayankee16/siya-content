"""SIYA Media Slide-Renderer.

Aufruf: python3 tools/render.py <spec.json>

Spec:
{
  "out": "ordnername",            # Ausgabe relativ zu tools/
  "size": "post" | "story",       # post = 1080x1350, story = 1080x1920
  "theme": "dark",                # Standard-Stil fuer alle Slides
  "tag": "INSIDER",               # Text oben rechts (leer = nur Zaehler)
  "foot": true,                   # Fusszeile an/aus
  "slides": [ "<html>", {"theme": "accent", "html": "<html>", "align": "top|center|bottom"} ]
}

Stile (ab 08.10.2026 nur noch siya / siyalight verwenden):
  siya      Navy #070718 wie die Website, Tuerkis #59BFAC als Akzent, kraeftiger Lichtschein
  siyalight Hell #F6F7FA, Navy-Schrift, Tuerkis #2E8F7E
  (alt) dark   Navy mit Raster (Website-Look)
  light  Hellgrau mit Raster
  accent Volle Tuerkis-Flaeche, Navy-Schrift
  paper  Warmes Papier, keine Raster, ruhig
  ink    Tiefschwarz, keine Raster, viel Kontrast

Bausteine (CSS-Klassen): label, h1, h2, h3, t (Akzentfarbe), hl (Marker),
p, card, row/num/rowt, flow/node/link(.bad), big, chip, chipfill, src, mono,
phone (Handy-Rahmen) mit chat/bin/bout (Chat-Blasen), note (Notizzettel),
quote, stamp, split/half (Vorher/Nachher), tick/cross (Listenpunkte).
Neu: cta (Button "Erstgespraech vereinbaren"), pill (Rahmen-Label wie auf der Website),
badge (gefuelltes Label), ui (UI-Karte) mit uih (Kopfzeile), tl/step (Ablauf mit Punkten).
"""
import base64, sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
def b64(n): return "data:image/png;base64," + base64.b64encode((ROOT / n).read_bytes()).decode()
LOGO_LIGHTTEXT = b64("logo_c.png")      # weisse Schrift
LOGO_DARKTEXT = b64("logo_dark.png")    # navy Schrift

THEMES = {
    "siya":  {"bg": "#070718", "fg": "#FFFFFF", "sub": "#CDD0E0", "acc": "#59BFAC", "line": "rgba(205,208,224,.14)", "grid": "rgba(255,255,255,.03)", "card": "rgba(16,18,42,.88)", "logo": LOGO_LIGHTTEXT, "glow": "siya"},
    "siyalight": {"bg": "#F6F7FA", "fg": "#070718", "sub": "#4A4D63", "acc": "#2E8F7E", "line": "rgba(7,7,24,.1)", "grid": "rgba(7,7,24,.035)", "card": "#FFFFFF", "logo": LOGO_DARKTEXT, "glow": "siyalight"},
 "dark":   {"bg": "#070718", "fg": "#FFFFFF", "sub": "#CDD0E0", "acc": "#59BFAC", "line": "rgba(205,208,224,.14)", "grid": "rgba(255,255,255,.035)", "card": "rgba(20,22,48,.75)", "logo": LOGO_LIGHTTEXT, "glow": True},
 "light":  {"bg": "#F6F7FA", "fg": "#0B0B1F", "sub": "#4A4D63", "acc": "#2E8F7E", "line": "rgba(11,11,31,.1)", "grid": "rgba(11,11,31,.045)", "card": "#FFFFFF", "logo": LOGO_DARKTEXT, "glow": False},
 "accent": {"bg": "#59BFAC", "fg": "#070718", "sub": "#0E2E2A", "acc": "#FFFFFF", "line": "rgba(7,7,24,.18)", "grid": "rgba(7,7,24,.06)", "card": "rgba(255,255,255,.9)", "logo": LOGO_DARKTEXT, "glow": False},
 "paper":  {"bg": "#EFEBE3", "fg": "#14141F", "sub": "#55535C", "acc": "#2E8F7E", "line": "rgba(20,20,31,.14)", "grid": None, "card": "#FBF9F5", "logo": LOGO_DARKTEXT, "glow": False},
 "brand":  {"bg": "#04050D", "fg": "#FFFFFF", "sub": "#B7BCD6", "acc": "#22D3EE", "line": "rgba(120,170,255,.18)", "grid": None, "card": "rgba(16,24,58,.55)", "logo": LOGO_LIGHTTEXT, "glow": "brand"},
 "brandlight": {"bg": "#F4F7FF", "fg": "#06081A", "sub": "#4A5070", "acc": "#1663F0", "line": "rgba(6,8,26,.1)", "grid": None, "card": "#FFFFFF", "logo": LOGO_DARKTEXT, "glow": "brandlight"},
 "ink":    {"bg": "#000000", "fg": "#FFFFFF", "sub": "#A9ABB8", "acc": "#59BFAC", "line": "rgba(255,255,255,.14)", "grid": None, "card": "#111114", "logo": LOGO_LIGHTTEXT, "glow": False},
}

def css(t, w, h, story):
    pad_top = 250 if story else 92
    pad_bot = 300 if story else 0
    grid = f"background-image:linear-gradient({t['grid']} 1px,transparent 1px),linear-gradient(90deg,{t['grid']} 1px,transparent 1px);background-size:108px 108px;" if t["grid"] else ""
    glow = ".s:after{content:'';position:absolute;width:900px;height:900px;right:-300px;bottom:-320px;background:radial-gradient(circle,rgba(89,191,172,.16),transparent 62%)}" if t["glow"] is True else ""
    if t["glow"] == "brand":
        glow = (".s:after{content:'';position:absolute;inset:0;background:radial-gradient(900px 700px at 105% -5%,rgba(22,99,240,.55),transparent 60%),radial-gradient(800px 600px at -10% 110%,rgba(34,211,238,.28),transparent 60%);z-index:0}"
                ".t{background:linear-gradient(90deg,#22E6F0,#1663F0);-webkit-background-clip:text;background-clip:text;color:transparent!important}"
                ".card{backdrop-filter:blur(8px);box-shadow:0 0 0 1px rgba(34,211,238,.25),0 20px 60px rgba(22,99,240,.25)}")
    if t["glow"] == "brandlight":
        glow = (".s:after{content:'';position:absolute;inset:0;background:radial-gradient(900px 600px at 110% 0%,rgba(22,99,240,.18),transparent 60%);z-index:0}"
                ".t{background:linear-gradient(90deg,#06B6D4,#1663F0);-webkit-background-clip:text;background-clip:text;color:transparent!important}")
    if t["glow"] == "siya":
        glow = (".s:after{content:'';position:absolute;inset:0;background:radial-gradient(1000px 760px at 110% -10%,rgba(89,191,172,.30),transparent 60%),radial-gradient(760px 620px at -14% 112%,rgba(1,180,223,.20),transparent 62%);z-index:0}"
                ".big.t,.grad{background:linear-gradient(90deg,#59BFAC,#3FE0D0 55%,#01C8E1);-webkit-background-clip:text;background-clip:text;color:transparent!important}"
                ".card,.ui{box-shadow:0 24px 60px rgba(0,0,0,.40)}")
    if t["glow"] == "siyalight":
        glow = (".s:after{content:'';position:absolute;inset:0;background:radial-gradient(900px 640px at 112% -6%,rgba(89,191,172,.22),transparent 60%);z-index:0}"
                ".big.t,.grad{background:linear-gradient(90deg,#2E8F7E,#0E9FB8);-webkit-background-clip:text;background-clip:text;color:transparent!important}"
                ".card,.ui{box-shadow:0 18px 44px rgba(7,7,24,.08)}")
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px}}
body{{font-family:'Inter Display','Inter',sans-serif;-webkit-font-smoothing:antialiased}}
.s{{position:relative;width:{w}px;height:{h}px;overflow:hidden;padding:{pad_top}px 100px {pad_bot}px;display:flex;flex-direction:column;background:{t['bg']};color:{t['fg']}}}
.s:before{{content:'';position:absolute;inset:0;{grid}}}
{glow}
.s>*{{position:relative;z-index:2}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.logo{{height:40px}}
.mono{{font-family:'DejaVu Sans Mono',monospace;letter-spacing:.3em;text-transform:uppercase;font-size:21px}}
.label{{color:{t['acc']};display:flex;align-items:center;gap:16px}}
.label:before{{content:'';width:10px;height:10px;border-radius:50%;background:{t['acc']}}}
.count{{color:{t['sub']};opacity:.6}}
.body{{flex:1;display:flex;flex-direction:column;gap:44px;padding:40px 0}}
.body.center{{justify-content:center}} .body.top{{justify-content:flex-start;padding-top:90px}} .body.bottom{{justify-content:flex-end}}
h1{{font-weight:700;font-size:100px;line-height:1.0;letter-spacing:-.04em}}
h2{{font-weight:650;font-size:76px;line-height:1.05;letter-spacing:-.03em}}
h3{{font-weight:600;font-size:52px;line-height:1.12;letter-spacing:-.02em}}
.t{{color:{t['acc']}}}
.hl{{background:linear-gradient(transparent 58%,rgba(89,191,172,.45) 58%);padding:0 6px}}
p{{font-size:38px;line-height:1.38;color:{t['sub']};letter-spacing:-.01em}}
p b{{color:{t['fg']};font-weight:600}}
.foot{{display:flex;justify-content:space-between;align-items:center;padding:36px 0 60px;border-top:1px solid {t['line']}}}
.foot .mono{{font-size:18px;color:{t['sub']};opacity:.6}}
.arrow{{font-size:40px;color:{t['acc']}}}
.card{{border:1px solid {t['line']};background:{t['card']};border-radius:22px;padding:36px 38px}}
.chip{{display:inline-block;border:1px solid {t['acc']};color:{t['acc']};border-radius:10px;padding:8px 14px;font-size:17px}}
.chipfill{{display:inline-block;background:{t['acc']};color:{t['bg']};border-radius:6px;padding:8px 14px;font-size:17px}}
.row{{display:flex;gap:30px;align-items:baseline;padding:28px 0;border-bottom:1px solid {t['line']}}}
.row:last-child{{border-bottom:none}}
.num{{font-family:'DejaVu Sans Mono',monospace;color:{t['acc']};font-size:28px;min-width:48px}}
.rowt{{font-size:38px;line-height:1.3;font-weight:500;letter-spacing:-.015em}}
.rowt span{{display:block;font-size:31px;font-weight:400;color:{t['sub']};margin-top:6px}}
.flow{{display:flex;align-items:center}}
.node{{border:1px solid {t['line']};background:{t['card']};border-radius:14px;padding:22px 20px;font-size:28px;font-weight:500;text-align:center;flex:0 0 auto}}
.link{{flex:1;height:2px;background:{t['acc']};min-width:18px}}
.link.bad{{background:repeating-linear-gradient(90deg,{t['sub']} 0 10px,transparent 10px 18px);opacity:.5}}
.big{{font-weight:700;letter-spacing:-.06em;line-height:.88}}
.src{{font-size:20px;color:{t['sub']};opacity:.7}}
.quote{{font-weight:600;font-size:72px;line-height:1.1;letter-spacing:-.03em}}
.quote:before{{content:'„';color:{t['acc']};display:block;font-size:160px;line-height:.6;margin-bottom:10px}}
.stamp{{display:inline-block;border:4px solid {t['acc']};color:{t['acc']};padding:10px 22px;border-radius:10px;transform:rotate(-4deg);font-family:'DejaVu Sans Mono',monospace;font-size:30px;letter-spacing:.2em;text-transform:uppercase;font-weight:700}}
.note{{background:#FFF6B8;color:#2A2A20;padding:40px 44px;border-radius:6px;box-shadow:0 18px 40px rgba(0,0,0,.18);transform:rotate(-1.5deg);font-size:38px;line-height:1.4}}
.split{{display:flex;gap:24px}} .half{{flex:1;border-radius:22px;padding:36px 30px;border:1px solid {t['line']};background:{t['card']}}}
.half h4{{font-family:'DejaVu Sans Mono',monospace;letter-spacing:.25em;font-size:20px;text-transform:uppercase;margin-bottom:22px;color:{t['sub']}}}
.half.good h4{{color:{t['acc']}}}
.half div{{font-size:36px;line-height:1.35;margin-bottom:14px}}
.tick:before{{content:'✓  ';color:#59BFAC;font-weight:700}} .cross:before{{content:'✕  ';color:#D9534F;font-weight:700}}
.phone{{width:620px;margin:0 auto;border-radius:56px;border:12px solid #1B1B22;background:#F2F2F7;padding:34px 26px 40px;box-shadow:0 30px 70px rgba(0,0,0,.35)}}
.phone .bar{{text-align:center;font-size:28px;font-weight:600;color:#111;padding-bottom:22px;border-bottom:1px solid #DDD;margin-bottom:22px}}
.chat{{display:flex;flex-direction:column;gap:14px}}
.bin,.bout,.bt{{max-width:84%;padding:20px 26px;border-radius:26px;font-size:33px;line-height:1.32}}
.bin{{background:#FFFFFF;color:#111;align-self:flex-start;border-bottom-left-radius:6px}}
.bout{{background:#1663F0;color:#FFFFFF;align-self:flex-end;border-bottom-right-radius:6px}}
.meta{{font-size:22px;color:#8A8A93;text-align:center}}
.cta{{display:inline-flex;align-items:center;gap:22px;background:#59BFAC;color:#070718;font-size:38px;font-weight:650;padding:30px 44px;border-radius:6px;letter-spacing:-.01em;align-self:flex-start}}
.cta:after{{content:'→';font-size:40px}}
.pill{{display:inline-flex;align-items:center;gap:12px;border:1px solid {t['line']};border-radius:999px;padding:12px 24px;font-family:'DejaVu Sans Mono',monospace;letter-spacing:.24em;text-transform:uppercase;font-size:19px;color:{t['sub']};align-self:flex-start}}
.badge{{display:inline-block;background:#59BFAC;color:#070718;border-radius:4px;padding:6px 12px;font-family:'DejaVu Sans Mono',monospace;letter-spacing:.18em;text-transform:uppercase;font-size:17px;font-weight:700}}
.ui{{border:1px solid {t['line']};background:{t['card']};border-radius:18px;padding:28px 32px}}
.ui.on{{border-color:#59BFAC}}
.uih{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.uih .pill{{font-size:16px;padding:8px 16px}}
.ui .ut{{font-size:36px;font-weight:600;letter-spacing:-.015em;line-height:1.25}}
.ui .us{{font-size:28px;color:{t['sub']};margin-top:6px;line-height:1.35}}
.tl{{display:flex;flex-direction:column;gap:18px;border-left:2px solid {t['line']};margin-left:12px;padding-left:36px}}
.step{{position:relative}}
.step:before{{content:'';position:absolute;left:-46px;top:34px;width:16px;height:16px;border-radius:50%;background:{t['bg']};border:3px solid #59BFAC}}
.av{{width:64px;height:64px;border-radius:50%;background:#59BFAC;color:#070718;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:600;flex:0 0 auto}}
.bt{{background:#2B7F72;color:#FFFFFF;align-self:flex-end;border-bottom-right-radius:6px}}
"""

def page(slide, default_theme, idx, total, tag, story, show_foot):
    if isinstance(slide, str): slide = {"html": slide}
    t = THEMES[slide.get("theme", default_theme)]
    w, h = (1080, 1920) if story else (1080, 1350)
    align = slide.get("align", "center")
    count = f"{tag} · {idx:02d}/{total:02d}" if tag else f"{idx:02d}/{total:02d}"
    if total == 1: count = tag
    foot = f"<div class='foot'><div class='mono'>SIYA MEDIA · AI &amp; MARKETING</div><div class='arrow'>{'→' if idx<total else '↺'}</div></div>" if show_foot and not story else ""
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{css(t,w,h,story)}</style></head><body>
<div class="s"><div class="top"><img class="logo" src="{t['logo']}"><div class="mono count">{count}</div></div>
<div class="body {align}">{slide['html']}</div>{foot}</div></body></html>"""

def render(post_file):
    spec = json.loads(pathlib.Path(post_file).read_text())
    story = spec.get("size") == "story"
    out = ROOT / spec["out"]; out.mkdir(parents=True, exist_ok=True)
    w, h = (1080, 1920) if story else (1080, 1350)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        n = len(spec["slides"])
        for i, s in enumerate(spec["slides"], 1):
            pg.set_content(page(s, spec.get("theme", "dark"), i, n, spec.get("tag", ""), story, spec.get("foot", True)))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"slide_{i:02d}.png"))
        b.close()
    print("ok", out)

if __name__ == "__main__":
    render(sys.argv[1])
