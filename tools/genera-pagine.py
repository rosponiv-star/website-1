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

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "route": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 11h.01M11 15h.01M16 16h.01"/><path d="m2 16 20 6-6-20A20 20 0 0 0 2 16"/><path d="M5.71 17.11a17 17 0 0 1 11.4-11.4"/></svg>',
    "download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "scooter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="5.5" cy="17.5" r="2.5"/><circle cx="18.5" cy="17.5" r="2.5"/><path d="M8 17.5h7.5l2-6H14l-2-4H9"/><path d="M15.5 11.5 18.5 17.5"/><path d="M3 11.5h6v3"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>',
    "wheat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 22 16 8"/><path d="M3.47 12.53 5 11l1.53 1.53a3.5 3.5 0 0 1 0 4.94L5 19l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M7.47 8.53 9 7l1.53 1.53a3.5 3.5 0 0 1 0 4.94L9 15l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M11.47 4.53 13 3l1.53 1.53a3.5 3.5 0 0 1 0 4.94L13 11l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M20 2h2v2a4 4 0 0 1-4 4h-2V6a4 4 0 0 1 4-4Z"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="currentColor"/><path class="ic-fg" fill="#fff" d="M15.4 12.6h-2.1V20h-3v-7.4H8.8v-2.6h1.5V8.4c0-2 .9-3.4 3.4-3.4h2v2.6h-1.3c-.9 0-1.1.4-1.1 1.1v1.3h2.4l-.3 2.6Z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="currentColor"/><rect class="ic-st" x="5.5" y="5.5" width="13" height="13" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle class="ic-st" cx="12" cy="12" r="3.1" fill="none" stroke="#fff" stroke-width="1.8"/><circle class="ic-fg" cx="15.9" cy="8.1" r="1" fill="#fff"/></svg>',
}


def sede(i):
    return [s for s in D["sedi"] if s["id"] == i][0]


def hours_rows(orari):
    rows = []
    for d in ORDINE:
        o = orari.get(str(d))
        rows.append(f'<tr><th scope="row">{GIORNI[d]}</th><td>{o[0] + " – " + o[1] if o else "Chiuso"}</td></tr>')
    return "".join(rows)


def head(title, desc, root, path):
    return f"""<!doctype html>
<html lang="it" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#be1c2f">
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
<link rel="preload" href="{root}assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/style.css">
"""


def header(root, current):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{root}{href}"{cur}>{label}</a>'
    return f"""<a class="skip-link" href="#main">Vai al contenuto</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{root or './'}" aria-label="El Magic, torna alla home">
      <img src="{root}assets/img/logo-360.webp" alt="El Magic Pizza Fast Food" width="47" height="52">
    </a>
    <nav class="nav" aria-label="Principale">
      {link("", "Home", "home").replace(f'href="{root}"', f'href="{root or "./"}"')}
      {link("menu/", "Menù", "menu")}
      {link("contatti/", "Contatti", "contatti")}
    </nav>
    <a class="btn btn--sm header-cta" href="{root}contatti/" data-call>{ICON["phone"]}Chiama</a>
  </div>
</header>
"""


def footer(root):
    cles, male = sede("cles"), sede("male")
    soc = D["social"]
    return f"""<footer class="site-footer torn-top">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/logo-360.webp" alt="El Magic Pizza Fast Food" width="120" height="132" loading="lazy">
        <p>Pizza con lievito madre, kebab e panini. A Cles e Malé, tutti i giorni con orario continuato.</p>
        <div class="footer-social">
          <a href="{soc["instagram"]["url"]}" target="_blank" rel="noopener" aria-label="Instagram @{e(soc["instagram"]["label"])}">{ICON["instagram"]}</a>
          <a href="{soc["facebook"]["url"]}" target="_blank" rel="noopener" aria-label="Facebook {e(soc["facebook"]["label"])}">{ICON["facebook"]}</a>
        </div>
      </div>
      <div>
        <h2>Le nostre sedi</h2>
        <ul class="footer-list">
          <li><a href="tel:{cles["telefono"]}">Cles · {cles["telefonoVisibile"]}</a><span>{e(cles["indirizzo"])}, {cles["cap"]} {e(cles["citta"])}</span></li>
          <li><a href="tel:{male["telefono"]}">Malé · {male["telefonoVisibile"]}</a><span>{e(male["indirizzo"])}, {male["cap"]} {e(male["citta"])}</span></li>
        </ul>
      </div>
      <div>
        <h2>Esplora</h2>
        <ul class="footer-list">
          <li><a href="{root or './'}">Home</a></li>
          <li><a href="{root}menu/">Menù</a></li>
          <li><a href="{root}contatti/">Contatti e orari</a></li>
          <li><a href="{root}{D["menuPdf"]}" data-menu-pdf download>Scarica il menù (PDF)</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> El Magic · Pizza · Fast Food</span>
      <span>Prezzi e orari possono variare: nel dubbio, chiamaci.</span>
    </div>
  </div>
</footer>

<nav class="mobile-bar" aria-label="Azioni rapide">
  <a href="{root}menu/">{ICON["menu"]}Menù</a>
  <a class="is-primary" href="{root}contatti/" data-call>{ICON["phone"]}Chiama</a>
  <a href="{root}contatti/#sedi">{ICON["route"]}Indicazioni</a>
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
            "logo": SITE + "assets/img/logo.png",
            "url": SITE,
            "telephone": s["telefono"],
            "servesCuisine": ["Pizza", "Kebab", "Fast food"],
            "priceRange": "€",
            "acceptsReservations": "False",
            "hasMenu": SITE + "menu/",
            "address": {"@type": "PostalAddress", "streetAddress": s["indirizzo"], "postalCode": s["cap"],
                        "addressLocality": s["citta"].replace(" (TN)", ""), "addressRegion": "TN", "addressCountry": "IT"},
            "openingHoursSpecification": spec,
            "sameAs": [D["social"]["instagram"]["url"], D["social"]["facebook"]["url"]],
        })
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False) + "</script>\n"


def sede_card(s, root, full=False):
    services = "".join(f'<li class="chip{" chip--green" if "domicilio" in x.lower() else ""}">{e(x)}</li>' for x in s["servizi"])
    today = f'<p class="sede-card__line">{ICON["clock"]}<span>Oggi: <span data-today="{s["id"]}">orario continuato</span></span></p>' if not full else ""
    extra = ""
    if full:
        extra += f'<table class="hours" data-hours="{s["id"]}"><caption class="visually-hidden">Orari {e(s["nome"])}</caption><tbody>{hours_rows(s["orari"])}</tbody></table>'
        if s.get("domicilio"):
            extra += f'''<div class="delivery">{ICON["scooter"]}<div><strong>Consegna a domicilio</strong><p>{e(s["domicilio"]["nota"])}</p><p><span data-delivery-status="{s["id"]}"></span></p></div></div>'''
        extra += f'''<div class="map"><div class="map__placeholder"><button class="btn btn--sm btn--ghost" type="button" data-map-load="{s["id"]}">{ICON["pin"]}Mostra la mappa</button><p>La mappa viene caricata da Google Maps solo se la apri.</p></div></div>'''
    return f"""<article class="sede-card{' contact-card' if full else ''} reveal" id="sede-{s["id"]}">
        <div class="sede-card__top">
          <div><h3 class="sede-card__name">{e(s["nome"])}</h3><span class="sede-card__valley">{e(s["valle"])}</span></div>
          <span class="status" data-status="{s["id"]}">Orario continuato</span>
        </div>
        <p class="sede-card__line">{ICON["pin"]}<a href="{s["mappa"]}" target="_blank" rel="noopener">{e(s["indirizzo"])}, {s["cap"]} {e(s["citta"])}</a></p>
        <p class="sede-card__line">{ICON["phone"]}<a href="tel:{s["telefono"]}">{s["telefonoVisibile"]}</a></p>
        {today}
        <ul class="chips" aria-label="Servizi">{services}</ul>
        {extra}
        <div class="sede-card__actions">
          <a class="btn btn--red" href="tel:{s["telefono"]}">{ICON["phone"]}Chiama</a>
          <a class="btn btn--ghost" href="{s["mappa"]}" target="_blank" rel="noopener">{ICON["route"]}Indicazioni</a>
        </div>
      </article>"""


def eyebrow(text):
    return f'<span class="eyebrow"><svg class="sparkle" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>{text}</span>'


def logo_img(cls, root, eager=True):
    return (f'<img class="{cls}" src="{root}assets/img/logo-720.webp" srcset="{root}assets/img/logo-360.webp 360w, {root}assets/img/logo-720.webp 720w" '
            f'sizes="(max-width: 430px) 70vw, 300px" width="300" height="331" alt="El Magic Pizza Fast Food"'
            + (' fetchpriority="high"' if eager else ' loading="lazy"') + ">")


# --------------------------------------------------------------------- HOME
def page_home():
    root = ""
    cles = sede("cles")
    h = head("El Magic | Pizza e fast food a Cles e Malé",
             "Pizza con lievito madre, kebab, panini e piadine a Cles e Malé (TN). Carne 100% halal, impasto senza glutine su richiesta. Aperti tutti i giorni con orario continuato.",
             root, "")
    h += jsonld() + "</head>\n<body data-root=\"\">\n" + header(root, "home")
    h += f"""
<main id="main">
  <section class="hero pattern torn-bottom">
    <div class="container">
      {logo_img("hero__logo", root)}
      <h1 class="hero__title">Pizza, kebab e un pizzico di <em>magia</em>.</h1>
      <p class="hero__lead">Impasti a lievito madre, ingredienti italiani e carne 100% halal. Ti aspettiamo a Cles e a Malé, tutti i giorni con orario continuato.</p>
      <div class="hero__actions">
        <a class="btn" href="menu/">Scopri il menù</a>
        <a class="btn btn--ghost" href="contatti/">Dove siamo</a>
      </div>
      <ul class="hero__badges">
        <li class="badge">Lievito madre</li>
        <li class="badge">100% halal</li>
        <li class="badge">Senza glutine su richiesta</li>
        <li class="badge">Aperti 7 giorni su 7</li>
      </ul>
    </div>
  </section>

  <section class="section section--red" id="sedi" style="padding-top: 28px">
    <div class="container">
      <div class="section-head section-head--center reveal">
        {eyebrow("Due sedi, la stessa magia")}
        <h2 class="section-title">Passa a trovarci</h2>
        <p class="section-lead">Mangia da noi o porta via: a Cles e a Malé il forno è acceso tutto il giorno.</p>
      </div>
      <div class="sedi-grid">
        {sede_card(sede("cles"), root)}
        {sede_card(sede("male"), root)}
      </div>
      <p style="text-align:center; margin: 32px 0 0"><a class="btn btn--white" href="contatti/">Orari completi e mappe</a></p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        {eyebrow("Perché ci tornerai")}
        <h2 class="section-title">Fatto bene, servito veloce.</h2>
        <p class="section-lead">Un fast food come piace a noi: veloce nel servizio, lento dove conta, cioè nella lievitazione.</p>
      </div>
      <ul class="features">
        <li class="feature reveal"><div class="feature__icon">{ICON["wheat"]}</div><h3>Lievito madre</h3><p>Tutti i nostri impasti lievitano con lievito madre, per una pizza leggera e digeribile. La vuoi integrale? Basta chiedere.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["heart"]}</div><h3>Qualità italiana</h3><p>Mozzarella, salumi, formaggi e verdure: scegliamo prodotti italiani di alta qualità.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["check"]}</div><h3>100% halal</h3><p>Tutto quello che prepariamo è rigorosamente halal, dal kebab al pollo.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["star"]}</div><h3>Per tutti i gusti</h3><p>Impasto senza glutine e mozzarella senza lattosio su richiesta, e tanti piatti vegetariani.</p></li>
      </ul>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
      <div class="section-head reveal">
        {eyebrow("I preferiti di casa")}
        <h2 class="section-title">Da qui non si sbaglia.</h2>
        <p class="section-lead">Le pizze e i kebab che ti consigliamo noi. Il resto lo trovi nel menù completo.</p>
      </div>
      <div class="dish-grid dish-grid--3" data-featured></div>
      <p style="margin: 28px 0 0"><a class="btn btn--red" href="menu/">Vedi tutto il menù</a></p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="magic reveal" data-magic>
        <div class="magic__stars" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="currentColor" style="width:26px;bottom:10%;right:46%"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>
          <svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;top:70%;left:42%;color:#fff;opacity:.6"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>
          <svg viewBox="0 0 24 24" fill="currentColor" style="width:18px;top:8%;right:8%"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>
        </div>
        <div class="magic__intro">
          {eyebrow("Indeciso?")}
          <h2>Non sai cosa scegliere? Lascia fare a noi.</h2>
          <p>Un tocco e ti diciamo cosa ordinare stasera. Se non ti convince, riprova: le magie non finiscono mai.</p>
          <button class="btn btn--red" type="button" data-magic-btn>{ICON["star"]}Fammi una magia</button>
        </div>
        <div class="magic__card" aria-live="polite">
          <span class="magic__cat">Il tuo piatto di stasera</span>
          <p class="magic__name">Pronto?</p>
          <p class="magic__desc">Premi il pulsante e lasciati sorprendere.</p>
          <span class="magic__price"></span>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top: 0">
    <div class="container">
      <div class="cta-band reveal">
        <div class="cta-band__icon">{ICON["scooter"]}</div>
        <div>
          <h2>A Cles te la portiamo a casa.</h2>
          <p>Consegna a domicilio tutti i giorni dalle 19:00 alle 21:00, tranne il martedì. Chiama e ordina.</p>
        </div>
        <a class="btn btn--white" href="tel:{cles["telefono"]}">{ICON["phone"]}{cles["telefonoVisibile"]}</a>
      </div>
    </div>
  </section>
</main>
"""
    h += footer(root) + scripts(root) + "</body>\n</html>\n"
    return h


# --------------------------------------------------------------------- MENU
def page_menu():
    root = "../"
    h = head("Menù | El Magic Cles e Malé",
             "Il menù completo di El Magic: pizze classiche e speciali con lievito madre, kebab, panini, piadine e bibite. Prezzi, ingredienti e allergeni.",
             root, "menu/")
    h += '</head>\n<body data-root="../">\n' + header(root, "menu")
    filters = [("all", "Tutto"), ("veg", "Vegetariane"), ("hot", "Piccanti"), ("mare", "Di mare"), ("top", "Consigliate")]
    fbtn = "".join(f'<button class="filter" type="button" data-filter="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in filters)
    h += f"""
<main id="main">
  <section class="page-hero pattern torn-bottom">
    <div class="container">
      {eyebrow("Stessi prezzi a Cles e Malé")}
      <h1>Il nostro menù</h1>
      <p>Pizze con impasto a lievito madre, kebab, panini e piadine. Cerca il tuo piatto, filtra per gusto o escludi gli allergeni.</p>
      <p style="margin-top: 22px"><a class="btn" href="../{D["menuPdf"]}" data-menu-pdf download>{ICON["download"]}Scarica il menù in PDF</a></p>
    </div>
  </section>

  <section class="section--red" style="padding: 6px 0 22px">
    <div class="container">
      <ul class="chips" style="justify-content:center; gap:8px">
        <li class="chip" style="background:rgba(255,255,255,.16);color:#fff">Impasto integrale +1 €</li>
        <li class="chip" style="background:rgba(255,255,255,.16);color:#fff">Senza glutine +2,5 €</li>
        <li class="chip" style="background:rgba(255,255,255,.16);color:#fff">Mozzarella senza lattosio su richiesta</li>
        <li class="chip" style="background:rgba(255,255,255,.16);color:#fff">100% halal</li>
      </ul>
    </div>
  </section>

  <div class="container menu-filters-wrap">
    <div class="menu-filters">
      <label class="search">
        <span class="visually-hidden">Cerca nel menù</span>
        {ICON["search"]}
        <input id="menu-search" type="search" placeholder="Cerca: tonno, kebab, bufala…" autocomplete="off" enterkeyhint="search">
      </label>
      <div class="filter-chips" role="group" aria-label="Filtra per tipo">
        {fbtn}
        <button class="filter filter--allergens" id="allergen-toggle" type="button" aria-expanded="false" aria-controls="allergen-panel">Escludi allergeni</button>
      </div>
    </div>
    <div class="allergen-panel" id="allergen-panel" hidden>
      <p>Tocca gli allergeni da evitare: nascondiamo i piatti che li contengono.</p>
      <div class="allergen-list" id="allergen-list"></div>
    </div>
  </div>

  <div class="menu-tools">
    <div class="container">
      <nav class="menu-tabs" id="menu-tabs" aria-label="Categorie del menù"></nav>
    </div>
  </div>

  <div class="container">
    <div id="menu-root"></div>
    <div class="menu-empty" id="menu-empty" hidden>
      <strong>Nessun piatto trovato</strong>
      <p>Prova a cambiare ricerca o filtri.</p>
      <button class="btn btn--ghost btn--sm" type="button" id="menu-reset">Azzera i filtri</button>
    </div>
    <noscript><p class="menu-empty">Per vedere il menù interattivo attiva JavaScript, oppure <a href="../{D["menuPdf"]}">scarica il menù in PDF</a>.</p></noscript>

    <div class="info-cards" style="margin-top: 56px">
      <div class="info-card"><h3>{ICON["star"]}Come la vuoi tu</h3><p>Aggiunte o variazioni da 0,50 € fino a un massimo di 3 €. Il <strong>Menù</strong> di kebab e panini include patatine e lattina.</p></div>
      <div class="info-card"><h3>{ICON["wheat"]}Impasti</h3><p>Tutti i nostri impasti sono lievitati con lievito madre. Su richiesta: integrale (+1 €) e senza glutine (+2,5 €).</p></div>
      <div class="info-card"><h3>{ICON["info"]}Allergeni</h3><p>Gli allergeni indicati seguono il nostro menù ufficiale. Per allergie o intolleranze parla sempre con il personale prima di ordinare.</p></div>
    </div>
    <p class="legal-note">Negli alimenti e nelle bevande preparati e somministrati possono essere contenuti ingredienti o coadiuvanti considerati allergeni (Reg. UE 1169/2011, allegato II). * Alcuni prodotti possono essere surgelati all'origine o congelati in loco: chiedi al personale per maggiori informazioni. Tutti i nostri prodotti sono di alta qualità italiana.</p>
  </div>
</main>
"""
    h += footer(root) + scripts(root, "menu.js") + "</body>\n</html>\n"
    return h


# ----------------------------------------------------------------- CONTATTI
def page_contatti():
    root = "../"
    soc = D["social"]
    h = head("Contatti e orari | El Magic Cles e Malé",
             "Indirizzi, telefoni e orari di El Magic a Cles (Via Trento 6) e Malé (Via Brescia 18). Asporto, posti a sedere e consegna a domicilio a Cles.",
             root, "contatti/")
    h += '</head>\n<body data-root="../">\n' + header(root, "contatti")
    h += f"""
<main id="main">
  <section class="page-hero pattern torn-bottom">
    <div class="container">
      {eyebrow("Cles · Malé")}
      <h1>Vieni a trovarci</h1>
      <p>Siamo aperti tutti i giorni con orario continuato. Chiama per ordinare da asporto, oppure passa e siediti da noi.</p>
    </div>
  </section>

  <section class="section section--red" id="sedi" style="padding-top: 28px">
    <div class="container">
      <div class="sedi-grid">
        {sede_card(sede("cles"), root, full=True)}
        {sede_card(sede("male"), root, full=True)}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <ul class="features">
        <li class="feature reveal"><div class="feature__icon">{ICON["users"]}</div><h3>Siete in tanti?</h3><p>Di solito non serve prenotare. Se venite in gruppo, chiamateci prima e vi teniamo i tavoli.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["scooter"]}</div><h3>Domicilio a Cles</h3><p>Dalle 19:00 alle 21:00, tutti i giorni tranne il martedì. Consegniamo noi, senza app.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["wheat"]}</div><h3>Esigenze alimentari</h3><p>Impasto senza glutine, mozzarella senza lattosio e piatti vegetariani. Tutto è 100% halal.</p></li>
        <li class="feature reveal"><div class="feature__icon">{ICON["menu"]}</div><h3>Il menù sempre con te</h3><p>Sfoglialo online o <a href="../{D["menuPdf"]}" data-menu-pdf download>scaricalo in PDF</a>. Prezzi uguali nelle due sedi.</p></li>
      </ul>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container" style="text-align:center">
      <div class="section-head section-head--center reveal">
        {eyebrow("Seguici")}
        <h2 class="section-title">Le novità le trovi qui</h2>
        <p class="section-lead">Pizze nuove, aperture speciali e qualche dietro le quinte dal forno.</p>
      </div>
      <div class="social-row reveal">
        <a class="social-btn" href="{soc["instagram"]["url"]}" target="_blank" rel="noopener">{ICON["instagram"]}@{e(soc["instagram"]["label"])}</a>
        <a class="social-btn" href="{soc["facebook"]["url"]}" target="_blank" rel="noopener">{ICON["facebook"]}{e(soc["facebook"]["label"])}</a>
      </div>
    </div>
  </section>
</main>
"""
    h += footer(root) + scripts(root) + "</body>\n</html>\n"
    return h


# ---------------------------------------------------------------------- 404
def page_404():
    # La 404 può essere servita da qualsiasi percorso: un <base> punta alla radice del sito
    # (dominio proprio su Cloudflare, oppure /nome-repo/ su GitHub Pages).
    root = ""
    h = head("Pagina non trovata | El Magic", "La pagina che cerchi non esiste.", root, "404.html")
    base = """<script>(function(){var b="/";if(/\\.github\\.io$/.test(location.hostname)){var s=location.pathname.split("/")[1];if(s)b="/"+s+"/";}document.write('<base href="'+b+'">');})();</script>\n"""
    h = h.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + base + '<meta name="robots" content="noindex">\n')
    h += '</head>\n<body data-root="">\n' + header(root, "")
    h += f"""
<main id="main">
  <section class="not-found pattern">
    <div class="container">
      {logo_img("", root)}
      <h1>Ops, questa pagina è sparita.</h1>
      <p style="color:var(--muted)">Dev'essere stata una magia venuta male. Torniamo a cose più buone?</p>
      <p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px">
        <a class="btn" href="./">Torna alla home</a>
        <a class="btn btn--ghost" href="menu/">Vai al menù</a>
      </p>
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
