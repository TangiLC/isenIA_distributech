import sqlite3

# Ajout debut#
import pandas as pd

# Ajout fin#


def extract_csv(commande_path):
    # Ajout debut : je lis csv
    df = pd.read_csv(commande_path)
    # Je vérifie import des données csv
    return df
    # Ajout fin#
    # Ticket no.1


import sqlite3
import pandas as pd
import os


def sqlite_to_csv(db_path, output_dir="./output_csv"):
    conn = sqlite3.connect(db_path)
    os.makedirs(output_dir, exist_ok=True)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, conn)
    fichiers_crees = []
    for table_name in tables["name"]:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        csv_path = os.path.join(output_dir, f"{table_name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"✅ Table '{table_name}' exportée vers {csv_path}")
        fichiers_crees.append(csv_path)
    conn.close()
    return fichiers_crees


def transform_csv(data_csv):

    # Je définis les champs obligatoires en prenant les noms de colonnes comme champs obligatoires :
    # data_csv.columns : récupère tous les noms de colonnes dans le fichier CSV (la ligne d'en-tête)
    # .tolist() : transforme ça en liste Python.

    champs_obligatoires = data_csv.columns.tolist()
    print(champs_obligatoires)
    # Je prépare une liste vide pour y stocker les lignes qui posent problème.
    erreurs = []

    # Je vérifie ligne par ligne notre csv:
    # data_csv.iterrows() permet de parcourir chaque ligne du CSV une par une.
    # index = numéro de la ligne (commence à 0)
    # ligne = données de cette ligne, sous forme de dictionnaire

    for index, ligne in data_csv.iterrows():
        # Pour chaque champ obligatoire, on regarde :
        # Est-ce que la cellule correspondante dans cette ligne est vide (NaN) ?
        # pd.isnull(...) retourne True si la valeur est absente ou nulle.
        champs_manquants = [
            champ for champ in champs_obligatoires if pd.isnull(ligne.get(champ))
        ]
        # On crée une liste champs_manquants avec tous les noms de colonnes qui sont manquants dans cette ligne.
        # Si la ligne est incomplète (il manque des champs) :
        # On ajoute un dictionnaire dans erreurs qui contient :
        # ligne: le numéro réel de la ligne dans le fichier CSV (on ajoute +2 car :
        # Python commence à 0
        # Et la première ligne est l’en-tête)
        # champs_manquants: liste des champs manquants
        # données: les données complètes de cette ligne

        if champs_manquants:
            erreurs.append(
                {
                    "ligne": index + 2,  # +2 pour tenir compte de l'en-tête (ligne 1)
                    "champs_manquants": champs_manquants,
                    "données": ligne.to_dict(),
                }
            )

    # Afficher les erreurs à l'écran : à vérifier plus tard comment le rendre plus précis
    if erreurs:
        print("Lignes avec des champs manquants :")
        for err in erreurs:
            print(f"Ligne {err['ligne']} → Champs manquants ")
    else:
        print("✅ Toutes les lignes sont valides.")


def main():
    data_csv = extract_csv("./data/commande_revendeur_tech_express.csv")
    data_sqlite = sqlite_to_csv("./data/base_stock.sqlite")
    print(data_sqlite)

    # transform_csv(data_csv)
    for i in range(0, len(data_sqlite) - 1):
        data = extract_csv(data_sqlite[i])
        transform_csv(data)


main()
