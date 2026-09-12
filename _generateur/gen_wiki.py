# -*- coding: utf-8 -*-
# Generateur du wiki Jedi. Le fichier est coupe en deux :
#   gen_wiki_tete.py  : la lecture des configs du serveur + les chiffres releves
#   gen_wiki_rendu.py : la mise en page HTML
# On les execute a la suite dans le meme espace de noms.
import io, os

ICI = os.path.dirname(os.path.abspath(__file__))
for part in ("gen_wiki_tete.py", "gen_wiki_rendu.py"):
    src = io.open(os.path.join(ICI, part), encoding="utf-8").read()
    exec(compile(src, part, "exec"), globals())

print("wiki genere dans %s" % OUT)
