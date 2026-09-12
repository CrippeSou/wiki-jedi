# -*- coding: utf-8 -*-
# Prepare le logo du wiki a partir du VRAI embleme de l'Ordre (celui envoye par
# l'utilisateur, recupere sur Wikimedia Commons : Jedi-order-crest-religious-symbol).
#
# L'image d'origine est un aplat NOIR sur fond transparent. Sur un site sombre
# elle serait invisible : on garde donc la forme (le canal alpha) et on remplace
# la couleur par un ton clair. On produit deux fichiers :
#   logo.png       clair, pour le fond sombre du site
#   logo-encre.png sombre, au cas ou un fond clair serait ajoute plus tard
#
# Aucun trace a la main : c'est bien le logo d'origine, au pixel pres.
import io, os
from PIL import Image

SRC = "jedi_crest.webp"
DEST = r"C:\Users\ytbcr\Desktop\wiki jedi"

# Le trait est noir pur : on ne touche qu'a la couleur, jamais a la forme.
TEINTES = {
    "logo.png":       (233, 240, 248),   # blanc legerement bleute
    "logo-encre.png": (18, 22, 30),      # presque noir, pour un fond clair
}

src = Image.open(SRC).convert("RGBA")
alpha = src.getchannel("A")

# Le fichier d'origine a un liseré d'antialiasing gris : l'alpha seul suffit a
# le reproduire, donc on repart d'une image unie a laquelle on recolle l'alpha.
for nom, rgb in TEINTES.items():
    out = Image.new("RGBA", src.size, rgb + (0,))
    out.putalpha(alpha)
    chemin = os.path.join(DEST, nom)
    out.save(chemin, optimize=True)
    print("%-16s %s  %d o" % (nom, out.size, os.path.getsize(chemin)))

# Page de controle : le logo aux trois tailles ou il sert sur le site.
apercu = '''<!doctype html><meta charset="utf-8">
<body style="margin:0;background:#0B0D10;display:flex;gap:44px;align-items:center;justify-content:center;height:420px">
<img src="logo.png" style="width:300px">
<img src="logo.png" style="width:120px">
<img src="logo.png" style="width:44px">
</body>'''
io.open(os.path.join(DEST, "_apercu_logo.html"), "w", encoding="utf-8", newline="\n").write(apercu)
