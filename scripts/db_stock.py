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


def extract_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Récupérer toutes les tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    base_donnees = {}

    for table_name in tables:
        table = table_name[0]
        cur.execute(f"SELECT * FROM {table}")
        lignes = cur.fetchall()
        colonnes = [desc[0] for desc in cur.description]

        # Transformer chaque ligne en dictionnaire
        lignes_dict = [dict(zip(colonnes, ligne)) for ligne in lignes]

        # Ajouter au dictionnaire général
        base_donnees[table] = lignes_dict

    conn.close()
    return base_donnees

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
    data_sqlite = extract_sqlite("./data/base_stock.sqlite")
    print(data_csv)
    transform_csv(data_csv)

main()
