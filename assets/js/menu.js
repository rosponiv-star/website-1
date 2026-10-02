/* El Magic — pagina Menù: rendering, ricerca, filtri e allergeni. */
(function () {
  "use strict";

  var D = window.EL_MAGIC;
  var U = window.EL_MAGIC_UTIL;
  var dishCard = window.EL_MAGIC_DISH;
  var rootEl = U.$("#menu-root");
  if (!rootEl) return;

  var tabsEl = U.$("#menu-tabs");
  var emptyEl = U.$("#menu-empty");
  var searchEl = U.$("#menu-search");
  var allergenBtn = U.$("#allergen-toggle");
  var allergenPanel = U.$("#allergen-panel");
  var allergenList = U.$("#allergen-list");

  var state = { q: "", tag: "all", exclude: [] };

  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }

  /* -------------------------------------------------- Rendering iniziale */
  tabsEl.innerHTML = D.categorie.map(function (c) {
    return '<a href="#' + c.id + '" data-tab="' + c.id + '">' + U.esc(c.titolo) + "</a>";
  }).join("");

  rootEl.innerHTML = D.categorie.map(function (c) {
    return '<section class="menu-section" id="' + c.id + '" aria-labelledby="h-' + c.id + '">' +
      '<div class="menu-section__head"><h2 id="h-' + c.id + '">' + U.esc(c.titolo) + "</h2>" +
      '<span class="menu-section__count" data-count="' + c.id + '"></span>' +
      "<p>" + U.esc(c.sottotitolo) + "</p></div>" +
      '<div class="dish-grid dish-grid--3">' +
      c.piatti.map(function (p, i) {
        return dishCard(p, c).replace('<article class="dish"', '<article class="dish" data-dish="' + c.id + ":" + i + '"');
      }).join("") +
      "</div></section>";
  }).join("");

  allergenList.innerHTML = Object.keys(D.allergeni).map(function (k) {
    return '<label><input type="checkbox" value="' + k + '">' + U.esc(D.allergeni[k]) + "</label>";
  }).join("");

  /* ------------------------------------------------------------ Filtri */
  function matches(p) {
    if (state.tag !== "all" && (p.tag || []).indexOf(state.tag) === -1) return false;
    for (var i = 0; i < state.exclude.length; i++) {
      if ((p.all || []).indexOf(state.exclude[i]) > -1) return false;
    }
    if (state.q) {
      var hay = norm(p.nome + " " + (p.desc || ""));
      var words = norm(state.q).split(/\s+/).filter(Boolean);
      for (var j = 0; j < words.length; j++) if (hay.indexOf(words[j]) === -1) return false;
    }
    return true;
  }

  function apply() {
    var total = 0;
    D.categorie.forEach(function (c) {
      var shown = 0;
      c.piatti.forEach(function (p, i) {
        var ok = matches(p);
        U.$('[data-dish="' + c.id + ":" + i + '"]', rootEl).hidden = !ok;
        if (ok) shown++;
      });
      total += shown;
      var sec = U.$("#" + c.id, rootEl);
      sec.hidden = shown === 0;
      U.$('[data-tab="' + c.id + '"]', tabsEl).hidden = shown === 0;
      var filtered = shown !== c.piatti.length;
      U.$('[data-count="' + c.id + '"]', rootEl).textContent = filtered
        ? shown + " di " + c.piatti.length
        : c.piatti.length + (c.piatti.length === 1 ? " proposta" : " proposte");
    });
    emptyEl.hidden = total > 0;
    allergenBtn.classList.toggle("has-value", state.exclude.length > 0);
    current = null;
    requestAnimationFrame(spy);
    allergenBtn.textContent = state.exclude.length ? "Senza allergeni (" + state.exclude.length + ")" : "Escludi allergeni";
  }

  var t;
  searchEl.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(function () { state.q = searchEl.value.trim(); apply(); }, 120);
  });

  U.$all("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      state.tag = b.getAttribute("data-filter");
      U.$all("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      apply();
    });
  });

  allergenBtn.addEventListener("click", function () {
    var open = allergenPanel.hidden;
    allergenPanel.hidden = !open;
    allergenBtn.setAttribute("aria-expanded", String(open));
  });
  allergenList.addEventListener("change", function () {
    state.exclude = U.$all("input:checked", allergenList).map(function (i) { return i.value; });
    apply();
  });

  U.$("#menu-reset").addEventListener("click", function () {
    state = { q: "", tag: "all", exclude: [] };
    searchEl.value = "";
    U.$all("input", allergenList).forEach(function (i) { i.checked = false; });
    U.$all("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", String(x.getAttribute("data-filter") === "all")); });
    apply();
  });

  apply();

  /* --------------------------------------- Scheda attiva durante lo scroll */
  var current = null, ticking = false;
  function stickyOffset() {
    return U.$(".site-header").offsetHeight + U.$(".menu-tools").offsetHeight + 8;
  }
  function spy() {
    ticking = false;
    var line = stickyOffset() + 40;
    var visible = U.$all(".menu-section", rootEl).filter(function (s) { return !s.hidden; });
    var active = visible[0];
    visible.forEach(function (s) { if (s.getBoundingClientRect().top <= line) active = s; });
    var id = active ? active.id : null;
    if (id === current) return;
    current = id;
    U.$all("a", tabsEl).forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("data-tab") === id); });
    var tab = id && U.$('[data-tab="' + id + '"]', tabsEl);
    if (tab) tabsEl.scrollTo({ left: tab.offsetLeft - 16, behavior: "smooth" });
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(spy); }
  }, { passive: true });
  spy();

  // Lo scroll verso una categoria tiene conto della barra fissa del menu.
  tabsEl.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    e.preventDefault();
    var target = document.getElementById(a.getAttribute("data-tab"));
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - stickyOffset(), behavior: "smooth" });
    history.replaceState(null, "", "#" + target.id);
  });
})();
