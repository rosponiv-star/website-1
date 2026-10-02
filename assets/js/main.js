/* El Magic — script comune a tutte le pagine. I dati arrivano da data.js. */
(function () {
  "use strict";

  var D = window.EL_MAGIC;
  var root = document.body.getAttribute("data-root") || "";
  document.documentElement.classList.remove("no-js");

  /* ---------------------------------------------------------- Icone */
  function svg(body) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + "</svg>";
  }
  var ICON = {
    phone: svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    close: svg('<path d="M18 6 6 18M6 6l12 12"/>'),
    leaf: svg('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>'),
    chili: svg('<path d="M17 7c-3 0-4 4-7 7s-6 4-8 4c4 3 12 2 15-4 1.5-3 1-6 0-7Z"/><path d="M17 7c0-2 1-3 3-4"/>'),
    fish: svg('<path d="M6.5 12c3-4.5 9-5.5 13-1.5-4 4-10 3-13-1.5Z"/><path d="M6.5 12 2 8.5v7L6.5 12Z"/>'),
    star: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0c.8 6.6 5.4 11.2 12 12-6.6.8-11.2 5.4-12 12-.8-6.6-5.4-11.2-12-12C6.6 11.2 11.2 6.6 12 0Z"/></svg>'
  };

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
  window.EL_MAGIC_UTIL = { esc: esc, euro: euro, $: $, $all: $all, icon: ICON, root: root };

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

  // Intervallo [apertura, chiusura] in minuti; se chiude dopo mezzanotte la chiusura supera 1440.
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
      var at = orari[openDay][1];
      return close - n.min <= 45
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
      var label = el.getAttribute("data-label");
      el.className = "status status--" + st.cls;
      el.textContent = (label ? label + " · " : "") + st.text;
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
      el.textContent = o ? o[0] + " – " + o[1] : "Chiuso";
    });
    $all("[data-hours]").forEach(function (el) {
      var s = sede(el.getAttribute("data-hours"));
      if (!s) return;
      var rows = ORDINE.map(function (d) {
        var o = s.orari[d];
        return "<tr" + (d === n.day ? ' class="is-today"' : "") + '><th scope="row">' + GIORNI[d] + "</th><td>" +
          (o ? o[0] + " – " + o[1] : "Chiuso") + "</td></tr>";
      }).join("");
      el.innerHTML = '<caption class="visually-hidden">Orari ' + esc(s.nome) + "</caption><tbody>" + rows + "</tbody>";
    });
  }

  renderStatus();
  renderHours();
  setInterval(renderStatus, 60000);

  /* ---------------------------------------------------- Header allo scroll */
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
      '<h2 id="call-title">Chi <span class="script">chiamiamo?</span></h2><p>Scegli la sede più vicina a te.</p><div class="dialog__options">' +
      D.sedi.map(function (s) {
        return '<a class="dialog__option" href="tel:' + s.telefono + '"><div><strong>' + esc(s.nome) + '</strong><span class="num">' +
          esc(s.telefonoVisibile) + '</span><span class="status" data-status="' + s.id + '"></span></div><span class="dialog__go">' + ICON.phone + "</span></a>";
      }).join("") + "</div>";
    document.body.appendChild(dialog);
    $(".dialog__close", dialog).addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
  }
  $all("[data-call]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (typeof HTMLDialogElement === "undefined") return; // senza dialog il link porta a Contatti
      e.preventDefault();
      if (!dialog) buildDialog();
      renderStatus();
      dialog.showModal();
    });
  });

  /* ------------------------------------------------ Link al menu in PDF */
  $all("[data-menu-pdf]").forEach(function (a) { a.setAttribute("href", root + D.menuPdf); });

  /* ------------------------------------------ Home: "Pesca una carta" */
  var deck = $("[data-trick]");
  if (deck) {
    var pool = [];
    D.categorie.forEach(function (c) {
      if (c.id === "bibite") return;
      c.piatti.forEach(function (p) { pool.push({ p: p, c: c }); });
    });
    var card = $(".card", deck);
    var btn = $("[data-trick-btn]");
    var catEl = $(".card__cat", card), nameEl = $(".card__name", card), descEl = $(".card__desc", card), priceEl = $(".card__price", card);
    var last = -1, busy = false;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var fill = function () {
      var i;
      do { i = Math.floor(Math.random() * pool.length); } while (i === last && pool.length > 1);
      last = i;
      var it = pool[i];
      catEl.textContent = it.c.titolo;
      nameEl.textContent = it.p.nome;
      descEl.textContent = it.p.desc || "";
      priceEl.textContent = "da " + euro(it.p.n);
    };
    var draw = function () {
      if (busy) return;
      busy = true;
      if (card.classList.contains("is-flipped") && !reduce) {
        card.classList.remove("is-flipped");
        setTimeout(function () { fill(); card.classList.add("is-flipped"); busy = false; }, 650);
      } else {
        fill();
        card.classList.add("is-flipped");
        busy = false;
      }
      if (btn) btn.innerHTML = ICON.star + "Pesca un'altra carta";
    };
    card.addEventListener("click", draw);
    card.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); draw(); } });
    if (btn) btn.addEventListener("click", draw);
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
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------------------------------------------------------- Anno */
  $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
