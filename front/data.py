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


def get_products_id_and_name():
    global cursor
    connexion()
    query = "SELECT * FROM produit"
    cursor.execute(query)
    responses = cursor.fetchall()
    products = []
    for response in responses:
        product = {}
        product["id"] = response[0]
        product["name"] = response[1]
        products.append(product)
    deconnexion()
    print("PRODUCTS", products)
    return products


def get_product_last_stock():
    global cursor
    connexion()
    query_all = """
        SELECT
          p.product_id   AS id,
          p.product_name AS name,
          v.quantity,
          v.mouvement,
          v.operateur,
          v.stock_date
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


get_product_last_stock()
