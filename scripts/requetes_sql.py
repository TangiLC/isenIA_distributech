import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_revendeur_region():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("BDD_HOST"),
            port=os.getenv("BDD_PORT"),
            user=os.getenv("BDD_USER"),
            password=os.getenv("BDD_PASSWORD"),
            database=os.getenv("BDD_NAME"),
        )
        cursor = conn.cursor()
        cursor.execute("SELECT revendeur_id, region_id FROM revendeur")

        # Construction du dictionnaire {revendeur_id: region_id}
        revendeur_region_map = {}
        for revendeur_id, region_id in cursor.fetchall():
            revendeur_region_map[revendeur_id] = region_id

        cursor.close()
        conn.close()

        return revendeur_region_map

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return {}


def get_product_unit_prices():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("BDD_HOST"),
            port=os.getenv("BDD_PORT"),
            user=os.getenv("BDD_USER"),
            password=os.getenv("BDD_PASSWORD"),
            database=os.getenv("BDD_NAME"),
        )
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, cout_unitaire FROM produit")

        product_price_map = {}
        for product_id, cout_unitaire in cursor.fetchall():
            product_price_map[product_id] = float(cout_unitaire)

        cursor.close()
        conn.close()

        return product_price_map

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return {}
