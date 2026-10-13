"""Creatives im neuen Stil (Pattern Interrupt, Riesen-Typo, schwebende UI) fuer KW 42/43.
Aufruf: python3 tools/feed/build_creatives.py -> tools/feed/cNN.json + cNN.txt
Rendern: python3 tools/creative.py tools/feed/cNN.json
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_kw42 import ICONS, TAGS

D = pathlib.Path(__file__).parent
ICONS["alert"] = "<path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3'/><path d='M12 9v4M12 17h.01'/>"
def ico(name, size=44, color="#59BFAC", sw=2):
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='{sw}' "
            f"stroke-linecap='round' stroke-linejoin='round' style='flex:0 0 auto'>{ICONS[name]}</svg>")
CURSOR = ("<svg width='70' height='70' viewBox='0 0 24 24' style='filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))'>"
          "<path d='M5 2.5l13 9.2-5.6 1.1 3.3 6.6-2.6 1.3-3.3-6.6L5.6 18z' fill='#FFFFFF' stroke='#070718' stroke-width='1.3' stroke-linejoin='round'/></svg>")
NAVY, TQ, TQD, GREY = "#070718", "#59BFAC", "#2E8F7E", "#ECEEF1"
DARKBG = f"radial-gradient(900px 700px at 85% 15%,rgba(89,191,172,.30),transparent 60%),radial-gradient(700px 600px at -10% 110%,rgba(1,180,223,.16),transparent 60%),{NAVY}"
def notif(icon, k, title, sub, w=820, style="", dot=True, bg=NAVY, icol=TQ, d=None, pop=True):
    a = (f" data-in='{d}'" + (" data-pop='1'" if pop else "")) if d is not None else ""
    return (f"<div class='card abs'{a} style='width:{w}px;display:flex;gap:26px;align-items:center;padding:30px 34px;{style}'>"
            + (f"<div class='abs' style='right:24px;top:24px;width:14px;height:14px;border-radius:50%;background:{TQ}'></div>" if dot else "")
            + f"<div class='ic' style='width:84px;height:84px;background:{bg}'>{ico(icon, 44, icol)}</div>"
            f"<div><div class='k'>{k}</div><div class='tt' style='font-size:36px'>{title}</div><div class='ss'>{sub}</div></div></div>")
def logo(kind="DARK", pos="left:84px;bottom:80px"):
    return f"<img class='logo abs' src='{{LOGO_{kind}}}' style='{pos}'>"

C = {}

# ======================= c01 · Fr 16.10. · Ehrlich gesagt (Einzelbild, Sperrbildschirm) =======================
C["c01"] = dict(tags="f01", caption="""Drei Wochen nach dem Kauf meldet sich das KI-Tool. Nicht, weil es Arbeit abgenommen hat. Sondern weil es keiner benutzt.

Ein Tool kaufen dauert fünf Minuten. Dann kommt der Montag danach: Wer richtet es ein? Wer zeigt dem Team, wie es geht? Und was passiert, wenn sich im Betrieb etwas ändert? Genau hier landet so manches Tool in der Schublade.

Deshalb verkaufen wir keine Tools. Wir schauen uns an, wie bei dir gearbeitet wird, bauen die KI in genau diese Abläufe ein und bleiben nach dem Start dran.

Wo sich das bei dir lohnt, finden wir im Erstgespräch heraus. Kostenlos und unverbindlich, Link in der Bio.""", slides=[
 {"bg": "radial-gradient(800px 900px at 50% 0%,rgba(89,191,172,.45),transparent 65%),radial-gradient(700px 700px at 100% 100%,rgba(1,140,190,.35),transparent 60%),#0B0F24",
  "html":
  "<div class='abs' style='top:120px;left:0;right:0;text-align:center;color:#fff'>"
  "<div style='font-size:34px;font-weight:500;opacity:.85'>Montag, drei Wochen später</div>"
  "<div style='font-size:230px;font-weight:600;letter-spacing:-.03em;line-height:1.05'>08:12</div></div>"
  "<div class='glass abs' style='left:80px;right:80px;top:470px;padding:30px 34px;opacity:.55;transform:scale(.95);filter:blur(1.5px)'>"
  "<div style='display:flex;align-items:center;gap:18px;font-size:24px;opacity:.85'><div class='ic' style='width:46px;height:46px;border-radius:12px;background:#59BFAC'>" + ico("refresh", 26, NAVY) + "</div>KI-TOOL · gestern</div>"
  "<div style='font-size:34px;font-weight:700;margin-top:14px'>Dein Abo wurde verlängert.</div></div>"
  "<div class='glass abs' style='left:80px;right:80px;top:560px;padding:32px 36px;background:rgba(255,255,255,.2)'>"
  "<div style='display:flex;align-items:center;gap:18px;font-size:26px;opacity:.9'><div class='ic' style='width:52px;height:52px;border-radius:14px;background:#59BFAC'>" + ico("spark", 30, NAVY) + "</div>KI-TOOL<span style='margin-left:auto;opacity:.7'>jetzt</span></div>"
  "<div style='font-size:42px;font-weight:700;margin-top:18px'>Wir vermissen dich.</div>"
  "<div style='font-size:32px;line-height:1.35;margin-top:6px;opacity:.92'>Dein Team hat sich seit 21 Tagen nicht mehr eingeloggt.</div></div>"
  "<div class='mega abs' style='left:80px;bottom:110px;font-size:118px;color:#fff'>Gekauft ist<br><span style='color:#59BFAC'>nicht genutzt.</span></div>"},
])

# ======================= c02 · Mo 19.10. · Kennst du das? (Angebot, Funkstille) =======================
C["c02"] = dict(tags="f02", caption="""Das Angebot ist raus. Im Gespräch war der Kunde begeistert. Und dann: nichts.

Das muss nicht am Angebot liegen. Manchmal fehlt im Alltag einfach die Zeit, nachzufassen. Und während das Angebot liegt, spricht der Kunde vielleicht schon mit jemand anderem.

Bei uns hat dein CRM jedes offene Angebot im Blick und erinnert dich, wann es Zeit ist. Die KI schlägt dir vor, was du schreiben oder fragen kannst. Entscheiden tust du. (Der Ablauf in den Slides ist ein Beispiel.)

Wie aus deinen Angeboten öfter Aufträge werden, schauen wir uns im Erstgespräch an. Kostenlos und unverbindlich, Link in der Bio.""", slides=[
 {"bg": DARKBG, "html":
  "<div class='mono abs' style='left:80px;top:110px;font-size:22px;color:#59BFAC'>Kennst du das?</div>"
  "<div class='card abs' style='left:90px;right:90px;top:250px;padding:56px 54px 50px;border-radius:30px;text-align:center'>"
  "<div style='display:flex;justify-content:center'><div class='ic' style='width:110px;height:110px;border-radius:28px;background:#FFF4D6'>" + ico("alert", 60, "#D98E04", 2.2) + "</div></div>"
  "<div style='font-size:54px;font-weight:800;letter-spacing:-.025em;line-height:1.12;margin-top:34px'>Angebot_2026-118<br>reagiert nicht.</div>"
  "<div style='font-size:32px;color:#5A5D73;line-height:1.4;margin-top:20px'>Seit 9 Tagen keine Antwort vom Kunden.<br>Wie möchtest du fortfahren?</div>"
  "<div style='display:flex;gap:18px;margin-top:44px'>"
  "<div style='flex:1;padding:28px 0;border-radius:16px;background:#ECEEF1;font-size:34px;font-weight:700;color:#3A3D52'>Weiter warten</div>"
  "<div style='flex:1;padding:28px 0;border-radius:16px;background:#59BFAC;font-size:34px;font-weight:700;color:#070718'>Nachfassen</div></div></div>"
  "<div class='abs' style='left:330px;top:905px'>" + CURSOR + "</div>"
  "<div class='mega abs' style='left:80px;bottom:110px;font-size:112px;color:#fff'>Worauf klickst<br><span style='color:#59BFAC'>du gerade?</span></div>"},
 {"bg": GREY, "anim": 6, "html":
  "<div class='mega abs' style='left:80px;top:110px;font-size:132px;color:#070718'>Du wartest.<br><span style='color:#2E8F7E'>Der Kunde<br>nicht.</span></div>"
  + notif("search", "Tag 3 · Beispiel", "Kunde holt zweites Angebot ein", "", w=830, style="left:110px;top:620px;transform:rotate(-2deg)", d=0.6)
  + notif("clock", "Tag 6", "Bei dir: volle Woche, keiner fasst nach", "", w=830, style="left:150px;top:820px;transform:rotate(1.5deg)", d=1.5, dot=False)
  + notif("phone", "Tag 9", "Der andere Anbieter ruft an.", "", w=830, style="left:100px;top:1020px;transform:rotate(-1deg)", d=2.4, bg="#E5484D", icol="#FFFFFF")},
 {"bg": DARKBG, "html":
  "<div class='mega abs' style='left:80px;top:110px;font-size:148px;color:#fff'>Dein CRM<br><span style='color:#59BFAC'>vergisst<br>nichts.</span></div>"
  "<div class='card abs' style='left:470px;top:640px;width:520px;padding:24px 28px;display:flex;gap:22px;align-items:center;transform:rotate(2deg)'>"
  "<div class='ic' style='width:68px;height:68px;border-radius:18px;background:#59BFAC'>" + ico("bell", 36, NAVY) + "</div><div><div class='k'>Erinnerung · Tag 3</div><div class='tt' style='font-size:32px'>Jetzt nachfassen?</div></div></div>"
  "<div class='card abs' style='left:110px;top:780px;width:860px;padding:34px 38px;transform:rotate(-2.5deg)'>"
  "<div style='display:flex;justify-content:space-between;align-items:center'><div class='k'>Pipeline · Beispiel</div><div class='mono' style='background:#59BFAC;color:#070718;font-weight:700;font-size:18px;padding:8px 14px;border-radius:6px;letter-spacing:.18em'>Heute nachfassen</div></div>"
  "<div class='tt' style='font-size:46px;margin-top:16px'>Angebot_2026-118</div>"
  "<div class='ss'>offen seit 3 Tagen · Kunde hatte nach der Lieferzeit gefragt</div>"
  "<div style='margin-top:22px;padding:20px 24px;border-radius:16px;background:#EEF8F6;display:flex;gap:16px;align-items:center'>" + ico("spark", 34, TQD)
  + "<div style='font-size:28px;color:#1F5A50;line-height:1.3'><b>KI-Vorschlag:</b> Kurz anrufen und die Lieferzeit bestätigen.</div></div></div>"
  "<div class='abs' style='left:80px;bottom:100px;font-size:34px;color:#CDD0E0'>Die KI schlägt vor. <b style='color:#fff'>Entscheiden tust du.</b></div>"},
 {"bg": GREY, "html":
  "<div class='mega abs' style='left:80px;top:150px;font-size:134px;color:#070718'>An Tag 3<br><span style='color:#2E8F7E'>rufst du an.</span></div>"
  "<div class='lead abs' style='left:80px;right:120px;top:540px;color:#3A3D52'>Nicht an Tag 9. Im Erstgespräch schauen wir, wie aus deinen Angeboten öfter Aufträge werden.</div>"
  "<div class='btn abs' style='left:80px;top:760px;background:#070718;color:#fff'>Jetzt Erstgespräch vereinbaren <span style='color:#59BFAC'>→</span></div>"
  "<div class='abs' style='left:80px;top:890px;font-size:26px;color:#5A5D73'>Kostenlos und unverbindlich · Link in der Bio</div>"
  + logo("DARK")},
])

# ======================= c03 · Mi 21.10. · So laeuft's (Termin verschieben per WhatsApp) =======================
CHAT = [("meta", "Mittwoch, 18:30"),
        ("in", "Hallo! Kurze Erinnerung: Morgen um 10:00 Uhr ist Ihr Beratungstermin bei uns. Passt das noch?"),
        ("out", "Oh, morgen klappt es leider nicht. Geht auch Freitag?"),
        ("in", "Klar. Am Freitag hätten wir 9:00 oder 14:30 Uhr frei."),
        ("out", "14:30 passt!"),
        ("in", "Ist eingetragen. Bis Freitag ✓")]
def chat(msgs, d0=0.4, step=0.9):
    out = ""
    for i, (who, t) in enumerate(msgs):
        cls = {"in": "bin", "out": "bt", "meta": "meta"}[who]
        out += f"<div class='{cls}' data-in='{d0 + i*step}'>{t}</div>"
    return out
C["c03"] = dict(tags="f03", caption="""Morgen um 10 Uhr steht ein Beratungstermin. Der Kunde hat ihn vergessen, oder ihm ist etwas dazwischengekommen. Im schlechtesten Fall merkst du es erst, wenn um 10:15 Uhr niemand da ist.

So kann es auch laufen: Am Vortag geht automatisch eine Erinnerung per WhatsApp raus. Will der Kunde verschieben, bietet die KI freie Zeiten aus deinem Kalender an und trägt den neuen Termin direkt ein. Dein Team sieht die Änderung sofort, ohne dass jemand telefonieren muss. Passt etwas nicht ins Schema, übernimmt ein Mensch.

(Der Chat in den Slides ist ein Beispiel.)

Welche Nachrichten bei dir jeden Tag von Hand geschrieben werden und was davon die KI übernehmen kann, zeigt dir unser kostenloser KI-Check auf WhatsApp. Schreib einfach „Ich möchte den kostenlosen KI-Check.“ Link in der Bio.""", slides=[
 {"bg": GREY, "html":
  "<div class='card abs' style='left:100px;top:130px;width:620px;padding:30px 34px;transform:rotate(-3deg)'>"
  "<div class='k'>Donnerstag</div><div style='margin-top:16px;padding:22px 24px;border-left:8px solid #E5484D;background:#FDECEC;border-radius:12px'>"
  "<div style='font-size:28px;color:#B4232A;font-weight:700'>10:00</div><div style='font-size:38px;font-weight:800;text-decoration:line-through;text-decoration-color:#E5484D;text-decoration-thickness:5px;color:#7A3A3E'>Beratungstermin</div></div></div>"
  "<div class='abs' style='left:640px;top:330px;font-size:120px;color:#2E8F7E;font-weight:900;transform:rotate(20deg)'>↘</div>"
  "<div class='card abs' style='left:380px;top:440px;width:620px;padding:30px 34px;transform:rotate(2.5deg)'>"
  "<div class='k'>Freitag</div><div style='margin-top:16px;padding:22px 24px;border-left:8px solid #59BFAC;background:#EEF8F6;border-radius:12px'>"
  "<div style='font-size:28px;color:#2E8F7E;font-weight:700'>14:30</div><div style='font-size:38px;font-weight:800'>Beratungstermin ✓</div></div></div>"
  "<div class='bt abs' style='right:90px;top:720px;font-size:36px;padding:22px 30px;box-shadow:0 20px 40px rgba(0,0,0,.18)'>14:30 passt!</div>"
  "<div class='mega abs' style='left:80px;bottom:110px;font-size:128px;color:#070718'>Verschoben.<br><span style='color:#2E8F7E'>Ohne Anruf.</span></div>"},
 {"bg": DARKBG, "anim": 7, "html":
  "<div class='mega abs' style='left:80px;top:100px;font-size:84px;color:#fff'>So sieht das für<br><span style='color:#59BFAC'>deinen Kunden aus.</span></div>"
  "<div class='abs' style='left:130px;right:130px;top:330px;border-radius:56px;border:12px solid #1B1B22;background:#F2F2F7;padding:28px 24px 34px;box-shadow:0 40px 90px rgba(0,0,0,.45)'>"
  "<div style='text-align:center;font-size:26px;font-weight:700;color:#111;padding-bottom:18px;border-bottom:1px solid #DDD;margin-bottom:18px'>Dein Betrieb · WhatsApp</div>"
  "<div style='display:flex;flex-direction:column;gap:12px'>" + chat(CHAT) + "</div></div>"},
 {"bg": NAVY, "html":
  "<div class='mega abs' style='left:80px;top:110px;font-size:150px;color:#fff'>Keiner<br>hat <span style='color:#59BFAC'>getippt.</span></div>"
  "<div class='abs' style='left:80px;right:80px;top:500px;display:grid;grid-template-columns:1fr 1fr;gap:22px'>"
  + "".join(f"<div style='background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:30px 30px 34px'>"
            f"<div class='ic' style='width:76px;height:76px;border-radius:20px;background:rgba(89,191,172,.16)'>{ico(i, 40)}</div>"
            f"<div style='font-size:34px;font-weight:700;color:#fff;margin-top:22px;line-height:1.2'>{t}</div>"
            f"<div style='font-size:26px;color:#CDD0E0;margin-top:8px;line-height:1.3'>{s}</div></div>"
            for i, t, s in [("calendar", "Termin im Kalender", "wie gewohnt"), ("bell", "Erinnerung am Vortag", "per WhatsApp, automatisch"),
                            ("chat", "KI bietet Zeiten an", "aus deinem Kalender"), ("check", "Neuer Termin steht", "dein Team sieht es sofort")])
  + "</div><div class='abs' style='left:80px;bottom:110px;display:flex;gap:18px;align-items:center;font-size:32px;color:#CDD0E0'>" + ico("user", 38)
  + "Passt etwas nicht ins Schema, übernimmt ein Mensch.</div>"},
 {"bg": TQ, "html":
  "<div class='mega abs' style='left:80px;top:150px;font-size:100px;color:#070718'>Was tippt<br>dein Team<br><span style='color:#FFFFFF'>noch von Hand?</span></div>"
  "<div class='lead abs' style='left:80px;right:120px;top:580px;color:#0E2E2A'>Finde es in zwei Minuten heraus: mit unserem kostenlosen KI-Check auf WhatsApp.</div>"
  "<div class='btn abs' style='left:80px;top:780px;background:#070718;color:#fff'>KI-Check starten <span style='color:#59BFAC'>→</span></div>"
  "<div class='abs' style='left:80px;top:910px;font-size:26px;color:#0E2E2A'>Schreib uns: „Ich möchte den kostenlosen KI-Check.“<br>Link in der Bio</div>"
  + logo("DARK")},
])

for k, v in C.items():
    (D / f"{k}.json").write_text(json.dumps({"out": f"out/feed-{k}", "slides": v["slides"]}, ensure_ascii=False, indent=1))
    (D / f"{k}.txt").write_text(v["caption"] + "\n\n" + TAGS[v["tags"]])
    print(k)
