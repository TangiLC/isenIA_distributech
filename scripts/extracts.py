import sqlite3
import pandas as pd
from datetime import datetime
import os
import shutil

from scripts.utils.requetes_sql import insert_into_bddlogs


def get_list_of_files(path):
    """Récupérer la liste des fichiers contenus dans le dossier {path}, classées par type
    Args:
        path (str): chemin du dossier
    Returns:
        files (dict): un dictionnaire des fichiers csv et sqlite
    """
    files = {}
    if not os.path.isdir(path):
        raise ValueError(f"❌ Le chemin {path} n'est pas un dossier valide.")

    for nom_fichier in os.listdir(path):
        chemin_fichier = os.path.join(path, nom_fichier)
        if os.path.isfile(chemin_fichier):
            ext = os.path.splitext(nom_fichier)[1].lower().lstrip(".")
            if ext in ["csv", "sqlite"]:
                if ext not in files:
                    files[ext] = []
                files[ext].append(nom_fichier)

    return files


###############################################################################
def save_to_logs(df, name, logs_dir="./logs_csv"):
    """Sauvegarde du fichier csv dans le dossier logs_csv
    Args:
        df (dataframe): le dataframe extrait des fichiers en entrée
        name (str): le nom précédent du fichier extrait
        logs_dir (str, optional): le chemin du dossier archive, defaults to "./logs_csv".
    Returns:
        csv_path(str): le nom complet du fichier archive créé
    """
    os.makedirs(logs_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%Hh%Mm%S")
    filename = f"{now}_{name}.csv"
    csv_path = os.path.join(logs_dir, filename)
    df.to_csv(csv_path, index=False)
    print(f"✅ Fichier sauvegardé : {csv_path}")
    return csv_path


###############################################################################
def extract_csv_to_df(commande_path, logs_dir="./logs_csv"):
    """Extraction d'un fichier csv vers dataframe (utilise Pandas)
    Args:
        commande_path (str): chemin du fichier commande revendeur
        logs_dir (str, optional): le chemin du dossier archive, defaults to "./logs_csv".

    Returns:
        base_name(str): le nom minimal du fichier de commande
        df (dataframe): le fichier dataframe correspondant extrait par Pandas
    """
    df = pd.read_csv(commande_path)
    base_name = os.path.splitext(os.path.basename(commande_path))[0]
    csvpath = save_to_logs(df, base_name, logs_dir)
    id = insert_into_bddlogs(csvpath, "log_commande_brut")
    base_name = [os.path.splitext(os.path.basename(commande_path))[0], id]
    return (base_name, df)


###############################################################################
def extract_sqlite_to_df(db_path, logs_dir="./logs_csv"):
    """Extraction d'un fichier sqlite vers dataframe (utilise Pandas)
    Args:
        db_path (str): chemin du fichier sqlite
        logs_dir (str, optional): le chemin du dossier archive, defaults to "./logs_csv".

    Returns:
        une liste de :
        table_name(str): le nom minimal de la table issue du fichier sqlite
        df (dataframe): le fichier dataframe correspondant extrait par Pandas
    """
    conn = sqlite3.connect(db_path)
    os.makedirs(logs_dir, exist_ok=True)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, conn)
    dataframes = []

    for table_name in tables["name"]:
        if table_name in ["production"]:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            csvpath = save_to_logs(df, table_name + "_brut", logs_dir)
            id = insert_into_bddlogs(csvpath, "log_production_brut")
            dataframes.append(([table_name, id], df))
        # TO DO Discuss elif ??
        elif table_name == "revendeur":
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            if "revendeur_name" in df.columns and "revendeur_id" in df.columns:
                df["revendeur_name"] = df["revendeur_id"].apply(anonymize_name)
            save_to_logs(df, table_name + "_rgpd", logs_dir)
            dataframes.append((table_name, df))

    conn.close()
    return dataframes


###############################################################################
def anonymize_name(id):
    """anonymisation partiel du nom du revendeur pour éviter de stocker
        des données sensibles en log (RGPD)
    Args:
        id (int): l'id du revendeur
    Returns:
        anonym (str): un nom partiellement anonymisé
    """
    formatted_id = str(id).zfill(3)
    return f"revendeur_{formatted_id}"


###############################################################################
def move_file_to_target(file, target):
    """
    Déplace un fichier vers un répertoire cible.
    Args:
        file: Chemin complet du fichier source à déplacer
        path: Chemin du répertoire de destination
    """
    os.makedirs(target, exist_ok=True)
    filename = os.path.basename(file)
    target_path = os.path.join(target, filename)

    shutil.move(file, target_path)
    print(f"Le fichier {file} a été archivé vers {target}")
