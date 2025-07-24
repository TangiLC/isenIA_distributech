import mysql-connector-python3 as connector
import csv

# Nous nous connectons à mySQL
connexion = connector.connect(
    host='localhost',
    user='ton_utilisateur',
    password='ton_mot_de_passe',
    database='ta_base',
    port=3306
)

try:
    with connexion.cursor() as curseur:
        # 🧠 Requête SQL : dernier stock par produit
        requete = """
        SELECT s.product_id, s.quantity, s.date
        FROM stock s
        JOIN (
            SELECT product_id, MAX(date) AS last_date
            FROM stock
            GROUP BY product_id
        ) latest
        ON s.product_id = latest.product_id AND s.date = latest.last_date;
        """

        # 🧾 Exécution
        curseur.execute(requete)
        resultats = curseur.fetchall()

        # 📋 Récupération des noms de colonnes
        colonnes = [desc[0] for desc in curseur.description]

        # 📁 Écriture CSV
        with open('stock_final.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(colonnes)       # Écrire l'entête
            writer.writerows(resultats)     # Écrire les lignes

        print("✅ Export CSV terminé avec succès !")