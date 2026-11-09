# -*- coding: utf-8 -*-
"""Genera le pagine italiane corrette, le pagine inglesi in /en/ e le didascalie delle foto.
Uso (dalla radice del repository):  python3 _i18n/build_imr.py
Legge gli originali da _i18n/src e scrive le pagine nella radice del repository.
Richiede: python3, pyyaml.
Le didascalie stanno in didascalie.yaml (accanto a questo script): una lista per pagina, una voce per foto
(file, it, en, credit). Campi vuoti = niente didascalia."""
import re, sys, os, html, shutil, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from en_testi import EN

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv)>2 else os.path.join(HERE,"src")
OUT = sys.argv[2] if len(sys.argv)>2 else os.path.dirname(HERE)
SITE = "https://ilmotorediricerca.github.io"
PAGES = ["index","che-pesci-prendere","oda","adelfia-fratelli","albania1e1000","otnarat","sogno-cirio","maerchen","giardino-radicale"]
LOG = []

def rd(p): return open(os.path.join(SRC,p),encoding="utf-8").read()
def wr(p,t):
    f=os.path.join(OUT,p); os.makedirs(os.path.dirname(f),exist_ok=True); open(f,"w",encoding="utf-8").write(t)

def sub(t, a, b, page, count=1):
    if a not in t:
        raise SystemExit(f"[{page}] testo non trovato: {a[:70]!r}")
    LOG.append((page,a,b))
    return t.replace(a,b)

# ---- correzioni al testo italiano (refusi) -----------------------------------
FIX = {
"index": [
 ("temporanemanete chiusa è stata reutilizzata","temporaneamente chiusa è stata riutilizzata"),
 ("ha explorato territori marginale","ha esplorato territori marginali"),
 ("Sud dell’Albania’;","Sud dell’Albania;"),
 ("(padre di Alberto Savino e Giorgio de Chirico)","(padre di Alberto Savinio e Giorgio de Chirico)"),
 ('<a href="" target="_blank" class="gold"><strong>Roberto Dell’Orco</strong></a>','<strong>Roberto Dell’Orco</strong>'),
 ('<a href="" target="_blank"> <strong>Michele Loiacono</strong></a>','<strong>Michele Loiacono</strong>'),
 ('href=" http://atelierquartino.com/"','href="http://atelierquartino.com/"'),
 ("</a>(2011)","</a> (2011)"),("</a>(2009)","</a> (2009)"),
],
"oda":[
 ("archiettura","architettura"),
 ("Regione Puglia Tirana International Film Festival","Regione Puglia, Tirana International Film Festival"),
],
"adelfia-fratelli":[
 ("Volos-Milies, Grece,","Volos-Milies, Grecia,"),
 ("Gli artist in diversi ruoli","Gli artisti in diversi ruoli"),
],
"albania1e1000":[("All’apperenza","All’apparenza"),("sugli albanesi , luoghi","sugli albanesi, luoghi")],
"otnarat":[
 ("in Gemania,","in Germania,") if False else ("Gemania","Germania"),
 ("moduli d’acciao","moduli d’acciaio"),
 ("laborario d’arte urbana Staker/ON","laboratorio d’arte urbana Stalker/ON"),
 ("<em>Regia: Nico Angiuli\nSceneggiatura: Nico Angiuli, Roberto dell’Orco, Michele Loiacono\nCon: Nicola Carrino, Matteo Fraterno, Lorenzo Romito, Angelo Losasso, Aldo Scatigna, Francesco Dracca\nMontaggio: Stefano Muti\nSuono: Mauro Boccuni\nMusica: Angelo Losasso, Francesco Dracca, Aldo Scatigna\nProgetto grafico: Roberto dell’Orco, PiaLivia Di Tardo\nProduzione: In Iride Sfoggio srl\nProgetto memoria",
  "<em>Regia: Nico Angiuli<br />\nSceneggiatura: Nico Angiuli, Roberto dell’Orco, Michele Loiacono<br />\nCon: Nicola Carrino, Matteo Fraterno, Lorenzo Romito, Angelo Losasso, Aldo Scatigna, Francesco Dracca<br />\nMontaggio: Stefano Muti<br />\nSuono: Mauro Boccuni<br />\nMusica: Angelo Losasso, Francesco Dracca, Aldo Scatigna<br />\nProgetto grafico: Roberto dell’Orco, PiaLivia Di Tardo<br />\nProduzione: In Iride Sfoggio srl<br />\nProgetto memoria"),
],
"sogno-cirio":[
 ("<title>Il Sognodi Francesco Cirio","<title>Il Sogno di Francesco Cirio"),
 ('<h2 class="page-title">Il Sognodi Francesco Cirio','<h2 class="page-title">Il Sogno di Francesco Cirio'),
 ("Il Sognodi Francesco Cirio, foto","Il Sogno di Francesco Cirio, foto"),
 ("Ragazzi di via Agliè,Marta","Ragazzi di via Agliè, Marta"),
],
"maerchen":[
 ("Nella note di luna piena","Nella notte di luna piena"),
 ("il logo, la storia","il luogo, la storia"),
],
"giardino-radicale":[],
"che-pesci-prendere":[],
}

# nomi EN dei link del menu (i titoli dei progetti restano in lingua originale)
def lang_block(lang, slug):
    if lang=="it":
        other = "/en/" if slug=="index" else f"/en/{slug}"
        return f'<p class="lang"><a href="{other}" hreflang="en" lang="en">English</a></p>'
    other = "/" if slug=="index" else f"/{slug}"
    return f'<p class="lang"><a href="{other}" hreflang="it" lang="it">Italiano</a></p>'

def head_fixes(t, lang, slug, title, desc):
    url = SITE + ("/" if slug=="index" else f"/{slug}") if lang=="it" else SITE + ("/en/" if slug=="index" else f"/en/{slug}")
    alt_it = SITE + ("/" if slug=="index" else f"/{slug}")
    alt_en = SITE + ("/en/" if slug=="index" else f"/en/{slug}")
    t = re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', t, 1)
    t = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title,quote=False)}</title>', t, 1, flags=re.S)
    t = re.sub(r'<meta property="og:locale" content="[^"]*" />', f'<meta property="og:locale" content="{"it_IT" if lang=="it" else "en_US"}" />', t, 1)
    for k in ('name="description"','property="og:description"'):
        t = re.sub(r'(<meta '+k+r' content=")[^"]*(" />)', lambda m: m.group(1)+html.escape(desc)+m.group(2), t, 1)
    for k in ('property="og:title"','property="twitter:title"'):
        t = re.sub(r'(<meta '+k+r' content=")[^"]*(" />)', lambda m: m.group(1)+html.escape(title.split(" | ")[0])+m.group(2), t, 1)
    t = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />\n<link rel="alternate" hreflang="it" href="{alt_it}" />\n<link rel="alternate" hreflang="en" href="{alt_en}" />\n<link rel="alternate" hreflang="x-default" href="{alt_it}" />', t, 1)
    t = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{url}" />', t, 1)
    t = re.sub(r'"description":"[^"]*","url":"[^"]*"', f'"description":"{desc}","url":"{url}"', t, 1)
    t = t.replace('<div class="content pure-u-1 pure-u-md-2-5">','<div class="content pure-u-1 pure-u-md-2-5 home-wide">',1)
    t = t.replace('<link rel="stylesheet" href="/assets/css/hydure.css">','<link rel="stylesheet" href="/assets/css/hydure.css">\n  <link rel="stylesheet" href="/assets/css/i18n.css">',1)
    # selettore di lingua + home del brand
    brand_old = '<a class="brand-title" href="/">ilMotorediRicerca</a>'
    assert brand_old in t
    home = "/" if lang=="it" else "/en/"
    t = t.replace(brand_old, f'<a class="brand-title" href="{home}">ilMotorediRicerca</a>\n  {lang_block(lang,slug)}',1)
    # piè di pagina: tag <a> chiuso male, frase inglese sbagliata
    t = t.replace('<a href="https://github.com/zivong/jekyll-theme-hydure" target="_blank">Hydure, developed by <a href="mailto: roorco@gmail.com">Roberto Dell\'Orco</a>',
                  '<a href="https://github.com/zivong/jekyll-theme-hydure" target="_blank">Hydure</a>, developed by <a href="mailto:roorco@gmail.com">Roberto dell’Orco</a>',1)
    t = t.replace("All right reserved.", "Tutti i diritti riservati." if lang=="it" else "All rights reserved.",1)
    if lang=="en":
        t = t.replace("Powered by","Powered by",1)
    return t

def page_parts(t):
    m = re.search(r'(<article class="page">)([\s\S]*?)(</article>)', t)
    return m


def gallery_caption(slug, lang, items):
    """Didascalia unica sotto la griglia. Se in didascalie.yaml c'e' _galleria: {slug: {it:, en:}} usa quella;
    altrimenti, se TUTTE le foto hanno un credito, elenca gli autori."""
    manual = ((yml.get("_galleria") or {}).get(slug) or {}).get(lang, "")
    if manual:
        txt = manual
    else:
        names = []
        for it in items:
            c = (it.get("credit") or "").strip()
            if not c: return ""
            if c not in names: names.append(c)
        txt = ("Immagini: " if lang=="it" else "Images: ") + ", ".join(names) + "."
    return '\n<p class="legende-galerie">' + html.escape(txt) + '</p>'

def grid_for(slug, lang, page_title, yml):
    """Ricostruisce il blocco <p class="photo-grid"> con alt e data-caption."""
    items = yml.get(slug) or []
    n = len(items); out=[]
    for i,it in enumerate(items,1):
        file = it["file"]
        folder = it["dir"]; thumbdir = it.get("thumbdir", folder)
        cap = (it.get(lang) or "").strip(); cr=(it.get("credit") or "").strip()
        full = cap + (" · " if cap and cr else "") + ("© "+cr if cr else "")
        alt = cap if cap else (f"{page_title}, foto {i} di {n}" if lang=="it" else f"{page_title}, photo {i} of {n}")
        out.append(f'<a href="/assets/images/{folder}/{file}" data-caption="{html.escape(full)}"><img src="/assets/images/thumbs/{thumbdir}/{file}" alt="{html.escape(alt)}" loading="lazy" /></a>')
    return '<p class="photo-grid">\n' + "\n".join(out) + '\n</p>' + gallery_caption(slug, lang, items)

def extract_images(slug, t):
    """Dalla pagina originale: elenco (cartella, file, cartella miniature)."""
    res=[]
    for m in re.finditer(r'<a href="/assets/images/([^/"]+)/([^"]+)"><img src="/assets/images/thumbs/([^/"]+)/([^"]+)"', t):
        res.append(dict(dir=m.group(1), file=m.group(2), thumbdir=m.group(3)))
    return res

# ---- didascalie.yaml: se manca, lo crea con tutte le foto e campi vuoti ---------
ypath = os.path.join(HERE,"didascalie.yaml")
orig = {s: rd(s+".html") for s in PAGES}
if not os.path.exists(ypath):
    d={}
    for s in PAGES[1:]:
        d[s]=[dict(file=i["file"],dir=i["dir"],thumbdir=i["thumbdir"],it="",en="",credit="") for i in extract_images(s,orig[s])]
    with open(ypath,"w",encoding="utf-8") as f:
        f.write("# Didascalie delle foto. Per ogni foto: it, en (testo) e credit (autore della foto).\n# Campi vuoti: nessuna didascalia. 'file', 'dir' e 'thumbdir' non vanno modificati.\n")
        yaml.safe_dump(d,f,allow_unicode=True,sort_keys=False,width=1000)
yml = yaml.safe_load(open(ypath,encoding="utf-8"))


# ---- home: lead + schede dei progetti + testo del metodo ----------------------------
CARDS = [
 ("che-pesci-prendere","Che pesci prendere","2011","Bari","Bari",
  "una pescheria temporaneamente chiusa è stata riutilizzata per raccogliere le storie di persone con un cognome di pesce",
  "a temporarily closed fish shop was reused to gather the stories of people with a fish name as a surname"),
 ("oda","Oda, non riesco ad essere infelice","2009","Tirana","Tirana",
  "installazione nel teatro nazionale di Tirana, Albania, che trasforma un luogo dismesso nella corte del teatro in uno spazio pubblico aperto e accogliente",
  "an installation at the national theatre of Tirana, Albania, that turns a disused place in the theatre’s courtyard into an open and welcoming public space"),
 ("adelfia-fratelli","Aδερφια-Fratelli","2009","Pilio, Grecia","Pelion, Greece",
  "ricerca e video performance collettiva sulla ferrovia costruita in Grecia da Evaristo de Chirico (padre di Alberto Savinio e Giorgio de Chirico)",
  "a collective research project and video performance on the railway built in Greece by Evaristo de Chirico (father of Alberto Savinio and Giorgio de Chirico)"),
 ("albania1e1000","Albania 1e1000","2008","Torino","Turin",
  "rivista italo-albanese basata a Torino, sviluppata attraverso un viaggio di esplorazione nel Sud dell’Albania",
  "an Italian-Albanian magazine based in Turin, developed through an exploratory journey in southern Albania"),
 ("otnarat","Otnarat. Taranto a futuro inverso","2009","Taranto","Taranto",
  "cortometraggio che esplora il presente della città di Taranto e un immaginario scenario futuro nascosto sotto la scultura di piazza Fontana",
  "a short film exploring the present of the city of Taranto and an imaginary future scenario hidden beneath the sculpture in Piazza Fontana"),
 ("sogno-cirio","Il Sogno di Francesco Cirio","2013","Torino","Turin",
  "i pomodori venduti al mercato di Porta Palazzo recano incise al laser le parole di Francesco Cirio, pioniere della conservazione in scatola",
  "the tomatoes sold at the Porta Palazzo market bear, laser-engraved, the words of Francesco Cirio, a pioneer of canned food"),
 ("maerchen","Storia di uno che andò via per cercare la paura","2011","Berlino","Berlin",
  "performance collettiva in una notte di luna piena nel cimitero di Sankt Matthaeus",
  "a collective performance on a full-moon night in the Sankt Matthaeus cemetery"),
 ("giardino-radicale","Giardino Radicale","2014","Lecce","Lecce",
  "nel carcere Borgo San Nicola i detenuti, con designer e artisti, trasformano collettivamente gli spazi comuni della loro sezione",
  "inside the Borgo San Nicola prison, detainees and a group of designers and artists collectively transform the common spaces of their section"),
]
HOME_TXT = {
"it": dict(
 lead='<strong>ilMotorediRicerca</strong> è un collettivo fondato nel 2008 da <a class="gold" target="_blank" href="http://www.nicoangiuli.com/"><strong>Nico Angiuli</strong></a>, <strong>Roberto dell’Orco</strong>, <a class="gold" href="http://atelierquartino.com/" target="_blank"><strong>Matteo Fraterno</strong></a> e <strong>Michele Loiacono</strong>. Come un motore di ricerca, ma fisico e non virtuale, ha esplorato territori marginali della contemporaneità, reinterpretando memorie e immaginari collettivi.',
 p1="Ogni progetto nasce in un luogo preciso e dal dialogo con le persone coinvolte: le idee realizzate sono il frutto di questo scambio. Il collettivo si è formato in Puglia e ha immaginato questa terra come una piattaforma protesa nel mare verso la Grecia e i Balcani.",
 p2="Questo sito è l’archivio dei progetti realizzati dal gruppo, dal 2008 al 2014."),
"en": dict(
 lead='<strong>ilMotorediRicerca</strong> is a collective founded in 2008 by <a class="gold" target="_blank" href="http://www.nicoangiuli.com/"><strong>Nico Angiuli</strong></a>, <strong>Roberto dell’Orco</strong>, <a class="gold" href="http://atelierquartino.com/" target="_blank"><strong>Matteo Fraterno</strong></a> and <strong>Michele Loiacono</strong>. Like a search engine, but physical rather than virtual, it has explored marginal territories of the contemporary, reinterpreting collective memories and imaginaries.',
 p1="Each project starts from a specific place and from a dialogue with the people involved: the ideas realised are the fruit of this exchange. The collective formed in Puglia and imagined this land as a platform stretching out into the sea towards Greece and the Balkans.",
 p2="This site is the archive of the projects carried out by the group, from 2008 to 2014."),
}
def home_article(lang):
    T = HOME_TXT[lang]; base = "" if lang=="it" else "/en"
    cards=[]
    for slug,title,year,pl_it,pl_en,b_it,b_en in CARDS:
        place = pl_it if lang=="it" else pl_en
        blurb = (b_it if lang=="it" else b_en)
        blurb = blurb[0].upper()+blurb[1:]+"."
        cards.append(f'<a href="{base}/{slug}" class="card"><span class="card-img"><img src="/assets/images/thumbs/{slug}.jpg" alt="{html.escape(title)}" loading="lazy" /></span><span class="card-meta">{year} · {html.escape(place)}</span><strong class="card-title">{html.escape(title)}</strong><span class="card-text">{html.escape(blurb)}</span></a>')
    return ('<h2 class="page-title"></h2>\n  <p class="lead">'+T["lead"]+'</p>\n\n<div class="cards">\n'+"\n".join(cards)+'\n</div>\n\n<p>'+T["p1"]+'</p>\n<p>'+T["p2"]+'</p>\n')

# ---- pagine --------------------------------------------------------------------
DESC_IT = "Sito archivio dei progetti del collettivo artistico ilMotorediRicerca."
DESC_EN = "Archive of the projects of the art collective ilMotorediRicerca."
NAV_TITLES = {}
for slug in PAGES:
    t = orig[slug]
    # --- italiano
    for a,b in FIX.get(slug,[]):
        t = sub(t,a,b,slug)
    pt = re.search(r'<h2 class="page-title">(.*?)</h2>',t)
    page_title = html.unescape(pt.group(1)) if pt and pt.group(1) else ""
    NAV_TITLES[slug]=page_title
    ttl_it = re.search(r'<title>(.*?)</title>',t).group(1)
    t_it = head_fixes(t,"it",slug,ttl_it,DESC_IT)
    if slug=="index":
        m_ = page_parts(t_it); t_it = t_it[:m_.start(2)] + "\n  " + home_article("it") + t_it[m_.end(2):]
        t_it = t_it.replace('<div class="content pure-u-1 pure-u-md-2-5">','<div class="content pure-u-1 pure-u-md-2-5 home-wide">',1)
    if slug!="index":
        t_it = re.sub(r'<p class="photo-grid">[\s\S]*?</p>', lambda m: grid_for(slug,"it",page_title,yml), t_it, 1)
    wr(("index.html" if slug=="index" else slug+".html"), t_it)

# titoli del menu: in inglese restano gli originali tranne "Contatti"
for slug in PAGES:
    t = orig[slug]
    for a,b in FIX.get(slug,[]): t = t.replace(a,b)
    a = page_parts(t)
    body = EN[slug]["body"] if slug!="index" else home_article("en")
    info_title = page_title = NAV_TITLES[slug]
    pre = ""
    if slug!="index":
        tr = EN[slug].get("title_tr")
        pre = f'<h2 class="page-title">{html.escape(page_title)}</h2>\n  <p class="info">{EN[slug]["info"]}'
        if tr: pre = pre.rstrip() + f'<em>“{html.escape(tr)}”</em></br>'
        pre += '</p>\n  '
        body = pre + body + "\n\n" + grid_for(slug,"en",page_title,yml) + ("\n\n" + re.search(r'<iframe[\s\S]*?</iframe>',t).group(0) if slug=="adelfia-fratelli" else "") + "\n"
    new = t[:a.start(2)] + "\n" + body + t[a.end(2):]
    # menu: link verso le pagine inglesi, "Contatti" -> "Contact"
    if slug=="index": new = new.replace('<div class="content pure-u-1 pure-u-md-2-5">','<div class="content pure-u-1 pure-u-md-2-5 home-wide">',1)
    new = re.sub(r'href="/(che-pesci-prendere|oda|adelfia-fratelli|albania1e1000|otnarat|sogno-cirio|maerchen|giardino-radicale)"', r'href="/en/\1"', new)
    new = new.replace("-Contatti","-Contact")
    new = new.replace('<a class="brand-title" href="/">','<a class="brand-title" href="/">',1)
    ttl = (f"{page_title} | ilMotorediRicerca" if slug!="index" else "ilMotorediRicerca | " + DESC_EN)
    new = head_fixes(new,"en",slug,ttl,DESC_EN)
    wr("en/index.html" if slug=="index" else f"en/{slug}.html", new)

# ---- griglia progetti in home (EN: stessi titoli, link /en/) --------------------
# (i link sono già riscritti sopra; le didascalie della griglia sono i titoli originali)

# ---- file di supporto -------------------------------------------------------------
shutil.copy(os.path.join(HERE,"i18n.css"), os.path.join(OUT,"assets/css/i18n.css")) if os.path.isdir(os.path.join(OUT,"assets/css")) else (os.makedirs(os.path.join(OUT,"assets/css"),exist_ok=True) or shutil.copy(os.path.join(HERE,"i18n.css"), os.path.join(OUT,"assets/css/i18n.css")))
# lightbox: usa data-caption
js = open(os.path.join(SRC,"assets/js/lightbox.js"),encoding="utf-8").read()
a = "var filename = href.split('/').pop();\n                var split = filename.split(\".\");\n                var name = split[0];\n                element.setAttribute('title',name);"
assert a in js
js = js.replace(a, "element.setAttribute('title', element.getAttribute('data-caption') || '');")
os.makedirs(os.path.join(OUT,"assets/js"),exist_ok=True)
open(os.path.join(OUT,"assets/js/lightbox.js"),"w",encoding="utf-8").write(js)
css = open(os.path.join(SRC,"assets/css/lightbox.css"),encoding="utf-8").read()
assert "#lightbox span {display: none;}" in css
css = css.replace("#lightbox span {display: none;}","#lightbox span:empty {display: none;}")
open(os.path.join(OUT,"assets/css/lightbox.css"),"w",encoding="utf-8").write(css)

with open(os.path.join(HERE,"CORREZIONI.txt"),"w",encoding="utf-8") as f:
    for p,a,b in LOG: f.write(f"[{p}] {a[:90]!r} -> {b[:90]!r}\n")
print("ok",len(LOG),"correzioni")
