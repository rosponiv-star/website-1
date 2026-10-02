/* El Magic — pagina Menù: rendering, ricerca, filtri e allergeni. */
(function () {
  "use strict";

  var D = window.EL_MAGIC;
  var U = window.EL_MAGIC_UTIL;
  var rootEl = U.$("#menu-root");
  if (!rootEl) return;

  var tabsEl = U.$("#menu-tabs");
  var emptyEl = U.$("#menu-empty");
  var searchEl = U.$("#menu-search");
  var allergenBtn = U.$("#allergen-toggle");
  var allergenPanel = U.$("#allergen-panel");
  var allergenList = U.$("#allergen-list");
  var foto = U.root + D.fotoDir;

  var TAGS = {
    veg: ["t-veg", U.icon.leaf, "Vegetariana"],
    hot: ["t-hot", U.icon.chili, "Piccante"],
    mare: ["t-mare", U.icon.fish, "Di mare"],
    top: ["t-top", U.icon.star, "Consigliata"]
  };
  var state = { q: "", tag: "all", exclude: [] };

  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function tagIcons(p) {
    var t = (p.tag || []).map(function (k) {
      var T = TAGS[k];
      return T ? '<span class="' + T[0] + '" title="' + T[2] + '" role="img" aria-label="' + T[2] + '">' + T[1] + "</span>" : "";
    }).join("");
    return t ? '<span class="item__tags">' + t + "</span>" : "";
  }

  /* -------------------------------------------------- Rendering iniziale */
  U.$("#menu-legend").innerHTML = Object.keys(TAGS).map(function (k) {
    var T = TAGS[k];
    return '<span><span class="item__tags"><span class="' + T[0] + '">' + T[1] + "</span></span>" + T[2] + "</span>";
  }).join("");

  tabsEl.innerHTML = D.categorie.map(function (c) {
    return '<a href="#' + c.id + '" data-tab="' + c.id + '">' + U.esc(c.titolo) + "</a>";
  }).join("");

  rootEl.innerHTML = D.categorie.map(function (c) {
    var labels = Object.assign({}, D.etichetteColonne, c.etichette || {});
    var cols = c.colonne.map(function (k) { return "<span>" + U.esc(labels[k]) + "</span>"; }).join("");
    var items = c.piatti.map(function (p, i) {
      var prices = c.colonne.map(function (k, j) {
        if (p[k] == null) return '<span class="is-empty">—</span>';
        return '<span' + (j > 0 ? ' class="is-alt"' : "") + ">" + U.euro(p[k]) + "</span>";
      }).join("");
      var all = p.all && p.all.length
        ? '<p class="item__all">Allergeni: ' + p.all.map(function (a) { return D.allergeni[a].toLowerCase(); }).join(", ") + "</p>"
        : "";
      return '<li class="item" data-dish="' + c.id + ":" + i + '">' +
        '<div class="item__head"><h3 class="item__name">' + U.esc(p.nome) + "</h3>" + tagIcons(p) +
        '<span class="item__lead" aria-hidden="true"></span><span class="item__prices">' + prices + "</span></div>" +
        (p.desc ? '<p class="item__desc">' + U.esc(p.desc) + "</p>" : "") + all + "</li>";
    }).join("");
    return '<section class="cat" id="' + c.id + '" aria-labelledby="h-' + c.id + '">' +
      '<div class="cat__aside">' +
      (c.foto ? '<div class="cat__photo"><img src="' + foto + c.foto + '-700.webp" srcset="' + foto + c.foto + "-700.webp 700w, " + foto + c.foto +
        '-1300.webp 1300w" sizes="(max-width: 980px) 92vw, 34vw" alt="" loading="lazy" decoding="async"></div>' : "") +
      '<span class="cat__count" data-count="' + c.id + '"></span>' +
      '<h2 class="cat__title" id="h-' + c.id + '">' + U.esc(c.titolo) + "</h2>" +
      '<p class="cat__sub">' + U.esc(c.sottotitolo) + "</p></div>" +
      '<div><div class="cat__cols" aria-hidden="true">' + cols + '</div><ul class="items">' + items + "</ul></div></section>";
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

  var current = null;
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
      U.$("#" + c.id, rootEl).hidden = shown === 0;
      U.$('[data-tab="' + c.id + '"]', tabsEl).hidden = shown === 0;
      U.$('[data-count="' + c.id + '"]', rootEl).textContent = shown !== c.piatti.length
        ? shown + " di " + c.piatti.length + " proposte"
        : c.piatti.length + (c.piatti.length === 1 ? " proposta" : " proposte");
    });
    emptyEl.hidden = total > 0;
    allergenBtn.classList.toggle("has-value", state.exclude.length > 0);
    allergenBtn.textContent = state.exclude.length ? "Senza allergeni (" + state.exclude.length + ")" : "Escludi allergeni";
    current = null;
    requestAnimationFrame(spy);
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

  /* --------------------------------------- Scheda attiva durante lo scroll */
  var ticking = false;
  function stickyOffset() {
    return U.$(".site-header").offsetHeight + U.$(".menu-bar").offsetHeight + 12;
  }
  function spy() {
    ticking = false;
    var line = stickyOffset() + 60;
    var visible = U.$all(".cat", rootEl).filter(function (s) { return !s.hidden; });
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

  tabsEl.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    e.preventDefault();
    var target = document.getElementById(a.getAttribute("data-tab"));
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - stickyOffset() + 1, behavior: "smooth" });
    history.replaceState(null, "", "#" + target.id);
  });

  apply();

  // Arrivo da un link con #categoria (es. dalla Home): posiziona la pagina sotto la barra fissa.
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target) setTimeout(function () {
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - stickyOffset() + 1, behavior: "auto" });
    }, 60);
  }
})();
