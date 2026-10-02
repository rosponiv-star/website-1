# El Magic · Pizza · Fast Food

Sito di **El Magic**, pizzeria e fast food a **Cles** (Via Trento 6) e **Malé** (Via Brescia 18).

È un sito statico (HTML, CSS e JavaScript), senza framework e senza passaggi di build: i file
di questa cartella sono già il sito pronto da pubblicare. Funziona così com'è su **GitHub Pages**
e su **Cloudflare Pages**.

## Pagine

| Percorso      | File                  | Contenuto                                                           |
| ------------- | --------------------- | ------------------------------------------------------------------- |
| `/`           | `index.html`          | Home: sedi con stato aperto/chiuso, punti di forza, piatti consigliati, "Fammi una magia", domicilio |
| `/menu/`      | `menu/index.html`     | Menù interattivo: categorie, ricerca, filtri, esclusione allergeni, PDF |
| `/contatti/`  | `contatti/index.html` | Indirizzi, telefoni, orari completi, domicilio, mappe, social       |
| (errore)      | `404.html`            | Pagina "non trovata"                                                |

## Struttura

```
.
├── index.html, menu/, contatti/, 404.html   pagine
├── assets/
│   ├── css/style.css        stile (colori del marchio in :root)
│   ├── js/data.js           ⭐ DATI: menù, prezzi, allergeni, sedi, orari, social
│   ├── js/main.js           logica comune (stato aperto/chiuso, orari, "Chiama", magia)
│   ├── js/menu.js           logica della pagina Menù
│   ├── img/                 logo, pattern, bordo strappato, icone, anteprima social
│   ├── fonts/               Montserrat (ospitato in locale, licenza OFL)
│   └── menu/menu-el-magic.pdf   menù scaricabile
├── tools/genera-pagine.py   rigenera le pagine HTML da data.js
├── _headers, _redirects     impostazioni per Cloudflare Pages
├── robots.txt, sitemap.xml, site.webmanifest, favicon.ico
└── .nojekyll                dice a GitHub Pages di pubblicare i file così come sono
```

## Come aggiornare

**Prezzi, piatti, allergeni**: modifica `assets/js/data.js`. Il menù, i piatti consigliati
(tag `"top"`) e "Fammi una magia" si aggiornano da soli.

**Orari, telefoni, indirizzi, social**: modifica `assets/js/data.js`, poi lancia

```bash
python3 tools/genera-pagine.py
```

così anche le parti scritte direttamente nell'HTML (footer, schede delle sedi, dati per Google)
restano allineate.

**Nuovo menù in PDF**: sostituisci `assets/menu/menu-el-magic.pdf` tenendo lo stesso nome.

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

## Note

- Lo stato "Aperto ora / Chiuso" usa l'ora italiana (Europe/Rome) e gestisce la chiusura dopo
  mezzanotte di Malé.
- La mappa di Google viene caricata solo quando il visitatore preme "Mostra la mappa":
  nessun cookie di terze parti all'apertura della pagina.
- Il font è ospitato sul sito stesso: nessuna richiesta a Google Fonts.
