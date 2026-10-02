/* El Magic — script comune a tutte le pagine. I dati arrivano da data.js. */
(function () {
  "use strict";

  var D = window.EL_MAGIC;
  var root = document.body.getAttribute("data-root") || "";
  document.documentElement.classList.remove("no-js");

  /* ---------------------------------------------------------- Icone */
  var ICON = {
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    route: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>',
    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    scooter: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="5.5" cy="17.5" r="2.5"/><circle cx="18.5" cy="17.5" r="2.5"/><path d="M8 17.5h7.5l2-6H14l-2-4H9"/><path d="M15.5 11.5 18.5 17.5"/><path d="M3 11.5h6v3"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    leaf: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/></svg>',
    chili: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 7c-3 0-4 4-7 7s-6 4-8 4c4 3 12 2 15-4 1.5-3 1-6 0-7Z"/><path d="M17 7c0-2 1-3 3-4"/></svg>',
    fish: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 12c3-4.5 9-5.5 13-1.5-4 4-10 3-13-1.5Z"/><path d="M6.5 12 2 8.5v7L6.5 12Z"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>'
  };
  window.EL_MAGIC_ICON = ICON;

  /* ---------------------------------------------------------- Utilità */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function euro(n) { return n.toFixed(2).replace(".", ",") + " €"; }
  function sede(id) { return D.sedi.filter(function (s) { return s.id === id; })[0]; }
  window.EL_MAGIC_UTIL = { esc: esc, euro: euro, $: $, $all: $all };

  /* ------------------------------------------- Ora attuale a Cles/Malé */
  var GIORNI = ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"];
  var ORDINE = [1, 2, 3, 4, 5, 6, 0];

  function nowRome() {
    var parts = {};
    try {
      new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Rome", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23"
      }).formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
    } catch (e) {
      var d = new Date();
      return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() };
    }
    var map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: map[parts.weekday], min: (parseInt(parts.hour, 10) % 24) * 60 + parseInt(parts.minute, 10) };
  }
  function toMin(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }

  // Restituisce l'intervallo [apertura, chiusura] in minuti; se chiude dopo mezzanotte la chiusura supera 1440.
  function span(orari, day) {
    var o = orari[day];
    if (!o) return null;
    var a = toMin(o[0]), c = toMin(o[1]);
    if (c <= a) c += 1440;
    return [a, c];
  }

  function statusOf(orari) {
    var n = nowRome();
    var today = span(orari, n.day);
    var yday = span(orari, (n.day + 6) % 7);
    var openDay = null, close = null;
    if (today && n.min >= today[0] && n.min < today[1]) { openDay = n.day; close = today[1]; }
    else if (yday && n.min + 1440 < yday[1]) { openDay = (n.day + 6) % 7; close = yday[1] - 1440; }
    if (openDay !== null) {
      var left = close - n.min;
      var at = orari[openDay][1];
      return left <= 45
        ? { cls: "soon", text: "Chiude tra poco · alle " + at }
        : { cls: "open", text: "Aperto ora · fino alle " + at };
    }
    if (today && n.min < today[0]) return { cls: "closed", text: "Chiuso · apre alle " + orari[n.day][0] };
    for (var i = 1; i <= 7; i++) {
      var d = (n.day + i) % 7;
      if (orari[d]) return { cls: "closed", text: "Chiuso · apre " + (i === 1 ? "domani" : GIORNI[d].toLowerCase()) + " alle " + orari[d][0] };
    }
    return { cls: "closed", text: "Chiuso" };
  }

  function renderStatus() {
    $all("[data-status]").forEach(function (el) {
      var s = sede(el.getAttribute("data-status"));
      if (!s) return;
      var st = statusOf(s.orari);
      el.className = "status status--" + st.cls;
      el.textContent = st.text;
    });
    $all("[data-delivery-status]").forEach(function (el) {
      var s = sede(el.getAttribute("data-delivery-status"));
      if (!s || !s.domicilio) return;
      var st = statusOf(s.domicilio.orari);
      el.className = "status status--" + st.cls;
      el.textContent = st.text
        .replace("Chiuso · apre", "Consegne chiuse · riprendono")
        .replace("Aperto ora", "Consegne attive")
        .replace("Chiude tra poco", "Ultimi ordini a domicilio");
    });
  }

  function renderHours() {
    var n = nowRome();
    $all("[data-today]").forEach(function (el) {
      var s = sede(el.getAttribute("data-today"));
      var o = s && s.orari[n.day];
      el.textContent = o ? o[0] + " – " + o[1] : "chiuso";
    });
    $all("[data-hours]").forEach(function (el) {
      var key = el.getAttribute("data-hours").split(":");
      var s = sede(key[0]);
      if (!s) return;
      var orari = key[1] === "domicilio" ? s.domicilio.orari : s.orari;
      var rows = ORDINE.map(function (d) {
        var o = orari[d];
        return '<tr' + (d === n.day ? ' class="is-today"' : "") + '><th scope="row">' + GIORNI[d] + "</th><td>" +
          (o ? o[0] + " – " + o[1] : "Chiuso") + "</td></tr>";
      }).join("");
      el.innerHTML = '<caption class="visually-hidden">Orari ' + esc(s.nome) + "</caption><tbody>" + rows + "</tbody>";
    });
  }

  renderStatus();
  renderHours();
  setInterval(renderStatus, 60000);

  /* ---------------------------------------------------- Header al scroll */
  var header = $(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------- Dialog "Chiama" */
  var dialog = null;
  function buildDialog() {
    dialog = document.createElement("dialog");
    dialog.className = "dialog";
    dialog.setAttribute("aria-labelledby", "call-title");
    dialog.innerHTML =
      '<button class="dialog__close" type="button" aria-label="Chiudi">' + ICON.close + "</button>" +
      '<h2 id="call-title">Chi vuoi chiamare?</h2><p>Scegli la sede più vicina a te.</p><div class="dialog__options">' +
      D.sedi.map(function (s) {
        return '<a class="dialog__option" href="tel:' + s.telefono + '"><div><strong>' + esc(s.nome) + "</strong><span>" +
          esc(s.telefonoVisibile) + '</span><br><span data-status="' + s.id + '"></span></div>' + ICON.phone + "</a>";
      }).join("") + "</div>";
    document.body.appendChild(dialog);
    $(".dialog__close", dialog).addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
  }
  $all("[data-call]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (typeof HTMLDialogElement === "undefined") return; // il link porta a Contatti
      e.preventDefault();
      if (!dialog) buildDialog();
      renderStatus();
      dialog.showModal();
    });
  });

  /* ------------------------------------------------ Link al menu in PDF */
  $all("[data-menu-pdf]").forEach(function (a) { a.setAttribute("href", root + D.menuPdf); });

  /* ---------------------------------------------- Card piatto (riusata) */
  function tagHtml(t) {
    var T = {
      veg: ["tag--veg", ICON.leaf, "Veg"],
      hot: ["tag--hot", ICON.chili, "Piccante"],
      mare: ["tag--mare", ICON.fish, "Mare"],
      top: ["tag--top", ICON.star, "Consigliata"]
    }[t];
    return T ? '<span class="tag ' + T[0] + '">' + T[1] + T[2] + "</span>" : "";
  }
  function dishCard(p, cat) {
    var labels = Object.assign({}, D.etichetteColonne, cat.etichette || {});
    var cols = cat.colonne.filter(function (c) { return p[c] != null; });
    var prices = cols.map(function (c, i) {
      var label = cols.length > 1 ? "<small>" + esc(labels[c]) + "</small>" : "";
      return '<span class="price' + (i > 0 ? " price--alt" : "") + '">' + label + euro(p[c]) + "</span>";
    }).join("");
    var tags = (p.tag || []).map(tagHtml).join("");
    var all = p.all && p.all.length
      ? '<p class="dish__allergens"><b>Allergeni:</b> ' + p.all.map(function (a) { return D.allergeni[a].toLowerCase(); }).join(", ") + "</p>"
      : "";
    return '<article class="dish"><div class="dish__head"><h3 class="dish__name">' + esc(p.nome) + "</h3>" +
      '<div class="dish__prices">' + prices + "</div></div>" +
      (p.desc ? '<p class="dish__desc">' + esc(p.desc) + "</p>" : "") +
      (tags || all ? '<div class="dish__meta">' + tags + all + "</div>" : "") + "</article>";
  }
  window.EL_MAGIC_DISH = dishCard;

  /* ------------------------------------------------ Home: i preferiti */
  var fav = $("[data-featured]");
  if (fav) {
    var picks = [];
    D.categorie.forEach(function (c) {
      c.piatti.forEach(function (p) { if ((p.tag || []).indexOf("top") > -1) picks.push(dishCard(p, c)); });
    });
    fav.innerHTML = picks.slice(0, 6).join("");
  }

  /* ---------------------------------------- Home: "Fammi una magia" */
  var magic = $("[data-magic]");
  if (magic) {
    var pool = [];
    D.categorie.forEach(function (c) {
      if (c.id === "bibite") return;
      c.piatti.forEach(function (p) { pool.push({ p: p, c: c }); });
    });
    var card = $(".magic__card", magic);
    var btn = $("[data-magic-btn]", magic);
    var nameEl = $(".magic__name", card), catEl = $(".magic__cat", card), descEl = $(".magic__desc", card), priceEl = $(".magic__price", card);
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var last = -1, busy = false;

    var show = function (item) {
      catEl.textContent = item.c.titolo;
      nameEl.textContent = item.p.nome;
      descEl.textContent = item.p.desc || "Il gusto di sempre, a modo nostro.";
      priceEl.textContent = "da " + euro(item.p.n);
    };
    var pick = function () {
      var i;
      do { i = Math.floor(Math.random() * pool.length); } while (i === last && pool.length > 1);
      last = i;
      return pool[i];
    };
    btn.addEventListener("click", function () {
      if (busy) return;
      busy = true;
      card.classList.remove("is-revealed");
      var final = pick();
      if (reduce) { show(final); busy = false; return; }
      card.classList.add("is-spinning");
      var t = 0, steps = 14;
      (function spin() {
        t++;
        nameEl.textContent = pool[Math.floor(Math.random() * pool.length)].p.nome;
        if (t < steps) { setTimeout(spin, 40 + t * 9); return; }
        card.classList.remove("is-spinning");
        show(final);
        void card.offsetWidth;
        card.classList.add("is-revealed");
        btn.innerHTML = ICON.star + "Un'altra magia";
        busy = false;
      })();
    });
  }

  /* ------------------------------------- Contatti: mappa su richiesta */
  $all("[data-map-load]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = sede(b.getAttribute("data-map-load"));
      var box = b.closest(".map");
      box.innerHTML = '<iframe title="Mappa El Magic ' + esc(s.nome) + '" src="' + s.embed +
        '" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>';
    });
  });

  /* ---------------------------------------- Comparsa delle sezioni */
  var reveals = $all(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------------------------------------------------------- Anno */
  $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
