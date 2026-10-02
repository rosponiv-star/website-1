#!/usr/bin/env python3
"""Genera le pagine HTML statiche di El Magic (header/footer condivisi).

Uso (dalla cartella del progetto, servono Python 3 e Node.js):

    python3 tools/genera-pagine.py

Rigenera index.html, menu/index.html, contatti/index.html e 404.html
leggendo assets/js/data.js. Va lanciato dopo aver cambiato indirizzi,
telefoni, orari o social in data.js (il menù invece si aggiorna da solo).
"""
import json, html, os, subprocess

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.loads(subprocess.check_output(
    ["node", "-e", "global.window={};require('./assets/js/data.js');process.stdout.write(JSON.stringify(window.EL_MAGIC))"],
    cwd=OUT))
SITE = "https://www.elmagic.it/"
GIORNI = ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"]
ORDINE = [1, 2, 3, 4, 5, 6, 0]
DAY_SCHEMA = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
e = html.escape


def svg(body, fill=False, sw="2"):
    if fill:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{body}</svg>'
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'


STAR_PATH = '<path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/>'
ICON = {
    "phone": svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "route": svg('<polygon points="3 11 22 2 13 21 11 13 3 11"/>'),
    "pin": svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    "arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "download": svg('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>'),
    "search": svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', sw="2.2"),
    "menu": svg('<path d="M15 11h.01M11 15h.01M16 16h.01"/><path d="m2 16 20 6-6-20A20 20 0 0 0 2 16"/><path d="M5.71 17.11a17 17 0 0 1 11.4-11.4"/>'),
    "scooter": svg('<circle cx="5.5" cy="17.5" r="2.5"/><circle cx="18.5" cy="17.5" r="2.5"/><path d="M8 17.5h7.5l2-6H14l-2-4H9"/><path d="M15.5 11.5 18.5 17.5"/><path d="M3 11.5h6v3"/>'),
    "users": svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'),
    "wheat": svg('<path d="M2 22 16 8"/><path d="M3.47 12.53 5 11l1.53 1.53a3.5 3.5 0 0 1 0 4.94L5 19l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M7.47 8.53 9 7l1.53 1.53a3.5 3.5 0 0 1 0 4.94L9 15l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M11.47 4.53 13 3l1.53 1.53a3.5 3.5 0 0 1 0 4.94L13 11l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M20 2h2v2a4 4 0 0 1-4 4h-2V6a4 4 0 0 1 4-4Z"/>'),
    "star": svg(STAR_PATH, fill=True),
    "facebook": svg('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "instagram": svg('<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/>'),
}


def sede(i):
    return [s for s in D["sedi"] if s["id"] == i][0]


def foto(name, root, w_small=700, w_big=1300, sizes="(max-width: 760px) 92vw, 33vw", alt="", cls="", lazy=True, w=None, h=None):
    src = f'{root}{D["fotoDir"]}{name}-{w_small}.webp'
    srcset = f'{root}{D["fotoDir"]}{name}-{w_small}.webp {w_small}w, {root}{D["fotoDir"]}{name}-{w_big}.webp {w_big}w'
    dims = f' width="{w}" height="{h}"' if w else ""
    return (f'<img{" class=" + chr(34) + cls + chr(34) if cls else ""} src="{src}" srcset="{srcset}" sizes="{sizes}" alt="{e(alt)}"{dims}'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + ">")


def hours_rows(orari):
    rows = []
    for d in ORDINE:
        o = orari.get(str(d))
        rows.append(f'<tr><th scope="row">{GIORNI[d]}</th><td>{o[0] + " – " + o[1] if o else "Chiuso"}</td></tr>')
    return "".join(rows)


# ------------------------------------------------------------------ parti comuni
def head(title, desc, root, path, extra=""):
    return f"""<!doctype html>
<html lang="it" class="no-js">
<head>
<meta charset="utf-8">
{extra}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#f4eddc">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="El Magic Pizza Fast Food">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}favicon.ico" sizes="48x48">
<link rel="icon" href="{root}assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preload" href="{root}assets/fonts/anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/style.css">
"""


def ticker():
    items = ["Pizza con lievito madre", "Kebab 100% halal", "Aperti 7 giorni su 7", "Cles · Val di Non",
             "Malé · Val di Sole", "Senza glutine su richiesta", "Domicilio a Cles"]
    row = "".join(f"<span>{e(i)}</span>" for i in items)
    return f'<div class="ticker" aria-hidden="true"><div class="ticker__track">{row}{row}</div></div>\n'


def header(root, current):
    home = root or "./"

    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<a class="skip-link" href="#main">Vai al contenuto</a>
{ticker()}<header class="site-header">
  <div class="container">
    <a class="brand" href="{home}" aria-label="El Magic, torna alla home">
      <img src="{root}assets/img/logo-360.webp" alt="El Magic Pizza Fast Food" width="53" height="58">
    </a>
    <nav class="nav" aria-label="Principale">
      {link(home, "Home", "home")}
      {link(root + "menu/", "Menù", "menu")}
      {link(root + "contatti/", "Contatti", "contatti")}
    </nav>
    <div class="header-actions">
      <span class="header-status"><span class="status" data-status="cles" data-label="Cles">Cles</span></span>
      <a class="btn btn--red btn--sm" href="{root}contatti/" data-call>{ICON["phone"]}Chiama</a>
    </div>
  </div>
</header>
"""


def footer(root, after_red=False):
    cles, male = sede("cles"), sede("male")
    soc = D["social"]
    lead = '<div class="mountains mountains--flip" aria-hidden="true"></div>\n' if after_red else '<div class="checker" aria-hidden="true"></div>\n'
    return lead + f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <p class="footer-claim">Pizza, kebab <span class="script">e un pizzico di magia</span></p>
        <div class="socials">
          <a href="{soc["instagram"]["url"]}" target="_blank" rel="noopener" aria-label="Instagram @{e(soc["instagram"]["label"])}">{ICON["instagram"]}</a>
          <a href="{soc["facebook"]["url"]}" target="_blank" rel="noopener" aria-label="Facebook {e(soc["facebook"]["label"])}">{ICON["facebook"]}</a>
        </div>
      </div>
      <div>
        <h2>Cles</h2>
        <ul class="footer-list">
          <li><a href="{cles["mappa"]}" target="_blank" rel="noopener">{e(cles["indirizzo"])}</a><small>{cles["cap"]} {e(cles["citta"])}</small></li>
          <li><a href="tel:{cles["telefono"]}">{cles["telefonoVisibile"]}</a></li>
          <li><small>Tutti i giorni · orario continuato</small></li>
        </ul>
      </div>
      <div>
        <h2>Malé</h2>
        <ul class="footer-list">
          <li><a href="{male["mappa"]}" target="_blank" rel="noopener">{e(male["indirizzo"])}</a><small>{male["cap"]} {e(male["citta"])}</small></li>
          <li><a href="tel:{male["telefono"]}">{male["telefonoVisibile"]}</a></li>
          <li><small>Tutti i giorni · 11:00 – 01:30</small></li>
        </ul>
      </div>
      <div>
        <h2>Esplora</h2>
        <ul class="footer-list">
          <li><a href="{root or './'}">Home</a></li>
          <li><a href="{root}menu/">Menù</a></li>
          <li><a href="{root}contatti/">Contatti e orari</a></li>
          <li><a href="{root}{D["menuPdf"]}" data-menu-pdf download>Menù in PDF</a></li>
        </ul>
      </div>
    </div>
  </div>
  <span class="wordmark" aria-hidden="true">El Magic</span>
  <div class="container footer-bottom">
    <span>© <span data-year>2026</span> El Magic · Pizza · Fast Food</span>
    <span>Le foto sono a scopo illustrativo · Prezzi e orari possono variare</span>
  </div>
</footer>

<nav class="mobile-bar" aria-label="Azioni rapide">
  <a href="{root}menu/">{ICON["menu"]}Menù</a>
  <a class="is-primary" href="{root}contatti/" data-call>{ICON["phone"]}Chiama</a>
  <a href="{root}contatti/#sedi">{ICON["route"]}Sedi</a>
</nav>
"""


def scripts(root, extra=""):
    s = f'<script src="{root}assets/js/data.js" defer></script>\n<script src="{root}assets/js/main.js" defer></script>\n'
    if extra:
        s += f'<script src="{root}assets/js/{extra}" defer></script>\n'
    return s


def jsonld():
    items = []
    for s in D["sedi"]:
        spec = []
        for d in range(7):
            o = s["orari"].get(str(d))
            if o:
                spec.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_SCHEMA[d], "opens": o[0], "closes": o[1]})
        items.append({
            "@type": "Restaurant",
            "name": f"El Magic {s['nome']}",
            "image": SITE + "assets/img/og-image.jpg",
            "logo": SITE + "assets/img/logo-720.webp",
            "url": SITE,
            "telephone": s["telefono"],
            "servesCuisine": ["Pizza", "Kebab", "Fast food"],
            "priceRange": "€",
            "hasMenu": SITE + "menu/",
            "address": {"@type": "PostalAddress", "streetAddress": s["indirizzo"], "postalCode": s["cap"],
                        "addressLocality": s["citta"].replace(" (TN)", ""), "addressRegion": "TN", "addressCountry": "IT"},
            "openingHoursSpecification": spec,
            "sameAs": [D["social"]["instagram"]["url"], D["social"]["facebook"]["url"]],
        })
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False) + "</script>\n"


def eyebrow(text, cls=""):
    return f'<span class="eyebrow {cls}">{text}</span>'


def services(s):
    return " · ".join(x.replace("Posti a sedere", "Sala").replace("Consegna a domicilio", "Domicilio") for x in s["servizi"])


def badge_spin():
    return f"""<div class="badge-spin" aria-hidden="true">
      <svg viewBox="0 0 200 200"><defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
        <circle cx="100" cy="100" r="99" fill="#1b1515"/>
        <text fill="#f4eddc" font-family="Anton, Impact, sans-serif" font-size="19" letter-spacing="3.2"><textPath href="#circ">LIEVITO MADRE ✦ 100% HALAL ✦ CLES ✦ MALÉ ✦</textPath></text>
      </svg>
      <span class="badge-spin__core">{ICON["star"]}</span>
    </div>"""


# ------------------------------------------------------------------------ HOME
def page_home():
    root = ""
    cles, male = sede("cles"), sede("male")
    h = head("El Magic | Pizza e kebab a Cles e Malé",
             "Pizza con impasto a lievito madre, kebab 100% halal, panini e piadine a Cles e Malé (TN). Aperti tutti i giorni con orario continuato. Impasto senza glutine su richiesta.",
             root, "")
    h += jsonld() + '</head>\n<body data-root="">\n' + header(root, "home")

    def place_card(s):
        return f"""<article class="place reveal">
          <div class="place__top">
            <div><h3 class="place__name">{e(s["nome"])}</h3><span class="place__valley">{e(s["valle"])}</span></div>
            <span class="pill"><span class="status" data-status="{s["id"]}">Orario continuato</span></span>
          </div>
          <div class="place__rows">
            <div class="place__row"><span>Indirizzo</span><a href="{s["mappa"]}" target="_blank" rel="noopener">{e(s["indirizzo"])}, {e(s["citta"])}</a></div>
            <div class="place__row"><span>Telefono</span><a href="tel:{s["telefono"]}">{s["telefonoVisibile"]}</a></div>
            <div class="place__row"><span>Oggi</span><span data-today="{s["id"]}">Orario continuato</span></div>
            <div class="place__row"><span>Servizi</span><span>{e(services(s))}</span></div>
          </div>
          <div class="place__actions">
            <a class="btn btn--red" href="tel:{s["telefono"]}">{ICON["phone"]}Chiama</a>
            <a class="btn btn--outline" href="{s["mappa"]}" target="_blank" rel="noopener">{ICON["route"]}Indicazioni</a>
          </div>
        </article>"""

    marquee_items = ["Pizza", "Kebab", "Piadine", "Calzoni", "Panini", "Box kebab", "Patatine"]
    mrow = "".join(f"<span>{i}</span>" for i in marquee_items)

    h += f"""
<main id="main">
  <section class="hero">
    <div class="container">
      <div class="hero__stage">
        <div class="hero__left">
          {eyebrow("Pizzeria · Kebab — Cles &amp; Malé")}
          <div class="hero__type" aria-hidden="true"><span>Pizza</span><span><span class="hero__amp">&amp;</span>Kebab</span></div>
          <h1>Pizza a lievito madre e kebab 100% halal, <em>a Cles e Malé.</em></h1>
          <div class="hero__actions">
            <a class="btn btn--red" href="menu/">Scopri il menù{ICON["arrow"]}</a>
            <a class="btn btn--outline" href="contatti/" data-call>{ICON["phone"]}Chiama</a>
          </div>
          <div class="hero__live">
            <span class="pill"><span class="status" data-status="cles" data-label="Cles">Cles</span></span>
            <span class="pill"><span class="status" data-status="male" data-label="Malé">Malé</span></span>
          </div>
        </div>
        <div class="hero__right">
          <img class="hero__slice" src="assets/img/foto/pizza-trancio-700.webp" srcset="assets/img/foto/pizza-trancio-700.webp 700w, assets/img/foto/pizza-trancio-1200.webp 1200w" sizes="(max-width: 760px) 92vw, 46vw" width="1200" height="1206" alt="Trancio di pizza margherita sollevato, con la mozzarella che fila" fetchpriority="high">
          <div class="hero__stamp" aria-hidden="true"><small>Pizze da</small><strong>7€</strong></div>
          <span class="callout callout--1" aria-hidden="true"><i></i>Lievito madre</span>
          <span class="callout callout--2" aria-hidden="true"><i></i>Mozzarella filante</span>
          <span class="hero__script" aria-hidden="true">un pizzico di magia</span>
        </div>
        <img class="hero__kebab" src="assets/img/foto/panino-kebab-500.webp" srcset="assets/img/foto/panino-kebab-500.webp 500w, assets/img/foto/panino-kebab-900.webp 900w" sizes="(max-width: 760px) 40vw, 17vw" width="900" height="878" alt="Panino kebab con carne, insalata, pomodoro e salsa">
      </div>
    </div>
  </section>

  <div class="checker" style="position:relative" aria-hidden="true">{badge_spin()}</div>

  <section class="manifesto">
    <div class="sticker sticker--1" aria-hidden="true">{foto("impasto", root, sizes="230px", alt="")}</div>
    <div class="sticker sticker--2" aria-hidden="true"><img src="assets/img/foto/patatine-500.webp" alt="" loading="lazy" style="object-fit:contain"></div>
    <div class="container">
      <span class="manifesto__script reveal">Il nostro segreto</span>
      <h2 class="manifesto__text reveal">Il trucco c'è, ma non si vede. <em>Si sente</em> al primo morso.</h2>
      <p class="reveal">Nessuna bacchetta magica: impasti a lievito madre, il tempo giusto e ingredienti italiani di qualità. Un fast food veloce quando hai fame, e lento dove serve.</p>
      <a class="btn btn--cream reveal" href="menu/">Sfoglia il menù{ICON["arrow"]}</a>
    </div>
  </section>

  <div class="marquee" aria-hidden="true"><div class="marquee__track">{mrow}{mrow}</div></div>

  <section class="section">
    <div class="container">
      <div class="section-head section-head--split">
        <div class="reveal">{eyebrow("Gli assi nella manica")}<h2 class="display title-lg">Scegli il tuo <span class="script">preferito</span></h2></div>
        <p class="lead reveal">Più di sessanta proposte e tre grandi classici di casa: la pizza a lievito madre, il kebab halal e la via di mezzo che mette tutti d'accordo.</p>
      </div>
      <div class="aces">
        <a class="ace reveal" href="menu/#classiche">
          {foto("margherita", root, alt="Pizza margherita vista dall'alto")}
          <div><span class="ace__num">01 — Pizze</span><h3 class="ace__title">Pizza<span class="script">a lievito madre</span></h3></div>
          <div class="ace__foot"><p>54 pizze tra classiche, specialità e fantasie del pizzaiolo.</p><span class="price-coin"><small>da</small><strong>7€</strong></span></div>
        </a>
        <a class="ace reveal reveal-d1" href="menu/#kebab">
          {foto("piadina-kebab", root, alt="Piadina kebab con carne, insalata, pomodoro e salsa")}
          <div><span class="ace__num">02 — Kebab</span><h3 class="ace__title">Kebab<span class="script">100% halal</span></h3></div>
          <div class="ace__foot"><p>Panini, piadine e box. Con il Menù: patatine e lattina.</p><span class="price-coin"><small>da</small><strong>5€</strong></span></div>
        </a>
        <a class="ace ace--receipt reveal reveal-d2" href="menu/#pizza-kebab">
          {foto("pizza-kebab", root, alt="Pizza kebab con cipolla rossa e salsa bianca")}
          <div class="receipt">
            <div class="receipt__head"><span>El Magic</span><span>N° 03</span></div>
            <h3>Pizza kebab completa</h3>
            <p>Pomodoro, mozzarella, carne kebab, verdure, salsa e patatine.</p>
            <div class="receipt__row"><span>Normale</span><span>12,00 €</span></div>
            <div class="receipt__row"><span>Maxi</span><span>25,00 €</span></div>
            <div class="receipt__total"><span>TOTALE</span><strong>Magia</strong></div>
            <div class="barcode"></div>
          </div>
        </a>
      </div>
    </div>
  </section>

  <section class="section trick on-dark">
    <div class="container trick__grid">
      <div class="reveal">
        {eyebrow("Indeciso?", "eyebrow--light")}
        <h2 class="display title-lg">Pesca <span class="script">una carta</span></h2>
        <p>Non sai cosa ordinare? Lascia fare al mago. Pesca una carta e ti diciamo noi cosa provare stasera. Non ti convince? Rimescola: le carte non finiscono mai.</p>
        <button class="btn btn--red" type="button" data-trick-btn>{ICON["star"]}Pesca una carta</button>
      </div>
      <div class="deck reveal reveal-d1" data-trick>
        <div class="deck__ghost"></div><div class="deck__ghost"></div>
        <div class="card" role="button" tabindex="0" aria-label="Pesca una carta">
          <div class="card__face card__back"><img src="assets/img/emblema.webp" alt="" width="512" height="512"></div>
          <div class="card__face card__front" aria-live="polite">
            <span class="card__corner card__corner--tl">A{ICON["star"]}</span>
            <span class="card__corner card__corner--br">A{ICON["star"]}</span>
            <span class="card__cat"></span><p class="card__name"></p><p class="card__desc"></p><p class="card__price"></p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head section-head--split">
        <div class="reveal">{eyebrow("Come funziona")}<h2 class="display title-lg">Tre mosse <span class="script">e voilà</span></h2></div>
        <p class="lead reveal">Mangia da noi, porta via o, a Cles, fattela portare a casa. Come preferisci tu.</p>
      </div>
      <ol class="steps">
        <li class="step reveal"><div class="step__img">{foto("pizza-porcini", root, alt="Pizza con funghi porcini e speck")}</div>
          <div class="step__head"><span class="step__num">Step 1</span><h3>Scegli</h3></div>
          <p>Sfoglia il menù: pizze, kebab, piadine e panini. Anche con impasto senza glutine o mozzarella senza lattosio.</p></li>
        <li class="step reveal reveal-d1"><div class="step__img">{foto("impasto", root, alt="Mani infarinate che lavorano l'impasto della pizza")}</div>
          <div class="step__head"><span class="step__num">Step 2</span><h3>Ordina</h3></div>
          <p>Chiama la sede più vicina, passa a trovarci o siediti da noi. Se siete in tanti, avvisaci prima.</p></li>
        <li class="step reveal reveal-d2"><div class="step__img">{foto("forno", root, alt="Pizza appena sfornata")}</div>
          <div class="step__head"><span class="step__num">Step 3</span><h3>Abracadabra</h3></div>
          <p>Il tempo di cuocerla ed è pronta: calda, fragrante, tua. Il resto è magia.</p></li>
      </ol>
    </div>
  </section>

  <div class="mountains" aria-hidden="true"></div>
  <section class="places on-dark" id="sedi">
    <div class="container">
      <div class="section-head section-head--split">
        <div class="reveal">{eyebrow("Dove trovarci", "eyebrow--light")}<h2 class="display title-lg">Due valli, <span class="script">una magia</span></h2></div>
        <p class="lead reveal">Val di Non e Val di Sole: due forni accesi tutto il giorno, sette giorni su sette.</p>
      </div>
      <div class="places__grid">
        {place_card(cles)}
        {place_card(male)}
      </div>
      <div class="delivery-strip reveal">
        <div class="delivery-strip__icon">{ICON["scooter"]}</div>
        <div><h3>A Cles arriviamo noi</h3><p>{e(cles["domicilio"]["nota"])} Chiama e ordina.</p></div>
        <a class="btn btn--cream" href="tel:{cles["telefono"]}">{ICON["phone"]}{cles["telefonoVisibile"]}</a>
      </div>
    </div>
  </section>
</main>
"""
    h += footer(root, after_red=True) + scripts(root) + "</body>\n</html>\n"
    return h


# ------------------------------------------------------------------------ MENU
def page_menu():
    root = "../"
    h = head("Menù | El Magic Cles e Malé",
             "Il menù completo di El Magic: pizze classiche e speciali a lievito madre, kebab, panini, piadine e bibite. Prezzi, ingredienti e allergeni.",
             root, "menu/")
    h += '</head>\n<body data-root="../">\n' + header(root, "menu")
    filters = [("all", "Tutto"), ("veg", "Vegetariane"), ("hot", "Piccanti"), ("mare", "Di mare"), ("top", "Consigliate")]
    fbtn = "".join(f'<button class="chip" type="button" data-filter="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in filters)
    h += f"""
<main id="main">
  <section class="menu-hero">
    <div class="menu-hero__bg" aria-hidden="true">{foto("ingredienti", root, w_small=1000, w_big=2048, sizes="100vw", alt="", lazy=False)}</div>
    <div class="container">
      {eyebrow("Stessi prezzi a Cles e Malé", "eyebrow--center")}
      <h1>Il menù <span class="script">dal forno a te</span></h1>
      <p>Pizze a lievito madre, kebab, piadine e panini. Cerca il tuo piatto, filtra per gusto o escludi gli allergeni.</p>
      <a class="btn" href="../{D["menuPdf"]}" data-menu-pdf download>{ICON["download"]}Scarica il menù in PDF</a>
    </div>
  </section>

  <div class="menu-bar">
    <div class="container"><nav class="menu-tabs" id="menu-tabs" aria-label="Categorie del menù"></nav></div>
  </div>

  <div class="container">
    <div class="menu-filters">
      <label class="search">
        <span class="visually-hidden">Cerca nel menù</span>
        {ICON["search"]}
        <input id="menu-search" type="search" placeholder="Cerca: tonno, bufala, kebab…" autocomplete="off" enterkeyhint="search">
      </label>
      <div class="chips" role="group" aria-label="Filtra per tipo">
        {fbtn}
        <button class="chip chip--allergens" id="allergen-toggle" type="button" aria-expanded="false" aria-controls="allergen-panel">Escludi allergeni</button>
      </div>
    </div>
    <div class="allergen-panel" id="allergen-panel" hidden>
      <p>Tocca gli allergeni da evitare: nascondiamo i piatti che li contengono.</p>
      <div class="allergen-list" id="allergen-list"></div>
    </div>
    <div class="legend" id="menu-legend"></div>

    <div id="menu-root"></div>
    <div class="menu-empty" id="menu-empty" hidden>
      <strong>Nessun piatto trovato</strong>
      <p>Prova a cambiare ricerca o filtri.</p>
      <button class="btn btn--outline btn--sm" type="button" id="menu-reset">Azzera i filtri</button>
    </div>
    <noscript><p class="menu-empty">Per il menù interattivo attiva JavaScript, oppure <a href="../{D["menuPdf"]}">scarica il menù in PDF</a>.</p></noscript>

    <div class="menu-notes">
      <div class="note"><h3>Come la vuoi tu</h3><p>Aggiunte o variazioni da 0,50 € fino a un massimo di 3 €. Il Menù di kebab e panini include patatine e lattina.</p></div>
      <div class="note"><h3>Impasti</h3><p>Tutti i nostri impasti lievitano con lievito madre. Su richiesta: integrale (+1 €) e senza glutine (+2,5 €). Mozzarella senza lattosio disponibile.</p></div>
      <div class="note"><h3>Allergeni</h3><p>Gli allergeni indicati seguono il nostro menù ufficiale. In caso di allergie o intolleranze parla sempre con il personale prima di ordinare.</p></div>
    </div>
    <p class="legal">Negli alimenti e nelle bevande preparati e somministrati possono essere presenti ingredienti o coadiuvanti considerati allergeni (Reg. UE 1169/2011, allegato II). * Alcuni prodotti possono essere surgelati all'origine o congelati in loco: chiedi al personale. Tutti i nostri prodotti sono di alta qualità italiana. Le foto sono a scopo illustrativo.</p>
  </div>
</main>
"""
    h += footer(root) + scripts(root, "menu.js") + "</body>\n</html>\n"
    return h


# -------------------------------------------------------------------- CONTATTI
def page_contatti():
    root = "../"
    soc = D["social"]
    h = head("Contatti e orari | El Magic Cles e Malé",
             "Indirizzi, telefoni e orari di El Magic a Cles (Via Trento 6) e Malé (Via Brescia 18). Sala, asporto e consegna a domicilio a Cles.",
             root, "contatti/")
    h += '</head>\n<body data-root="../">\n' + header(root, "contatti")

    def loc(s, alt=False):
        delivery = ""
        if s.get("domicilio"):
            delivery = f'''<div class="board__delivery">{ICON["scooter"]}<p><strong>Consegna a domicilio</strong>{e(s["domicilio"]["nota"])}<br><span class="status" data-delivery-status="{s["id"]}"></span></p></div>'''
        chips = "".join(f'<span class="tag-soft">{e(x)}</span>' for x in s["servizi"])
        return f"""<section class="loc{' loc--alt' if alt else ''}" id="sede-{s["id"]}">
    <div class="container loc__grid">
      <div class="loc__info reveal">
        <h2 class="loc__name">{e(s["nome"])}</h2>
        <span class="loc__valley">{e(s["valle"])}</span>
        <span class="pill"><span class="status" data-status="{s["id"]}">Orario continuato</span></span>
        <div class="place__rows">
          <div class="place__row"><span>Indirizzo</span><a href="{s["mappa"]}" target="_blank" rel="noopener">{e(s["indirizzo"])}, {s["cap"]} {e(s["citta"])}</a></div>
          <div class="place__row"><span>Telefono</span><a href="tel:{s["telefono"]}">{s["telefonoVisibile"]}</a></div>
        </div>
        <div class="tags-row">{chips}</div>
        <div class="place__actions" style="margin-top:26px">
          <a class="btn btn--red" href="tel:{s["telefono"]}">{ICON["phone"]}Chiama {e(s["nome"])}</a>
          <a class="btn btn--outline" href="{s["mappa"]}" target="_blank" rel="noopener">{ICON["route"]}Indicazioni</a>
        </div>
      </div>
      <div class="reveal reveal-d1">
        <div class="board">
          <h3>Orari <span class="status" data-status="{s["id"]}"></span></h3>
          <table class="hours" data-hours="{s["id"]}"><caption class="visually-hidden">Orari {e(s["nome"])}</caption><tbody>{hours_rows(s["orari"])}</tbody></table>
          {delivery}
        </div>
        <div class="map"><div class="map__ph"><button class="btn btn--outline btn--sm" type="button" data-map-load="{s["id"]}">{ICON["pin"]}Mostra la mappa</button><p>La mappa viene caricata da Google Maps solo se la apri.</p></div></div>
      </div>
    </div>
  </section>"""

    h += f"""
<main id="main">
  <section class="c-hero">
    <div class="container c-hero__grid">
      <div class="reveal">
        {eyebrow("Contatti")}
        <h1>Vieni a <span class="script">trovarci</span></h1>
        <p class="lead" style="margin-top:22px">Siamo aperti tutti i giorni con orario continuato. Chiama per l'asporto, siediti da noi o, a Cles, fattela portare a casa.</p>
        <div class="hero__actions" style="margin-top:28px">
          <a class="btn btn--red" href="#sedi" data-call>{ICON["phone"]}Chiama</a>
          <a class="btn btn--outline" href="../menu/">Vedi il menù{ICON["arrow"]}</a>
        </div>
      </div>
      <div class="c-hero__photo reveal reveal-d1">
        {foto("impasto", root, sizes="(max-width: 900px) 92vw, 40vw", alt="Mani infarinate che lavorano l'impasto della pizza", lazy=False)}
        <div class="hero__stamp" aria-hidden="true"><small>Aperti</small><strong>7/7</strong></div>
      </div>
    </div>
  </section>

  <div id="sedi">
  {loc(sede("cles"))}
  {loc(sede("male"), alt=True)}
  </div>

  <section class="section" style="border-top:1.5px solid var(--ink)">
    <div class="container">
      <div class="section-head section-head--split">
        <div class="reveal">{eyebrow("Buono a sapersi")}<h2 class="display title-md">Prima di <span class="script">passare</span></h2></div>
      </div>
      <div class="perks">
        <div class="perk reveal"><div class="perk__icon">{ICON["users"]}</div><h3>Siete in tanti?</h3><p>Di solito non serve prenotare. Se venite in gruppo, chiamateci prima e vi teniamo i tavoli.</p></div>
        <div class="perk reveal reveal-d1"><div class="perk__icon">{ICON["scooter"]}</div><h3>Domicilio a Cles</h3><p>Dalle 19:00 alle 21:00, tutti i giorni tranne il martedì. Consegniamo noi, senza app.</p></div>
        <div class="perk reveal reveal-d2"><div class="perk__icon">{ICON["wheat"]}</div><h3>Per tutti</h3><p>Impasto senza glutine, mozzarella senza lattosio, piatti vegetariani. Tutto 100% halal.</p></div>
        <div class="perk reveal reveal-d3"><div class="perk__icon">{ICON["menu"]}</div><h3>Il menù</h3><p>Sfoglialo <a href="../menu/">online</a> o <a href="../{D["menuPdf"]}" data-menu-pdf download>scaricalo in PDF</a>. Stessi prezzi nelle due sedi.</p></div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0; text-align:center">
    <div class="container reveal">
      {eyebrow("Seguici", "eyebrow--center")}
      <h2 class="display title-lg" style="margin-bottom:28px">@{e(soc["instagram"]["label"])}</h2>
      <div class="social-big">
        <a class="btn btn--red" href="{soc["instagram"]["url"]}" target="_blank" rel="noopener">{ICON["instagram"]}Instagram</a>
        <a class="btn btn--outline" href="{soc["facebook"]["url"]}" target="_blank" rel="noopener">{ICON["facebook"]}Facebook</a>
      </div>
    </div>
  </section>
</main>
"""
    h += footer(root) + scripts(root) + "</body>\n</html>\n"
    return h


# ------------------------------------------------------------------------- 404
def page_404():
    # Servita da qualsiasi percorso: un <base> punta alla radice del sito
    # (dominio proprio su Cloudflare, oppure /nome-repo/ su GitHub Pages).
    root = ""
    base = """<script>(function(){var b="/";if(/\\.github\\.io$/.test(location.hostname)){var s=location.pathname.split("/")[1];if(s)b="/"+s+"/";}document.write('<base href="'+b+'">');})();</script>
<meta name="robots" content="noindex">
"""
    h = head("Pagina non trovata | El Magic", "La pagina che cerchi non esiste.", root, "404.html", extra=base)
    h += '</head>\n<body data-root="">\n' + header(root, "")
    h += f"""
<main id="main">
  <section class="nf">
    <div class="container">
      <h1>404 <span class="script">questa pagina è sparita</span></h1>
      <p>Dev'essere stata una magia venuta male. Torniamo a cose più buone?</p>
      <div class="hero__actions">
        <a class="btn btn--red" href="./">Torna alla home</a>
        <a class="btn btn--outline" href="menu/">Vai al menù{ICON["arrow"]}</a>
      </div>
    </div>
  </section>
</main>
"""
    h += footer(root) + scripts(root) + "</body>\n</html>\n"
    return h


os.makedirs(f"{OUT}/menu", exist_ok=True)
os.makedirs(f"{OUT}/contatti", exist_ok=True)
open(f"{OUT}/index.html", "w").write(page_home())
open(f"{OUT}/menu/index.html", "w").write(page_menu())
open(f"{OUT}/contatti/index.html", "w").write(page_contatti())
open(f"{OUT}/404.html", "w").write(page_404())
print("ok")
