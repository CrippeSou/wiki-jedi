/* Wiki Jedi. Cree par Pote.
   Trois choses, et rien d'autre : le ciel etoile, l'apparition des sections au
   defilement, et le filtre de recherche des pouvoirs et des formes. */

/* --------------------------------------------------------------------------
   Le ciel
   -------------------------------------------------------------------------- */
(function () {
  var toile = document.getElementById("etoiles");
  if (!toile) return;
  var ctx = toile.getContext("2d");
  var etoiles = [];
  var sobre = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function semer() {
    toile.width = window.innerWidth;
    toile.height = window.innerHeight;
    // Une densite, pas un nombre fixe : sinon un grand ecran parait vide.
    var combien = Math.min(260, Math.round(toile.width * toile.height / 9000));
    etoiles = [];
    for (var i = 0; i < combien; i++) {
      etoiles.push({
        x: Math.random() * toile.width,
        y: Math.random() * toile.height,
        r: Math.random() * 1.25 + 0.25,
        a: Math.random() * 0.5 + 0.2,
        v: (Math.random() * 0.4 + 0.1) / 60,
        p: Math.random() * Math.PI * 2
      });
    }
  }

  function peindre() {
    ctx.clearRect(0, 0, toile.width, toile.height);
    for (var i = 0; i < etoiles.length; i++) {
      var s = etoiles[i];
      s.p += s.v;
      var a = sobre ? s.a : s.a + Math.sin(s.p) * 0.18;
      ctx.globalAlpha = Math.max(0.05, Math.min(1, a));
      ctx.fillStyle = i % 9 === 0 ? "#E8C46A" : "#BFD9FF";
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    if (!sobre) requestAnimationFrame(peindre);
  }

  semer();
  peindre();
  var attente;
  window.addEventListener("resize", function () {
    clearTimeout(attente);
    attente = setTimeout(function () { semer(); if (sobre) peindre(); }, 150);
  });
})();

/* --------------------------------------------------------------------------
   Apparition au defilement
   -------------------------------------------------------------------------- */
(function () {
  var cibles = document.querySelectorAll("section");
  if (!("IntersectionObserver" in window)) return;
  var oeil = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add("vue");
        oeil.unobserve(en.target);
      }
    });
  }, { threshold: 0.06, rootMargin: "0px 0px -40px 0px" });
  for (var i = 0; i < cibles.length; i++) {
    // Le hero est deja a l'ecran au chargement : il ne doit rien attendre.
    if (cibles[i].id === "hero") { cibles[i].classList.add("vue"); continue; }
    cibles[i].classList.add("apparait");
    oeil.observe(cibles[i]);
  }
})();

/* --------------------------------------------------------------------------
   Recherche
   -------------------------------------------------------------------------- */
(function () {
  var champ = document.getElementById("filtre");
  if (!champ) return;
  var compte = document.getElementById("compte");
  var cartes = [].slice.call(document.querySelectorAll(".carte"));
  var sections = [].slice.call(document.querySelectorAll(".section-voie"));

  function filtrer() {
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
  }

  champ.addEventListener("input", filtrer);
})();
