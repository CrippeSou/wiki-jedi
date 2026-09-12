# -*- coding: utf-8 -*-
# Partie RENDU du wiki (la partie donnees est dans gen_wiki_tete.py, qui est
# execute juste avant). Mise en page de wiki : barre laterale fixe, sections
# ancrees, fiches par pouvoir, recherche instantanee.
#
# Les couleurs des voies sont celles du jeu (PALETTES dans cl_trees_uikit.lua) :
# le vert du Consulaire, le bleu du Gardien, l'or de la Sentinelle. Un joueur
# retrouve donc dans le wiki la couleur qu'il voit dans son arbre.

# =============================================================================
# Couleurs et libelles des voies
# =============================================================================
VOIES = {
 "padawan":      ("Padawan Jedi",      "#7E9AB4", "Le tronc commun, avant toute spécialisation."),
 "chevalier":    ("Chevalier Jedi",    "#9BB8D4", "Ce qu'un Chevalier ajoute au tronc commun."),
 "consulaire_i": ("Consulaire · Initié",  "#50BE76", "L'esprit ouvert à la Force : soigner, soutenir, tenir le groupe debout."),
 "consulaire_a": ("Consulaire · Avancé",  "#2DA55A", ""),
 "consulaire_m": ("Consulaire · Maître",  "#148744", ""),
 "gardien_i":    ("Gardien · Initié",     "#5A9DF0", "Le rempart de l'Ordre : encaisser, protéger, contenir."),
 "gardien_a":    ("Gardien · Avancé",     "#377DE1", ""),
 "gardien_m":    ("Gardien · Maître",     "#1E5FCD", ""),
 "sentinelle_i": ("Sentinelle · Initié",  "#F5CD5F", "La lame qui frappe la première : vitesse, discrétion, information."),
 "sentinelle_a": ("Sentinelle · Avancé",  "#EBB637", ""),
 "sentinelle_m": ("Sentinelle · Maître",  "#D79B19", ""),
 "conseil":      ("Conseil Jedi",         "#FFD250", "Réservé au Conseil, au Maître de l'Ordre et au Grand Maître."),
}
ORDRE = ["padawan", "chevalier", "consulaire_i", "consulaire_a", "consulaire_m",
         "gardien_i", "gardien_a", "gardien_m",
         "sentinelle_i", "sentinelle_a", "sentinelle_m", "conseil"]

PAGES = [("index.html", "Le fonctionnement"), ("pouvoirs.html", "Les pouvoirs"),
         ("formes.html", "Les formes"), ("competences.html", "Les compétences")]

# Change de valeur a chaque retouche du style : le navigateur du joueur garde la
# feuille en cache sinon, et il voit la page sans aucune mise en forme.
VERS = "3"

# L'embleme de l'Ordre, trace a la main : le halo de la lame vient du CSS.
CRETE = ('<svg class="crete" viewBox="0 0 64 64" aria-hidden="true">'
         '<g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">'
         '<path d="M13 37a19 19 0 0 0 38 0"/>'
         '<path d="M13 37C10 25 12 15 16.5 9c1.8 8 4.6 14.5 8.5 18.5"/>'
         '<path d="M51 37c3-12 1-22-3.5-28-1.8 8-4.6 14.5-8.5 18.5"/>'
         '</g>'
         '<path class="lame" d="M32 4l1.7 15.5V45h-3.4V19.5z" fill="currentColor"/>'
         '</svg>')


def e(x):
    return html.escape(str(x))


def page(nom, titre, sous_titre, sections, corps, script=""):
    """sections : [(ancre, libelle)] pour le sommaire de la barre laterale."""
    liens = "".join(
        '<a href="%s" class="%s">%s</a>' % (f, "actif" if f == nom else "", e(t))
        for f, t in PAGES)
    sommaire = ""
    if sections:
        sommaire = '<div class="sommaire"><span class="titre-sommaire">Sur cette page</span>%s</div>' % "".join(
            '<a href="#%s">%s</a>' % (a, e(l)) for a, l in sections)
    doc = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titre)s · Wiki Jedi</title>
<meta name="description" content="%(sous)s">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&family=Share+Tech+Mono&display=swap">
<link rel="stylesheet" href="style.css?v=%(vers)s">
</head>
<body>
<div class="voute" aria-hidden="true"></div>
<input type="checkbox" id="menu" class="bascule-menu" hidden>
<label for="menu" class="bouton-menu" aria-label="Menu">Menu</label>

<aside class="cote">
  <a class="marque" href="index.html">%(crete)s<span class="nom">Ordre Jedi<small>Archives du Temple</small></span></a>
  <nav class="nav-pages">%(liens)s</nav>
  %(sommaire)s
  <div class="pied-cote">Créé par Poté</div>
</aside>

<main>
  <header class="entete">
    <div class="fil">Wiki Jedi · %(titre)s</div>
    <h1>%(titre)s</h1>
    <p class="chapeau">%(sous)s</p>
  </header>
  %(corps)s
  <footer>Créé par Poté</footer>
</main>
%(script)s
</body>
</html>
''' % {"titre": e(titre), "sous": e(sous_titre), "liens": liens, "sommaire": sommaire,
       "corps": corps, "script": script, "vers": VERS, "crete": CRETE}
    io.open(os.path.join(OUT, nom), "w", encoding="utf-8", newline="\n").write(doc)


def pastille(texte, classe=""):
    return '<span class="pastille %s">%s</span>' % (classe, e(texte))


def fiche(nom, seances, chips, texte, couleur):
    ch = "".join('<span class="chip"><span class="cle">%s</span>%s</span>' % (e(k), e(v)) for k, v in chips)
    sea = ("Gratuit" if seances == 0 else "%d séance%s" % (seances, "s" if seances > 1 else ""))
    return '''<article class="fiche" style="--voie:%s">
  <div class="fiche-tete"><h3>%s</h3>%s</div>
  <div class="chips">%s</div>
  <p>%s</p>
</article>''' % (couleur, e(nom), pastille(sea, "seances"), ch, texte)


def recherche(cible, placeholder):
    return '''<div class="recherche">
  <input type="search" id="filtre" placeholder="%s" autocomplete="off">
  <span class="compte" id="compte"></span>
</div>''' % e(placeholder), '''<script>
(function(){
  var champ = document.getElementById("filtre");
  var compte = document.getElementById("compte");
  var fiches = Array.prototype.slice.call(document.querySelectorAll(".fiche"));
  var sections = Array.prototype.slice.call(document.querySelectorAll(".section-voie"));
  function filtrer(){
    var q = champ.value.trim().toLowerCase();
    var n = 0;
    fiches.forEach(function(f){
      var visible = q === "" || f.textContent.toLowerCase().indexOf(q) !== -1;
      f.hidden = !visible;
      if (visible) n++;
    });
    sections.forEach(function(s){
      s.hidden = s.querySelectorAll(".fiche:not([hidden])").length === 0;
    });
    compte.textContent = q === "" ? "" : n + (n > 1 ? " résultats" : " résultat");
  }
  champ.addEventListener("input", filtrer);
})();
</script>'''


# =============================================================================
# Page 1 : le fonctionnement
# =============================================================================
corps = '''
<section id="en-bref" class="bloc">
  <h2>En bref</h2>
  <div class="grille-bref">
    <div class="bref"><span class="nombre">2</span><span class="quoi">arbres à monter</span><p>Les pouvoirs et les formes de combat, chacun avec ses paliers.</p></div>
    <div class="bref"><span class="nombre">1</span><span class="quoi">séance par jour</span><p>Un pouvoir à « 3 séances » demande trois jours, et un seul apprentissage tourne à la fois.</p></div>
    <div class="bref"><span class="nombre">1</span><span class="quoi">seule voie</span><p>Gardien, Sentinelle ou Consulaire. On ne cumule pas.</p></div>
    <div class="bref"><span class="nombre">F6</span><span class="quoi">pour tout voir</span><p>Le menu du sabre : inventaire, arbres, réglages.</p></div>
  </div>
</section>

<section id="progression" class="bloc">
  <h2>Ta progression, de haut en bas</h2>
  <ol class="echelle">
    <li style="--voie:#7E9AB4"><h3>Padawan</h3><p>La branche Padawan s'ouvre à tout Jedi. Saut, Concentration, Extinction, Brèche.</p></li>
    <li style="--voie:#9BB8D4"><h3>Chevalier</h3><p>Le grade de Chevalier ajoute la branche Chevalier : Lancer, Poussée, Attraction, Saut II.</p></li>
    <li style="--voie:#50BE76"><h3>Initié de ta voie</h3><p>La whitelist de Gardien, Sentinelle ou Érudit ouvre le premier palier de ta spécialisation.</p></li>
    <li style="--voie:#EBB637"><h3>Avancé</h3><p>Ce palier ne s'ouvre plus tout seul : le Conseil te l'accorde depuis l'onglet Gérance.</p></li>
    <li style="--voie:#FFD250"><h3>Maître</h3><p>Même chose, accordé par le Conseil, une fois le palier Avancé terminé.</p></li>
  </ol>
  <p class="encadre"><strong>Deux conditions pour ouvrir un palier :</strong> avoir la whitelist du palier, <em>et</em> avoir terminé le palier précédent en entier. À l'intérieur d'un palier, tu apprends ce que tu veux, dans l'ordre que tu veux.</p>
</section>

<section id="seances" class="bloc">
  <h2>Les séances d'entraînement</h2>
  <p>Un pouvoir marqué « 3 séances » demande trois entraînements, <strong>un par tranche de 24 heures</strong>. Tu cliques une première fois, tu reviens le lendemain, et ainsi de suite jusqu'à la dernière séance : le pouvoir est alors appris pour de bon.</p>
  <p>Tant qu'une séance est en cours, <strong>aucun autre apprentissage</strong> ne peut démarrer, dans aucun des deux arbres. Les entrées marquées « Gratuit » s'obtiennent d'un seul clic.</p>
  <p class="encadre">Apprendre ne suffit pas à jouer le pouvoir : il faut ensuite l'<strong>activer</strong> dans l'arbre pour qu'il apparaisse dans ta roue. Les passifs, eux, agissent dès qu'ils sont appris.</p>
</section>

<section id="voies" class="bloc">
  <h2>Les trois voies</h2>
  <div class="grille-voies">
    <div class="voie" style="--voie:#50BE76"><h3>Consulaire</h3><p class="devise">L'esprit ouvert à la Force</p><p>Le soin et le soutien : Soin I à III, Soin d'autrui, Soin de masse, Réanimation, Grand soin. C'est la voie qui tient un groupe debout.</p></div>
    <div class="voie" style="--voie:#5A9DF0"><h3>Gardien</h3><p class="devise">Le rempart de l'Ordre</p><p>Encaisser et contenir : Immunité, Riposte, Barrière, Mur de Force, Jugements, Agenouillement. La voie qui reste debout au milieu.</p></div>
    <div class="voie" style="--voie:#F5CD5F"><h3>Sentinelle</h3><p class="devise">La lame qui frappe la première</p><p>Vitesse et information : Camouflage, Perception, Adrénaline, Téléportation, Rempart, Tourbillon. La voie qui choisit ses combats.</p></div>
  </div>
  <p>On ne monte que dans <strong>une</strong> voie. Dès qu'un palier t'est accordé, les deux autres se ferment ; pour en changer, le Conseil doit d'abord te retirer tes paliers.</p>
</section>

<section id="force" class="bloc">
  <h2>La Force, ta ressource</h2>
  <p>Chaque pouvoir coûte de la Force. Ta réserve remonte seule quand tu as les pieds au sol, et deux pouvoirs vivent entièrement de cette mécanique :</p>
  <ul>
    <li><strong>Concentration</strong> t'en rend d'un coup, au prix d'un ralentissement le temps de méditer.</li>
    <li><strong>Immunité</strong> ne te protège que tant que ta réserve reste au-dessus d'un seuil : 50 % au premier niveau, 35 % au deuxième, 20 % au troisième. Vider sa Force, c'est redevenir vulnérable aux pouvoirs adverses.</li>
  </ul>
</section>

<section id="combat" class="bloc">
  <h2>Ce que tu vois pendant le combat</h2>
  <div class="grille-bref">
    <div class="bref"><span class="quoi">La roue</span><p>En bas de l'écran : tes pouvoirs actifs, et le compte à rebours de celui que tu vises. Chaque pouvoir a son propre rechargement.</p></div>
    <div class="bref"><span class="quoi">Barre bleue</span><p>Un effet que tu as lancé et qui dure : Camouflage, Perception, Riposte, Tourbillon.</p></div>
    <div class="bref"><span class="quoi">Barre rouge</span><p>Un effet que tu <em>subis</em> : étourdissement, aveuglement, agenouillement forcé, pris dans un tourbillon.</p></div>
    <div class="bref"><span class="quoi">Éclat bleu</span><p>Ton Immunité vient d'absorber un pouvoir ennemi.</p></div>
  </div>
</section>
'''
page("index.html", "Le fonctionnement",
     "Comment un Jedi progresse : les séances, les paliers, les voies, la Force et ce que l'écran te dit pendant un combat.",
     [("en-bref", "En bref"), ("progression", "Ta progression"), ("seances", "Les séances"),
      ("voies", "Les trois voies"), ("force", "La Force"), ("combat", "Pendant le combat")],
     corps)

# =============================================================================
# Page 2 : les pouvoirs
# =============================================================================
par_cle = {cle: (label, noeuds) for cle, label, noeuds in POUVOIRS}
blocs, sections = [], []
champ, script = recherche("pouvoirs.html", "Chercher un pouvoir, un effet, un coût…")
blocs.append(champ)
for cle in ORDRE:
    if cle not in par_cle:
        continue
    _, noeuds = par_cle[cle]
    if not noeuds:
        continue
    titre, couleur, note = VOIES[cle]
    fiches = []
    for pid, nom, jours in noeuds:
        cout, rech, txt = P.get(pid, ("—", "—", ""))
        fiches.append(fiche(nom, jours, [("Coût", cout), ("Rechargement", rech)], txt, couleur))
    sections.append((cle, titre))
    blocs.append('''<section class="bloc section-voie" id="%s" style="--voie:%s">
  <div class="tete-voie"><h2>%s</h2><span class="compteur">%d pouvoir%s</span></div>
  %s
  <div class="fiches">%s</div>
</section>''' % (cle, couleur, e(titre), len(noeuds), "s" if len(noeuds) > 1 else "",
                 ('<p class="note-voie">%s</p>' % e(note)) if note else "", "".join(fiches)))
page("pouvoirs.html", "Les pouvoirs",
     "Tout ce qu'un Jedi peut apprendre, voie par voie et palier par palier. Les pouvoirs absents de l'arbre ne figurent pas ici : personne ne peut les obtenir.",
     sections, "".join(blocs), script)

# =============================================================================
# Page 3 : les formes
# =============================================================================
par_cle = {cle: (label, noeuds) for cle, label, noeuds in FORMES}
blocs, sections = [], []
champ, script = recherche("formes.html", "Chercher une forme…")
blocs.append(champ)
blocs.append('<p class="encadre">Une forme change tes enchaînements, tes dégâts au sabre et la garde que tu perds quand tu bloques. Celles marquées <strong>double sabre</strong> utilisent la lame de la main gauche ; avec une forme à une main, le second manche reste au fourreau.</p>')
for cle in ORDRE:
    if cle not in par_cle:
        continue
    _, noeuds = par_cle[cle]
    if not noeuds:
        continue
    titre, couleur, _ = VOIES[cle]
    fiches = []
    for fid, nom, jours in noeuds:
        st = FORMES_STATS.get(fid, {})
        try:
            pct = round((float(st.get("degats", "1")) - 1) * 100)
            degats = ("+%d %%" % pct) if pct else "normaux"
        except ValueError:
            degats = "normaux"
        chips = [("Dégâts", degats), ("Garde perdue", str(st.get("garde", "—"))),
                 ("Sabre", "double" if st.get("gauche") else "simple")]
        fiches.append(fiche(nom, jours, chips, FORMES_TXT.get(fid, ""), couleur))
    sections.append((cle, titre))
    blocs.append('''<section class="bloc section-voie" id="%s" style="--voie:%s">
  <div class="tete-voie"><h2>%s</h2><span class="compteur">%d forme%s</span></div>
  <div class="fiches">%s</div>
</section>''' % (cle, couleur, e(titre), len(noeuds), "s" if len(noeuds) > 1 else "", "".join(fiches)))
page("formes.html", "Les formes", "Les styles de combat au sabre, dans l'ordre où on les apprend.",
     sections, "".join(blocs), script)

# =============================================================================
# Page 4 : les compétences
# =============================================================================
EFFETS = {
 "speed": "vitesse de course", "walk": "vitesse en marchant", "hp": "PV maximum",
 "jump": "hauteur de saut", "fall": "dégâts de chute", "armor": "armure",
 "dmg_taken": "dégâts subis", "saber_dmg": "dégâts de sabre", "hp_regen": "PV régénérés hors combat",
 "guard": "garde", "force_regen": "régénération de Force", "force_max": "Force maximum",
 "force_cost": "coût des pouvoirs",
}
COULEUR_COMP = {"tronc": "#7E9AB4", "gardien": "#5A9DF0", "sentinelle": "#F5CD5F", "consulaire": "#50BE76"}


def lisible(effets):
    out = []
    for m in re.finditer(r"(\w+)\s*=\s*([\-\d.]+)", effets):
        cle, v = m.group(1), float(m.group(2))
        nom = EFFETS.get(cle, cle)
        if cle in ("dmg_taken", "force_cost", "fall"):
            out.append("%s −%d %%" % (nom, round(v * 100)))
        elif cle in ("saber_dmg", "jump"):
            out.append("%s +%d %%" % (nom, round(v * 100)))
        elif cle in ("guard", "force_regen"):
            out.append("%s ×%g" % (nom, v))
        else:
            out.append("%s +%g" % (nom, v))
    return out


blocs, sections = [], []
blocs.append('<p class="encadre">Les points viennent de ton <strong>niveau</strong>, qui monte en jouant sur un job Jedi. Chaque compétence coûte en plus des dataris, et s\'achète <strong>dans l\'ordre</strong> : la deuxième exige la première. Une voie complète demande 45 points et 110 000 dataris, le tronc 6 points et 13 000.</p>')
for cle, label, noeuds in COMPETENCES:
    couleur = COULEUR_COMP.get(cle, "#7E9AB4")
    items = []
    for i, (nom, desc, points, prix, effets) in enumerate(noeuds, 1):
        eff = "".join('<span class="chip">%s</span>' % e(x) for x in lisible(effets))
        items.append('''<li>
  <div class="rang">%d</div>
  <div class="contenu">
    <div class="fiche-tete"><h3>%s</h3><span class="pastille">%d point%s · %s dataris</span></div>
    <div class="chips">%s</div>
    <p>%s</p>
  </div>
</li>''' % (i, e(nom), points, "s" if points > 1 else "", "{:,}".format(prix).replace(",", " "), eff, e(desc)))
    sections.append((cle, label))
    blocs.append('''<section class="bloc section-voie" id="%s" style="--voie:%s">
  <div class="tete-voie"><h2>%s</h2><span class="compteur">%d compétences</span></div>
  <ol class="escalier">%s</ol>
</section>''' % (cle, couleur, e(label), len(noeuds), "".join(items)))
page("competences.html", "Les compétences",
     "Les bonus permanents de l'arbre de compétences. Ils agissent en continu, sans rien lancer, tant que tu es sur un job Jedi.",
     sections, "".join(blocs))
