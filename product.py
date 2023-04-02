from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#Réalisé par Emmanuel Levy MBINA
#Une API REST pour une plateforme de gestion de d'activité commerciale .
# Le projet est conçu à l'aide du framework flask de python ,
# cet API est conçu comme un web service qui va permettre à différentes applications de pouvoir faire des appels.
# Nous avons défini deux classes , la classe produit et la classe vente.

#A REST API for a business activity management platform.
# The project is designed using the python flask framework,
# this API is designed as a web service that will allow different applications to be able to make calls.
# We have defined two classes, the product class and the sale class.


class Product:
    def __init__(self, product_name: str, product_categorie: str, product_prix: float):
        self.product_name = product_name
        self.product_categorie = product_categorie
        self.product_prix = product_prix
        self.sales = []

        self.conn = sqlite3.connect('app.db')
        self.c = self.conn.cursor()

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS products
        (product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        product_categorie TEXT NOT NULL,
        product_prix REAL);
        ''')
        self.conn.commit()

    def add_product_to_database(self):
        self.c.execute(
            "INSERT INTO products (product_name, product_categorie, product_prix) VALUES (?,?,?)",
            (self.product_name, self.product_categorie, self.product_prix))
        self.conn.commit()

    def set_price(self, product_prix):
        self.product_prix = product_prix

    def set_name(self, product_name):
        self.product_name = product_name

    def set_cat(self, product_categorie):
        self.product_categorie = product_categorie

    def get_price(self) -> float:
        return self.product_prix

    def get_name(self) -> str:
        return self.product_name

    def get_cat(self) -> str:
        return self.product_categorie


# Récupère tous les produits enregistrés
@app.route('/products', methods=['GET'])
def get_all_products():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return jsonify(products)


# Récupère un produit en particulier par son id
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    return jsonify(product)


# Ajoute un nouveau produit
@app.route('/product', methods=['POST'])
def add_product():
    product_data = request.get_json()
    new_product = Product(product_data['product_name'], product_data['product_categorie'], product_data['product_prix'])
    new_product.add_product_to_database()
    return 'Le produit a été ajouté avec succès'


# Met à jour un produit existant par son id
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    product_data = request.get_json()
    c.execute("UPDATE products SET product_name=?, product_categorie=?, product_prix=? WHERE product_id=?",
              (product_data['product_name'], product_data['product_categorie'], product_data['product_prix'],
               product_id))
    conn.commit()
    conn.close()
    return 'Le produit a été mis à jour avec succès'


# Supprime un produit par son id
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE product_id=?", (product_id,))
    conn.commit()
    conn.close()
    return 'Le produit a été supprimé avec succès'

