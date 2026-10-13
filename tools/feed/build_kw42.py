"""Specs fuer die ersten Feed-Beitraege nach der neuen Strategie (KW 42/43).
Aufruf: python3 tools/feed/build_kw42.py -> schreibt tools/feed/fNN.json + fNN.txt
Rendern: python3 tools/animate.py tools/feed/fNN.json
"""
import json, pathlib
D = pathlib.Path(__file__).parent

# --- Icons (Linien-Icons im Lucide-Stil, inline SVG) ---
ICONS = {
 "phone": "<path d='M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z'/>",
 "calendar": "<rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/>",
 "bell": "<path d='M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9'/><path d='M10.3 21a1.94 1.94 0 0 0 3.4 0'/>",
 "check": "<path d='M20 6 9 17l-5-5'/>",
 "mail": "<rect x='2' y='4' width='20' height='16' rx='2'/><path d='m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'/>",
 "chat": "<path d='M7.9 20A9 9 0 1 0 4 16.1L2 22Z'/>",
 "spark": "<path d='M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z'/>",
 "user": "<circle cx='12' cy='7' r='4'/><path d='M5.5 21a6.5 6.5 0 0 1 13 0'/>",
 "clock": "<circle cx='12' cy='12' r='10'/><path d='M12 6v6l4 2'/>",
 "file": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><path d='M14 2v6h6M8 13h8M8 17h5'/>",
 "send": "<path d='m22 2-7 20-4-9-9-4Z'/><path d='M22 2 11 13'/>",
 "search": "<circle cx='11' cy='11' r='8'/><path d='m21 21-4.3-4.3'/>",
 "people": "<circle cx='9' cy='7' r='4'/><path d='M2 21a7 7 0 0 1 14 0'/><path d='M16 3.13a4 4 0 0 1 0 7.75M22 21a7 7 0 0 0-4-6.3'/>",
 "refresh": "<path d='M21 12a9 9 0 0 1-15.5 6.2L3 16'/><path d='M3 12a9 9 0 0 1 15.5-6.2L21 8'/><path d='M21 3v5h-5M3 21v-5h5'/>",
}
def ico(name, size=44, color="#59BFAC", sw=2):
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='{sw}' "
            f"stroke-linecap='round' stroke-linejoin='round' style='flex:0 0 auto'>{ICONS[name]}</svg>")
def tile(name, size=88, bg="rgba(89,191,172,.14)", color="#59BFAC", isize=46):
    return (f"<div style='width:{size}px;height:{size}px;border-radius:22px;background:{bg};display:flex;"
            f"align-items:center;justify-content:center;flex:0 0 auto'>{ico(name, isize, color)}</div>")
def irow(icon, title, sub="", d=None, dark=True):
    a = f" data-in='{d}'" if d is not None else ""
    s = f"<div style='font-size:30px;color:{'#CDD0E0' if dark else '#4A4D63'};margin-top:4px;line-height:1.3'>{sub}</div>" if sub else ""
    return (f"<div{a} style='display:flex;gap:30px;align-items:center'>{tile(icon)}"
            f"<div><div style='font-size:40px;font-weight:600;letter-spacing:-.015em;line-height:1.2'>{title}</div>{s}</div></div>")
def label(t): return f"<div class='mono label'>{t}</div>"
def cta(text="Jetzt Erstgespräch vereinbaren", extra="Kostenlos und unverbindlich · Link in der Bio"):
    return f"<div class='cta' data-in='0'>{text}</div><div class='src' style='font-size:24px'>{extra}</div>"
def phone(bar, msgs, width=760, d0=None, step=0.9):
    out = ""
    for i, (who, txt) in enumerate(msgs):
        dd = f" data-in='{d0 + i*step}'" if d0 is not None else ""
        cls = {"in": "bin", "out": "bt", "meta": "meta"}[who]
        out += f"<div class='{cls}'{dd}>{txt}</div>"
    return f"<div class='phone' style='width:{width}px'><div class='bar'>{bar}</div><div class='chat'>{out}</div></div>"

TAGS = {
 "f01": "#siyamedia #kiimunternehmen #ki #künstlicheintelligenz #kitools #digitalisierung #automatisierung #prozesse #prozessoptimierung #effizienz #teamwork #mitarbeiter #beratung #kiberatung #unternehmen #unternehmer #mittelstand #kmu #selbstständig #unternehmensentwicklung",
 "f02": "#siyamedia #angebot #angebote #nachfassen #vertrieb #verkauf #crm #crmsystem #leadmanagement #salespipeline #kundengewinnung #auftrag #ki #künstlicheintelligenz #kiimunternehmen #automatisierung #unternehmen #unternehmer #mittelstand #kmu",
 "f03": "#siyamedia #terminvereinbarung #termine #terminerinnerung #noshow #whatsapp #whatsappbusiness #kundenkommunikation #kundenservice #kalender #automatisierung #kiagent #ki #künstlicheintelligenz #kiimunternehmen #digitalisierung #unternehmen #unternehmer #mittelstand #kmu",
}

P = {}

# ---------- f01 · Fr 16.10. · Ehrlich gesagt (Einzelbild, Tuerkis-Flaeche) ----------
P["f01"] = dict(theme="accent", caption="""Ein KI-Tool kaufen dauert fünf Minuten. Account anlegen, Abo abschließen, fertig.

Dann kommt der Montag danach. Wer richtet es ein? Wer zeigt dem Team, wie es geht? Und was passiert, wenn sich im Betrieb etwas ändert? Genau hier landet so manches Tool in der Schublade.

Deshalb verkaufen wir keine Tools. Wir schauen uns an, wie bei dir gearbeitet wird, bauen die KI in genau diese Abläufe ein und bleiben nach dem Start dran.

Wo sich das bei dir lohnt, finden wir im Erstgespräch heraus. Kostenlos und unverbindlich, Link in der Bio.""", slides=[
 {"html":
  "<div class='mono' style='display:flex;align-items:center;gap:16px;color:#070718'><span style='width:10px;height:10px;border-radius:50%;background:#070718'></span>Ehrlich gesagt</div>"
  "<h1 style='font-size:98px;line-height:1.02;letter-spacing:-.045em'>Ein KI-Tool kaufen<br>dauert fünf Minuten.</h1>"
  "<h2 style='font-size:54px;font-weight:600;line-height:1.16;color:#0E2E2A'>Dass dein Team es in drei Wochen<br>noch nutzt:<br><span style='color:#FFFFFF'>Das ist die eigentliche Arbeit.</span></h2>"
  "<div style='display:flex;gap:12px;flex-wrap:nowrap'>"
  + "".join(f"<div style='display:flex;align-items:center;gap:14px;background:#070718;color:#FFFFFF;border-radius:999px;padding:14px 22px 14px 16px;font-size:25px;font-weight:600;white-space:nowrap'>{ico(i,28)}{t}</div>"
            for i, t in [("search", "Abläufe verstehen"), ("people", "Team mitnehmen"), ("refresh", "Dranbleiben")])
  + "</div>"},
])

# ---------- f02 · Mo 19.10. · Kennst du das? (Angebot, dann Funkstille) ----------
P["f02"] = dict(theme="siya", caption="""Das Angebot ist raus. Im Gespräch war der Kunde begeistert. Und dann: nichts.

Das muss nicht am Angebot liegen. Manchmal fehlt im Alltag einfach die Zeit, nachzufassen. Und während das Angebot liegt, spricht der Kunde vielleicht schon mit jemand anderem.

Bei uns hat dein CRM jedes offene Angebot im Blick und erinnert dich, wann es Zeit ist. Die KI schlägt dir vor, was du schreiben oder fragen kannst. Entscheiden tust du. (Der Ablauf in den Slides ist ein Beispiel.)

Wie aus deinen Angeboten öfter Aufträge werden, schauen wir uns im Erstgespräch an. Kostenlos und unverbindlich, Link in der Bio.""", slides=[
 {"html":
  label("Kennst du das?")
  + "<div class='big grad' style='font-size:300px;line-height:1;padding-bottom:24px'>Tag 9.</div>"
  + "<h2 style='font-size:72px'>Das Angebot ist raus.<br>Seitdem: <span class='t'>Funkstille.</span></h2>"
  + "<div class='ui' style='display:flex;gap:26px;align-items:center'>" + tile("file", 92) +
    "<div style='flex:1'><div class='ut'>Angebot_2026-118.pdf</div><div class='us'>gesendet vor 9 Tagen · keine Antwort</div></div>"
    + ico("send", 40, "#CDD0E0") + "</div>"},
 {"anim": 6, "html":
  label("Was in den 9 Tagen passiert · Beispiel")
  + "<h2 style='font-size:66px'>Du wartest. <span class='t'>Der Kunde nicht.</span></h2>"
  + "<div class='tl'>"
  + "".join(f"<div class='step' data-in='{d}'><div class='ui' style='display:flex;gap:24px;align-items:center;padding:24px 28px'>{tile(i,72,isize=38)}<div><div style='font-size:24px;color:#59BFAC;font-family:DejaVu Sans Mono,monospace;letter-spacing:.2em'>{day}</div><div style='font-size:34px;font-weight:600;line-height:1.25'>{t}</div></div></div></div>"
            for d, i, day, t in [(0.5, "send", "TAG 1", "Das Angebot geht raus"),
                                 (1.3, "search", "TAG 3", "Der Kunde holt ein zweites Angebot ein"),
                                 (2.1, "clock", "TAG 6", "Bei dir: volle Woche, keiner fasst nach"),
                                 (2.9, "phone", "TAG 9", "Der andere Anbieter ruft an")])
  + "</div>"},
 {"html":
  label("So läuft es mit uns")
  + "<h2 style='font-size:70px'>Dein CRM vergisst<br><span class='t'>kein Angebot.</span></h2>"
  + "<div class='ui on' style='padding:26px 30px'><div class='uih'><span class='pill'>Pipeline · Beispiel</span><span class='badge'>Heute nachfassen</span></div>"
    "<div class='ut'>Angebot_2026-118</div><div class='us'>offen seit 3 Tagen · Kunde hatte nach der Lieferzeit gefragt</div></div>"
  + "<div style='display:flex;flex-direction:column;gap:26px'>"
  + irow("bell", "Erinnert dich zur richtigen Zeit", "bevor das Angebot kalt wird")
  + irow("spark", "Schlägt vor, was du sagen kannst", "auf Basis eurer Notizen zum Kunden")
  + irow("check", "Entscheiden tust du", "die KI arbeitet zu, nicht über dich hinweg")
  + "</div>"},
 {"theme": "siyalight", "html":
  "<h1 style='font-size:90px'>An Tag 9 hättest du <span class='grad'>längst angerufen.</span></h1>"
  "<p>Im Erstgespräch schauen wir, wie aus deinen Angeboten öfter Aufträge werden.</p>"
  + cta()},
])

# ---------- f03 · Mi 21.10. · So laeuft's (Termin per WhatsApp verschieben) ----------
CHAT = [("meta", "Mittwoch, 18:30"),
        ("in", "Hallo! Kurze Erinnerung: Morgen um 10:00 Uhr ist Ihr Beratungstermin bei uns. Passt das noch?"),
        ("out", "Oh, morgen klappt es leider nicht. Geht auch Freitag?"),
        ("in", "Klar. Am Freitag hätten wir 9:00 oder 14:30 Uhr frei."),
        ("out", "14:30 passt!"),
        ("in", "Ist eingetragen. Bis Freitag ✓")]
P["f03"] = dict(theme="siya", caption="""Morgen um 10 Uhr steht ein Beratungstermin. Der Kunde hat ihn vergessen, oder ihm ist etwas dazwischengekommen. Im schlechtesten Fall merkst du es erst, wenn um 10:15 Uhr niemand da ist.

So kann es auch laufen: Am Vortag geht automatisch eine Erinnerung per WhatsApp raus. Will der Kunde verschieben, bietet die KI freie Zeiten aus deinem Kalender an und trägt den neuen Termin direkt ein. Dein Team sieht die Änderung sofort, ohne dass jemand telefonieren muss. Passt etwas nicht ins Schema, übernimmt ein Mensch.

(Der Chat in den Slides ist ein Beispiel.)

Welche Nachrichten bei dir jeden Tag von Hand geschrieben werden und was davon die KI übernehmen kann, zeigt dir unser kostenloser KI-Check auf WhatsApp. Schreib einfach „Ich möchte den kostenlosen KI-Check.“ Link in der Bio.""", slides=[
 {"align": "top", "html":
  label("So läuft’s · Beispiel")
  + "<h2 style='font-size:76px'>Termin verschoben.<br><span class='grad'>Ohne einen Anruf.</span></h2>"
  + phone("WhatsApp · Dein Betrieb", CHAT[:4], width=820)},
 {"anim": 7, "html":
  label("Was im Hintergrund passiert")
  + "<h2 style='font-size:62px'>Vier Schritte.<br><span class='t'>Keiner davon von Hand.</span></h2>"
  + "<div style='display:flex;flex-direction:column;gap:30px'>"
  + irow("calendar", "Der Termin steht im Kalender", "wie gewohnt", d=0.5)
  + irow("bell", "Am Vortag: Erinnerung per WhatsApp", "geht automatisch raus", d=1.4)
  + irow("chat", "Kunde will verschieben?", "die KI bietet freie Zeiten an", d=2.3)
  + irow("check", "Neuer Termin ist eingetragen", "dein Team sieht es sofort", d=3.2)
  + "</div>"
  + "<div data-in='4.1' style='display:flex;gap:20px;align-items:center;font-size:30px;color:#CDD0E0'>" + ico("user", 36) + "Passt etwas nicht ins Schema, übernimmt ein Mensch.</div>"},
 {"html":
  label("Der Unterschied")
  + "<h2 style='font-size:66px'>Gleicher Termin.<br><span class='t'>Anderer Morgen.</span></h2>"
  + "<div class='split' style='font-size:0'><div class='half' style='--x:0'><h4 style='color:#E5484D'>Ohne</h4>"
    "<div class='cross'>Termin vergessen</div><div class='cross'>Absage nur per Anruf</div><div class='cross'>10:15 Uhr: niemand da</div></div>"
    "<div class='half good'><h4>Mit</h4>"
    "<div class='tick'>Erinnerung am Vortag</div><div class='tick'>Verschieben im Chat</div><div class='tick'>Kalender stimmt immer</div></div></div>"},
 {"theme": "siyalight", "html":
  "<h1 style='font-size:84px'>Welche Nachrichten schreibt dein Team <span class='grad'>jeden Tag von Hand?</span></h1>"
  "<p>Finde es in zwei Minuten heraus: mit unserem kostenlosen KI-Check auf WhatsApp.</p>"
  + cta("KI-Check starten", "Schreib uns: „Ich möchte den kostenlosen KI-Check.“ · Link in der Bio")},
])

for k, v in P.items():
    spec = {"out": f"out/feed-{k}", "size": "post", "theme": v["theme"], "tag": "", "foot": True, "slides": v["slides"]}
    (D / f"{k}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
    (D / f"{k}.txt").write_text(v["caption"] + "\n\n" + TAGS[k])
    print(k, len(TAGS[k].split()), "hashtags")
