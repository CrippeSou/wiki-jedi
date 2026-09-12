# -*- coding: utf-8 -*-
# Prepare le logo du wiki a partir de l'image fournie par l'utilisateur,
# `logo_jedi.png` (posee a la main dans le dossier du wiki). C'est la SOURCE :
# on ne la modifie jamais, on en derive.
#
# L'original est un aplat noir sur fond transparent. On garde sa forme exacte
# (le canal alpha) et on ne change que la couleur, pour disposer d'une version
# encre (fond clair) et d'une version claire (si un fond sombre revenait).
#
# On recadre aussi l'image sur son contenu, puis on la centre dans un carre :
# sans ca, le cercle du site ne tombe pas au milieu de l'embleme.
import io, os
from PIL import Image

DEST = r"C:\Users\ytbcr\Desktop\wiki jedi"
SRC = os.path.join(DEST, "logo_jedi.png")

TEINTES = {
    "logo-encre.png": (26, 29, 33),      # presque noir, pour le fond papier
    "logo-clair.png": (240, 238, 232),   # ivoire, pour un fond sombre
}
# Un peu d'air autour de l'embleme, en fraction du cote : dans un cadre rond,
# une forme qui touche le bord parait a l'etroit.
MARGE = 0.06

src = Image.open(SRC).convert("LA")
alpha = src.getchannel("A")

# Recadrage sur le dessin, puis mise au carre en gardant le centre.
boite = alpha.getbbox()
alpha = alpha.crop(boite)
cote = int(max(alpha.size) * (1 + 2 * MARGE))
carre = Image.new("L", (cote, cote), 0)
carre.paste(alpha, ((cote - alpha.size[0]) // 2, (cote - alpha.size[1]) // 2))

for nom, rgb in TEINTES.items():
    out = Image.new("RGBA", (cote, cote), rgb + (0,))
    out.putalpha(carre)
    chemin = os.path.join(DEST, nom)
    out.save(chemin, optimize=True)
    print("%-16s %s  %d o" % (nom, out.size, os.path.getsize(chemin)))

# Page de controle : dans le cadre rond du site, aux trois tailles utilisees.
apercu = '''<!doctype html><meta charset="utf-8">
<style>
body{margin:0;background:#F4F1EB;display:flex;gap:44px;align-items:center;justify-content:center;height:420px}
.rond{border-radius:50%;background:#fff;border:1px solid #E3DDD2;display:flex;align-items:center;justify-content:center}
.rond img{width:76%;height:76%}
</style>
<div class="rond" style="width:240px;height:240px"><img src="logo-encre.png"></div>
<div class="rond" style="width:110px;height:110px"><img src="logo-encre.png"></div>
<div class="rond" style="width:38px;height:38px"><img src="logo-encre.png"></div>
'''
io.open(os.path.join(DEST, "_apercu_logo.html"), "w", encoding="utf-8", newline="\n").write(apercu)
