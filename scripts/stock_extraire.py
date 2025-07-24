from dotenv import load_dotenv
import mysql.connector
from datetime import datetime
import csv


load_dotenv()

# Nous nous connectons à mySQL
connexion = mysql.connector.connect(
    host='localhost',
    user=BDD_USER,
    password=BDD_PASSWORD,
    database=BDD_NAME,
    port=3306
)

try:
    with connexion.cursor() as curseur:
        # Nous lancons une requête SQL pour recevoir notr dernier stock par produit
        requete = """
        SELECT s.product_id, s.quantity, s.stock_date, p.product_name
        FROM stock s
        JOIN produit p ON s.product_id = p.product_id
        JOIN (
            SELECT product_id, MAX(stock_date) AS last_date
            FROM stock
            GROUP BY product_id
        ) latest
        ON s.product_id = latest.product_id AND s.stock_date = latest.last_date;
        """

        # Nous exécutons notre requête et nous récupérons toutes les lignes retournées par la requête SQL dans une liste de tuples.
        curseur.execute(requete)
        resultats = curseur.fetchall()

        # Nous récupérons des noms de colonnes pour pouvoir les écrire comme en-tête dans le CSV.
        colonnes = [desc[0] for desc in curseur.description]

        # Nous créons notre CSV avec les données d'état actuel de stock
            now = datetime.now().strftime("%Y%m%d")
            filename = f"{now}_stock_final.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(colonnes)       # On écrit l'entête
            writer.writerows(resultats)     # On écrit les lignes

        print("✅ Le fichier CSV du stock a été généré avec succès.")