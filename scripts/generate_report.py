from dotenv import load_dotenv
import mysql.connector
from datetime import datetime
import csv
import os


load_dotenv()

VUES = {
    "stock_final_produit": "vue_stock_final_produit",
    "stock_final_revendeur": "vue_stock_final_revendeur",
    "historique_par_revendeur": "vue_historique_stock_par_revendeur",
}


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
    """Récupération des vues dans la BDD avec mysql-connector
    Création de fichier csv à partir de ces vues
    """
    # Connexion à la base de données MySQL

    try:
        conn = init_connection()
        cursor = conn.cursor()

        # Extraction des données des vues MySQL et export au format CSV
        # pour obtenir le dernier état des stocks par produit et par revendeur.

        for label, vue in VUES.items():
            # Construction de la requête SQL pour interroger la vue.
            requete = f"SELECT * FROM {vue};"
            # Exécution de la requête et récupération de toutes les lignes retournées.
            cursor.execute(requete)
            resultats = cursor.fetchall()
            # Récupération des noms de colonnes pour les utiliser comme en-têtes dans le fichier CSV.
            colonnes = [desc[0] for desc in cursor.description]

            # Création du fichier CSV avec les données actuelles des stocks.
            now = datetime.now().strftime("%Y%m%d")
            os.makedirs("exports", exist_ok=True)
            filename = os.path.join("exports", f"{now}_{label}.csv")
            with open(filename, "w", newline="", encoding="utf-8") as fichier_csv:
                writer = csv.writer(fichier_csv)
                writer.writerow(colonnes)  # On écrit l'entête
                writer.writerows(resultats)  # On écrit les lignes

            print(
                f"✅ Le fichier CSV du {label.replace('_', ' ').title()} a été généré avec succès."
            )

        # Fermeture du curseur pour libérer la mémoire et les ressources utilisées par ce curseur.
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(
            f"❌ Échec de l'extraction des données depuis la base MySQL. Détail de l'erreur : {err}"
        )
        return None
