from scripts.extracts import extract_csv_to_df, extract_sqlite_to_df
from scripts.transforms import transform_data_vide_df

# COMMANDE_PATH="data/commande_revendeur_tech_express.csv"
COMMANDE_PATH = "data/commande_avec_erreurs.csv"
SQLITE_PATH = "data/base_stock.sqlite"


def main():

    ### 1- INITIALISATION : Extraction
    df_a_traiter = []
    df_a_traiter.append(extract_csv_to_df(COMMANDE_PATH))
    data_sqlite_brut = extract_sqlite_to_df(SQLITE_PATH)

    for i in range(len(data_sqlite_brut)):
        df_a_traiter.append(data_sqlite_brut[i])

    ### 2- TRANSFORMATION
    ### 2.1 Transformation : suppression des éléments vides
    df_sans_vide = []
    for data in df_a_traiter:
        dsv = transform_data_vide_df(data[0], data[1])
        df_sans_vide.append((data[0], dsv))

    # print(df_sans_vide)


if __name__ == "__main__":
    main()
