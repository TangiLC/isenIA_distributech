from dotenv import load_dotenv
import mysql.connector
from datetime import datetime
import csv
import os


load_dotenv()


def init_connection():
    """Initialisation de la connection mysql-connector
    Returns:
        connector.connect: le connecteur actif
    """
    return mysql.connector.connect(
        host=os.getenv("BDD_HOST"),
        port=os.getenv("BDD_PORT"),
        user=os.getenv("BDD_USER"),
        password=os.getenv("BDD_PASSWORD"),
        database=os.getenv("BDD_NAME"),
    )


def extraire_stock():
    # Nous nous connectons à mySQL

    try:
        conn = init_connection()
        cursor = conn.cursor()

        # Nous lancons une requête SQL pour recevoir notr dernier stock par produit
        requete = """
        SELECT s.stock_date,s.product_id, p.product_name, s.quantity, 
        COALESCE(r.revendeur_name, 'Distributech') AS operateur,
        CASE WHEN s.operator_id IS NULL THEN s.movement
           ELSE -1 * s.movement END AS mouvement
        FROM stock s
        JOIN produit p ON s.product_id = p.product_id
        JOIN (
            SELECT product_id, MAX(stock_date) AS last_date
            FROM stock
            GROUP BY product_id
        ) latest
        ON s.product_id = latest.product_id AND s.stock_date = latest.last_date
        JOIN revendeur r ON s.operator_id = r.revendeur_id;
        """

        # Nous exécutons notre requête et nous récupérons toutes les lignes retournées par la requête SQL dans une liste de tuples.
        cursor.execute(requete)
        resultats = cursor.fetchall()

        # Nous récupérons des noms de colonnes pour pouvoir les écrire comme en-tête dans le CSV.
        colonnes = [desc[0] for desc in cursor.description]

        # Nous créons notre CSV avec les données d'état actuel de stock
        now = datetime.now().strftime("%Y%m%d")
        os.makedirs("exports", exist_ok=True)
        filename = os.path.join("exports", f"{now}_stock_final_produit.csv")
        with open(filename, "w", newline="", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(colonnes)  # On écrit l'entête
            writer.writerows(resultats)  # On écrit les lignes

        print("✅ Le fichier CSV du stock par revendeur a été généré avec succès.")

        filename = os.path.join("exports", f"{now}_stock_final_revendeur.csv")
        with open(filename, "w", newline="", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(colonnes)  # On écrit l'entête
            writer.writerows(resultats)  # On écrit les lignes

        print("✅ Le fichier CSV du stock par produit a été généré avec succès.")

        # conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'insertion du log : {err}")
        return None
