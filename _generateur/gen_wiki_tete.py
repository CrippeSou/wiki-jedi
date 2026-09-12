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
# Ce que fait chaque pouvoir : releve dans le code le 2026-09-13
# =============================================================================
# Regle commune depuis le 2026-09-13 : un pouvoir qui ne fait rien (personne a
# portee, cible deja soignee, Force insuffisante, jauge pleine...) ne prend ni
# Force ni rechargement. Le rechargement part des qu'il reussit.
#
#            id : (cout, rechargement, description)
P = {
 "jump":        ("40 de Force", "2 s", "Bond en avant propulsé par la Force, depuis le sol. Aucune chute ne te blesse pendant les 15 s qui suivent."),
 "jumpii":      ("40 de Force", "2 s", "Même bond, bien plus haut. Utile pour franchir un mur ou décrocher d'un combat."),
 "jumpiii":     ("45 de Force", "2 s", "Le bond le plus haut et le plus long des trois."),
 "meditate":    ("gratuit", "8 s", "Rend 25 points de Force petit à petit pendant 5 s, et tu es ralenti de moitié tout ce temps. Si tu meurs pendant la concentration, le reste est perdu. À Force pleine, rien ne se passe."),
 "meditateii":  ("gratuit", "8 s", "Rend 40 points de Force en seulement 3 s, avec un ralentissement un peu plus léger."),
 "extinguish":  ("20 de Force", "aucun", "Éteint les flammes sur ce que tu vises, à moins de 300 unités. Si tu ne vises rien en feu mais que tu brûles, c'est toi qui es éteint."),
 "breach":      ("gratuit (10 de Force requis)", "2 s", "Ouvre une porte verrouillée à moins de 150 unités. Rien ne se passe si tu ne vises pas une porte."),
 "throw":       ("5 de Force par seconde de vol", "1 s", "Lance ton sabre, jusqu'à 800 unités. Il revient quand tu relâches la touche, quand tu rappuies ou quand ta Force est vide."),
 "pull":        ("10 de Force (20 requis)", "1 s", "Attire vers toi ce qui est devant, jusqu'à 200 unités. Rien n'est pris si rien ne bouge."),
 "pullii":      ("20 de Force", "1 s", "Attire plus loin (500) et plus fort."),
 "push":        ("10 de Force (20 requis)", "1 s", "Repousse ce qui est devant toi, jusqu'à 800 unités. Aucun dégât : c'est du déplacement. Rien n'est pris si rien ne bouge."),
 "pushii":      ("20 de Force", "1 s", "Repousse deux fois plus fort."),
 "greaterpush": ("40 de Force", "1 s", "Souffle large : tout ce qui est devant toi, jusqu'à 900 unités, part très vite. Aucun dégât direct."),
 "greaterpull": ("40 de Force", "1 s", "Attire violemment tout ce qui est devant toi, jusqu'à 900 unités."),
 "heal":        ("25 de Force", "4 s", "Rend 200 PV, sur toi. Sans effet si tu es déjà au maximum, et rien n'est consommé dans ce cas."),
 "healii":      ("35 de Force", "6 s", "Rend 500 PV, sur toi."),
 "healiii":     ("45 de Force", "10 s", "Rend 700 PV, sur toi."),
 "sharedhealing": ("10 de Force", "5 s", "Rend 500 PV au joueur visé, à moins de 300 unités. C'est le soin d'appoint du groupe. Rien n'est pris s'il est déjà en pleine santé."),
 "massheal":    ("5 de Force par personne soignée (10 requis)", "12 s", "Tant que tu maintiens la touche (3,5 s au plus), chaque joueur à moins de 200 unités, toi compris, récupère 30 % de ses PV maximum à chaque impulsion. Rien ne part si personne n'a besoin de soin."),
 "greaterheal": ("55 de Force", "6 s", "Remet toute ta vie d'un coup. C'est le soin d'urgence, il coûte une vraie réserve. Rien n'est pris si tu es déjà en pleine santé."),
 "revive":      ("100 de Force", "5 s", "Rappelle un allié tombé, à l'endroit de son corps, avec 100 PV. Vise le corps, à moins de 250 unités. Le rechargement ne part que si la réanimation réussit."),
 "grab":        ("4 de Force par seconde", "5 s", "Saisit ce que tu vises à moins de 400 unités et le maintient tant que tu tiens la touche. Clic droit pour rapprocher, clic gauche pour éloigner : au-delà de 700 unités, la cible est projetée."),
 "sense1":      ("50 de Force", "1 s", "Tu vois les présences à travers les murs pendant 10 s, jusqu'à 800 unités, avec leur vie."),
 "sense2":      ("40 de Force", "1 s", "15 s de vision, jusqu'à 1600 unités."),
 "sense3":      ("35 de Force", "1 s", "25 s de vision, jusqu'à 2400 unités."),
 "sense":       ("20 de Force", "1 s", "40 s de vision, jusqu'à 3200 unités. La version la moins chère et la plus longue."),
 "sfbarrier":   ("50 de Force", "10 s", "Bouclier personnel pendant 10 s : tu ne subis plus que 20 % des dégâts. Ta Force ne remonte pas tant qu'il tient."),
 "wizbarrierwall": ("10 de Force à l'ouverture (40 requis), puis 1 à 10 par coup absorbé", "8 s après la fin", "Bouclier incurvé d'environ 143 unités de rayon devant toi, tant que tu tiens la touche (30 s au maximum). Les coups venus de face n'atteignent plus ceux qui sont à l'abri, et chaque coup absorbé te coûte de la Force. Ce qui arrive de côté ou de derrière passe."),
 "wizbarrierdome": ("10 de Force à l'ouverture (40 requis), puis 1 à 10 par coup absorbé", "8 s après la fin", "Dôme d'environ 166 unités de rayon autour de toi, tant que tu tiens la touche (30 s au maximum). Les coups venus de l'extérieur n'atteignent plus ceux qui sont dedans, joueurs et PNJ, et chaque coup absorbé te coûte de la Force. Ce qui se passe à l'intérieur n'est pas protégé."),
 "judgementi":  ("7 de Force par impulsion (10 requis)", "1 s", "Éclair de jugement bleu tant que tu tiens la touche, 3,5 s au maximum : 40 dégâts par impulsion, dans un cône étroit jusqu'à 700 unités. Les impulsions coûtent même si rien n'est touché."),
 "judgementii": ("7 de Force par impulsion (10 requis)", "1 s", "Éclair vert, 55 dégâts par impulsion."),
 "judgementiii":("7 de Force par impulsion (10 requis)", "1 s", "Éclair violet, 70 dégâts par impulsion."),
 "judgementiv": ("7 de Force par impulsion (10 requis)", "1 s", "Éclair doré, 85 dégâts par impulsion."),
 "judgementstun": ("40 de Force (50 requis)", "20 s", "Un éclair bleu frappe une cible unique jusqu'à 1000 unités : 40 dégâts, et elle tombe à genoux, immobilisée 6 s, entourée d'une aura électrique."),
 "clascleave":  ("10 de Force au coup (50 requis pour charger)", "5 s", "Maintiens la touche pour charger, relâche pour frapper : de 100 à 350 dégâts selon la charge, sur tous les joueurs et PNJ dans un cône devant toi, à moins de 400 unités. Rien n'est pris si le coup ne touche personne."),
 "whirlwind":   ("35 de Force", "16 s", "Pose un vortex au sol jusqu'à 800 unités. Il aspire tout, fait monter les gens dans les airs pendant 3 s, inflige 200 dégâts au sommet puis les éjecte. L'Immunité ne protège pas de ce pouvoir."),
 "immunity":    ("passif", "aucun", "Tant que ta Force dépasse 50 %, les pouvoirs de Force lancés sur toi n'ont aucun effet et te rendent 1 point de Force. Il faut porter un job Jedi. Rien à activer : il suffit de l'apprendre. Ne protège ni du Tourbillon, ni des Agenouillements, ni du Rempart, ni de l'Embrasement."),
 "immunityii":  ("passif", "aucun", "Même protection, mais elle tient tant que ta Force dépasse 35 %."),
 "immunityiii": ("passif", "aucun", "Même protection, jusqu'à 20 % de Force seulement."),
 "rebuke":      ("20 de Force", "10 s", "Pendant 10 s, tu ne subis plus que 15 % des dégâts, et la moitié des dégâts reçus est renvoyée à celui qui te frappe."),
 "adrenaline":  ("environ 3 de Force par seconde", "3 s", "+200 de vitesse tant que tu maintiens la touche."),
 "adrenalineii":("environ 3 de Force par seconde", "3 s", "+400 de vitesse."),
 "adrenalineiii":("environ 3 de Force par seconde", "3 s", "+400 de vitesse, pour une consommation identique."),
 "adrenalineiiii":("20 de Force puis un filet", "3 s", "Pas de l'ombre : +400 de vitesse, la course du Conseil."),
 "cloak":       ("40 de Force", "25 s après la fin", "Invisibilité totale pendant 25 s, sans bruit de pas. Tirer, être touché, mourir ou rappuyer te révèle. Une barre affiche le temps restant. Le rechargement bloque les trois niveaux de Camouflage."),
 "cloakii":     ("40 de Force", "25 s après la fin", "Invisibilité totale pendant 40 s."),
 "cloakiii":    ("40 de Force", "25 s après la fin", "Invisibilité totale pendant 120 s."),
 "teleport":    ("20 de Force", "2 s", "Tu te projettes jusqu'à 1500 unités devant toi, en te rattrapant aux rebords."),
 "rook":        ("24 de Force", "8 s", "Rempart : tu échanges ta position avec un joueur proche, à moins de 300 unités, sans avoir à le viser."),
 "kneeldowntarget": ("25 de Force", "2 s", "Force le joueur visé, à moins de 300 unités, à rester à genoux tant que tu maintiens la touche."),
 "kneeldown":   ("25 de Force", "12 s", "Met à genoux tous les joueurs à moins de 300 unités pendant 6 s, alliés compris. Rien n'est pris si personne n'est à portée."),
 "sfrockthrow": ("50 de Force", "6 s", "Arrache un rocher et le tient tant que tu maintiens la touche ; relâche pour le projeter. 1500 dégâts à l'impact."),
 "ignite":      ("50 de Force", "5 s", "Embrase le joueur ou le PNJ visé à moins de 200 unités. Rien n'est pris si la cible brûle déjà."),
 "boulderthrow":("100 de Force", "6 s", "Un bloc de pierre lancé à pleine vitesse, qui explose au contact. Il faut appuyer deux fois pour confirmer : c'est cher et ça ne se lance pas par erreur."),
 "blind":       ("80 de Force", "8 s", "Aveugle tous les joueurs à moins de 200 unités pendant 8,5 s, alliés compris : leur écran devient entièrement noir. Rien n'est pris si personne n'est touché."),
}

FORMES_TXT = {
 "form1a": "La forme d'entrée, celle qu'on apprend en premier.",
 "form2a": "Makashi : le duel au sabre, précis et économe.",
 "form3a": "Soresu : la défense, pensée pour encaisser les tirs.",
 "form4a": "Ataru : l'acrobatie, des enchaînements rapides.",
 "form5a": "Shien Djem So : le contre, renvoyer la force du coup.",
 "form7a": "Juyo : la forme la plus agressive, réservée au Conseil.",
}

