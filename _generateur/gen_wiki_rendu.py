# -*- coding: utf-8 -*-
# Partie RENDU du wiki (les donnees sont dans gen_wiki_tete.py, execute juste
# avant).
#
# Parti pris : une page CALME, sur un papier chaud et sable. Beaucoup d'air,
# coins arrondis, titres en serif chaud. Rien ne clignote, rien ne brille.
#
# Structure : UNE SEULE page. L'en-tete (embleme, titre, devise) reste en haut,
# les quatre rubriques sont des ONGLETS poses juste en dessous, et le contenu
# s'ouvre sous eux sans recharger quoi que ce soit. Les trois anciennes adresses
# (pouvoirs.html, formes.html, competences.html) sont conservees : ce sont des
# redirections vers l'onglet correspondant, pour ne casser aucun lien deja
# partage.
#
# Les couleurs des voies restent celles du jeu (PALETTES dans cl_trees_uikit.lua)
# - vert Consulaire, bleu Gardien, or Sentinelle - assombries pour tenir sur un
# fond clair.

# Change de valeur a chaque retouche du style ou du script : sans ca, le
# navigateur garde l'ancienne feuille en cache et la page s'affiche nue.
VERS = "10"

# =============================================================================
# Couleurs et libelles des voies
# =============================================================================
VOIES = {
 "padawan":      ("Padawan Jedi",        "#A6B2BE", "Le tronc commun, avant toute spécialisation."),
 "chevalier":    ("Chevalier Jedi",      "#B7C3CE", "Ce qu'un Chevalier ajoute au tronc commun."),
 "consulaire_i": ("Consulaire · Initié", "#7FC49C", "L'esprit ouvert à la Force : soigner, soutenir, tenir le groupe debout."),
 "consulaire_a": ("Consulaire · Avancé", "#6EB78C", ""),
 "consulaire_m": ("Consulaire · Maître", "#5FA87D", ""),
 "gardien_i":    ("Gardien · Initié",    "#8CB0E0", "Le rempart de l'Ordre : encaisser, protéger, contenir."),
 "gardien_a":    ("Gardien · Avancé",    "#7BA0D6", ""),
 "gardien_m":    ("Gardien · Maître",    "#6A90C9", ""),
 "sentinelle_i": ("Sentinelle · Initié", "#D7B978", "La lame qui frappe la première : vitesse, discrétion, information."),
 "sentinelle_a": ("Sentinelle · Avancé", "#C9A960", ""),
 "sentinelle_m": ("Sentinelle · Maître", "#BB9A4C", ""),
 "conseil":      ("Conseil Jedi",        "#E0C68A", "Réservé au Conseil, au Maître de l'Ordre et au Grand Maître."),
}
ORDRE = ["padawan", "chevalier", "consulaire_i", "consulaire_a", "consulaire_m",
         "gardien_i", "gardien_a", "gardien_m",
         "sentinelle_i", "sentinelle_a", "sentinelle_m", "conseil"]

ONGLETS = [("accueil", "Accueil"), ("pouvoirs", "Pouvoirs"),
           ("formes", "Formes"), ("competences", "Compétences")]


def e(x):
    return html.escape(str(x))


def entete_section(numero, titre, compte):
    return '''      <div class="tete-section">
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


def tete_rubrique(titre, intro):
    """Titre de la rubrique et son chapeau. La rangee de pastilles vers chaque
    palier a ete RETIREE : les en-tetes de section numerotes suffisent, et elle
    encombrait le haut de chaque rubrique."""
    return '''      <header class="tete-rubrique">
        <h2 class="titre-rubrique">%s</h2>
        <p class="intro-rubrique">%s</p>
      </header>
''' % (e(titre), e(intro))


def champ(placeholder):
    return '''      <div class="recherche">
        <input type="search" class="filtre" placeholder="%s" autocomplete="off">
        <span class="compte"></span>
      </div>
''' % e(placeholder)


# =============================================================================
# Onglet 1 : l'accueil
# =============================================================================
RACCOURCIS = [
 ("pouvoirs", "Pouvoirs", "Tout ce qui s'apprend dans l'arbre, voie par voie"),
 ("formes", "Formes", "Les styles de combat au sabre"),
 ("competences", "Compétences", "Les bonus permanents et leur prix"),
]
cartes = "".join('''<a class="raccourci" href="#%s">
          <span class="raccourci-num">%02d</span>
          <span class="raccourci-titre">%s</span>
          <span class="raccourci-desc">%s</span>
        </a>''' % (f, i, e(t), e(d)) for i, (f, t, d) in enumerate(RACCOURCIS, 1))

ACCUEIL = '''      <header class="tete-rubrique">
        <p class="intro-rubrique accroche">Tout ce qu'un Jedi peut apprendre sur le serveur : les pouvoirs de Force, les formes de combat au sabre et les compétences permanentes. Les chiffres affichés sont ceux que le serveur applique vraiment.</p>
        <div class="raccourcis">%s</div>
      </header>

      <section id="progression">
%s
        <p class="intro-section">Un Jedi monte <strong>deux arbres</strong> : celui des pouvoirs de Force et celui des formes de combat. Les deux fonctionnent de la même façon, par paliers, et le passage d'un palier au suivant ne dépend pas que de toi.</p>
        <ol class="echelle">
          <li style="--voie:#A6B2BE"><h3>Padawan</h3><p>La branche Padawan s'ouvre à tout Jedi. Saut, Concentration, Extinction, Brèche.</p></li>
          <li style="--voie:#B7C3CE"><h3>Chevalier</h3><p>Le grade de Chevalier ajoute la branche Chevalier : Lancer, Poussée, Attraction, Saut II.</p></li>
          <li style="--voie:#7FC49C"><h3>Initié de ta voie</h3><p>La whitelist de Gardien, Sentinelle ou Érudit ouvre le premier palier de ta spécialisation.</p></li>
          <li style="--voie:#C9A960"><h3>Avancé</h3><p>Ce palier ne s'ouvre plus tout seul : le Conseil te l'accorde depuis l'onglet Gérance.</p></li>
          <li style="--voie:#E0C68A"><h3>Maître</h3><p>Même chose, accordé par le Conseil, une fois le palier Avancé terminé.</p></li>
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
          <div class="voie" style="--voie:#7FC49C"><h3>Consulaire</h3><p class="devise-voie">L'esprit ouvert à la Force</p><p>Le soin et le soutien : Soin I à III, Soin d'autrui, Soin de masse, Réanimation, Grand soin. C'est la voie qui tient un groupe debout.</p></div>
          <div class="voie" style="--voie:#8CB0E0"><h3>Gardien</h3><p class="devise-voie">Le rempart de l'Ordre</p><p>Encaisser et contenir : Immunité, Riposte, Barrière, Mur de Force, Jugements, Agenouillement. La voie qui reste debout au milieu.</p></div>
          <div class="voie" style="--voie:#C9A960"><h3>Sentinelle</h3><p class="devise-voie">La lame qui frappe la première</p><p>Vitesse et information : Camouflage, Perception, Adrénaline, Téléportation, Rempart, Tourbillon. La voie qui choisit ses combats.</p></div>
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
       entete_section(1, "Ta progression", "5 paliers"),
       entete_section(2, "Les séances d'entraînement", "1 par jour"),
       entete_section(3, "Les trois voies", "1 seule au choix"),
       entete_section(4, "La Force", "ta ressource"),
       entete_section(5, "Pendant le combat", "lire l'écran"))


# =============================================================================
# Onglets 2 et 3 : les deux arbres, meme fabrication
# =============================================================================
def rubrique_arbre(source, titre, intro, place, compter, fabrique):
    par_cle = {cle: noeuds for cle, _, noeuds in source}
    blocs, n = [], 0
    for cle in ORDRE:
        noeuds = par_cle.get(cle)
        if not noeuds:
            continue
        libelle, couleur, note = VOIES[cle]
        n += 1
        fiches = "".join(fabrique(noeud, couleur) for noeud in noeuds)
        blocs.append('''      <section class="section-voie" id="%s" style="--voie:%s">
%s
%s
        <div class="grille-cartes">%s</div>
      </section>''' % (cle, couleur,
                       entete_section(n, libelle, compter(len(noeuds))),
                       ('        <p class="intro-section">%s</p>' % e(note)) if note else "",
                       fiches))
    return tete_rubrique(titre, intro) + champ(place) + "".join(blocs)


def fiche_pouvoir(noeud, couleur):
    pid, nom, jours = noeud
    cout, rech, txt = P.get(pid, ("—", "—", ""))
    return fiche(nom, jours, [("Coût", cout), ("Rechargement", rech)], txt, couleur)


def fiche_forme(noeud, couleur):
    fid, nom, jours = noeud
    st = FORMES_STATS.get(fid, {})
    try:
        pct = round((float(st.get("degats", "1")) - 1) * 100)
        degats = ("+%d %%" % pct) if pct else "normaux"
    except ValueError:
        degats = "normaux"
    chips = [("Dégâts", degats), ("Garde perdue", str(st.get("garde", "—"))),
             ("Sabre", "double" if st.get("gauche") else "simple")]
    return fiche(nom, jours, chips, FORMES_TXT.get(fid, ""), couleur)


POUVOIRS_HTML = rubrique_arbre(
    POUVOIRS, "Les pouvoirs",
    "Les pouvoirs de Force présents dans l'arbre, avec leur coût, leur rechargement et le nombre de séances. Ceux qui n'y figurent pas ne sont apprenables par personne.",
    "Chercher un pouvoir, un effet, un coût...",
    lambda k: "%d pouvoir%s" % (k, "s" if k > 1 else ""),
    fiche_pouvoir)

FORMES_HTML = rubrique_arbre(
    FORMES, "Les formes",
    "Une forme change tes enchaînements, tes dégâts au sabre et la garde que tu perds en bloquant. Celles marquées double sabre utilisent la lame de la main gauche ; avec une forme à une main, le second manche reste au fourreau.",
    "Chercher une forme...",
    lambda k: "%d forme%s" % (k, "s" if k > 1 else ""),
    fiche_forme)


# =============================================================================
# Onglet 4 : les compétences
# =============================================================================
EFFETS = {
 "speed": "vitesse de course", "walk": "vitesse en marchant", "hp": "PV maximum",
 "jump": "hauteur de saut", "fall": "dégâts de chute", "armor": "armure",
 "dmg_taken": "dégâts subis", "saber_dmg": "dégâts de sabre", "hp_regen": "PV régénérés hors combat",
 "guard": "garde", "force_regen": "régénération de Force", "force_max": "Force maximum",
 "force_cost": "coût des pouvoirs",
}
COULEUR_COMP = {"tronc": "#A6B2BE", "gardien": "#8CB0E0", "sentinelle": "#C9A960", "consulaire": "#7FC49C"}


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


blocs, n = [], 0
for cle, label, noeuds in COMPETENCES:
    couleur = COULEUR_COMP.get(cle, "#A6B2BE")
    n += 1
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
    blocs.append('''      <section class="section-voie" id="%s" style="--voie:%s">
%s
        <ol class="escalier">%s</ol>
      </section>''' % (cle, couleur,
                       entete_section(n, label, "%d compétences" % len(noeuds)),
                       "".join(items)))

COMPETENCES_HTML = tete_rubrique(
    "Les compétences",
    "Des bonus permanents, qui agissent en continu sans rien lancer, tant que tu es sur un job Jedi. Les points viennent de ton niveau ; chaque compétence coûte en plus des dataris et s'achète dans l'ordre. Une voie complète demande 45 points et 110 000 dataris, le tronc 6 points et 13 000.") + "".join(blocs)


# =============================================================================
# Assemblage de la page unique
# =============================================================================
PANNEAUX = {"accueil": ACCUEIL, "pouvoirs": POUVOIRS_HTML,
            "formes": FORMES_HTML, "competences": COMPETENCES_HTML}

onglets = "".join(
    '<a href="#%s" data-onglet="%s"%s>%s</a>' % (c, c, ' class="actif"' if i == 0 else "", e(t))
    for i, (c, t) in enumerate(ONGLETS))

panneaux = "".join(
    '''    <div class="panneau" data-panneau="%s"%s>
%s    </div>
''' % (c, "" if i == 0 else " hidden", PANNEAUX[c])
    for i, (c, _) in enumerate(ONGLETS))

doc = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wiki Jedi</title>
<meta name="description" content="Le wiki des Jedi du Clone Wars RP Cosmos : pouvoirs de Force, formes de combat, compétences et progression.">
<meta name="theme-color" content="#1E1A15">
<link rel="icon" type="image/png" href="logo-clair.png">
<style>html,body{background:#1E1A15;}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Mulish:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=%(vers)s">
</head>
<body>

<header class="chapeau">
  <div class="embleme"><img src="logo-clair.png" alt="Emblème de l'Ordre Jedi"></div>
  <h1 class="titre-site">Ordre Jedi</h1>
  <p class="sous-titre">Wiki des Jedi · Clone Wars RP Cosmos</p>
  <p class="devise">Il n'y a pas d'émotion, il y a la paix</p>
</header>

<nav class="onglets">%(onglets)s</nav>

<main>
%(panneaux)s</main>

<footer>
  <span class="pied-embleme"><img src="logo-clair.png" alt=""></span>
  <span>Créé par Poté</span>
</footer>

<script src="script.js?v=%(vers)s"></script>
</body>
</html>
''' % {"onglets": onglets, "panneaux": panneaux, "vers": VERS}

io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(doc)

# Les anciennes adresses restent valides : elles renvoient sur le bon onglet.
# Un lien deja partage dans un Discord ne doit pas tomber sur une page morte.
for fichier, cle, titre in [("pouvoirs.html", "pouvoirs", "les pouvoirs"),
                            ("formes.html", "formes", "les formes"),
                            ("competences.html", "competences", "les compétences")]:
    redirection = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Wiki Jedi</title>
<link rel="icon" type="image/png" href="logo-clair.png">
<link rel="canonical" href="index.html#%(cle)s">
<meta http-equiv="refresh" content="0; url=index.html#%(cle)s">
</head>
<body>
<p>Cette rubrique a rejoint la page principale. <a href="index.html#%(cle)s">Ouvrir %(titre)s</a>.</p>
<script>location.replace("index.html#%(cle)s");</script>
</body>
</html>
''' % {"cle": cle, "titre": e(titre)}
    io.open(os.path.join(OUT, fichier), "w", encoding="utf-8", newline="\n").write(redirection)

print("index.html + 3 redirections")
