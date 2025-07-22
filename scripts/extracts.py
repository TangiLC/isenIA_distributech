import sqlite3
import pandas as pd
from datetime import datetime
import os


#########  SAVE TO OUTPUT  ####################################################
# Sauvegarde d'un fichier horodaté dans le dossier cible
# Paramètre d'entrée : le contenu DataFrame du fichier, le nom cible
# Sortie : le chemin du fichier sauvegardé
def save_to_output(df, name, output_dir="./output_csv"):
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%Hh%Mm%S")
    filename = f"{now}_{name}_brut.csv"
    csv_path = os.path.join(output_dir, filename)
    df.to_csv(csv_path, index=False)
    print(f"✅ Fichier sauvegardé : {csv_path}")
    return csv_path


#########  EXTRACT CSV TO DF  #################################################
# Extraction d'un fichier CSV
# Paramètre d'entrée : le chemin du fichier CSV
# Sortie : le contenu du fichier CSV sous forme de DataFrame pandas
def extract_csv_to_df(commande_path, output_dir="./output_csv"):
    df = pd.read_csv(commande_path)
    base_name = os.path.splitext(os.path.basename(commande_path))[0]
    save_to_output(df, base_name, output_dir)
    return (base_name, df)


#########  EXTRACT SQLITE TO CSV  #############################################
# Extraction d'une BDD SQLite
# avec conversion des tables en fichiers CSV stockés dans /output_scv
# Paramètre d'entrée : le chemin de la BDD
# Sortie : liste de dataframes correspondant aux tables SQLite
def extract_sqlite_to_df(db_path, output_dir="./output_csv"):
    conn = sqlite3.connect(db_path)
    os.makedirs(output_dir, exist_ok=True)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, conn)
    dataframes = []

    for table_name in tables["name"]:
        if table_name != "sqlite_sequence":
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            save_to_output(df, table_name, output_dir)
            dataframes.append((table_name, df))
    conn.close()
    return dataframes
