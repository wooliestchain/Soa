from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime
from product import Product

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

class Sales:
    def __init__(self, product_name: str, amount: float, quantity: int, date: datetime.date = datetime.now().date(),
                 year: int = datetime.now().year, month: int = datetime.now().month, day: int = datetime.now().day, sales_id: int = None
                 ):
        self.sales_id = sales_id
        self.product_name = product_name
        self.amount = amount
        self.quantity = quantity
        self.date = date
        self.month = month
        self.year = year
        self.day = day
        self.sales_id = sales_id if sales_id else str(uuid.uuid4())

        self.conn = sqlite3.connect('app.db')
        self.c = self.conn.cursor()

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS sales 
        ( sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        amount REAL, 
        quantity INTEGER, 
        date TEXT NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL, 
        day INTEGER NOT NULL
        );
        ''')
        self.conn.commit()

    #Ajoutez une vente en base de données
    def add_sale_to_database(self):
        try:
            self.c.execute(
                "INSERT INTO sales (product_name, amount, quantity, date, year, month, day) VALUES (?,?,?,?,?,?,?)",
                (self.product_name, self.amount, self.quantity, str(self.date), str(self.year), str(self.month),
                 str(self.day)))
            self.conn.commit()
            print("Vente ajouté avec succés!")
            return "Vente ajouté avec succés!", 200
        except sqlite3.Error as e:
            print("Une erreur s'est produite lors de l'ajout dans la base:", e)
            return {"message": "Une erreur s'est produite lors de l'ajout dans la base"}, 500


    def update_sale(self):
        try:
            a = input("Entrer le nom du produit")
        except ValueError:
            print("Veuillez entrer une valeur correcte")
            a = input("Entrer le nom du produit")

        try:
            b = float(input("Entrer le montant de la vente"))
        except ValueError:
            print("Veuillez entrer une valeur correcte")
            b = float(input("Entrer le montant de la vente"))
        try:
            c = int(input("Entrer la quantité vendue"))
        except ValueError:
            print("Veuillez entrer une valeur correcte")
            c = int(input("Entrer la quantité vendue"))

        try:
            self.c.execute(
                "UPDATE sales SET amount=?, quantity=?, product_name=? WHERE sales_id=? ",
                (a, b, c, self.sales_id)
            )
            self.conn.commit()

        except sqlite3.Error as e:
            print("Modification echoué", e)

    def get_all_sales(self):
        self.c.execute(
            "SELECT FROM sales"
        )
        self.conn.commit()

    def get_sale(self):
        self.c.execute(
            "SELECT * FROM sales WHERE sales_id=?", (self.sales_id,)
        )
        self.conn.commit()

    def delete_sale(self):
        self.c.execute(
            "DELETE * FROM sales WHERE sales_id=?", (self.sales_id,)
        )
        self.conn.commit()

@app.route('/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    sale = Sales(data['product_name'], data['amount'], data['quantity'])
    return sale.add_sale_to_database()

@app.route('/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    sale = Sales(data['product_name'], data['amount'], data['quantity'])
    sale.add_sale_to_database()
    return jsonify({"message": "Vente ajoutée avec succès!"}), 201

# route pour récupérer toutes les ventes de la base de données
@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sales.get_all_sales()
    return jsonify({"sales": sales}), 200

# route pour récupérer une vente spécifique de la base de données
@app.route('/sales/<string:sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = Sales.get_sale(sale_id)
    if sale:
        return jsonify({"sale": sale}), 200
    else:
        return jsonify({"message": "Vente introuvable"}), 404

# route pour supprimer une vente de la base de données
@app.route('/sales/<string:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    Sales.delete_sale(sale_id)
    return jsonify({"message": "Vente supprimée avec succès"}), 200

# route pour mettre à jour une vente de la base de données
@app.route('/sales/<string:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    data = request.get_json()
    Sales.update_sale(sale_id, data['product_name'], data['amount'], data['quantity'])
    return jsonify({"message": "Vente mise à jour avec succès"}), 200


if __name__ == '__main__':
    app.run(debug=True)
