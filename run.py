from sqlite3.dbapi2 import Cursor
from init_db import DATABASE
from flask import Flask, jsonify, g, abort, request
import sqlite3


app = Flask(__name__)
DATABASE = 'app.db'


# fonction pour se connecter à la base de données
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# ########## Les exos sur la table categorises #############
# Une route qui return tous les catégories
@app.route("/categories")
def index_categories():
    # connection au db
    db = get_db()
    # requete pour selectionner les ids et names de la table categories
    cursor = db.execute("SELECT id,name FROM categories")
    # pour afficher le contenu de la table categories comme
    # liste de dictionnaire
    categories = []
    for cat in cursor:
        categories.append({"id": cat[0], "name": cat[1]})
    return jsonify(categories)


# Une route qui renvoie les détails d'un jouet donné par son id
@app.route("/categories/<cat_id>")
def show_cat(cat_id):
    # connection au db
    db = get_db()
    # requete pour selectionner l'id et le name d'un jouet donné par son id
    cursor = db.execute("SELECT id, name from categories WHERE id = ?",
                        [int(cat_id)])
    category = cursor.fetchone()
    # vérifier si le jouet n'existe pas, on renvoie un error 404
    if category is None:
        abort(404)
    else:
        return jsonify({"id": category[0], "name": category[1]})


# Une route qui crée un nouveau jouet et renvoie ce jouet nouvellement créé.
@app.route("/categories", methods=["POST"])
def create_category():
    # connection au db
    db = get_db()
    # récuper new_category du form
    new_category = request.form.get('name')
    # verifier que la clef du form existe
    if not new_category:
        abort(422)
    else:
        # chercher dans db new_category
        cursor = db.execute("SELECT id, name from categories WHERE name = ?",
                            [new_category])
        category = cursor.fetchone()
        # vérifier que new_category n'est pas dans le db
        if category is None:
            # ajouter new_category au db
            cursor = db.execute("INSERT INTO categories( name) VALUES (?)",
                                [new_category])
            cursor = db.execute("SELECT id, name from categories WHERE\
                                name = ?", [new_category])
            category_created = cursor.fetchone()
            db.commit()
            return jsonify({"id": category_created[0],
                            "name": category_created[1]})
        else:
            abort(404)


# Une route qui met à jour un jouet donné et renvoie
# les détails du jouet mis à jour
@app.route("/categories/<category_id>", methods=["PUT"])
def update_category(category_id):
    # connection au db
    db = get_db()
    cursor = db.execute("SELECT id, name FROM categories WHERE id = (?)",
                        [int(category_id)])
    id_cat = cursor.fetchone()
    # verifier que l'id existe
    if id_cat is None:
        abort(404)
    # je recupre la donnée qui est passee dans le form
    new_category = request.form.get("name")
    print(new_category)
    # verifier que la clef du form existe
    if new_category:
        # mettre à jour le jouet donné
        cursor = db.execute("UPDATE categories SET name = ? Where id = (?)",
                            [new_category, int(category_id)])
        db.commit()
        # sélectionner le jouet modifié
        cursor = db.execute("SELECT id, name from categories Where id = (?)",
                            [int(category_id)])
        category_updated = cursor.fetchone()
        return jsonify({"id": category_updated[0],
                        "name": category_updated[1]})


# Une route qui supprime un jouet donné et renvoie
# les détails du jouet supprimé
@app.route("/categories/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    # connection au db
    db = get_db()
    cursor = db.execute("SELECT id, name FROM categories WHERE id = (?)",
                        [int(category_id)])
    id_cat = cursor.fetchone()
    # verifier que l'id existe
    if id_cat is None:
        abort(404)
    else:
        # suprimer le jouet donné
        cursor = db.execute("DELETE from categories WHERE id = (?)",
                            [int(category_id)])
        db.commit()
    return jsonify({"id": id_cat[0], "name": id_cat[1]})


# ########## Les exos sur la table toys #############
# Une route qui return tous les Toys
@app.route("/toys")
def index_toys():
    # connection au db
    db = get_db()
    # requete pour selectionner les ids et names de la table toys
    cursor = db.execute("SELECT toys.id,toys.name,toys.description,\
                        toys.price, categories.name AS category from \
                        toys left join categories on\
                        toys.category_id = categories.id ")
    # pour afficher le contenu de la table toys comme
    # liste de dictionnaire
    toys = []
    for toy in cursor:
        toys.append({"id": toy[0], "name": toy[1], "description": toy[2],
                    "price": toy[3], "category": toy[4]})
    return jsonify(toys)


# Une route qui renvoie les détails d'un jouet donné par son id
@app.route("/toys/<toy_id>")
def show_toy(toy_id):
    # connection au db
    db = get_db()
    # requete pour selectionner l'id et le name d'un jouet donné par son id
    cursor = db.execute("SELECT toys.id,toys.name,toys.description, \
                        toys.price, categories.name AS category from \
                        toys left join categories on \
                        toys.category_id = categories.id \
                        WHERE toys.id = ?", [int(toy_id)])
    toy = cursor.fetchone()
    # vérifier si le jouet n'existe pas, on renvoie un error 404
    if toy is None:
        abort(404)
    else:
        return jsonify({"id": toy[0], "name": toy[1], "description": toy[2],
                        "price": toy[3], "category": toy[4]})


# Une route qui crée un nouveau jouet et renvoie ce jouet nouvellement créé.
@app.route("/toys", methods=["POST"])
def create_toy():
    # connection au db
    db = get_db()
    # récuper new_toy du form
    name_toy = request.form.get('name')
    description_toy = request.form.get('description')
    price_toy = request.form.get('price')
    name_category = request.form.get('category')
    # verifier que la clef du form existe
    if not name_toy and not description_toy and not\
            price_toy and not name_category:
        abort(422)
    else:
        # chercher dans db new_toy
        cursor = db.execute("SELECT id,name,description,price,category_id \
                            from toys WHERE name = ?", [name_toy])
        toy = cursor.fetchone()
        # vérifier que new_toy n'est pas dans le db
        if toy is None:
            # recuperer id categorie
            cursor = db.execute("SELECT id from categories WHERE name = ?",
                                [name_category])
            id_cat = cursor.fetchone()
            # ajouter new_toy au db
            cursor = db.execute("INSERT INTO toys(name,description,\
                                price,category_id) VALUES (?, ?, ?, ?)",
                                [name_toy, description_toy,
                                    int(price_toy), id_cat[0]])
            db.commit()
            cursor = db.execute("SELECT toys.id,toys.name,toys.description,\
                                toys.price, categories.name AS category from \
                                toys left join categories on \
                                toys.category_id = categories.id WHERE \
                                toys.name = ?", [name_toy])
            toy_created = cursor.fetchone()
            return jsonify({"id": toy_created[0], "name": toy_created[1],
                            "description": toy_created[2],
                            "price": toy_created[3],
                            "category": toy_created[4]})
        else:
            abort(404)


# Une route qui met à jour un jouet donné et renvoie
# les détails du jouet mis à jour
@app.route("/toys/<toy_id>", methods=["PUT"])
def update_toy(toy_id):
    # connection au db
    db = get_db()
    cursor = db.execute("SELECT id,name,description,price,category_id \
                        FROM toys WHERE id = (?)", [int(toy_id)])
    id_toy = cursor.fetchone()
    # print("id_toy = ", id_toy)
    # verifier que l'id existe
    if id_toy is None:
        abort(404)
    else:
        # je recupre la donnée qui est passee dans le form
        name_toy = request.form.get("name")
        description_toy = request.form.get("description")
        price_toy = request.form.get("price")
        category_id_toy = request.form.get("category_id")
        name_category_toy = request.form.get("category")
        # verifier que la clef du form existe
        if name_toy:
            # mettre à jour le jouet donné
            cursor = db.execute("UPDATE toys SET name = ? Where id = (?)",
                                [name_toy, int(toy_id)])
            db.commit()
        # verifier que la clef du form existe
        if description_toy:
            # mettre à jour le jouet donné
            cursor = db.execute("UPDATE toys SET description = ?\
                                Where id = (?)",
                                [description_toy, int(toy_id)])
            db.commit()
        # verifier que la clef du form existe
        if price_toy:
            # mettre à jour le jouet donné
            cursor = db.execute("UPDATE toys SET price = ? \
                                Where id = (?)",
                                [int(price_toy), int(toy_id)])
            db.commit()
        # verifier que la clef du form existe
        if category_id_toy:
            # mettre à jour le jouet donné
            cursor = db.execute("UPDATE toys SET category_id = ? \
                                Where id = (?)",
                                [int(category_id_toy), int(toy_id)])
            db.commit()
            # verifier que la clef du form existe
        if name_category_toy:
            # selectionner le id categorie a partir de son nom
            cursor = db.execute("SELECT id from categories where name = ?",
                                [name_category_toy])
            new_id_cat = cursor.fetchone()
            # mettre à jour le jouet donné
            cursor = db.execute("UPDATE toys SET category_id = ? \
                                Where id = (?)", [new_id_cat[0], int(toy_id)])
            db.commit()
        # sélectionner le jouet modifié
        cursor = db.execute("SELECT toys.id,toys.name,toys.description,\
                                toys.price, categories.name AS category\
                                from toys left join categories on \
                                toys.category_id = categories.id WHERE \
                                toys.id = ?", [toy_id])
        toy_updated = cursor.fetchone()
        return jsonify({"id": toy_updated[0], "name": toy_updated[1],
                        "description": toy_updated[2],
                        "price": toy_updated[3],
                        "category": toy_updated[4]})


# Une route qui supprime un jouet donné et renvoie
# les détails du jouet supprimé
@app.route("/toys/<toy_id>", methods=["DELETE"])
def delete_toy(toy_id):
    # connection au db
    db = get_db()
    cursor = db.execute("SELECT id,name,description,price,category_id \
                        FROM toys WHERE id = (?)", [int(toy_id)])
    id_toy = cursor.fetchone()
    # verifier que l'id existe
    if id_toy is None:
        abort(404)
    else:
        # suprimer le jouet donné
        cursor = db.execute("DELETE FROM toys WHERE id = (?)", [int(toy_id)])
        db.commit()
    return jsonify({"id": id_toy[0], "name": id_toy[1],
                    "description": id_toy[2],
                    "price": id_toy[3],
                    "category": id_toy[4]})


@app .route("/categories/<name>/toys")
def addition_cat(name):
    # connection au db
    db = get_db()
    cursor = db.execute("SELECT name from categories where name = ?", [name])
    name_cat = cursor.fetchall()
    print("ici name cat", name_cat)
    if name_cat != []:
        # selectiooner tous les toys avec un nom de categorie
        cursor = db.execute("SELECT toys.id,toys.name,toys.description,\
                        toys.price, categories.name AS category from \
                        toys left join categories on\
                        toys.category_id = categories.id WHERE \
                        categories.name = ?", [name])
        # pour afficher le contenu de la table toys comme
        # liste de dictionnaire
        toys = []
        for toy in cursor:
            toys.append({"id": toy[0], "name": toy[1], "description": toy[2],
                        "price": toy[3], "category": toy[4]})
        return jsonify(toys)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run(debug=True)
