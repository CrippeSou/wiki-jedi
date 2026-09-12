# -*- coding: utf-8 -*-
# Partie RENDU du wiki (les donnees sont dans gen_wiki_tete.py, execute juste
# avant). Mise en page reprise de l'esprit du site de l'Escouade Omega :
# barre de navigation collante en haut, ciel etoile anime, hero avec l'embleme
# rond, en-tetes de section numerotes, cartes a coin coupe.
#
# Les couleurs des voies sont celles du jeu (PALETTES dans cl_trees_uikit.lua) :
# vert Consulaire, bleu Gardien, or Sentinelle. Un joueur retrouve dans le wiki
# la couleur qu'il voit dans son arbre.

# Change de valeur a chaque retouche du style ou du script : sans ca, le
# navigateur garde l'ancienne feuille en cache et la page s'affiche nue.
VERS = "5"

# =============================================================================
# Couleurs et libelles des voies
# =============================================================================
VOIES = {
 "padawan":      ("Padawan Jedi",        "#8FB4D8", "Le tronc commun, avant toute spécialisation."),
 "chevalier":    ("Chevalier Jedi",      "#A8CBEA", "Ce qu'un Chevalier ajoute au tronc commun."),
 "consulaire_i": ("Consulaire · Initié", "#56D08D", "L'esprit ouvert à la Force : soigner, soutenir, tenir le groupe debout."),
 "consulaire_a": ("Consulaire · Avancé", "#3BBA73", ""),
 "consulaire_m": ("Consulaire · Maître", "#2AA05E", ""),
 "gardien_i":    ("Gardien · Initié",    "#5AA8FF", "Le rempart de l'Ordre : encaisser, protéger, contenir."),
 "gardien_a":    ("Gardien · Avancé",    "#3D8BEE", ""),
 "gardien_m":    ("Gardien · Maître",    "#2A6FD8", ""),
 "sentinelle_i": ("Sentinelle · Initié", "#F5D174", "La lame qui frappe la première : vitesse, discrétion, information."),
 "sentinelle_a": ("Sentinelle · Avancé", "#E8BC4C", ""),
 "sentinelle_m": ("Sentinelle · Maître", "#D5A22C", ""),
 "conseil":      ("Conseil Jedi",        "#FFD86B", "Réservé au Conseil, au Maître de l'Ordre et au Grand Maître."),
}
ORDRE = ["padawan", "chevalier", "consulaire_i", "consulaire_a", "consulaire_m",
         "gardien_i", "gardien_a", "gardien_m",
         "sentinelle_i", "sentinelle_a", "sentinelle_m", "conseil"]

PAGES = [("index.html", "Accueil"), ("pouvoirs.html", "Pouvoirs"),
         ("formes.html", "Formes"), ("competences.html", "Compétences")]


def e(x):
    return html.escape(str(x))


def page(nom, titre, sous_titre, corps, hero=False):
    liens = "".join(
        '<a href="%s"%s>%s</a>' % (f, ' class="actif"' if f == nom else "", e(t))
        for f, t in PAGES)
    doc = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titre)s · Wiki Jedi</title>
<meta name="description" content="%(sous)s">
<meta name="theme-color" content="#04060B">
<link rel="icon" type="image/svg+xml" href="logo.svg">
<style>html,body{background:#04060B;}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=%(vers)s">
</head>
<body>
<canvas id="etoiles"></canvas>

<nav>
  <a class="nav-marque" href="index.html">
    <span class="nav-embleme"><img src="logo.svg" alt=""></span>
    <span class="nav-nom">Wiki Jedi</span>
  </a>
  %(liens)s
</nav>

<div class="contenu">
%(corps)s
  <footer>
    <span class="pied-embleme"><img src="logo.svg" alt=""></span>
    Créé par Poté
  </footer>
</div>

<script src="script.js?v=%(vers)s"></script>
</body>
</html>
''' % {"titre": e(titre), "sous": e(sous_titre), "liens": liens,
       "corps": corps, "vers": VERS}
    io.open(os.path.join(OUT, nom), "w", encoding="utf-8", newline="\n").write(doc)


def tete_page(titre, intro, ancres):
    """En-tete des pages internes : titre, chapeau, et les raccourcis vers
    chaque palier (12 sections sur la page des pouvoirs, sans eux on scrolle
    a l'aveugle)."""
    puces = "".join('<a href="#%s" style="--voie:%s">%s</a>' % (a, c, e(l)) for a, l, c in ancres)
    return '''  <header class="tete-page">
    <div class="sur-titre">Archives de l'Ordre</div>
    <h1>%s</h1>
    <p class="intro-page">%s</p>
    <nav class="ancres">%s</nav>
  </header>
''' % (e(titre), e(intro), puces)


def entete_section(numero, titre, compte, couleur):
    return '''  <div class="tete-section">
    <span class="num-section">%02d</span>
    <h2 class="titre-section">%s</h2>
    <span class="ligne-section"></span>
    <span class="compte-section">%s</span>
  </div>''' % (numero, e(titre), e(compte))


def fiche(nom, seances, chips, texte, couleur):
    ch = "".join('<span class="chip"><span class="cle">%s</span>%s</span>' % (e(k), e(v)) for k, v in chips)
    sea = ("Gratuit" if seances == 0 else "%d séance%s" % (seances, "s" if seances > 1 else ""))
    return '''<article class="carte" style="--voie:%s">
  <div class="carte-tete"><h3>%s</h3><span class="badge">%s</span></div>
  <div class="chips">%s</div>
  <p>%s</p>
</article>''' % (couleur, e(nom), e(sea), ch, texte)


CHAMP = '''  <div class="recherche">
    <input type="search" id="filtre" placeholder="%s" autocomplete="off">
    <span class="compte" id="compte"></span>
  </div>
'''


# =============================================================================
# Page 1 : l'accueil
# =============================================================================
RACCOURCIS = [
 ("pouvoirs.html", "Pouvoirs", "Tout ce qui s'apprend dans l'arbre, voie par voie"),
 ("formes.html", "Formes", "Les styles de combat au sabre"),
 ("competences.html", "Compétences", "Les bonus permanents et leur prix"),
]
cartes = "".join('''<a class="raccourci" href="%s">
      <span class="raccourci-num">%02d</span>
      <span class="raccourci-titre">%s</span>
      <span class="raccourci-desc">%s</span>
    </a>''' % (f, i, e(t), e(d)) for i, (f, t, d) in enumerate(RACCOURCIS, 1))

corps = '''  <section id="hero">
    <div class="hero-embleme"><img src="logo.svg" alt="Emblème de l'Ordre Jedi"></div>
    <div class="hero-titre">Ordre Jedi</div>
    <div class="hero-sous">Wiki des Jedi · Clone Wars RP Cosmos</div>
    <div class="hero-devise"><em>Il n'y a pas d'émotion, il y a la paix</em></div>
    <div class="raccourcis">%s</div>
  </section>

  <section id="progression">
%s
    <p class="intro-section">Un Jedi monte <strong>deux arbres</strong> : celui des pouvoirs de Force et celui des formes de combat. Les deux fonctionnent de la même façon, par paliers, et le passage d'un palier au suivant ne dépend pas que de toi.</p>
    <ol class="echelle">
      <li style="--voie:#8FB4D8"><h3>Padawan</h3><p>La branche Padawan s'ouvre à tout Jedi. Saut, Concentration, Extinction, Brèche.</p></li>
      <li style="--voie:#A8CBEA"><h3>Chevalier</h3><p>Le grade de Chevalier ajoute la branche Chevalier : Lancer, Poussée, Attraction, Saut II.</p></li>
      <li style="--voie:#56D08D"><h3>Initié de ta voie</h3><p>La whitelist de Gardien, Sentinelle ou Érudit ouvre le premier palier de ta spécialisation.</p></li>
      <li style="--voie:#E8BC4C"><h3>Avancé</h3><p>Ce palier ne s'ouvre plus tout seul : le Conseil te l'accorde depuis l'onglet Gérance.</p></li>
      <li style="--voie:#FFD86B"><h3>Maître</h3><p>Même chose, accordé par le Conseil, une fois le palier Avancé terminé.</p></li>
    </ol>
    <div class="note"><strong>Deux conditions pour ouvrir un palier :</strong> avoir la whitelist du palier, <em>et</em> avoir terminé le palier précédent en entier. À l'intérieur d'un palier, tu apprends ce que tu veux, dans l'ordre que tu veux.</div>
  </section>

  <section id="seances">
%s
    <p class="intro-section">Un pouvoir marqué « 3 séances » demande trois entraînements, <strong>un par tranche de 24 heures</strong>. Tu cliques une première fois, tu reviens le lendemain, et ainsi de suite jusqu'à la dernière séance : le pouvoir est alors appris pour de bon.</p>
    <div class="grille-info">
      <div class="info"><h4>Un apprentissage à la fois</h4><p>Tant qu'une séance est en cours, aucun autre apprentissage ne peut démarrer, dans aucun des deux arbres.</p></div>
      <div class="info"><h4>Apprendre puis équiper</h4><p>Un pouvoir appris n'arrive pas tout seul dans ta roue : il faut l'activer dans l'arbre. Les passifs, eux, agissent dès qu'ils sont appris.</p></div>
      <div class="info"><h4>Les entrées gratuites</h4><p>Celles marquées « Gratuit » s'obtiennent d'un seul clic, sans attendre.</p></div>
      <div class="info"><h4>F6</h4><p>Le menu du sabre : inventaire, arbres, réglages. C'est de là que tout se pilote.</p></div>
    </div>
  </section>

  <section id="voies">
%s
    <p class="intro-section">On ne monte que dans <strong>une</strong> voie. Dès qu'un palier t'est accordé, les deux autres se ferment ; pour en changer, le Conseil doit d'abord te retirer tes paliers.</p>
    <div class="grille-voies">
      <div class="voie" style="--voie:#56D08D"><h3>Consulaire</h3><p class="devise">L'esprit ouvert à la Force</p><p>Le soin et le soutien : Soin I à III, Soin d'autrui, Soin de masse, Réanimation, Grand soin. C'est la voie qui tient un groupe debout.</p></div>
      <div class="voie" style="--voie:#5AA8FF"><h3>Gardien</h3><p class="devise">Le rempart de l'Ordre</p><p>Encaisser et contenir : Immunité, Riposte, Barrière, Mur de Force, Jugements, Agenouillement. La voie qui reste debout au milieu.</p></div>
      <div class="voie" style="--voie:#E8BC4C"><h3>Sentinelle</h3><p class="devise">La lame qui frappe la première</p><p>Vitesse et information : Camouflage, Perception, Adrénaline, Téléportation, Rempart, Tourbillon. La voie qui choisit ses combats.</p></div>
    </div>
  </section>

  <section id="force">
%s
    <p class="intro-section">Chaque pouvoir coûte de la Force. Ta réserve remonte seule quand tu as les pieds au sol, et deux pouvoirs vivent entièrement de cette mécanique.</p>
    <div class="grille-info">
      <div class="info"><h4>Concentration</h4><p>Rend de la Force d'un coup, au prix d'un ralentissement le temps de méditer. On médite à l'abri, pas au milieu d'un échange.</p></div>
      <div class="info"><h4>Immunité</h4><p>Ne te protège que tant que ta réserve reste au-dessus d'un seuil : 50 %% au premier niveau, 35 %% au deuxième, 20 %% au troisième. Vider sa Force, c'est redevenir vulnérable.</p></div>
    </div>
  </section>

  <section id="combat">
%s
    <p class="intro-section">Pendant un combat, l'interface te dit tout ce dont tu as besoin. Apprends à la lire, elle ne ment pas.</p>
    <div class="grille-info">
      <div class="info"><h4>La roue</h4><p>En bas de l'écran : tes pouvoirs actifs et le compte à rebours de celui que tu vises. Chaque pouvoir a son propre rechargement.</p></div>
      <div class="info tonalite-bleu"><h4>Barre bleue</h4><p>Un effet que tu as lancé et qui dure : Camouflage, Perception, Riposte, Tourbillon.</p></div>
      <div class="info tonalite-rouge"><h4>Barre rouge</h4><p>Un effet que tu subis : étourdissement, aveuglement, agenouillement forcé, pris dans un tourbillon.</p></div>
      <div class="info tonalite-bleu"><h4>Éclat bleu</h4><p>Ton Immunité vient d'absorber un pouvoir ennemi.</p></div>
    </div>
  </section>
''' % (cartes,
       entete_section(1, "Ta progression", "5 paliers", "#5AA8FF"),
       entete_section(2, "Les séances d'entraînement", "1 par jour", "#5AA8FF"),
       entete_section(3, "Les trois voies", "1 seule au choix", "#5AA8FF"),
       entete_section(4, "La Force", "ta ressource", "#5AA8FF"),
       entete_section(5, "Pendant le combat", "lire l'écran", "#5AA8FF"))

page("index.html", "Accueil",
     "Le wiki des Jedi du Clone Wars RP Cosmos : pouvoirs de Force, formes de combat, compétences et progression.",
     corps, hero=True)

# =============================================================================
# Page 2 : les pouvoirs
# =============================================================================
par_cle = {cle: (label, noeuds) for cle, label, noeuds in POUVOIRS}
blocs, ancres, n = [], [], 0
for cle in ORDRE:
    if cle not in par_cle or not par_cle[cle][1]:
        continue
    noeuds = par_cle[cle][1]
    titre, couleur, note = VOIES[cle]
    n += 1
    ancres.append((cle, titre, couleur))
    fiches = []
    for pid, nom, jours in noeuds:
        cout, rech, txt = P.get(pid, ("—", "—", ""))
        fiches.append(fiche(nom, jours, [("Coût", cout), ("Rechargement", rech)], txt, couleur))
    blocs.append('''  <section class="section-voie" id="%s" style="--voie:%s">
%s
%s
    <div class="grille-cartes">%s</div>
  </section>''' % (cle, couleur,
                   entete_section(n, titre, "%d pouvoir%s" % (len(noeuds), "s" if len(noeuds) > 1 else ""), couleur),
                   ('    <p class="intro-section">%s</p>' % e(note)) if note else "",
                   "".join(fiches)))

page("pouvoirs.html", "Pouvoirs",
     "Tout ce qu'un Jedi peut apprendre, voie par voie et palier par palier.",
     tete_page("Les pouvoirs",
               "Les pouvoirs de Force présents dans l'arbre, avec leur coût, leur rechargement et le nombre de séances. Ceux qui n'y figurent pas ne sont apprenables par personne.",
               ancres)
     + (CHAMP % "Chercher un pouvoir, un effet, un coût...") + "".join(blocs))

# =============================================================================
# Page 3 : les formes
# =============================================================================
par_cle = {cle: (label, noeuds) for cle, label, noeuds in FORMES}
blocs, ancres, n = [], [], 0
for cle in ORDRE:
    if cle not in par_cle or not par_cle[cle][1]:
        continue
    noeuds = par_cle[cle][1]
    titre, couleur, _ = VOIES[cle]
    n += 1
    ancres.append((cle, titre, couleur))
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
    blocs.append('''  <section class="section-voie" id="%s" style="--voie:%s">
%s
    <div class="grille-cartes">%s</div>
  </section>''' % (cle, couleur,
                   entete_section(n, titre, "%d forme%s" % (len(noeuds), "s" if len(noeuds) > 1 else ""), couleur),
                   "".join(fiches)))

page("formes.html", "Formes", "Les styles de combat au sabre, dans l'ordre où on les apprend.",
     tete_page("Les formes",
               "Une forme change tes enchaînements, tes dégâts au sabre et la garde que tu perds en bloquant. Celles marquées double sabre utilisent la lame de la main gauche ; avec une forme à une main, le second manche reste au fourreau.",
               ancres)
     + (CHAMP % "Chercher une forme...") + "".join(blocs))

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
COULEUR_COMP = {"tronc": "#8FB4D8", "gardien": "#5AA8FF", "sentinelle": "#E8BC4C", "consulaire": "#56D08D"}


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


blocs, ancres, n = [], [], 0
for cle, label, noeuds in COMPETENCES:
    couleur = COULEUR_COMP.get(cle, "#8FB4D8")
    n += 1
    ancres.append((cle, label, couleur))
    items = []
    for i, (nom, desc, points, prix, effets) in enumerate(noeuds, 1):
        eff = "".join('<span class="chip">%s</span>' % e(x) for x in lisible(effets))
        items.append('''<li>
      <span class="rang">%d</span>
      <div class="rang-corps">
        <div class="carte-tete"><h3>%s</h3><span class="badge">%d point%s · %s dataris</span></div>
        <div class="chips">%s</div>
        <p>%s</p>
      </div>
    </li>''' % (i, e(nom), points, "s" if points > 1 else "",
                 "{:,}".format(prix).replace(",", " "), eff, e(desc)))
    blocs.append('''  <section class="section-voie" id="%s" style="--voie:%s">
%s
    <ol class="escalier">%s</ol>
  </section>''' % (cle, couleur,
                   entete_section(n, label, "%d compétences" % len(noeuds), couleur),
                   "".join(items)))

page("competences.html", "Compétences",
     "Les bonus permanents de l'arbre de compétences, leur coût en points et en dataris.",
     tete_page("Les compétences",
               "Des bonus permanents, qui agissent en continu sans rien lancer, tant que tu es sur un job Jedi. Les points viennent de ton niveau ; chaque compétence coûte en plus des dataris et s'achète dans l'ordre. Une voie complète demande 45 points et 110 000 dataris, le tronc 6 points et 13 000.",
               ancres)
     + "".join(blocs))
