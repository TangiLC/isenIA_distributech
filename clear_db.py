import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


####### FONCTION DE NETTOYAGE BDD POUR TEST. NE PAS INCLURE EN PROD ###########
def init_connection():
    return mysql.connector.connect(
        host=os.getenv("BDD_HOST"),
        port=os.getenv("BDD_PORT"),
        user=os.getenv("BDD_USER"),
        password=os.getenv("BDD_PASSWORD"),
        database=os.getenv("BDD_NAME"),
    )


def clear_db():
    try:
        conn = init_connection()
        cursor = conn.cursor()
        tables = [
            "commande_produit",
            "commande",
            "log_commande_brut",
            "production_produit",
            "production",
            "log_production_brut",
            "stock",
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"deleting {table}")
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")


clear_db()
