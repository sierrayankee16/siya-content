"""SIYA Media Reel-Renderer (1080x1920, 30 fps, MP4).

Aufruf: python3 tools/reel.py <reel.json> [audio.mp3]

Spec:
{
  "out": "out/reel-name",
  "duration": 26.0,
  "scenes": [ {"start": 0, "end": 4.5, "html": "..."} ]
}
Elemente in einer Szene mit data-in="Sekunden ab Szenenstart" blenden weich ein (von unten).
data-pop="1" skaliert stattdessen auf. data-count="1000" zaehlt eine Zahl hoch (data-suffix, data-prefix).
Klasse .ring laesst ein Element pulsieren (eingehender Anruf).
Mit Audio: Laenge wird an die Tonspur angepasst (letzte Szene verlaengert).
"""
import sys, json, pathlib, subprocess, shutil, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render import THEMES, css
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30

JS = """
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x,0),1), 3);
window.setT = function(t){
  document.querySelectorAll('.scene').forEach(sc => {
    const s = +sc.dataset.start, e = +sc.dataset.end;
    const fin = ease((t - s) / 0.35), fout = ease((e - t) / 0.3);
    const vis = t >= s - 0.01 && t <= e + 0.01;
    sc.style.opacity = vis ? Math.min(fin, fout) : 0;
    const lt = t - s;
    sc.querySelectorAll('[data-in]').forEach(el => {
      const p = ease((lt - (+el.dataset.in)) / 0.45);
      if (el.dataset.pop) el.style.transform = `scale(${0.7 + 0.3 * p})`;
      else el.style.transform = `translateY(${(1 - p) * 50}px)`;
      el.style.opacity = p;
    });
    sc.querySelectorAll('[data-count]').forEach(el => {
      const p = ease((lt - (+(el.dataset.in || 0))) / 1.2);
      const v = Math.round((+el.dataset.count) * p);
      el.textContent = (el.dataset.prefix || '') + v.toLocaleString('de-DE') + (el.dataset.suffix || '');
    });
    sc.querySelectorAll('.ring').forEach(el => {
      const k = (Math.sin(lt * 9) + 1) / 2;
      el.style.boxShadow = `0 0 0 ${6 + 18 * k}px rgba(48,164,108,${0.35 - 0.25 * k})`;
    });
  });
};
"""

def build_html(spec):
    t = THEMES["brand"]
    style = css(t, 1080, 1920, True) + """
.scene{position:absolute;left:84px;right:84px;top:300px;bottom:360px;display:flex;flex-direction:column;justify-content:center;gap:48px;opacity:0}
.cap{position:absolute;left:0;right:0;bottom:170px;text-align:center;z-index:3}
"""
    scenes = "".join(f"<div class='scene' data-start='{s['start']}' data-end='{s['end']}'>{s['html']}</div>" for s in spec["scenes"])
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{style}</style></head><body>
<div class='s'><div class='top'><img class='logo' src='{t['logo']}' style='height:52px'></div>{scenes}
<div class='cap mono' style='font-size:22px;color:#B7BCD6;opacity:.7'>SIYA MEDIA · AI &amp; MARKETING</div></div>
<script>{JS}</script></body></html>"""

def audio_len(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout
    return float(out.strip())

def render(spec_file, audio=None):
    spec = json.loads(pathlib.Path(spec_file).read_text())
    dur = spec["duration"]
    if audio:
        dur = max(dur, audio_len(audio) + 0.6)
        spec["scenes"][-1]["end"] = dur
    out = ROOT / spec["out"]; frames = out / "frames"
    shutil.rmtree(frames, ignore_errors=True); frames.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(build_html(spec)); pg.wait_for_timeout(300)
        n = int(dur * FPS)
        for i in range(n):
            pg.evaluate(f"setT({i / FPS})")
            pg.screenshot(path=str(frames / f"f{i:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    mp4 = out / "reel.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg")]
    if audio: cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(mp4)]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(mp4), "-frames:v", "1", str(out / "cover.jpg")], check=True)
    shutil.rmtree(frames)
    print("ok", mp4, round(dur, 1), "s")

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
