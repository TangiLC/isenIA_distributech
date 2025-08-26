import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def init_connection():
    conn = mysql.connector.connect(
        host=os.getenv("BDD_HOST"),
        port=os.getenv("BDD_PORT"),
        user=os.getenv("BDD_USER"),
        password=os.getenv("BDD_PASSWORD"),
        database=os.getenv("BDD_NAME"),
    )
    if conn.is_connected():
        print("[ok] connexion à la base réussie")
    return conn


bdd = None
cursor = None


def connexion():
    global bdd
    global cursor
    bdd = init_connection()
    cursor = bdd.cursor()


def deconnexion():
    global cursor, bdd
    if cursor:
        cursor.close()
        cursor = None
    if bdd:
        bdd.close()
        bdd = None


def get_product_last_stock():
    global cursor
    connexion()
    query_all = """
        SELECT
          p.product_id   AS id, p.product_name AS name,
          v.quantity, v.mouvement, v.operateur, v.stock_date
        FROM produit p
        LEFT JOIN vue_stock_final_produit v
          ON v.product_id = p.product_id
        ORDER BY p.product_id
        """
    cursor.execute(query_all)
    responses = cursor.fetchall()

    products = []
    for response in responses:
        product = {}
        product["id"] = response[0]
        product["name"] = response[1]
        product["quantity"] = response[2]
        product["movement"] = response[3]
        product["operator"] = response[4]
        product["date"] = response[5]
        products.append(product)
    deconnexion()
    print("PRODUCTS", products)
    return products


def get_products_3_last_movements():
    global cursor
    connexion()

    query_movements = """
        SELECT
            product_id, product_name, operateur, date_2,
            movement_2, date_1, movement_1, latest_date, movement_0
        FROM vue_historique_stock_par_revendeur
        ORDER BY product_id, operateur
    """

    cursor.execute(query_movements)
    movements_data = cursor.fetchall()

    query_final_stock = """
        SELECT
            product_id, product_name, quantity, operateur,
            mouvement, stock_date
        FROM vue_stock_final_produit
        ORDER BY product_id
    """

    cursor.execute(query_final_stock)
    final_stock_data = cursor.fetchall()

    products_dict = {}

    for response in final_stock_data:
        product_id = response[0]
        product_name = response[1]
        final_quantity = response[2]
        final_date = response[5]

        products_dict[product_id] = {
            "id": product_id,
            "name": product_name,
            "final_stock": {"quantity": final_quantity, "date": str(final_date)},
            "last_movements": [],
        }

    for response in movements_data:
        product_id = response[0]
        product_name = response[1]
        operateur = response[2]
        date_2 = response[3]
        movement_2 = response[4]
        date_1 = response[5]
        movement_1 = response[6]
        latest_date = response[7]
        movement_0 = response[8]

        if product_id not in products_dict:
            products_dict[product_id] = {
                "id": product_id,
                "name": product_name,
                "final_stock": None,
                "last_movements": [],
            }

        movements = []

        if movement_2 != 0 and str(date_2) != "2020-01-01":
            movements.append(
                {
                    "operator": operateur,
                    "date": str(date_2),
                    "movement": (
                        movement_2 if operateur == "Distributech" else -movement_2
                    ),
                }
            )

        if movement_1 != 0 and str(date_1) != "2020-01-01":
            movements.append(
                {
                    "operator": operateur,
                    "date": str(date_1),
                    "movement": (
                        movement_1 if operateur == "Distributech" else -movement_1
                    ),
                }
            )

        movements.append(
            {
                "operator": operateur,
                "date": str(latest_date),
                "movement": movement_0 if operateur == "Distributech" else -movement_0,
            }
        )

        products_dict[product_id]["last_movements"].extend(movements)

    products = list(products_dict.values())

    deconnexion()
    print("PRODUCTS WITH FINAL STOCK AND LAST MOVEMENTS", products)
    return products


get_products_3_last_movements()
