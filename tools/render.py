import base64, sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo_c.png").read_bytes()).decode()
LOGO_D = "data:image/png;base64," + base64.b64encode((ROOT / "logo_dark.png").read_bytes()).decode()

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{font-family:'Inter Display','Inter',sans-serif;-webkit-font-smoothing:antialiased}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;padding:92px 84px 0;display:flex;flex-direction:column}
.dark{background:#070718;color:#fff}
.dark:before{content:'';position:absolute;inset:0;
 background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
 background-size:108px 108px}
.dark:after{content:'';position:absolute;width:900px;height:900px;right:-300px;bottom:-320px;
 background:radial-gradient(circle,rgba(89,191,172,.16),transparent 62%)}
.light{background:#F6F7FA;color:#0B0B1F}
.light:before{content:'';position:absolute;inset:0;
 background-image:linear-gradient(rgba(11,11,31,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(11,11,31,.045) 1px,transparent 1px);
 background-size:108px 108px}
.s>*{position:relative;z-index:2}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:auto}
.logo{height:40px}
.lightlogo{height:40px}
.mono{font-family:'DejaVu Sans Mono',monospace;letter-spacing:.32em;text-transform:uppercase;font-size:21px}
.label{color:#59BFAC;display:flex;align-items:center;gap:16px}
.label:before{content:'';width:10px;height:10px;border-radius:50%;background:#59BFAC}
.light .label{color:#2E8F7E}.light .label:before{background:#2E8F7E}
.count{color:rgba(205,208,224,.55)}
.light .count{color:rgba(11,11,31,.4)}
.body{margin:auto 0;display:flex;flex-direction:column;gap:44px}
h1{font-weight:600;font-size:96px;line-height:1.02;letter-spacing:-.035em}
h2{font-weight:600;font-size:76px;line-height:1.06;letter-spacing:-.03em}
.t{color:#59BFAC}
.light .t{color:#2E8F7E}
p{font-size:38px;line-height:1.38;color:#CDD0E0;font-weight:400;letter-spacing:-.01em}
.light p{color:#4A4D63}
.foot{display:flex;justify-content:space-between;align-items:center;padding:40px 0 64px;margin-top:auto;border-top:1px solid rgba(205,208,224,.12)}
.light .foot{border-top:1px solid rgba(11,11,31,.1)}
.foot .mono{font-size:18px;color:rgba(205,208,224,.5)}
.light .foot .mono{color:rgba(11,11,31,.4)}
.arrow{font-size:40px;color:#59BFAC}
.card{border:1px solid rgba(205,208,224,.16);background:rgba(20,22,48,.7);border-radius:22px;padding:36px 38px}
.light .card{background:#fff;border:1px solid rgba(11,11,31,.08);box-shadow:0 20px 50px rgba(11,11,31,.07)}
.chip{display:inline-block;border:1px solid rgba(89,191,172,.5);color:#59BFAC;border-radius:10px;padding:8px 14px;font-size:17px}
.chipfill{display:inline-block;background:#59BFAC;color:#070718;border-radius:6px;padding:7px 12px;font-size:16px}
.row{display:flex;gap:30px;align-items:baseline;padding:30px 0;border-bottom:1px solid rgba(205,208,224,.14)}
.light .row{border-bottom:1px solid rgba(11,11,31,.1)}
.row:last-child{border-bottom:none}
.num{font-family:'DejaVu Sans Mono',monospace;color:#59BFAC;font-size:28px;min-width:48px}
.light .num{color:#2E8F7E}
.rowt{font-size:40px;line-height:1.3;font-weight:500;letter-spacing:-.015em}
.rowt span{display:block;font-size:31px;font-weight:400;color:#CDD0E0;margin-top:6px}
.light .rowt span{color:#4A4D63}
.wave{display:flex;gap:7px;align-items:center;height:70px}
.wave i{display:block;width:8px;border-radius:4px;background:#59BFAC}
.flow{display:flex;align-items:center;gap:0}
.node{border:1px solid rgba(11,11,31,.14);background:#fff;border-radius:14px;padding:22px 20px;font-size:28px;font-weight:500;text-align:center;flex:0 0 auto}
.dark .node{background:rgba(20,22,48,.9);border-color:rgba(205,208,224,.2);color:#fff}
.link{flex:1;height:2px;background:#59BFAC;opacity:.7;min-width:18px}
.link.bad{background:repeating-linear-gradient(90deg,#C9CBD6 0 10px,transparent 10px 18px);opacity:1}
.big{font-weight:600;letter-spacing:-.06em;line-height:.9}
.src{font-size:20px;color:rgba(11,11,31,.45);letter-spacing:.02em}
.dark .src{color:rgba(205,208,224,.45)}
"""

def page(slide, theme, idx, total, tag):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>
<div class="s {theme}">
 <div class="top"><img class="logo" src="{LOGO if theme=='dark' else LOGO_D}"><div class="mono count">{tag} · {idx:02d}/{total:02d}</div></div>
 <div class="body">{slide}</div>
 <div class="foot"><div class="mono">SIYA MEDIA · AI &amp; MARKETING</div><div class="arrow">{'→' if idx<total else '↺'}</div></div>
</div></body></html>"""

def render(post_file):
    spec = json.loads(pathlib.Path(post_file).read_text())
    out = ROOT / spec["out"]; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width":1080,"height":1350})
        n = len(spec["slides"])
        for i, s in enumerate(spec["slides"], 1):
            pg.set_content(page(s, spec["theme"], i, n, spec["tag"]))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"slide_{i:02d}.png"))
        b.close()
    print("ok", out)

if __name__ == "__main__":
    render(sys.argv[1])
