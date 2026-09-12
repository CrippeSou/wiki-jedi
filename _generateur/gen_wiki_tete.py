# -*- coding: utf-8 -*-
# Genere le wiki Jedi (site statique, pour GitHub Pages) dans Desktop\wiki jedi.
#
# Les LISTES (voies, paliers, seances) sont lues dans les fichiers de config du
# serveur : elles ne peuvent pas mentir. Les CHIFFRES de chaque pouvoir et le
# texte qui explique ce qu'il fait sont ecrits ici, releves dans le code le
# 2026-09-12. Relancer ce script apres un changement d'arbre met le site a jour.
#
# On ne liste QUE ce qu'un joueur peut apprendre : les pouvoirs hors arbre ne
# figurent nulle part.
import io, os, re, html

SRC = (r"c:\Users\ytbcr\Documents\Claude serveur cosmos\claude_cosmos_clone_wars_dev"
       r"\garrysmod\addons\addon_lscs\lua\lscs")
OUT = r"C:\Users\ytbcr\Desktop\wiki jedi"

# =============================================================================
# Lecture des arbres
# =============================================================================
def branches(fichier, champ):
    s = io.open(SRC + r"\autorun\\" + fichier, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'key   = "([\w]+)",\s*\n\s*label = "([^"]*)"', s):
        fin = s.find("key   =", m.end())
        bloc = s[m.end(): fin if fin > 0 else len(s)]
        noeuds = re.findall(
            r'\{\s*id\s*=\s*"([\w]+)",\s*%s\s*=\s*"([\w]+)",\s*label\s*=\s*"([^"]*)",\s*days\s*=\s*(\d+)' % champ,
            bloc)
        out.append((m.group(1), m.group(2), [(n[1], n[2], int(n[3])) for n in noeuds]))
    return out


POUVOIRS = branches("powertree_config.lua", "powerId")
FORMES = branches("formtree_config.lua", "formId")

# Competences (passifs)
def competences():
    """Le tronc puis les trois voies. Un noeud tient sur trois lignes : id, label,
    points et prix ; puis desc ; puis effects."""
    s = io.open(os.path.join(SRC, "autorun", "skilltree_config.lua"), encoding="utf-8").read()
    motif = re.compile(
        r'\{ id = "[\w]+", label = "([^"]*)", points = (\d+), price = (\d+),\s+'
        r'desc = "([^"]*)",\s+effects = \{([^}]*)\}')
    groupes = []
    for m in re.finditer(r'key = "([\w]+)", label = "([^"]*)"', s):
        fin = s.find('key = "', m.end())
        bloc = s[m.end(): fin if fin > 0 else len(s)]
        noeuds = motif.findall(bloc)
        if noeuds:
            groupes.append((m.group(1), m.group(2),
                            [(n[0], n[3], int(n[1]), int(n[2]), n[4].strip()) for n in noeuds]))
    return groupes


COMPETENCES = competences()

# Formes : ce que dit le fichier de combo.
def stats_formes():
    out = {}
    for f in os.listdir(SRC + r"\combos"):
        if not f.endswith(".lua"):
            continue
        s = io.open(SRC + r"\combos\\" + f, encoding="utf-8", errors="replace").read()
        cle = re.search(r'COMBO\.id\s*=\s*"([\w]+)"', s)
        if not cle:
            continue

        def val(k, defaut="-"):
            m = re.search(r'COMBO\.%s\s*=\s*([\w.]+)' % k, s)
            return m.group(1) if m else defaut

        out[cle.group(1)] = {
            "degats": val("DamageMultiplier", "1"),
            "garde": val("BPDrainPerHit", "-"),
            "gauche": val("LeftSaberActive", "false") == "true",
            "attaques": len(re.findall(r'\["[A-Z_]+"\]\s*=\s*\{', s)),
        }
    return out


FORMES_STATS = stats_formes()

# =============================================================================
# Ce que fait chaque pouvoir : releve dans le code le 2026-09-12
# =============================================================================
#            id : (cout, rechargement, description)
P = {
 "jump":        ("45 de Force", "2 s", "Bond en avant propulsé par la Force. Une onde de choc part au décollage (25 dégâts) et à l'arrivée (50 dégâts) dans un rayon de 200. Aucune chute ne te blesse pendant les 15 s qui suivent."),
 "jumpii":      ("45 de Force", "2 s", "Même bond, plus haut. Utile pour franchir un mur ou décrocher d'un combat."),
 "jumpiii":     ("45 de Force", "2 s", "Le bond le plus haut des trois."),
 "meditate":    ("gratuit", "10 s", "Rend 25 points de Force. Tu es ralenti de moitié pendant 15 s : on médite à l'abri, pas au milieu d'un échange."),
 "meditateii":  ("gratuit", "10 s", "Rend 40 points de Force, avec un ralentissement un peu plus court (10 s)."),
 "extinguish":  ("20 de Force", "aucun", "Éteint les flammes sur la cible visée."),
 "breach":      ("gratuit", "2 s", "Ouvre une porte verrouillée à moins de 150 unités. Rien ne se consomme si tu ne vises pas une porte."),
 "throw":       ("gratuit", "1 s", "Projette l'objet que tu tiens par la Force."),
 "pull":        ("10 de Force", "1 s", "Attire vers toi ce que tu vises, jusqu'à 200 unités."),
 "pullii":      ("20 de Force", "1 s", "Attire plus loin (500) et plus fort."),
 "push":        ("10 de Force", "1 s", "Repousse devant toi, jusqu'à 800 unités. Aucun dégât : c'est du déplacement."),
 "pushii":      ("20 de Force", "1 s", "Repousse deux fois plus fort."),
 "greaterpush": ("40 de Force", "1 s", "Souffle large : tout ce qui est devant toi part à 900 unités, très vite. Aucun dégât direct."),
 "greaterpull": ("40 de Force", "1 s", "Attire violemment tout ce qui est devant toi, jusqu'à 900 unités."),
 "heal":        ("25 de Force", "4 s", "Rend 200 PV, sur toi. Sans effet si tu es déjà au maximum, et rien n'est consommé dans ce cas."),
 "healii":      ("35 de Force", "6 s", "Rend 500 PV, sur toi."),
 "healiii":     ("45 de Force", "10 s", "Rend 700 PV, sur toi."),
 "sharedhealing": ("10 de Force", "6 s", "Rend 500 PV au joueur visé, à moins de 300 unités. C'est le soin d'appoint du groupe."),
 "massheal":    ("5 de Force par personne", "15 s", "Soigne 30 % des PV maximum de chaque joueur dans un rayon de 200, et continue pendant 3,5 s tant que tu maintiens."),
 "greaterheal": ("40 de Force", "15 s", "Remet toute ta vie d'un coup. C'est le soin d'urgence, il coûte une vraie réserve."),
 "revive":      ("100 de Force", "5 s", "Rappelle un allié tombé, à l'endroit de son corps. Vise le corps. Le rechargement ne part que si la réanimation réussit."),
 "grab":        ("4 de Force par seconde", "5 s entre deux prises", "Soulève une cible à distance (600) et la maintient tant que tu tiens la touche."),
 "sense1":      ("50 de Force", "1 s", "Tu vois les présences à travers les murs pendant 10 s, jusqu'à 800 unités, avec leur vie."),
 "sense2":      ("40 de Force", "1 s", "15 s de vision, jusqu'à 1600 unités."),
 "sense3":      ("35 de Force", "1 s", "25 s de vision, jusqu'à 2400 unités."),
 "sense":       ("20 de Force", "1 s", "40 s de vision, jusqu'à 3200 unités. La version la moins chère et la plus longue."),
 "sfbarrier":   ("50 de Force", "10 s", "Bouclier personnel qui encaisse à ta place."),
 "wizbarrierwall": ("10 de Force à l'ouverture", "10 s après la fin", "Mur de Force devant toi. Ce qui vient du dehors ne blesse plus ceux qui sont derrière, et chaque coup absorbé te coûte de la Force. Il tient 30 s au maximum."),
 "wizbarrierdome": ("10 de Force à l'ouverture", "10 s après la fin", "Dôme de protection autour de toi. Les tirs venus de l'extérieur n'atteignent plus ceux qui sont dedans, à ton prix en Force. Il tient 30 s au maximum."),
 "judgementi":  ("7 de Force par impulsion", "1 s", "Éclair de jugement bleu, 40 dégâts par impulsion, dans un cône de 14° jusqu'à 700 unités. Se maintient 3,5 s."),
 "judgementii": ("7 de Force par impulsion", "1 s", "Éclair vert, 55 dégâts par impulsion."),
 "judgementiii":("7 de Force par impulsion", "1 s", "Éclair violet, 70 dégâts par impulsion."),
 "judgementiv": ("7 de Force par impulsion", "1 s", "Éclair doré, 85 dégâts par impulsion. Réservé au Conseil."),
 "judgementstun": ("40 de Force (50 requis)", "25 s", "Un éclair bleu frappe une cible unique jusqu'à 1000 unités : 40 dégâts, et elle tombe à genoux, immobilisée 6 s, entourée d'une aura électrique."),
 "clascleave":  ("10 de Force", "6 s", "Se charge en maintenant la touche : jusqu'à 350 dégâts sur ce que tu vises à moins de 400 unités. Plus tu charges, plus ça frappe fort."),
 "whirlwind":   ("35 de Force", "20 s", "Pose un vortex au sol jusqu'à 800 unités. Il aspire tout, fait monter les gens dans les airs pendant 3 s, inflige 200 dégâts au sommet puis les éjecte. L'Immunité ne protège pas de ce pouvoir."),
 "immunity":    ("passif", "aucun", "Tant que ta Force dépasse 50 %, les pouvoirs de Force lancés sur toi n'ont aucun effet et t'en rendent un peu. Rien à activer : il suffit de l'apprendre."),
 "immunityii":  ("passif", "aucun", "Même protection, mais elle tient tant que ta Force dépasse 35 %."),
 "immunityiii": ("passif", "aucun", "Même protection, jusqu'à 20 % de Force seulement."),
 "rebuke":      ("20 de Force", "12 s", "Pendant 10 s, tu renvoies la moitié des dégâts reçus à celui qui te frappe, et tu n'en encaisses qu'une petite partie."),
 "adrenaline":  ("2 de Force par seconde", "3 s", "+200 de vitesse de course tant que tu maintiens."),
 "adrenalineii":("2 de Force par seconde", "3 s", "+400 de vitesse."),
 "adrenalineiii":("2 de Force par seconde", "3 s", "+400 de vitesse, pour une consommation identique."),
 "adrenalineiiii":("20 de Force puis un filet", "3 s", "Pas de l'ombre : +400 de vitesse, la course du Conseil."),
 "cloak":       ("40 de Force", "30 s après la fin", "Invisibilité totale pendant 25 s. Tirer, être touché, mourir ou rappuyer te révèle. Une barre affiche le temps restant."),
 "cloakii":     ("40 de Force", "30 s après la fin", "Invisibilité totale pendant 40 s."),
 "cloakiii":    ("40 de Force", "30 s après la fin", "Invisibilité totale pendant 120 s."),
 "teleport":    ("20 de Force", "2 s", "Tu te projettes jusqu'à 1500 unités devant toi, en te rattrapant aux rebords."),
 "rook":        ("24 de Force", "10 s", "Rempart : tu échanges ta position avec un joueur proche (300 unités)."),
 "kneeldowntarget": ("25 de Force", "2 s", "Force la cible visée à rester à genoux tant que tu maintiens la touche."),
 "kneeldown":   ("25 de Force", "15 s", "Met à genoux tout le monde dans un rayon de 300 pendant 6 s."),
 "sfrockthrow": ("50 de Force", "8 s", "Arrache un rocher et le projette sur ta cible."),
 "ignite":      ("50 de Force", "5 s", "Embrase la cible visée à moins de 200 unités."),
 "boulderthrow":("100 de Force", "8 s", "Un bloc de pierre lancé à pleine vitesse. Il faut appuyer deux fois pour confirmer : c'est cher et ça ne se lance pas par erreur."),
 "blind":       ("80 de Force", "10 s", "Aveugle tous les adversaires dans un rayon de 200 pendant 8,5 s. Ils voient un voile très sombre, pas un écran noir."),
}

FORMES_TXT = {
 "form1a": "La forme d'entrée, celle qu'on apprend en premier.",
 "form2a": "Makashi : le duel au sabre, précis et économe.",
 "form3a": "Soresu : la défense, pensée pour encaisser les tirs.",
 "form4a": "Ataru : l'acrobatie, des enchaînements rapides.",
 "form5a": "Shien Djem So : le contre, renvoyer la force du coup.",
 "form7a": "Juyo : la forme la plus agressive, réservée au Conseil.",
}

