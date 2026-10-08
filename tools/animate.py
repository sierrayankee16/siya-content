"""SIYA Media: animierte Carousel-Slides (1080x1350, 30 fps, MP4 mit stiller Tonspur).

Aufruf: python3 tools/animate.py <post.json>

Gleiche Spec wie render.py. Slides mit "anim": <Sekunden> werden als Video
(slide_XX.mp4) gerendert, alle anderen als PNG wie gewohnt.
Im HTML wirken dieselben Attribute wie bei reel.py:
  data-in="1.2"   blendet das Element 1,2 s nach Start weich ein (von unten)
  data-pop="1"    skaliert statt zu schieben
  data-count="167" zaehlt eine Zahl hoch (data-prefix, data-suffix)
  class="ring"    pulsiert (eingehender Anruf)
Am Ende steht das fertige Bild mindestens HOLD Sekunden (Lesezeit), dann loopt Instagram.
Die erste Slide eines Posts sollte statisch bleiben: Das Raster zeigt ihr erstes Bild.
"""
import sys, json, pathlib, subprocess, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render import page
from reel import JS
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
HOLD = 6.0  # Sekunden Standbild am Ende, bevor Instagram das Video neu startet
RING = "<style>.ring{border-radius:50%}</style>"

def run(post_file):
    spec = json.loads(pathlib.Path(post_file).read_text())
    out = ROOT / spec["out"]; out.mkdir(parents=True, exist_ok=True)
    n = len(spec["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(spec["slides"], 1):
            html = page(s, spec.get("theme", "siya"), i, n, spec.get("tag", ""), False, spec.get("foot", True))
            dur = s.get("anim") if isinstance(s, dict) else None
            if not dur:
                pg.set_content(html); pg.wait_for_timeout(150)
                pg.screenshot(path=str(out / f"slide_{i:02d}.png")); continue
            html = html.replace("<div class=\"body", "<div class=\"scene body", 1).replace("</body>", f"{RING}<script>{JS}</script></body>")
            html = html.replace("class=\"scene body", "data-start=\"0\" data-end=\"999\" class=\"scene body", 1)
            pg.set_content(html); pg.wait_for_timeout(200)
            pg.evaluate("document.querySelector('.scene').style.opacity=1")
            last_in = pg.evaluate("Math.max(0,...[...document.querySelectorAll('[data-in]')].map(e=>+e.dataset.in))")
            dur = max(float(dur), last_in + 0.6 + HOLD)
            frames = out / f"_f{i:02d}"; shutil.rmtree(frames, ignore_errors=True); frames.mkdir()
            for k in range(int(dur * FPS)):
                pg.evaluate(f"window.setT({k / FPS}); document.querySelector('.scene').style.opacity=1")
                pg.screenshot(path=str(frames / f"f{k:05d}.jpg"), type="jpeg", quality=92)
            mp4 = out / f"slide_{i:02d}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"),
                            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "18",
                            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(mp4)], check=True)
            shutil.copy(frames / f"f{int(dur * FPS) - 1:05d}.jpg", out / f"slide_{i:02d}_end.jpg")
            shutil.rmtree(frames)
        b.close()
    print("ok", out)

if __name__ == "__main__":
    run(sys.argv[1])
