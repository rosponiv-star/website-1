# El Magic · Pizza · Fast Food

Sito di **El Magic**, pizzeria e fast food a **Cles** (Via Trento 6) e **Malé** (Via Brescia 18).

È un sito statico (HTML, CSS e JavaScript), senza framework e senza passaggi di build: i file
di questa cartella sono già il sito pronto da pubblicare. Funziona così com'è su **GitHub Pages**
e su **Cloudflare Pages**.

## Pagine

| Percorso      | File                  | Contenuto                                                           |
| ------------- | --------------------- | ------------------------------------------------------------------- |
| `/`           | `index.html`          | Home: poster con stato aperto/chiuso, manifesto, "assi nella manica", "Pesca una carta", come funziona, sedi, domicilio |
| `/menu/`      | `menu/index.html`     | Menù in stile carta stampata: categorie con foto, ricerca, filtri, esclusione allergeni, PDF |
| `/contatti/`  | `contatti/index.html` | Indirizzi, telefoni, orari completi, domicilio, mappe, social       |
| (errore)      | `404.html`            | Pagina "non trovata"                                                |

## Struttura

```
.
├── index.html, menu/, contatti/, 404.html   pagine
├── assets/
│   ├── css/style.css        stile (colori e font del marchio in :root)
│   ├── js/data.js           ⭐ DATI: menù, prezzi, allergeni, sedi, orari, social
│   ├── js/main.js           logica comune (stato aperto/chiuso, orari, "Chiama", carta magica)
│   ├── js/menu.js           logica della pagina Menù
│   ├── img/                 logo, emblema, profilo montagne, icone, anteprima social
│   ├── img/foto/            foto dei piatti (ognuna in due misure: -700 e -1300)
│   ├── fonts/               Anton, Instrument Serif, Inter (in locale, licenze OFL in fonts/licenze)
│   └── menu/menu-el-magic.pdf   menù scaricabile
├── tools/genera-pagine.py   rigenera le pagine HTML da data.js
├── _headers, _redirects     impostazioni per Cloudflare Pages
├── robots.txt, sitemap.xml, site.webmanifest, favicon.ico
└── .nojekyll                dice a GitHub Pages di pubblicare i file così come sono
```

## Come aggiornare

**Prezzi, piatti, allergeni**: modifica `assets/js/data.js`. Il menù, le icone (tag `"veg"`,
`"hot"`, `"mare"`, `"top"`) e "Pesca una carta" si aggiornano da soli.

**Orari, telefoni, indirizzi, social**: modifica `assets/js/data.js`, poi lancia

```bash
python3 tools/genera-pagine.py
```

così anche le parti scritte direttamente nell'HTML (footer, schede delle sedi, dati per Google)
restano allineate.

**Nuovo menù in PDF**: sostituisci `assets/menu/menu-el-magic.pdf` tenendo lo stesso nome.

**Foto**: quelle attuali sono **generate con l'intelligenza artificiale** e servono a dare
l'idea (nel sito c'è la nota "foto a scopo illustrativo"). Appena ci sono foto vere dei piatti,
sostituisci i file in `assets/img/foto/` mantenendo nome e misure (es. `margherita-700.webp`
largo 700 px e `margherita-1300.webp` largo 1300 px). `pizza-trancio`, `panino-kebab` e
`patatine` sono scontornate (sfondo trasparente).

Per provare il sito sul computer:

```bash
python3 -m http.server 8000
# poi apri http://localhost:8000
```

## Pubblicazione

### GitHub Pages (adesso)

1. Unisci questo branch in `main`.
2. Su GitHub: **Settings → Pages → Build and deployment**
   - Source: **Deploy from a branch**
   - Branch: **main**, cartella **/ (root)**
3. Dopo un minuto il sito è online su `https://<utente>.github.io/<repository>/`.

Tutti i link sono relativi, quindi il sito funziona anche dentro la sottocartella del repository.

### Cloudflare Pages (in seguito)

1. Cloudflare → **Workers & Pages → Create → Pages → Connect to Git** e scegli questo repository.
2. Impostazioni di build:
   - Framework preset: **None**
   - Build command: *(vuoto)*
   - Build output directory: **`/`**
   - Production branch: **main**
3. Aggiungi il dominio in **Custom domains** (es. `www.elmagic.it` ed `elmagic.it`).

Cloudflare usa da solo `_headers` (cache e sicurezza), `_redirects` (`/menu.pdf` porta al PDF
del menù) e `404.html`. Quando il dominio è collegato a Cloudflare puoi disattivare GitHub Pages.

> L'indirizzo `https://www.elmagic.it/` è usato per i link canonici, la sitemap e l'anteprima
> sui social. Se il dominio finale cambia, aggiorna `SITE` in `tools/genera-pagine.py`
> (poi rigenera), `sitemap.xml` e `robots.txt`.

## Design

- **Colori**: rosso logo `#BE1C2F`, crema `#F4EDDC`, nero caldo `#1B1515`, verde basilico `#288F4A`.
- **Font**: Anton (titoli da manifesto), Instrument Serif corsivo (accenti eleganti), Inter (testi).
- **Motivi**: tovaglia a quadri, profilo delle montagne (dal bordo strappato del vecchio sito:
  le valli di Non e di Sole), stelline del logo, scontrino, timbro del prezzo, carte da gioco.

## Note

- Lo stato "Aperto ora / Chiuso" usa l'ora italiana (Europe/Rome) e gestisce la chiusura dopo
  mezzanotte di Malé.
- La mappa di Google viene caricata solo quando il visitatore preme "Mostra la mappa":
  nessun cookie di terze parti all'apertura della pagina.
- I font sono ospitati sul sito stesso: nessuna richiesta a Google Fonts.
