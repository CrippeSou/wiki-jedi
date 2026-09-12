# Wiki Jedi — Clone Wars RP Cosmos

Site statique, sans dépendance ni étape de compilation : quatre pages HTML et une
feuille de style. Il se publie tel quel sur GitHub Pages.

## Mettre en ligne

1. Créer un dépôt GitHub, par exemple `wiki-jedi`.
2. Y copier le contenu de ce dossier (les `.html`, `style.css`, ce fichier).
3. Dans **Settings → Pages**, choisir la branche `main` et le dossier `/ (root)`.
4. L'adresse est alors `https://<compte>.github.io/wiki-jedi/`.

`index.html` est la page d'accueil, GitHub Pages la sert automatiquement.

## Mettre à jour après un changement en jeu

Les listes (voies, paliers, nombre de séances, compétences, formes) sont **lues
dans la configuration du serveur** par le script `gen_wiki.py`. Après un
changement d'arbre, relancer ce script régénère les pages.

Les chiffres de chaque pouvoir (coût, rechargement, effet) et les textes
d'explication sont écrits dans le script lui-même, dans la table `P` : c'est là
qu'il faut corriger si un pouvoir change de valeur.

## Ce que le wiki contient

- **Comment ça marche** : séances, grades, whitelists, une seule voie, la Force,
  rechargements et barres de durée.
- **Pouvoirs** : uniquement ceux qu'un joueur peut apprendre, voie par voie.
- **Formes de combat** : dégâts au sabre, double sabre, garde entamée.
- **Compétences** : les bonus permanents, leur coût en points et en dataris.
