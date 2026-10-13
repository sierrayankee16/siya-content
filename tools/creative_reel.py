"""SIYA Media: frei gestaltete Reels (1080x1920, 30 fps) im Creative-Stil, auf eine Tonspur gelegt.

Aufruf: python3 tools/creative_reel.py <spec.json> <voice.mp3> [musik.mp3]

Spec: {"out": "out/reel-x", "hold": 1.6, "scenes": [{"start": 0, "end": 2.6, "bg": "<css>", "html": "..."}]}
- Harte Schnitte (0,08 s), Elemente mit data-in="Sek. ab Szenenstart", data-pop="1" skaliert, .ring pulsiert.
- Sichere Zone: wichtige Inhalte zwischen 250 px oben und 1450 px, rechts 170 px frei (Instagram-Buttons).
- Musik (optional) wird auf -20 dB unter die Stimme gemischt und am Ende ausgeblendet.
"""
import sys, json, pathlib, subprocess, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from creative import CSS, LOGOS
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
JS = """
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x,0),1), 3);
window.setT = function(t){
  document.querySelectorAll('.sc').forEach(sc => {
    const s = +sc.dataset.start, e = +sc.dataset.end;
    sc.style.opacity = (t >= s && t < e) ? Math.min(1, (t - s) / 0.08 + 0.001) : 0;
    const lt = t - s;
    sc.querySelectorAll('[data-in]').forEach(el => {
      const p = ease((lt - (+el.dataset.in)) / 0.35);
      const base = el.dataset.rot ? ` rotate(${el.dataset.rot}deg)` : '';
      el.style.transform = (el.dataset.pop ? `scale(${0.6 + 0.4 * p})` : `translateY(${(1 - p) * 60}px)`) + base;
      el.style.opacity = p;
    });
    sc.querySelectorAll('.ring').forEach(el => {
      const k = (Math.sin(lt * 9) + 1) / 2;
      el.style.boxShadow = `0 0 0 ${8 + 22 * k}px rgba(89,191,172,${0.45 - 0.3 * k})`;
    });
  });
};
"""

def run(spec_file, voice, music=None):
    spec = json.loads(pathlib.Path(spec_file).read_text())
    out = ROOT / spec["out"]; out.mkdir(parents=True, exist_ok=True)
    vlen = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice]).decode())
    dur = vlen + spec.get("hold", 1.5)
    spec["scenes"][-1]["end"] = dur + 1
    scenes = ""
    for s in spec["scenes"]:
        h = s["html"]
        for k, v in LOGOS.items(): h = h.replace(k, v)
        scenes += f"<div class='sc abs' data-start='{s['start']}' data-end='{s['end']}' style='inset:0;opacity:0;background:{s.get('bg', '#070718')}'>{h}</div>"
    css = CSS.replace("height:1350px", "height:1920px")
    html = f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body><div class='s'>{scenes}</div><script>{JS}</script></body></html>"
    frames = out / "_frames"; shutil.rmtree(frames, ignore_errors=True); frames.mkdir()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(html); pg.wait_for_timeout(300)
        for k in range(int(dur * FPS)):
            pg.evaluate(f"window.setT({k / FPS})")
            pg.screenshot(path=str(frames / f"f{k:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    shutil.copy(frames / "f00045.jpg", out / "cover.jpg")
    mp4 = out / "reel.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"), "-i", voice]
    if music:
        cmd += ["-stream_loop", "-1", "-i", music, "-filter_complex",
                f"[2:a]volume=-20dB,afade=t=out:st={dur-1.5}:d=1.5[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0,apad[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-filter_complex", "[1:a]apad[a]", "-map", "0:v", "-map", "[a]"]
    cmd += ["-t", f"{dur:.2f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", str(mp4)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames)
    print("ok", mp4, f"{dur:.1f}s")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
