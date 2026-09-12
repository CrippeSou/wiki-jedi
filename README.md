# Wiki Jedi

Le wiki des Jedi du serveur Clone Wars RP Cosmos. Site statique, sans dépendance
ni étape de compilation : quatre pages HTML et une feuille de style, publiables
tels quels sur GitHub Pages.

Créé par Poté.

## Mettre en ligne

1. Dans **Settings > Pages**, choisir la branche `main` et le dossier `/ (root)`.
2. L'adresse est alors `https://<compte>.github.io/wiki-jedi/`.

`index.html` est la page d'accueil, GitHub Pages la sert automatiquement.

## Mettre à jour après un changement en jeu

Le générateur est dans `_generateur/`, en deux morceaux :

- `gen_wiki_tete.py` lit la configuration du serveur (voies, paliers, nombre de
  séances, compétences, formes) et porte la table `P`, où sont écrits le coût, le
  rechargement et l'explication de chaque pouvoir ;
- `gen_wiki_rendu.py` fabrique les pages HTML.

`python _generateur/gen_wiki.py` exécute les deux à la suite et réécrit les
quatre pages. Après un changement d'arbre, il suffit de le relancer ; si un
pouvoir change de valeur, c'est la table `P` qu'il faut corriger.

Le chemin du serveur est en dur en haut de `gen_wiki_tete.py` (`SRC`), tout comme
le dossier de sortie (`OUT`).

## Ce que le wiki contient

- **Le fonctionnement** : séances, grades, whitelists, une seule voie, la Force,
  rechargements et barres de durée.
- **Les pouvoirs** : uniquement ceux qu'un joueur peut apprendre, voie par voie.
- **Les formes** : dégâts au sabre, double sabre, garde entamée.
- **Les compétences** : les bonus permanents, leur coût en points et en dataris.
