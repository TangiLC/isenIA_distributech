from scripts.affichage import affiche_titre
from scripts.extracts import extract_csv_to_df, extract_sqlite_to_df
from scripts.transf_coherence import (
    transform_coherence_commande_df,
    transform_coherence_prix_unitaire_df,
    transform_coherence_revendeur_df,
)
from scripts.transforms import (
    transform_data_vide_df,
    transform_type_df,
)

# COMMANDE_PATH="data/commande_revendeur_tech_express.csv"
COMMANDE_PATH = "data/commande_avec_erreurs.csv"
SQLITE_PATH = "data/base_stock.sqlite"


def main():

    ### 1- INITIALISATION : Extraction
    title = ">EXTRACTION DES DONNÉES".ljust(110)
    affiche_titre(title)
    df_a_traiter = []
    df_a_traiter.append(extract_csv_to_df(COMMANDE_PATH))
    data_sqlite_brut = extract_sqlite_to_df(SQLITE_PATH)

    for i in range(len(data_sqlite_brut)):
        df_a_traiter.append(data_sqlite_brut[i])

    ### 2- TRANSFORMATION
    ### 2.1 Transformation : suppression des éléments vides
    title = ">TRANSFORMATION : Suppression des données vides".ljust(110)
    affiche_titre(title)
    df_sans_vide = []
    for data in df_a_traiter:
        dsv = transform_data_vide_df(data[0], data[1])
        df_sans_vide.append((data[0], dsv))

    ### 2.2 Transformation : validation des types
    title = ">TRANSFORMATION : Validation ou correction des types".ljust(110)
    affiche_titre(title)
    df_type = []
    for data in df_sans_vide:
        dsv = transform_type_df(data[0], data[1])
        df_type.append((data[0], dsv))

    ### 2.3 Transformation : Gestion des valeurs manquantes
    title = ">TRANSFORMATION : Correction des valeurs manquantes / aberrentes".ljust(
        110
    )
    affiche_titre(title)
    df_complet = []
    for data in df_type:
        t0 = transform_coherence_commande_df(data[0], data[1])
        t1 = transform_coherence_prix_unitaire_df(data[0], t0)
        t2 = transform_coherence_revendeur_df(data[0], t1)
        df_complet.append((data[0], t2))

    ### 2.4 Transformation : Suppression des doublons
    title = ">TRANSFORMATION : Contrôle unicité et suppression des doublons".ljust(110)
    affiche_titre(title)
    df_unique = []

    ### 3 LOAD
    title = ">LOAD : sauvegarde des logs dans la BDD".ljust(110)
    affiche_titre(title)
    df_final = []


if __name__ == "__main__":
    main()
