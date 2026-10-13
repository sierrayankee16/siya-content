"""SIYA Media: frei gestaltete Creatives (ohne festes Slide-Geruest).

Aufruf: python3 tools/creative.py <spec.json>

Spec: {"out": "out/xyz", "slides": [{"bg": "<css background>", "html": "<html>", "anim": 6?}]}
- Kein Logo/Zaehler/Fusszeile automatisch. Logo nur, wo es im HTML steht ({LOGO_LIGHT}/{LOGO_DARK}).
- "anim": Sekunden -> MP4 (wie animate.py: data-in, data-pop, data-count, HOLD Sekunden Standbild am Ende).
"""
import sys, json, pathlib, subprocess, shutil, base64
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from reel import JS
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS, HOLD = 30, 6.0
def b64(n): return "data:image/png;base64," + base64.b64encode((ROOT / n).read_bytes()).decode()
LOGOS = {"{LOGO_LIGHT}": b64("logo_c.png"), "{LOGO_DARK}": b64("logo_dark.png")}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Inter Display','Inter',sans-serif;-webkit-font-smoothing:antialiased}
.s{position:relative;width:1080px;height:1350px;overflow:hidden}
.abs{position:absolute}
.mega{font-family:'Inter Display';font-weight:900;text-transform:uppercase;letter-spacing:-.05em;line-height:.9}
.mono{font-family:'DejaVu Sans Mono',monospace;letter-spacing:.24em;text-transform:uppercase}
.lead{font-size:38px;line-height:1.35;letter-spacing:-.01em}
.card{background:#FFFFFF;border-radius:28px;box-shadow:0 40px 90px rgba(7,7,24,.22),0 8px 22px rgba(7,7,24,.10);color:#070718}
.glass{background:rgba(255,255,255,.14);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.18);border-radius:30px;color:#FFFFFF}
.ic{border-radius:22px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}
.k{font-family:'DejaVu Sans Mono',monospace;font-size:18px;letter-spacing:.22em;text-transform:uppercase;color:#8A8DA3}
.tt{font-size:40px;font-weight:800;letter-spacing:-.02em;line-height:1.12}
.ss{font-size:27px;color:#5A5D73;margin-top:4px;line-height:1.3}
.btn{display:inline-flex;align-items:center;gap:20px;font-size:38px;font-weight:700;padding:30px 44px;border-radius:14px;letter-spacing:-.01em}
.bin,.bt{max-width:82%;padding:20px 26px;border-radius:26px;font-size:31px;line-height:1.3}
.bin{background:#FFFFFF;color:#111;align-self:flex-start;border-bottom-left-radius:6px}
.bt{background:#2B7F72;color:#FFFFFF;align-self:flex-end;border-bottom-right-radius:6px}
.meta{font-size:22px;color:#8A8A93;text-align:center}
.logo{height:38px}
"""

def html_for(slide):
    h = slide["html"]
    for k, v in LOGOS.items(): h = h.replace(k, v)
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>"
            f"<div class='s scene' data-start='0' data-end='999' style='background:{slide.get('bg', '#070718')}'>{h}</div></body></html>")

def run(spec_file):
    spec = json.loads(pathlib.Path(spec_file).read_text())
    out = ROOT / spec["out"]; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(spec["slides"], 1):
            html = html_for(s)
            if not s.get("anim"):
                pg.set_content(html); pg.wait_for_timeout(200)
                pg.screenshot(path=str(out / f"slide_{i:02d}.png")); continue
            html = html.replace("</body>", f"<script>{JS}</script></body>")
            pg.set_content(html); pg.wait_for_timeout(200)
            pg.evaluate("document.querySelector('.scene').style.opacity=1")
            last_in = pg.evaluate("Math.max(0,...[...document.querySelectorAll('[data-in]')].map(e=>+e.dataset.in))")
            dur = max(float(s["anim"]), last_in + 0.6 + HOLD)
            frames = out / f"_f{i:02d}"; shutil.rmtree(frames, ignore_errors=True); frames.mkdir()
            for k in range(int(dur * FPS)):
                pg.evaluate(f"window.setT({k / FPS}); document.querySelector('.scene').style.opacity=1")
                pg.screenshot(path=str(frames / f"f{k:05d}.jpg"), type="jpeg", quality=92)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"),
                            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "18",
                            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out / f"slide_{i:02d}.mp4")], check=True)
            shutil.copy(frames / f"f{int(dur * FPS) - 1:05d}.jpg", out / f"slide_{i:02d}_end.jpg")
            shutil.rmtree(frames)
        b.close()
    print("ok", out)

if __name__ == "__main__":
    run(sys.argv[1])
