"""Reel 'Von der Anfrage bis zum Auftrag' (Stimme: voice/reel_anfrage.mp3, Schnitte nach Pausen der Aufnahme 13.10.2026).
Aufruf: python3 tools/feed/build_reel_anfrage.py -> tools/feed/r01.json
Rendern: python3 tools/creative_reel.py tools/feed/r01.json <voice.mp3> [musik.mp3]
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_creatives import ico, NAVY, TQ, TQD, GREY, DARKBG

D = pathlib.Path(__file__).parent
L, W = 90, 820  # linker Rand, nutzbare Breite (rechts 170 px fuer Instagram-Buttons)

def card(icon, k, title, sub="", top=0, d=0.0, rot=0, icbg=NAVY, icol=TQ, w=W, pop=True):
    s = f"<div class='ss'>{sub}</div>" if sub else ""
    return (f"<div class='card abs' data-in='{d}'{' data-pop=1' if pop else ''} data-rot='{rot}' "
            f"style='left:{L}px;top:{top}px;width:{w}px;display:flex;gap:26px;align-items:center;padding:30px 32px'>"
            f"<div class='ic' style='width:84px;height:84px;background:{icbg}'>{ico(icon, 44, icol)}</div>"
            f"<div><div class='k'>{k}</div><div class='tt' style='font-size:38px'>{title}</div>{s}</div></div>")
def mega(text, top, size, color="#fff", d=None, extra=""):
    a = f" data-in='{d}'" if d is not None else ""
    return f"<div class='mega abs'{a} style='left:{L}px;top:{top}px;font-size:{size}px;color:{color};{extra}'>{text}</div>"

LOCK = "radial-gradient(900px 1100px at 50% 0%,rgba(89,191,172,.40),transparent 65%),radial-gradient(800px 800px at 100% 100%,rgba(1,140,190,.30),transparent 60%),#0B0F24"
S = []
# 0,00 – 2,58  "Neunzehn Uhr zwoelf. Ein Kunde ruft an."
S.append(dict(start=0, end=2.58, bg=LOCK, html=
  "<div class='abs' style='top:300px;left:0;right:0;text-align:center;color:#fff'>"
  "<div style='font-size:40px;font-weight:500;opacity:.85'>Donnerstag</div>"
  "<div style='font-size:300px;font-weight:600;letter-spacing:-.03em;line-height:1.05'>19:12</div></div>"
  "<div class='glass abs' data-in='1.25' data-pop='1' style='left:90px;right:90px;top:820px;padding:36px 40px;display:flex;align-items:center;gap:30px'>"
  "<div class='ring' style='width:110px;height:110px;border-radius:50%;background:#59BFAC;display:flex;align-items:center;justify-content:center;flex:0 0 auto'>" + ico("phone", 54, NAVY) + "</div>"
  "<div><div style='font-size:30px;opacity:.85'>Eingehender Anruf</div><div style='font-size:52px;font-weight:700'>Kunde</div></div></div>"))
# 2,58 – 4,47  "Bei dir ist laengst Feierabend."
S.append(dict(start=2.58, end=4.47, bg=NAVY, html=
  "<div class='abs' style='left:90px;top:560px;font-size:46px;color:#CDD0E0'>Bei dir ist längst</div>"
  + mega("Feier-<br>abend.", 640, 230)))
# 4,47 – 6,82  "Normalerweise landet er auf der Mailbox."
S.append(dict(start=4.47, end=6.82, bg=GREY, html=
  card("phone", "Verpasster Anruf", "Kunde · 19:12", top=330, d=0.0, rot=-2, icbg="#E5484D", icol="#fff")
  + card("phone", "Verpasster Anruf", "Kunde · 19:14", top=500, d=0.35, rot=1.5, icbg="#E5484D", icol="#fff")
  + card("phone", "Mailbox", "Neue Sprachnachricht", top=670, d=0.7, rot=-1, icbg="#E5484D", icol="#fff")
  + mega("Mailbox.", 960, 196, NAVY)))
# 6,82 – 8,76  "Und ruft vielleicht nie wieder an."
S.append(dict(start=6.82, end=8.76, bg=GREY, html=
  mega("Ruft er<br><span style='color:#E5484D'>nochmal</span><br>an?", 540, 160, NAVY)))
# 8,76 – 10,45  "Bei uns geht jemand ran."
S.append(dict(start=8.76, end=10.45, bg=TQ, html=
  mega("Bei uns<br>geht<br>jemand<br><span style='color:#fff'>ran.</span>", 440, 182, NAVY)))
# 10,45 – 14,69  "Unsere KI klaert, was gebraucht wird, und schlaegt direkt einen Termin vor."
S.append(dict(start=10.45, end=14.69, bg=DARKBG, html=
  mega("Die KI<br><span style='color:#59BFAC'>klärt das.</span>", 300, 148)
  + "<div class='glass abs' data-in='0.3' style='left:90px;width:820px;top:700px;padding:28px 32px;display:flex;gap:24px;align-items:center'>"
    "<div class='ring' style='width:80px;height:80px;border-radius:50%;background:#59BFAC;display:flex;align-items:center;justify-content:center;flex:0 0 auto'>" + ico("phone", 40, NAVY) + "</div>"
    "<div><div style='font-size:26px;opacity:.8'>Gespräch läuft · Beispiel</div><div style='font-size:40px;font-weight:700'>Maya · KI-Assistentin</div></div></div>"
  + card("check", "Anliegen erfasst", "Beratung gewünscht", top=900, d=1.0, rot=-1.5)
  + card("calendar", "Termin vorgeschlagen", "Do, 10:00 Uhr ✓", top=1080, d=2.6, rot=1.5, icbg=TQ, icol=NAVY)))
# 14,69 – 19,35  "Am naechsten Morgen liegt die Anfrage fertig im CRM. Mit Zusammenfassung."
S.append(dict(start=14.69, end=19.35, bg=GREY, html=
  mega("Am nächsten<br><span style='color:#2E8F7E'>Morgen.</span>", 300, 150, NAVY)
  + "<div class='card abs' data-in='0.6' data-pop='1' data-rot='-2' style='left:90px;top:780px;width:820px;padding:36px 38px'>"
    "<div style='display:flex;justify-content:space-between;align-items:center'><div class='k'>CRM · Neue Anfrage</div>"
    "<div class='mono' style='background:#E5484D;color:#fff;font-weight:700;font-size:20px;padding:8px 14px;border-radius:6px;letter-spacing:.18em'>Heiß</div></div>"
    "<div class='tt' style='font-size:48px;margin-top:16px'>Anruf von gestern, 19:12</div>"
    "<div class='ss'>Termin Do, 10:00 Uhr steht im Kalender</div>"
    "<div data-in='3.3' style='margin-top:24px;padding:24px 26px;border-radius:16px;background:#EEF8F6;display:flex;gap:18px;align-items:flex-start'>"
    + ico("spark", 38, TQD) + "<div style='font-size:31px;color:#1F5A50;line-height:1.35'><b>Zusammenfassung:</b> möchte eine Beratung, hat nach der Lieferzeit gefragt.</div></div></div>"))
# 19,35 – 23,50  "Und ist das Angebot raus, erinnert dich das System, wann du nachfassen solltest."
S.append(dict(start=19.35, end=23.5, bg=DARKBG, html=
  card("file", "Angebot · gesendet", "Angebot_2026-118", "offen seit 3 Tagen", top=330, d=0.0, rot=-1.5, pop=False)
  + card("bell", "Erinnerung", "Heute nachfassen?", top=560, d=1.6, rot=2, icbg=TQ, icol=NAVY)
  + mega("Kein Angebot<br><span style='color:#59BFAC'>bleibt liegen.</span>", 900, 118, d=2.4)))
# 23,50 – 29,30  "Von der ersten Anfrage bis zum Auftrag. Gebaut um deinen Betrieb. Und wir bleiben dran."
steps = [("phone", "Anfrage"), ("calendar", "Termin"), ("file", "Angebot"), ("check", "Auftrag")]
flow = "".join(
    f"<div data-in='{0.15 + i*0.45}' data-pop='1' style='display:flex;align-items:center;gap:22px;margin-bottom:18px'>"
    f"<div class='ic' style='width:76px;height:76px;background:{TQ if i == 3 else NAVY}'>{ico(ic, 40, NAVY if i == 3 else TQ)}</div>"
    f"<div style='font-size:46px;font-weight:800;color:{NAVY};letter-spacing:-.02em'>{t}{' ✓' if i == 3 else ''}</div></div>"
    for i, (ic, t) in enumerate(steps))
S.append(dict(start=23.5, end=29.3, bg=GREY, html=
  f"<div class='abs' style='left:90px;top:300px;border-left:4px solid {TQ};padding-left:30px'>{flow}</div>"
  + mega("Gebaut um<br>deinen Betrieb.", 830, 112, NAVY, d=2.65)
  + mega("Und wir<br><span style='color:#2E8F7E'>bleiben dran.</span>", 1100, 112, NAVY, d=4.37)))
# 29,30 – Ende  "Ruf Maya an und hoer selbst. Oder buch dein kostenloses Erstgespraech. Link in der Bio."
S.append(dict(start=29.3, end=99, bg=DARKBG, html=
  mega("Ruf Maya an.<br><span style='color:#59BFAC'>Hör selbst.</span>", 300, 112)
  + "<div class='abs' data-in='0.4' data-pop='1' style='left:90px;top:640px;display:flex;align-items:center;gap:26px'>"
    "<div class='ring' style='width:96px;height:96px;border-radius:50%;background:#59BFAC;display:flex;align-items:center;justify-content:center'>" + ico("phone", 48, NAVY) + "</div>"
    "<div style='font-size:86px;font-weight:800;color:#fff;letter-spacing:-.02em'>02323 3986083</div></div>"
  + "<div class='btn abs' data-in='1.9' style='left:90px;top:900px;background:#59BFAC;color:#070718'>Kostenloses Erstgespräch →</div>"
  + "<div class='abs' data-in='4.3' style='left:90px;top:1050px;font-size:34px;color:#CDD0E0'>Link in der Bio</div>"
  + "<img class='abs' data-in='4.3' src='{LOGO_LIGHT}' style='left:90px;top:1240px;height:56px'>"))

(D / "r01.json").write_text(json.dumps({"out": "out/reel-r01", "hold": 1.6, "scenes": S}, ensure_ascii=False, indent=1))
print("r01", len(S), "Szenen")
