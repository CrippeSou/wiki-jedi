/* Wiki Jedi. Cree par Pote.
   Deux choses, et rien d'autre : un fondu discret des sections a l'arrivee, et
   le filtre de recherche des pouvoirs et des formes. Pas d'animation continue :
   la page doit se lire, pas se regarder bouger. */

/* --------------------------------------------------------------------------
   Fondu a l'arrivee d'une section
   -------------------------------------------------------------------------- */
(function () {
  var sections = [].slice.call(document.querySelectorAll("section"));
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var oeil = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add("vue");
      oeil.unobserve(en.target);
    });
  }, { threshold: 0.05, rootMargin: "0px 0px -40px 0px" });

  sections.forEach(function (s) {
    // Ce qui est deja a l'ecran au chargement ne doit rien attendre : sinon la
    // premiere image de la page est vide.
    if (s.getBoundingClientRect().top < window.innerHeight) return;
    s.classList.add("apparait");
    oeil.observe(s);
  });
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
