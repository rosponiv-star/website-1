/*
 * El Magic — dati del sito.
 * Per aggiornare prezzi, piatti, orari o contatti modifica SOLO questo file:
 * Home, Menù e Contatti si aggiornano da soli.
 *
 * Fonte del menu: menu_2025_06.pdf (giugno 2025). I prezzi sono uguali a Cles e Malé.
 */
window.EL_MAGIC = {
  /* ---------------------------------------------------------------- SEDI */
  sedi: [
    {
      id: "cles",
      nome: "Cles",
      valle: "Val di Non",
      indirizzo: "Via Trento, 6",
      cap: "38023",
      citta: "Cles (TN)",
      telefono: "+393317897969",
      telefonoVisibile: "331 789 7969",
      mappa: "https://www.google.com/maps/search/?api=1&query=El+Magic+Pizzeria+Fast+Food+Via+Trento+6+38023+Cles+TN",
      embed: "https://www.google.com/maps?q=Via+Trento+6,+38023+Cles+TN&output=embed",
      // 0 = domenica … 6 = sabato. Orario continuato. "chiude" dopo mezzanotte = giorno dopo.
      orari: {
        1: ["11:00", "22:30"],
        2: ["11:30", "22:30"],
        3: ["11:00", "22:30"],
        4: ["11:00", "22:30"],
        5: ["11:00", "23:00"],
        6: ["11:00", "23:00"],
        0: ["11:00", "23:00"]
      },
      servizi: ["Posti a sedere", "Asporto", "Consegna a domicilio"],
      domicilio: {
        orari: { 0: ["19:00", "21:00"], 1: ["19:00", "21:00"], 3: ["19:00", "21:00"], 4: ["19:00", "21:00"], 5: ["19:00", "21:00"], 6: ["19:00", "21:00"] },
        nota: "Tutti i giorni dalle 19:00 alle 21:00, tranne il martedì."
      }
    },
    {
      id: "male",
      nome: "Malé",
      valle: "Val di Sole",
      indirizzo: "Via Brescia, 18",
      cap: "38027",
      citta: "Malé (TN)",
      telefono: "+393762366958",
      telefonoVisibile: "376 236 6958",
      mappa: "https://www.google.com/maps/search/?api=1&query=El+Magic+Via+Brescia+18+38027+Mal%C3%A9+TN",
      embed: "https://www.google.com/maps?q=Via+Brescia+18,+38027+Mal%C3%A9+TN&output=embed",
      orari: {
        0: ["11:00", "01:30"],
        1: ["11:00", "01:30"],
        2: ["11:00", "01:30"],
        3: ["11:00", "01:30"],
        4: ["11:00", "01:30"],
        5: ["11:00", "01:30"],
        6: ["11:00", "01:30"]
      },
      servizi: ["Posti a sedere", "Asporto"],
      domicilio: null
    }
  ],

  social: {
    instagram: { label: "el_magic_cles", url: "https://www.instagram.com/el_magic_cles/" },
    facebook: { label: "El Magic Pizzeria Fast Food", url: "https://www.facebook.com/elmagicpizzeria/" }
  },

  menuPdf: "assets/menu/menu-el-magic.pdf",

  /* ----------------------------------------------------------- ALLERGENI */
  // Reg. UE 1169/2011, allegato II. Le sigle sono usate nei piatti qui sotto.
  allergeni: {
    glutine: "Glutine",
    lattosio: "Lattosio",
    uovo: "Uova",
    pesce: "Pesce",
    crostacei: "Crostacei",
    molluschi: "Molluschi",
    guscio: "Frutta a guscio",
    arachidi: "Arachidi",
    soia: "Soia",
    sedano: "Sedano",
    senape: "Senape",
    sesamo: "Sesamo",
    solfiti: "Solfiti",
    lupini: "Lupini"
  },

  /* ---------------------------------------------------------------- MENU */
  // prezzi: n = normale, maxi = pizza maxi, menu = panino/piadina + patatine + lattina.
  // tag: veg = vegetariana, hot = piccante, mare = pesce/frutti di mare, top = consigliata.
  // * = prodotto che può essere surgelato all'origine o congelato in loco.
  categorie: [
    {
      id: "classiche",
      titolo: "Pizze classiche",
      sottotitolo: "Le intramontabili. Impasto a lievito madre, pomodoro e mozzarella: la magia comincia da qui.",
      foto: "margherita",
      colonne: ["n", "maxi"],
      piatti: [
        { nome: "Margherita", desc: "Pomodoro, mozzarella", n: 7, maxi: 13, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Pioggia", desc: "Pomodoro, doppia mozzarella", n: 7.5, maxi: 16, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Prosciutto", desc: "Pomodoro, mozzarella, prosciutto cotto", n: 7.5, maxi: 17.5, all: ["glutine", "lattosio"] },
        { nome: "Funghi", desc: "Pomodoro, mozzarella, funghi champignon", n: 7.5, maxi: 17, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Prosciutto e funghi", desc: "Pomodoro, mozzarella, prosciutto cotto, funghi champignon", n: 8.5, maxi: 19, all: ["glutine", "lattosio"] },
        { nome: "Capricciosa", desc: "Pomodoro, mozzarella, prosciutto cotto, funghi champignon, carciofi", n: 9, maxi: 20, all: ["glutine", "lattosio"] },
        { nome: "Quattro stagioni", desc: "Pomodoro, mozzarella, prosciutto cotto, funghi champignon, carciofi, olive", n: 9, maxi: 20, all: ["glutine", "lattosio"] },
        { nome: "Pugliese", desc: "Mozzarella, cipolla, pomodorini, basilico, tutto in cottura", n: 8.5, maxi: 19, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Romana", desc: "Pomodoro, mozzarella, acciughe, capperi, origano", n: 8, maxi: 18, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Napoletana", desc: "Pomodoro, mozzarella, acciughe, origano", n: 7.5, maxi: 18, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Calzone special", desc: "Pomodoro, mozzarella, prosciutto cotto, funghi champignon", n: 9, maxi: null, all: ["glutine", "lattosio"] },
        { nome: "Viennese", desc: "Pomodoro, mozzarella, würstel", n: 7.5, maxi: 17, all: ["glutine", "lattosio"] },
        { nome: "Tirolese", desc: "Pomodoro, mozzarella, speck, gorgonzola", n: 10, maxi: 22, all: ["glutine", "lattosio"], tag: ["top"] },
        { nome: "Quattro formaggi", desc: "Pomodoro, mozzarella, fontina, grana, gorgonzola", n: 9, maxi: 20, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Tonno e cipolle", desc: "Pomodoro, mozzarella, tonno, cipolle", n: 9, maxi: 20, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Diavola", desc: "Pomodoro, mozzarella, peperoni, salamino piccante", n: 8.5, maxi: 19, all: ["glutine", "lattosio"], tag: ["hot"] },
        { nome: "Toscana", desc: "Mozzarella, rucola, pomodorini, scaglie di grana", n: 9, maxi: 20, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Vegetariana", desc: "Pomodoro, mozzarella, verdure miste, pomodorini, carciofi, funghi, basilico in cottura, olive taggiasche", n: 10, maxi: 22, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Ricotta", desc: "Pomodoro, mozzarella, ricotta", n: 8, maxi: 18, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Calabrese", desc: "Mozzarella, aglio, peperoncino", n: 7.5, maxi: 17, all: ["glutine", "lattosio"], tag: ["veg", "hot"] },
        { nome: "Marta", desc: "Pomodoro, mozzarella, cipolla di Tropea, porcini, speck", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Irina", desc: "Pomodoro, mozzarella, gorgonzola, ricotta", n: 9, maxi: 20, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Carciofi", desc: "Pomodoro, mozzarella, carciofi", n: 8.5, maxi: 19, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Cigola", desc: "Pomodoro, mozzarella, cipolla, origano", n: 7.5, maxi: 17, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Speck", desc: "Pomodoro, mozzarella, speck", n: 8.5, maxi: 19, all: ["glutine", "lattosio"] },
        { nome: "Pancetta", desc: "Pomodoro, mozzarella, pancetta, gorgonzola", n: 10, maxi: 22, all: ["glutine", "lattosio"] },
        { nome: "Crucola", desc: "Pomodoro, mozzarella, crudo, rucola", n: 9.5, maxi: 21, all: ["glutine", "lattosio"] },
        { nome: "El Magic", desc: "Pomodoro, mozzarella, pomodorini, basilico", n: 8.5, maxi: 18, all: ["glutine", "lattosio"], tag: ["veg", "top"] },
        { nome: "Americana", desc: "Pomodoro, mozzarella, würstel, patatine fritte*", n: 9, maxi: 20, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Nonesa", desc: "Pomodoro, mozzarella, funghi finferli, pancetta, cipolle", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Bresaola", desc: "Pomodoro, mozzarella, bresaola, rucola, scaglie di grana", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Tonno", desc: "Pomodoro, mozzarella, tonno", n: 9, maxi: 20, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Romana Magic", desc: "Pomodoro, mozzarella, acciughe, capperi, olive, gorgonzola, pomodorini, basilico", n: 11, maxi: 23, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] }
      ]
    },
    {
      id: "pizzaiolo",
      titolo: "Specialità del pizzaiolo",
      sottotitolo: "Porcini, speck, burrata, lucanica: le pizze firmate dal nostro pizzaiolo.",
      foto: "pizza-porcini",
      colonne: ["n", "maxi"],
      piatti: [
        { nome: "Dolomiti", desc: "Pomodoro, mozzarella, funghi, salsiccia, speck", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Boscaiola", desc: "Pomodoro, mozzarella, funghi porcini, finferli e chiodini, grana", n: 10, maxi: 22, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Mexicana", desc: "Pomodoro, mozzarella, mais, peperoni, cipolle, salamino piccante", n: 10, maxi: 22, all: ["glutine", "lattosio"], tag: ["hot"] },
        { nome: "Camuna", desc: "Pomodoro, mozzarella, bresaola, funghi porcini", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Ricky", desc: "Pomodoro, mozzarella, gorgonzola, salamino piccante, rucola", n: 11, maxi: 23, all: ["glutine", "lattosio"], tag: ["hot"] },
        { nome: "Elsa", desc: "Mozzarella, brie, zucchine", n: 9, maxi: 20, all: ["glutine", "lattosio"], tag: ["veg"] },
        { nome: "Parmigiana", desc: "Mozzarella, prosciutto crudo, grana", n: 9.5, maxi: 21, all: ["glutine", "lattosio"] },
        { nome: "Handy", desc: "Mozzarella, gorgonzola, pomodorini, tonno, cipolla di Tropea, rucola, scaglie di grana", n: 12, maxi: 24, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Beatrice", desc: "Mozzarella, gorgonzola, noci", n: 11, maxi: 23, all: ["glutine", "lattosio", "guscio", "arachidi"], tag: ["veg"] },
        { nome: "Nonna", desc: "Pomodoro, mozzarella, funghi porcini, lucanica, gorgonzola", n: 11, maxi: 23, all: ["glutine", "lattosio"] },
        { nome: "Estate", desc: "Pomodoro, mozzarella, burrata o bufala, prosciutto crudo di Parma, datterini gialli, basilico", n: 12, maxi: 25, all: ["glutine", "lattosio"], tag: ["top"] }
      ]
    },
    {
      id: "fantasia",
      titolo: "Fantasia del pizzaiolo",
      sottotitolo: "Quando il pizzaiolo si diverte: mare, formaggi e abbinamenti che non ti aspetti.",
      foto: "pizza-mare",
      colonne: ["n", "maxi"],
      piatti: [
        { nome: "Il Maestro", desc: "Pomodoro, mozzarella, scamorza, pesto, salmone affumicato*", n: 11, maxi: 23, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Angelina", desc: "Pomodoro, mozzarella, salmone affumicato*", n: 10, maxi: 22, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Special El Magic", desc: "Pomodoro, mozzarella, pomodorini gialli e rossi, filetto di acciuga, burrata, olive, basilico in cottura", n: 11, maxi: 23, all: ["glutine", "lattosio", "pesce"], tag: ["mare", "top"] },
        { nome: "Cles", desc: "Pomodoro, mozzarella, brie, prosciutto crudo, rucola", n: 10, maxi: 22, all: ["glutine", "lattosio"] },
        { nome: "Profumo di mare", desc: "Pomodoro, mozzarella, verdure miste, salmone affumicato*, tre gamberetti Jumbo*, cipolla rossa di Tropea", n: 15, maxi: 33, all: ["glutine", "lattosio", "pesce", "crostacei", "molluschi"], tag: ["mare"] },
        { nome: "Frutti di mare", desc: "Pomodoro, mozzarella, frutti di mare*, pomodorini, basilico in cottura", n: 15, maxi: 33, all: ["glutine", "lattosio", "pesce", "crostacei", "molluschi"], tag: ["mare"] },
        { nome: "Golden Sheere", desc: "Mozzarella, mela, formaggio nostrano, noci", n: 10, maxi: 22, all: ["glutine", "lattosio", "guscio", "arachidi"], tag: ["veg"] },
        { nome: "Ring", desc: "Mozzarella, verdure miste, tonno, cipolla di Tropea", n: 12, maxi: 24, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Mare del Nord", desc: "Mozzarella, verdure miste, cipolla di Tropea, salmone*", n: 13, maxi: 26, all: ["glutine", "lattosio", "pesce"], tag: ["mare"] },
        { nome: "Melanzane", desc: "Pomodoro, mozzarella, melanzane, pomodorini, burrata di bufala", n: 11, maxi: 23, all: ["glutine", "lattosio"], tag: ["veg"] }
      ]
    },
    {
      id: "kebab",
      titolo: "Kebab, panini e piadine",
      sottotitolo: "Carne 100% halal, pane caldo e salse. Con il Menù aggiungi patatine e lattina.",
      foto: "piadina-kebab",
      colonne: ["n", "menu"],
      piatti: [
        { nome: "Panino kebab", n: 5, menu: 7.9, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"], tag: ["top"] },
        { nome: "Piadina kebab", n: 6, menu: 8.5, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Panino pollo", n: 6, menu: 7.9, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Piadina pollo", n: 6, menu: 8.5, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Hamburger", n: 6, menu: 8.5, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Panino falafel", n: 5, menu: 7.9, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"], tag: ["veg"] },
        { nome: "Piadina falafel", n: 6, menu: 8.5, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"], tag: ["veg"] }
      ]
    },
    {
      id: "pizza-kebab",
      titolo: "Pizza kebab e piatti",
      sottotitolo: "Il meglio dei due mondi: la nostra pizza incontra il kebab.",
      foto: "pizza-kebab",
      colonne: ["n", "maxi"],
      piatti: [
        { nome: "Pizza kebab", desc: "Solo carne", n: 10, maxi: 20, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Pizza kebab", desc: "Carne, verdure e salsa", n: 11, maxi: 23, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Pizza kebab completa", desc: "Carne, verdure, salsa e patatine", n: 12, maxi: 25, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"], tag: ["top"] },
        { nome: "Piatto kebab", desc: "Carne, verdure e salsa", n: 11, maxi: null, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Piatto kebab con patatine", desc: "Carne, verdure, salsa e patatine", n: 12, maxi: null, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] },
        { nome: "Box kebab", n: 5.5, maxi: 7.5, all: ["glutine", "lattosio", "uovo", "arachidi", "senape", "sesamo"] }
      ]
    },
    {
      id: "bibite",
      titolo: "Bibite",
      sottotitolo: "Ghiacciate, per accompagnare tutto quanto.",
      foto: "bibite",
      colonne: ["n", "grande"],
      etichette: { n: "Media", grande: "Grande" },
      piatti: [
        { nome: "Bibite in lattina", desc: "Coca-Cola, Fanta, Sprite, Lemonsoda, Pepsi, Red Bull, tè limone o pesca", n: 2.5, grande: null, all: [] },
        { nome: "Bibite alla spina", desc: "Media o grande", n: 3, grande: 4, all: [] },
        { nome: "Acqua in bottiglia", desc: "Naturale o frizzante", n: 1.5, grande: null, all: [] }
      ]
    }
  ],

  etichetteColonne: { n: "Normale", maxi: "Maxi", menu: "Menù", grande: "Grande" },

  // Le foto sono illustrative (generate con IA): sostituiscile con foto vere in assets/img/foto/
  // mantenendo gli stessi nomi (es. margherita-700.webp e margherita-1300.webp).
  fotoDir: "assets/img/foto/"
};
