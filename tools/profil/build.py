"""Erzeugt die Specs fuer die 12 Profil-Beitraege (Relaunch Oktober 2026).
Aufruf: python3 tools/profil/build.py  -> schreibt tools/profil/pNN.json
"""
import json, pathlib
D = pathlib.Path(__file__).parent

def label(t): return f"<div class='mono label'>{t}</div>"
def cta(text="Jetzt Erstgespräch vereinbaren", extra="Kostenlos und unverbindlich · Link in der Bio"):
    return f"<div class='cta' data-in='0'>{text}</div><div class='src' style='font-size:24px'>{extra}</div>"
def ui(tag, title, sub="", badge="", on=False, d=None, pop=False):
    a = f" data-in='{d}'" if d is not None else ""
    a += " data-pop='1'" if pop else ""
    b = f"<span class='badge'>{badge}</span>" if badge else ""
    s = f"<div class='us'>{sub}</div>" if sub else ""
    return f"<div class='ui{' on' if on else ''}'{a}><div class='uih'><span class='pill'>{tag}</span>{b}</div><div class='ut'>{title}</div>{s}</div>"
def rows(items, d0=None, step=0.5):
    out = ""
    for i, (a, b) in enumerate(items):
        dd = f" data-in='{d0 + i*step}'" if d0 is not None else ""
        sub = f"<span>{b}</span>" if b else ""
        out += f"<div class='row'{dd}><div class='num'>{i+1:02d}</div><div class='rowt'>{a}{sub}</div></div>"
    return f"<div>{out}</div>"
def ticks(items, cls="tick", d0=None, step=0.45, size=38):
    out = ""
    for i, a in enumerate(items):
        dd = f" data-in='{d0 + i*step}'" if d0 is not None else ""
        out += f"<div class='{cls}' style='font-size:{size}px;line-height:1.35;margin:10px 0'{dd}>{a}</div>"
    return f"<div class='card' style='padding:34px 38px'>{out}</div>"
def phone(bar, msgs, width=760, d0=None, step=0.9):
    out = ""
    for i, (who, txt) in enumerate(msgs):
        dd = f" data-in='{d0 + i*step}'" if d0 is not None else ""
        cls = {"in": "bin", "out": "bt", "meta": "meta"}[who]
        out += f"<div class='{cls}'{dd}>{txt}</div>"
    return f"<div class='phone' style='width:{width}px'><div class='bar'>{bar}</div><div class='chat'>{out}</div></div>"
def call(name, sub, ring=True, d=None):
    a = f" data-in='{d}' data-pop='1'" if d is not None else ""
    return (f"<div class='card'{a} style='display:flex;align-items:center;gap:30px;padding:30px 34px'>"
            f"<div class='{'ring ' if ring else ''}' style='width:104px;height:104px;border-radius:50%;background:#30A46C;display:flex;align-items:center;justify-content:center;font-size:50px;flex:0 0 auto'>✆</div>"
            f"<div><div style='font-size:28px;color:#CDD0E0'>{sub}</div><div style='font-size:44px;font-weight:700'>{name}</div></div></div>")

P = {}

# 01 Wer wir sind (Pin)
P[1] = dict(caption="""Wir sind SIYA Media. Wir bringen KI dahin, wo sie in Unternehmen wirklich Arbeit abnimmt: ans Telefon, in den Posteingang, ins CRM und ins Marketing.

Kein Tool-Abo, das nach drei Wochen keiner mehr öffnet. Sondern Abläufe, die im Alltag mitlaufen, während dein Team sich um Kunden kümmert.

Auf diesem Account zeigen wir, was heute schon möglich ist. Und wenn du wissen willst, wo das bei dir ansetzen kann: Das Erstgespräch ist kostenlos. Link in der Bio.

#KI #Automatisierung #Unternehmen #Mittelstand #Marketing #SIYAMedia""", slides=[
 {"html": "<span class='pill'>Für Unternehmen</span><h1 style='font-size:128px'>KI, die<br><span class='grad'>mitarbeitet.</span></h1><h3 style='color:#CDD0E0;font-weight:500'>Nicht nur in der Präsentation.</h3><div style='display:flex;gap:14px;flex-wrap:wrap'><span class='pill'>Telefon</span><span class='pill'>Anfragen</span><span class='pill'>Abläufe</span><span class='pill'>Marketing</span></div>"},
 {"anim": 6, "html": label("Was wir übernehmen") + "<h2>Vier Stellen, an denen dein Team Zeit zurückbekommt.</h2><div style='display:grid;grid-template-columns:1fr 1fr;gap:20px'>"
  + ui("Telefon", "KI nimmt Anrufe an", "auch nach Feierabend", d=0.6, pop=True)
  + ui("Chat", "Anfragen sofort beantwortet", "z. B. per WhatsApp", d=1.2, pop=True)
  + ui("Abläufe", "Daten laufen von allein", "Mail, Kalender, CRM", d=1.8, pop=True)
  + ui("Marketing", "Werbung, die Anfragen bringt", "Content & Kampagnen", d=2.4, pop=True) + "</div>"},
 {"html": label("So arbeiten wir") + "<h2>Erst zuhören. <span class='t'>Dann bauen.</span></h2>" + rows([
   ("Wir schauen uns eure Abläufe an", "bevor wir irgendetwas vorschlagen"),
   ("Ihr bucht nur, was ihr braucht", "jede Leistung gibt es auch einzeln"),
   ("Nach dem Start bleiben wir dran", "und passen an, wenn sich etwas ändert")])},
 {"html": "<h1 style='font-size:96px'>Wo verliert dein Betrieb gerade <span class='grad'>Zeit?</span></h1><p>Im Erstgespräch finden wir es gemeinsam heraus. Danach weißt du, wo KI sich lohnt.</p>" + cta()},
])

# 02 Ablauf (Pin)
P[2] = dict(caption="""Wie läuft eine Zusammenarbeit mit uns eigentlich ab? In vier Schritten.

Zuerst hören wir zu: Wie kommen Anfragen rein, wo bleibt Zeit liegen? Dann bekommst du einen konkreten Vorschlag mit Reihenfolge und Aufwand, also etwas, auf dessen Grundlage du entscheiden kannst. Erst danach bauen wir, testen an echten Fällen und weisen dein Team ein. Und nach dem Start bleiben wir dran.

Schritt 1 ist das Erstgespräch. Kostenlos, unverbindlich, Link in der Bio.

#KI #Automatisierung #Unternehmen #Digitalisierung #Mittelstand #SIYAMedia""", slides=[
 {"html": label("So arbeiten wir") + "<div class='big grad' style='font-size:420px'>4</div><h2 style='font-size:78px'>Schritte vom ersten Gespräch bis zur KI, die in deinem Unternehmen <span class='t'>läuft.</span></h2>"},
 {"anim": 6.5, "html": "<h2 style='font-size:66px'>Kein Paket von der Stange.</h2><div class='tl'>"
  + "".join(f"<div class='step' data-in='{0.6+i*1.0}'>{ui(t, a, b, on=(i==0))}</div>" for i, (t, a, b) in enumerate([
    ("01 · Zuhören", "Wo geht bei euch Zeit verloren?", "Wir schauen auf Anfragen, Abläufe, Systeme."),
    ("02 · Planen", "Konkreter Vorschlag", "Mit Reihenfolge und Aufwand. Du entscheidest."),
    ("03 · Bauen & testen", "An echten Fällen", "Dein Team wird vor dem Start eingewiesen."),
    ("04 · Dranbleiben", "Anpassen statt vergessen", "Änderungen nach fester Absprache.")])) + "</div>"},
 {"html": label("Nach dem Erstgespräch") + "<h2>Das hast du danach in der Hand:</h2>" + ticks([
   "Eine ehrliche Einschätzung, wo KI bei dir passt",
   "Die Stellen, an denen es sich zuerst lohnt",
   "Einen klaren nächsten Schritt"])},
 {"html": "<h1 style='font-size:104px'>Schritt 1 kostet <span class='grad'>nichts.</span></h1><p>Wir melden uns innerhalb eines Werktags.</p>" + cta()},
])

# 03 Maya live (Pin)
P[3] = dict(caption="""Bevor du uns etwas glaubst: Ruf an.

Unter 02323 3986083 geht Maya ran, unsere eigene KI-Assistentin. Frag sie, was wir machen, erzähl ihr von deinem Unternehmen oder vereinbare direkt einen Termin mit uns.

So hörst du in zwei Minuten, wie ein KI-Telefonassistent für deine Kunden klingen würde. Lieber direkt mit uns sprechen? Das Erstgespräch ist kostenlos, Link in der Bio.

(Es gelten die Verbindungskosten deines Anbieters.)

#KI #KITelefon #Telefonassistent #Kundenservice #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Live testen") + "<h1 style='font-size:118px'>Ruf unsere<br><span class='grad'>KI</span> an.</h1>" + call("Maya", "KI-Assistentin von SIYA Media") + "<div class='big' style='font-size:92px;letter-spacing:-.02em'>02323 3986083</div><p>Erzähl ihr von deinem Unternehmen. Sie hört zu.</p>"},
 {"anim": 7, "html": "<span class='pill'>Beispielgespräch</span>" + phone("Anruf · Maya, SIYA Media", [
   ("out", "Hallo, wir verpassen in der Firma viele Anrufe. Könnt ihr da helfen?"),
   ("in", "Ja, genau dafür bauen wir KI-Telefonassistenten. Wie viele Anrufe habt ihr ungefähr am Tag?"),
   ("out", "So um die 30."),
   ("in", "Dann schauen wir uns das am besten zusammen an. Passt dir Donnerstag, 10 Uhr?"),
   ("out", "Ja, passt."),
   ("meta", "✓ Erstgespräch eingetragen")], d0=0.5, step=1.05)},
 {"html": label("Was du Maya fragen kannst") + "<h2>Ein Anruf, drei Möglichkeiten:</h2>" + ticks([
   "Frag sie, was SIYA Media macht",
   "Erzähl ihr von deinem Unternehmen",
   "Vereinbare direkt einen Termin mit uns"]) + "<p>Genau so würde ein KI-Assistent bei deinen Kunden rangehen.</p>"},
 {"html": "<h1 style='font-size:92px'>So klingt dein Unternehmen, wenn <span class='grad'>KI rangeht.</span></h1><div class='big' style='font-size:84px;letter-spacing:-.02em'>02323 3986083</div><p>Oder sprich direkt mit uns:</p>" + cta()},
])

# 04 KI-Telefonassistent
P[4] = dict(caption="""18:47 Uhr. Das Telefon klingelt, aber im Betrieb ist niemand mehr. Der Anruf landet auf der Mailbox, und ob der Kunde morgen noch einmal anruft, weiß keiner.

Mit einem KI-Telefonassistenten geht jemand ran. Er fragt, was gebraucht wird, bis wann und in welchem Umfang, erkennt, wann es konkret wird, und schlägt direkt einen Termin vor. Danach bekommst du eine kurze Zusammenfassung: wer angerufen hat, was er will und wie heiß die Anfrage ist. Rund um die Uhr, auch am Wochenende. Du startest den nächsten Morgen mit klaren Anfragen statt mit einer Liste von Rückrufen.

Wie das für deinen Betrieb aussehen kann, klären wir im Erstgespräch. Link in der Bio.

#KI #KITelefon #Telefonassistent #Erreichbarkeit #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Leistung · KI-Telefonassistent") + "<div class='big grad' style='font-size:300px'>18:47</div><h1 style='font-size:100px'>Wer geht bei euch jetzt noch ran?</h1>" + call("Neuer Kunde", "Eingehender Anruf")},
 {"anim": 7, "html": "<h2 style='font-size:66px'>Ab hier übernimmt die KI.</h2><div class='tl'>"
  + "".join(f"<div class='step' data-in='{0.5+i*1.1}'>{ui(t, a, b, badge=bd, on=(i==3))}</div>" for i, (t, a, b, bd) in enumerate([
    ("18:47", "Anruf angenommen", "Sofort, ohne Warteschleife.", ""),
    ("18:48", "Bedarf geklärt", "Was wird gebraucht, bis wann, welcher Umfang?", ""),
    ("18:50", "Termin vorgeschlagen", "Direkt im Kalender eingetragen.", "Termin"),
    ("18:51", "Zusammenfassung an dich", "Wer, was, wie heiß die Anfrage ist.", "Neu")])) + "</div>"},
 {"html": "<h2>Derselbe Anruf. Zwei Abende.</h2><div class='split'><div class='half'><h4>Ohne</h4><div class='cross'>Mailbox</div><div class='cross'>Rückruf erst morgen</div><div class='cross'>Kunde ist vielleicht schon woanders</div></div><div class='half good'><h4>Mit KI</h4><div class='tick'>Anruf angenommen</div><div class='tick'>Termin steht</div><div class='tick'>Zusammenfassung im Postfach</div></div></div>"},
 {"html": "<h1 style='font-size:100px'>Erreichbar, auch wenn <span class='grad'>keiner da ist.</span></h1><p>Rund um die Uhr. Mit euren Antworten, euren Zeiten, eurem Ablauf.</p>" + cta()},
])

# 05 KI-Agent fuer Anfragen
P[5] = dict(caption="""Deine Kunden schreiben nicht zu deinen Öffnungszeiten. Sie schreiben abends vom Sofa, per WhatsApp.

Ein KI-Agent beantwortet sie sofort: Er klärt, was fehlt, beantwortet die üblichen Fragen und legt die Anfrage sortiert für dein Team ab. Wird es kompliziert, übergibt er an einen Menschen. Was er sagen darf und wo er stoppt, legen wir vorher gemeinsam fest.

Du willst sehen, wie das bei dir aussehen würde? Erstgespräch über den Link in der Bio.

#KI #KIAgent #WhatsAppBusiness #Kundenanfragen #Automatisierung #SIYAMedia""", slides=[
 {"html": label("Leistung · KI-Agent für Anfragen") + "<h1 style='font-size:84px'>Dein Kunde schreibt um 22:13 Uhr.<br><span class='grad'>Dein KI-Agent antwortet sofort.</span></h1>" + phone("Dein Unternehmen · WhatsApp", [("out", "Hallo, ich bräuchte ein Angebot für neue Fenster."), ("in", "Gern! Wie viele Fenster sind es ungefähr?")], width=780)},
 {"anim": 7.5, "html": "<span class='pill'>Beispiel · so sieht es dein Kunde</span>" + phone("Dein Unternehmen · WhatsApp", [
   ("out", "Hallo, ich bräuchte ein Angebot für neue Fenster."),
   ("in", "Gern! Wie viele Fenster sind es ungefähr, und bis wann soll es fertig sein?"),
   ("out", "6 Stück, bis Ende November."),
   ("in", "Danke! Passt dir ein Termin zum Ausmessen am Donnerstag um 10 Uhr?"),
   ("out", "Ja, passt."),
   ("meta", "✓ Termin bestätigt · Anfrage liegt sortiert bei deinem Team")], d0=0.5, step=1.05)},
 {"html": label("Was der Agent übernimmt") + rows([
   ("Antwortet sofort", "auch nachts und am Wochenende"),
   ("Fragt nach, was fehlt", "statt dass ihr hinterhertelefoniert"),
   ("Legt Anfragen sortiert ab", "fertig für dein Team"),
   ("Übergibt an einen Menschen", "wenn es kompliziert wird")])},
 {"html": "<h1 style='font-size:104px'>Du bestimmst, was er <span class='grad'>sagen darf.</span></h1><p>Inhalte, Grenzen und Übergabepunkte legen wir vorher gemeinsam fest.</p>" + cta()},
])

# 06 Anzeige bis Termin
P[6] = dict(caption="""Eine Anzeige läuft. Jemand klickt, fragt an. Und dann? Genau hier geht in vielen Betrieben das meiste verloren: Die Anfrage liegt, der Rückruf erreicht niemanden, der Termin geht per Mail hin und her.

Wir bauen die ganze Strecke als einen Ablauf: Anzeige, Anfrage, Vorklärung durch die KI, Termin im Kalender. Ohne dass jemand dazwischen etwas abtippen muss. Bestehende Systeme beziehen wir dabei ein. (Das Beispiel in den Slides ist ein stilisierter Ablauf.)

Ob die ganze Strecke oder nur das Stück, das bei dir fehlt: Lass uns im Erstgespräch draufschauen. Link in der Bio.

#Leadgenerierung #KI #Automatisierung #MetaAds #Unternehmen #SIYAMedia""", slides=[
 {"html": "<span class='pill'>Beispielablauf</span><h1 style='font-size:118px'>Anzeige gesehen.<br><span class='grad'>Termin gebucht.</span></h1><h3 style='color:#CDD0E0;font-weight:500'>Und in deinem Unternehmen tippt keiner etwas ab.</h3>"},
 {"anim": 7.5, "html": "<div class='tl'>"
  + f"<div class='step' data-in='0.4'>{ui('Werbeanzeige', 'Neues Bad? Jetzt Beratung sichern', 'Kampagne in der Region')}</div>"
  + f"<div class='step' data-in='1.5'><div class='ui on'><div class='uih'><span class='pill'>Anfrage</span><span class='badge'>Neu</span></div><div style='display:flex;gap:22px;align-items:center'><div class='av'>T</div><div><div class='ut'>Thomas B.</div><div class='us'>möchte sein Bad renovieren</div></div></div></div></div>"
  + f"<div class='step' data-in='2.8'>{ui('KI klärt vor', 'Wie groß? Bis wann? Budget grob?', 'per Telefon oder WhatsApp')}</div>"
  + f"<div class='step' data-in='4.1' data-pop='1'>{ui('Termin bestätigt', 'Beratung Donnerstag, 10:00 Uhr', 'steht im Kalender, Team informiert', badge='Erledigt', on=True)}</div></div>"},
 {"html": label("Wo es sonst hängt") + "<h2>Drei Stellen, an denen Anfragen verloren gehen:</h2>" + ticks([
   "Die Anfrage liegt im Postfach",
   "Der Rückruf erreicht niemanden",
   "Der Termin geht per Mail hin und her"], cls="cross")},
 {"html": "<h1 style='font-size:96px'>Wir bauen die ganze Strecke.<br><span class='grad'>Oder das Stück, das fehlt.</span></h1>" + cta()},
])

# 07 Automatisierung
P[7] = dict(caption="""Mail öffnen, Name kopieren, ins CRM einfügen, Termin in den Kalender, Kollegen Bescheid geben. Jeder Schritt dauert nur eine Minute. Zusammen frisst er jeden Tag Zeit.

Solche Abläufe verbinden wir so, dass sie von allein laufen: Die Anfrage kommt rein, landet im CRM, der Termin steht im Kalender und das Team bekommt Bescheid. Bestehende Systeme beziehen wir ein, und wo ein Mensch entscheiden soll, bauen wir einen Freigabepunkt ein.

Welche Abläufe sich bei dir lohnen, klären wir im Erstgespräch. Link in der Bio.

#Automatisierung #KI #Prozesse #CRM #Digitalisierung #SIYAMedia""", slides=[
 {"html": label("Leistung · Automatisierung") + "<div style='display:flex;gap:20px;align-items:center'><div class='ui' style='font-size:60px;font-weight:700;padding:26px 34px'>Strg + C</div><div class='ui' style='font-size:60px;font-weight:700;padding:26px 34px'>Strg + V</div></div><h1 style='font-size:110px'>Wie oft heute <span class='grad'>schon?</span></h1><p>Dieselben Kundendaten von A nach B. In deinem Büro, jeden Tag.</p>"},
 {"anim": 6.5, "html": "<h2 style='font-size:66px'>Einmal einrichten. <span class='t'>Läuft.</span></h2><div class='tl'>"
  + "".join(f"<div class='step' data-in='{0.5+i*1.0}'>{ui(t, a, '', badge=('Automatisch' if i else ''), on=(i==3))}</div>" for i, (t, a) in enumerate([
    ("E-Mail", "Anfrage kommt rein"),
    ("CRM", "Kontakt automatisch angelegt"),
    ("Kalender", "Termin eingetragen"),
    ("Team", "Zuständiger bekommt Bescheid")])) + "</div>"},
 {"html": label("Typische Abläufe") + "<h2>Das automatisieren wir zum Beispiel:</h2>" + rows([
   ("Anfragen vorsortieren", "nach Dringlichkeit und Thema"),
   ("Termine buchen und bestätigen", ""),
   ("Daten zwischen Programmen übertragen", ""),
   ("Kunden auf dem Laufenden halten", "Eingang, Status, Erinnerung")])},
 {"html": "<h1 style='font-size:100px'>Erst schauen, was da ist. <span class='grad'>Dann verbinden.</span></h1><p>Bestehende Systeme beziehen wir ein. Wo ein Mensch entscheiden soll, bleibt ein Mensch.</p>" + cta()},
])

# 08 CRM
P[8] = dict(caption="""Kurze Frage: Wo steht gerade die Anfrage von letzter Woche? Wer hat zurückgerufen, wann wird nachgefasst?

Wenn die Antwort „Moment, ich schau mal in die Liste“ lautet, fehlt meistens ein System, das alle nutzen. Wir richten CRM und Leadmanagement so ein, dass jede Anfrage an einem Ort liegt, klar ist, wer dran ist, und niemand das Nachfassen vergisst.

Wie das bei dir aussehen kann, zeigen wir dir im Erstgespräch. Link in der Bio.

#CRM #Leadmanagement #Vertrieb #Automatisierung #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Leistung · CRM & Leadmanagement") + "<h1 style='font-size:104px'>Wo steht eigentlich die Anfrage von <span class='grad'>letzter Woche?</span></h1>" + ui("Anfrage · 12 Tage alt", "Zuständig: ?", "Letzter Kontakt: ?")},
 {"anim": 6.5, "html": "<h2 style='font-size:62px'>Jede Anfrage. Ein Ort. <span class='t'>Ein nächster Schritt.</span></h2><div style='display:grid;grid-template-columns:repeat(2,1fr);gap:18px'>"
  + ui("Neu", "Laura M.", "Anfrage über Website", d=0.5, pop=True)
  + ui("Kontaktiert", "Kemal Y.", "Rückruf erledigt", d=1.2, pop=True)
  + ui("Termin", "Familie Berger", "Fr, 9:00 Uhr", d=1.9, pop=True)
  + ui("Nachfassen", "Andreas K.", "Erinnerung morgen", badge="Heute", on=True, d=2.6, pop=True) + "</div><div class='src' data-in='3.4'>Beispielansicht</div>"},
 {"html": "<h2>Warum Anfragen verloren gehen. Und was sich ändert.</h2><div class='split'><div class='half'><h4>Ohne System</h4><div class='cross'>Rückruf kommt zu spät</div><div class='cross'>Nachfassen wird vergessen</div><div class='cross'>Keiner weiß, wer zuständig ist</div></div><div class='half good'><h4>Mit CRM</h4><div class='tick'>Jede Anfrage an einem Ort</div><div class='tick'>Zuständigkeit klar</div><div class='tick'>Erinnerung zum Nachfassen</div></div></div>"},
 {"html": "<h1 style='font-size:100px'>Keine Liste mehr, die <span class='grad'>nur einer versteht.</span></h1>" + cta()},
])

# 09 Wissensassistent
P[9] = dict(caption="""„Wie war das nochmal mit …?“ Diese Frage hört jeder Betrieb mehrmals am Tag. Und meistens kennt nur eine Person die Antwort.

Ein Wissensassistent beantwortet solche Fragen aus euren freigegebenen Unternehmensunterlagen: Abläufe, Zuständigkeiten, Produktinfos, Anleitungen. Mit klaren Zugriffsrechten, damit jeder nur sieht, was er sehen soll. Neue Kollegen finden Antworten selbst, und das Wissen hängt nicht mehr an einzelnen Köpfen.

Welche Unterlagen sich dafür eignen, schauen wir uns im Erstgespräch an. Link in der Bio.

#KI #Wissensmanagement #Einarbeitung #Team #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Leistung · Wissensassistent") + "<h1 style='font-size:108px'>„Wie war das <span class='grad'>nochmal</span> mit …?“</h1><p>Die Frage, die in jedem Team fällt. Und die oft nur eine Person beantworten kann.</p>"},
 {"anim": 6.5, "html": "<span class='pill'>Beispiel · intern</span>" + phone("Wissensassistent · intern", [
   ("out", "Wie läuft bei uns eine Reklamation ab?"),
   ("in", "In 4 Schritten: Foto anfordern, Auftrag prüfen, Termin vergeben, Kunde informieren."),
   ("meta", "Quelle: Ablauf Reklamation.pdf"),
   ("out", "Und wer gibt Gutschriften frei?"),
   ("in", "Laut Handbuch die Teamleitung.")], d0=0.5, step=1.1)},
 {"html": label("Was sich ändert") + rows([
   ("Neue Kollegen finden Antworten selbst", "ohne jedes Mal zu fragen"),
   ("Wissen hängt nicht an einer Person", "auch nicht im Urlaub"),
   ("Nur aus freigegebenen Unterlagen", "mit klaren Zugriffsrechten")])},
 {"html": "<h1 style='font-size:100px'>Euer Wissen. <span class='grad'>Für alle abrufbar.</span></h1>" + cta()},
])

# 10 Werbung & Leads
P[10] = dict(caption="""Likes sind schön. Bezahlen tun sie nichts.

Wir planen Kampagnen auf das, was am Ende zählt: Anfragen von Menschen in deiner Region, die wirklich etwas wollen. Mit einem klaren nächsten Schritt in der Anzeige, und mit einer Bearbeitung, die danach nicht liegen bleibt. Genau da verbinden wir Marketing mit KI.

Lass uns im Erstgespräch auf deine Werbung schauen. Link in der Bio.

#Leadgenerierung #MetaAds #Marketing #Werbung #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Leistung · Kampagnen & Leads") + "<h1 style='font-size:118px'>Werbung für <span class='grad'>Anfragen.</span></h1><h2 style='color:#CDD0E0;font-weight:500;font-size:70px'>Nicht für Likes.</h2><p>Kampagnen für Unternehmen, die neue Kunden in ihrer Region wollen.</p>"},
 {"anim": 6, "html": "<h2 style='font-size:64px'>Von der Anzeige bis zum Gespräch.</h2><div style='display:flex;flex-direction:column;gap:16px;align-items:center'>"
  + "".join(f"<div class='ui{' on' if i==3 else ''}' data-in='{0.5+i*0.9}' data-pop='1' style='width:{100-i*14}%;text-align:center'><div class='ut'>{a}</div><div class='us'>{b}</div></div>" for i, (a, b) in enumerate([
    ("Anzeige", "die richtige Zielgruppe in der Region"),
    ("Klick", "klarer nächster Schritt"),
    ("Anfrage", "sofort bearbeitet"),
    ("Gespräch", "")])) + "</div>"},
 {"html": label("Worauf wir achten") + rows([
   ("Die richtigen Leute", "in deiner Region, mit echtem Bedarf"),
   ("Ein klarer nächster Schritt", "Formular, Anruf oder WhatsApp"),
   ("Keine Anfrage bleibt liegen", "weil die Bearbeitung mitgedacht ist")])},
 {"html": "<h1 style='font-size:100px'>Mehr Budget löst <span class='grad'>selten</span> das Problem.</h1><p>Oft fehlt der Schritt nach dem Klick. Den bauen wir mit.</p>" + cta()},
])

# 11 Content & Social Media
P[11] = dict(caption="""Gute Inhalte für deinen Betrieb müssen nicht nach Agentur aussehen. Sie müssen nach deinem Betrieb aussehen.

Mit SIYA GROWTH übernehmen wir Content und Social Media: Konzept, Fotos, Videos und Reels, Redaktionsplanung, Betreuung des Kanals und Kampagnen für mehr Sichtbarkeit. Alles als Paket oder einzeln.

Was zu deinem Betrieb passt, besprechen wir im Erstgespräch. Link in der Bio.

#SocialMedia #ContentMarketing #Reels #Marketing #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Leistung · SIYA GROWTH") + "<h1 style='font-size:108px'>Content, der nach <span class='grad'>eurem Betrieb</span> aussieht.</h1><p>Nicht nach Stockfoto.</p>"},
 {"html": "<h2>Drei Bereiche, die wir übernehmen:</h2>" + "".join(ui(t, a, b) for t, a, b in [
   ("01 · Produktion", "Fotos, Videos, Reels", "Konzept und Umsetzung"),
   ("02 · Social Media", "Planung und Betreuung", "Strategie, Redaktionsplan, laufende Betreuung"),
   ("03 · Kampagnen", "Sichtbarkeit, die Anfragen bringt", "gezielt in deiner Region")])},
 {"html": label("Flexibel") + "<h1 style='font-size:110px'>Alles. Oder <span class='grad'>nur ein Teil.</span></h1><p>Jeder Bereich ist auch einzeln buchbar.</p>"},
 {"html": "<h1 style='font-size:100px'>Lass uns zeigen, was <span class='grad'>in deinem Betrieb</span> steckt.</h1>" + cta()},
])

# 12 KI-Check WhatsApp
P[12] = dict(caption="""Du willst erst einmal wissen, ob KI für deinen Betrieb überhaupt etwas bringt? Dafür gibt es unseren KI-Check auf WhatsApp.

Du schreibst „Ich möchte den kostenlosen KI-Check.“ und unser KI-Assistent stellt dir ein paar kurze Fragen zu deinem Unternehmen. Danach bekommst du eine erste Einschätzung, welche Aufgaben sich für KI-Unterstützung eignen könnten. Dauert etwa zwei Minuten und ist 100 % kostenlos und unverbindlich. Tipp: Denk dabei an Aufgaben, die sich oft wiederholen.

Link in der Bio. Und wenn du danach tiefer einsteigen willst: Das Erstgespräch ist der nächste Schritt.

#KI #KICheck #WhatsApp #Automatisierung #Unternehmen #SIYAMedia""", slides=[
 {"html": label("Kostenloser KI-Check · WhatsApp") + "<div class='big grad' style='font-size:330px'>2 Min.</div><h1 style='font-size:84px'>und du weißt, wo KI in deinem Unternehmen <span class='t'>passt.</span></h1>"},
 {"anim": 7, "html": "<span class='pill'>Beispiel · so läuft der KI-Check</span>" + phone("SIYA Media · KI-Check", [
   ("out", "Ich möchte den kostenlosen KI-Check."),
   ("in", "Gern! Welche Aufgabe wiederholt sich bei euch jede Woche?"),
   ("out", "Termine mit Kunden abstimmen.")], d0=0.5, step=1.1)
 + "<div class='card' data-in='3.9' data-pop='1' style='border:2px solid #59BFAC;background:rgba(89,191,172,.16);padding:30px 36px;display:flex;gap:24px;align-items:center'><div style='width:72px;height:72px;border-radius:50%;background:#59BFAC;color:#070718;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:800;flex:0 0 auto'>✓</div><div><div style='font-size:44px;font-weight:750;line-height:1.15;letter-spacing:-.02em'>Deine erste Einschätzung</div><div style='font-size:30px;color:#CDD0E0;margin-top:6px'>kommt direkt im Chat. Nach ca. 2 Minuten.</div></div></div>"},
 {"html": label("Nach zwei Minuten") + "<h2>Danach weißt du:</h2>" + ticks([
   "Welche Aufgaben sich für KI eignen könnten",
   "Wo du am ehesten anfängst",
   "Ob ein Erstgespräch sich lohnt"]) + "<p><b>Tipp:</b> Denk an Aufgaben, die sich oft wiederholen, etwa Kundenanfragen oder Terminabsprachen.</p>"},
 {"html": "<h1 style='font-size:100px'>Kurz testen, <span class='grad'>dann entscheiden.</span></h1><p>100 % kostenlos und unverbindlich.</p>" + cta("Jetzt KI-Check starten", "Link in der Bio · danach gern ins Erstgespräch")},
])

for n, post in P.items():
    spec = {"out": f"out/profil-{n:02d}", "size": "post", "theme": "siya", "tag": "", "foot": True, "slides": post["slides"]}
    (D / f"p{n:02d}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
    (D / f"p{n:02d}.txt").write_text(post["caption"])
print("ok", len(P))
