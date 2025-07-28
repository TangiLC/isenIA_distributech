import os
from scripts.affichage import affiche_titre
from scripts.extracts import extract_csv_to_df, extract_sqlite_to_df, get_list_of_files
from scripts.load_commande_production import (
    load_commande_produit,
    load_production_produit,
)
from scripts.stock_extraire import extraire_stock
from scripts.transf_coherence import (
    transform_coherence_commande_df,
    transform_coherence_historique_df,
    transform_coherence_prix_unitaire_df,
    transform_coherence_quantity_df,
    transform_coherence_revendeur_df,
)
from scripts.transf_unicite import nettoyer_dataframe_unicite
from scripts.transforms import (
    transform_data_vide_df,
    transform_type_df,
)

# COMMANDE_PATH="data/commande_revendeur_tech_express.csv"
# COMMANDE_PATH = "data/commande_avec_erreurs.csv"
# SQLITE_PATH = "data/base_stock.sqlite"
DATA_PATH = "data/"


def main():

    ### 1- INITIALISATION : Extraction
    # Récupération de la liste des fichiers dans DATA_PATH
    # Extraction avec sauvegarde des données brutes en log
    # Conversion en csv et dataframe
    title = ">EXTRACTION DES DONNÉES".ljust(110)
    affiche_titre(title)
    df_a_traiter = []
    all_files = get_list_of_files(DATA_PATH)
    # extraitre les fichiers sqlite de production
    for sqlite_file in all_files.get("sqlite", []):
        chemin_sqlite = os.path.join(DATA_PATH, sqlite_file)
        data_sqlite_brut = extract_sqlite_to_df(chemin_sqlite)
    for df in data_sqlite_brut:
        df_a_traiter.append(df)
    # extraire les fichiers cvs de commande
    for csv_file in all_files.get("csv", []):
        chemin_csv = os.path.join(DATA_PATH, csv_file)
        df = extract_csv_to_df(chemin_csv)
        df_a_traiter.append(df)

    ### 2- TRANSFORMATION
    ### 2.1 Transformation : suppression des éléments vides
    title = ">TRANSFORMATION : Suppression des données vides".ljust(110)
    affiche_titre(title)
    df_sans_vide = []
    for data in df_a_traiter:
        # data[0] est la liste [nom du fichier, id du log]
        # data[1] est le dataframe à traiter
        dsv = transform_data_vide_df(data[0][0], data[1])
        df_sans_vide.append((data[0], dsv))

    ### 2.2 Transformation : validation des types
    title = ">TRANSFORMATION : Validation ou correction des types".ljust(110)
    affiche_titre(title)
    df_type = []
    for data in df_sans_vide:
        dsv = transform_type_df(data[0][0], data[1])
        df_type.append((data[0], dsv))

    ### 2.3 Transformation : Gestion des valeurs manquantes
    title = ">TRANSFORMATION : Correction des valeurs manquantes / aberrantes".ljust(
        110
    )
    affiche_titre(title)
    df_complet = []
    for data in df_type:  # Passage par toutes les étapes de cohérence
        t0 = transform_coherence_commande_df(data[0][0], data[1])
        t1 = transform_coherence_prix_unitaire_df(data[0][0], t0)
        t2 = transform_coherence_revendeur_df(data[0][0], t1)
        t3 = transform_coherence_quantity_df(data[0][0], t2)
        t4 = transform_coherence_historique_df(data[0][0], t3)
        df_complet.append((data[0], t4))

    ### 2.4 Transformation : Suppression des doublons
    title = ">TRANSFORMATION : Contrôle unicité et suppression des doublons".ljust(110)
    affiche_titre(title)
    df_unique = []
    for data in df_complet:
        df_unicite = nettoyer_dataframe_unicite(data[0][0], data[1])
        df_unique.append((data[0], df_unicite))

    ### 3 LOAD
    title = ">LOAD : sauvegarde des logs dans la BDD".ljust(110)
    affiche_titre(title)
    for data in df_unique:
        if "production_id" in data[1].columns:
            load_production_produit(data[0], data[1])
        if "numero_commande" in data[1].columns:
            load_commande_produit(data[0], data[1])
        # print(data[1])

    ### 4 Extraire Stock
    title = ">STOCK : Création des fiches de stock csv à jour".ljust(110)
    affiche_titre(title)
    extraire_stock()


if __name__ == "__main__":
    main()
