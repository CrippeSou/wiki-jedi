/* Wiki Jedi. Cree par Pote.
   Deux choses : les onglets (ils ouvrent leur rubrique juste en dessous, sans
   recharger la page) et le filtre de recherche de chaque rubrique. */

(function () {
  var onglets = [].slice.call(document.querySelectorAll("[data-onglet]"));
  var panneaux = [].slice.call(document.querySelectorAll("[data-panneau]"));
  if (!onglets.length) return;

  var cles = panneaux.map(function (p) { return p.getAttribute("data-panneau"); });

  function ouvrir(cle, defiler) {
    if (cles.indexOf(cle) === -1) cle = cles[0];
    onglets.forEach(function (o) {
      o.classList.toggle("actif", o.getAttribute("data-onglet") === cle);
    });
    panneaux.forEach(function (p) {
      var visible = p.getAttribute("data-panneau") === cle;
      p.hidden = !visible;
      if (visible) {
        // Reparti a zero : on relance le fondu a chaque ouverture.
        p.classList.remove("entre");
        void p.offsetWidth;
        p.classList.add("entre");
      }
    });
    if (defiler) {
      var barre = document.querySelector(".onglets");
      var y = barre ? barre.getBoundingClientRect().top + window.pageYOffset - 8 : 0;
      window.scrollTo({ top: y, behavior: "smooth" });
    }
    return cle;
  }

  // Une ancre peut viser un onglet (#pouvoirs) ou une SECTION a l'interieur
  // d'un onglet (#gardien_m) : dans le second cas on ouvre le bon onglet, puis
  // on va a la section.
  function suivre(hash, defiler) {
    var cle = (hash || "").replace("#", "");
    if (!cle) { ouvrir(cles[0], false); return; }
    if (cles.indexOf(cle) !== -1) { ouvrir(cle, defiler); return; }

    var cible = document.getElementById(cle);
    if (!cible) { ouvrir(cles[0], false); return; }

    var parent = cible.closest("[data-panneau]");
    if (parent) ouvrir(parent.getAttribute("data-panneau"), false);
    cible.scrollIntoView({ behavior: defiler ? "smooth" : "auto", block: "start" });
  }

  onglets.forEach(function (o) {
    o.addEventListener("click", function (ev) {
      ev.preventDefault();
      var cle = o.getAttribute("data-onglet");
      history.replaceState(null, "", "#" + cle);
      ouvrir(cle, true);
    });
  });

  // Les cartes de l'accueil ouvrent elles aussi une rubrique.
  [].slice.call(document.querySelectorAll(".raccourci")).forEach(function (a) {
    a.addEventListener("click", function (ev) {
      var cle = a.getAttribute("href").replace("#", "");
      if (cles.indexOf(cle) === -1) return;
      ev.preventDefault();
      history.replaceState(null, "", "#" + cle);
      ouvrir(cle, true);
    });
  });

  window.addEventListener("hashchange", function () { suivre(location.hash, true); });
  suivre(location.hash, false);
})();

/* --------------------------------------------------------------------------
   Recherche, une par rubrique
   -------------------------------------------------------------------------- */
[].slice.call(document.querySelectorAll(".filtre")).forEach(function (champ) {
  var panneau = champ.closest("[data-panneau]");
  if (!panneau) return;
  var compte = panneau.querySelector(".compte");
  var cartes = [].slice.call(panneau.querySelectorAll(".carte"));
  var sections = [].slice.call(panneau.querySelectorAll(".section-voie"));

  champ.addEventListener("input", function () {
    var q = champ.value.trim().toLowerCase();
    var n = 0;
    cartes.forEach(function (c) {
      var visible = q === "" || c.textContent.toLowerCase().indexOf(q) !== -1;
      c.hidden = !visible;
      if (visible) n++;
    });
    sections.forEach(function (s) {
      s.hidden = s.querySelectorAll(".carte:not([hidden])").length === 0;
    });
    if (compte) compte.textContent = q === "" ? "" : n + (n > 1 ? " résultats" : " résultat");
  });
});
