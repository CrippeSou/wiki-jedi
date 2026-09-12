# -*- coding: utf-8 -*-
# Trace de l'embleme de l'Ordre Jedi, redessine a la main en SVG a partir du
# logo envoye : anneau, deux ailes par cote, lame centrale et etincelle a huit
# branches. Tout est symetrique : on ne decrit que la moitie GAUCHE, la droite
# est la meme retournee (scale(-1,1)).
import io, math, os

OUT = r"C:\Users\ytbcr\Desktop\wiki jedi\logo.svg"

# --- l'etincelle a huit branches, a la base de la lame ------------------------
CX, CY = 100.0, 137.0
# Longueur de chaque branche, en partant de la droite et en tournant.
RAYONS = [27, 12.5, 11, 12.5, 27, 12.5, 15, 12.5]
CREUX = 2.6


def etincelle():
    pts = []
    for i, r in enumerate(RAYONS):
        a = math.radians(i * 45.0)
        pts.append((CX + r * math.cos(a), CY - r * math.sin(a)))
        a2 = math.radians(i * 45.0 + 22.5)
        pts.append((CX + CREUX * math.cos(a2), CY - CREUX * math.sin(a2)))
    return "M" + " L".join("%.2f %.2f" % p for p in pts) + " Z"


# --- les deux ailes de gauche -------------------------------------------------
# Grande aile : pointe haute pres du centre, ventre a gauche, pointe basse au
# ras de la lame. Son bord interieur se resserre a mi-hauteur : c'est ce
# pincement qui donne les deux lobes clairs du logo.
AILE_INT = (
    "M82 26 "
    "C46 42 27 82 28 116 "
    "C29 150 54 174 95 179 "
    "C72 164 62 140 70 121 "
    "C79 104 87 97 85 87 "
    "C82 65 78 44 82 26 Z"
)

# Petite aile exterieure : plus fine, decalee vers le bord de l'anneau, et
# terminee en pointe en bas comme sur le logo d'origine.
AILE_EXT = (
    "M50 33 "
    "C27 57 17 94 20 126 "
    "C22 146 31 159 43 167 "
    "C34 148 28 129 28 110 "
    "C28 82 39 53 50 33 Z"
)

# --- la lame ------------------------------------------------------------------
LAME = (
    "M100 22 "
    "C100.9 58 101.9 90 101.9 108 "
    "L101.2 178 L98.8 178 L98.1 108 "
    "C98.1 90 99.1 58 100 22 Z"
)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Embleme de l'Ordre Jedi">
  <defs>
    <linearGradient id="or" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#DCEBFF"/>
      <stop offset="0.55" stop-color="#8FBFFF"/>
      <stop offset="1" stop-color="#E3BE72"/>
    </linearGradient>
  </defs>
  <g fill="url(#or)">
    <path d="M100 3.5a96.5 96.5 0 1 0 0 193a96.5 96.5 0 1 0 0-193zm0 11.5a85 85 0 1 1 0 170a85 85 0 1 1 0-170z"/>
    <g>
      <path d="%(int)s"/>
      <path d="%(ext)s"/>
    </g>
    <g transform="translate(200,0) scale(-1,1)">
      <path d="%(int)s"/>
      <path d="%(ext)s"/>
    </g>
    <path d="%(lame)s"/>
    <path d="%(etincelle)s"/>
  </g>
</svg>
''' % {"int": AILE_INT, "ext": AILE_EXT, "lame": LAME, "etincelle": etincelle()}

io.open(OUT, "w", encoding="utf-8", newline="\n").write(svg)
print("ecrit :", OUT, len(svg), "octets")

# Page de controle : le logo en grand, sur le fond du site.
apercu = '''<!doctype html><meta charset="utf-8">
<body style="margin:0;background:#04060B;display:flex;gap:40px;align-items:center;justify-content:center;height:420px">
<img src="logo.svg" style="width:320px">
<img src="logo.svg" style="width:120px">
<img src="logo.svg" style="width:48px">
</body>'''
io.open(os.path.join(os.path.dirname(OUT), "_apercu_logo.html"), "w",
        encoding="utf-8", newline="\n").write(apercu)
