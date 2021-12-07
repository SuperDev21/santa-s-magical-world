# Santa's Magical World project (API REST)

Ce projet est une petite API REST avec le framework Flask

## Objectifs du projet

* Comprendre le fonctionnement du Web
* Construisez une petite application back-end avec Flask
* Comprendre le fonctionnement du routage
* Comprendre ce qu'est une API
* Familiarisez-vous avec un format de données : JSON

## Lancer le projet

* Rénitialiser la base de données dans le terminal avec la commande `python3 init_db.py`
* Puis lancer le serveur dans le terminal avec la commande  `python3 run.py`
* Ouvrir un autre terminal pour exécuter les requêtes

### Quelques commandes (requêtes) pour tester l'API

#### Toys

* La route /toys `curl http://127.0.0.1:5000/toys`

* La route /toys/<toy_id>  `curl http://127.0.0.1:5000/toys/2`

* La route /toys avec la méthode POST `curl -d "name=Minesweeper&description=Home computer classic&price=0&category=Outdoor" -X POST http://127.0.0.1:5000/toys`

* La route pour mettre à jour /toys/<toy_id> avec la méthode PUT `curl -d "name=Checkers" -X PUT http://127.0.0.1:5000/toys/4`

* La route pour supprimer /toys/<toy_id> avec la méthode DELETE `curl -X DELETE http://127.0.0.1:5000/toys/4`

* La route /categories/< name>/toys qui renvoie tous les jouets d'une catégorie donnée `curl http://127.0.0.1:5000/categories/Boardgames/toys`

#### Categories

* La route /categories `curl http://127.0.0.1:5000/categories`

* La route /categories/<category_id> `curl http://127.0.0.1:5000/categories/1`

* La route /categories avec la méthode POST  `curl -d "name=Water Games" -X POST http://127.0.0.1:5000/categories`

* La route pour mettre à jour /categories/<category_id> avec la méthode PUT  `curl -d "name=Old School Games" -X PUT  http://127.0.0.1:5000/categories/1`

* La route pour supprimer /categories/<category_id> avec la méthode DELETE `curl -X DELETE http://127.0.0.1:5000/categories/3`
