import pandas as pd
from datetime import datetime

from scripts.utils import (
    affiche_outcome,
    corriger_date,
    nettoyer_texte,
    nettoyer_typographie,
    nettoyer_typographie_agressif,
)


#########  TRANSFORM ELEMENT VIDE  #############################################
# Transformation des éléments vides d'une dataframe
# ajout de '*' en cas d'élément manquant
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_data_vide_df(name, data_df):

    champs_obligatoires = data_df.columns.tolist()
    print(f"[{name.upper()}]Champs attendus : {champs_obligatoires}")
    erreurs = []
    lignes_valides = []

    # data_df.iterrows() permet de parcourir chaque ligne du CSV une par une.
    # index = numéro de la ligne (commence à 0)
    # ligne = données de cette ligne, sous forme de dictionnaire

    for index, ligne in data_df.iterrows():
        ligne_dict = ligne.to_dict()
        valeurs = list(ligne_dict.values())

        # Vérification 1 : ligne avec un mauvais nombre de colonnes

        if len(valeurs) < len(champs_obligatoires) or pd.isnull(valeurs[-1]):
            # TO DO : Moyen de reconstituer une valeur manquante avec décalage des colonnes ?
            erreurs.append(
                {
                    "ligne": index + 2,  # +2 pour tenir compte de l'en-tête (ligne 1)
                    "erreur": "Longueur de ligne incorrecte",
                    "data": ligne_dict,
                }
            )
            continue

        # Remplacement des champs manquants ou nuls par '*'
        ligne_complete = {}
        for champ, val in ligne_dict.items():
            if pd.isnull(val):
                ligne_complete[champ] = "*"
            else:
                ligne_complete[champ] = val

        # Vérification : détection des champs marqués comme manquants
        champs_erreurs = [champ for champ, val in ligne_complete.items() if val == "*"]

        if champs_erreurs:
            erreurs.append(
                {
                    "ligne": index + 2,
                    "erreur": "Champs manquants",
                    "champs_erreurs": champs_erreurs,
                    "data": ligne_complete,
                }
            )

        lignes_valides.append(ligne_complete)

    # Afficher les erreurs à l'écran : à vérifier plus tard comment le rendre plus précis
    affiche_outcome(
        name, "Toutes les lignes sont vérifiées, absence de valeur nulle.", erreurs
    )

    # On crée un nouveau fichier avec uniquement les lignes valides.
    df_valide = pd.DataFrame(lignes_valides)

    return df_valide


#########  TRANSFORM TYPE  #############################################
# Validation des types des colonnes du dataframe
# ajout de '*' en cas d'élément incohérent
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_type_df(name, data_df):
    champs_obligatoires = data_df.columns.tolist()
    erreurs = []
    lignes_valides = []

    for index, ligne in data_df.iterrows():
        ligne_dict = ligne.to_dict()
        ligne_valide = {}
        ligne_erreurs = []

        for champ, valeur in ligne_dict.items():
            val = str(valeur).strip()

            if champ in [
                "production_id",
                "product_id",
                "quantity",
                "region_id",
                "revendeur_id",
            ]:
                try:
                    val_float = float(val)
                    if val_float.is_integer():
                        ligne_valide[champ] = int(val_float)
                    else:
                        raise ValueError("Nombre décimal détecté")
                except:
                    ligne_valide[champ] = "*"
                    ligne_erreurs.append(champ)
                continue

            # --------- Champs de type FLOTTANT ---------
            if champ in ["cout_unitaire", "unit_price"]:
                try:
                    val_float = float(val)
                    if val_float <= 0:
                        raise ValueError("float <= 0")
                    ligne_valide[champ] = val_float
                except:
                    ligne_valide[champ] = "*"
                    ligne_erreurs.append(champ)
                continue

            # --------- Champs de type DATE ---------
            if champ in ["date_production", "commande_date"]:
                try:
                    datetime.strptime(val, "%Y-%m-%d")
                    ligne_valide[champ] = val
                except:
                    correct = corriger_date(val)
                    ligne_valide[champ] = correct
                continue

            # --------- Champs de type TEXTE ---------
            if champ in [
                "product_name",
                "region_name",
                "revendeur_name",
                "numero_commande",
            ]:

                if not any(c.isalpha() for c in val):
                    ligne_valide[champ] = "*"
                    ligne_erreurs.append(champ)
                else:
                    if champ != "numero_commande":
                        val1 = nettoyer_texte(val)
                        val2 = nettoyer_typographie(val1)
                        # val3 = nettoyer_typographie_agressif(val2)
                        ligne_valide[champ] = val2
                continue

            # --------- Champs inconnus (non référencés) ---------
            ligne_valide[champ] = val

        if ligne_erreurs:
            erreurs.append(
                {
                    "ligne": index + 2,  # +2 pour prendre en compte l'en-tête
                    "erreur": "Champs invalides ou non conformes",
                    "champs_erreurs": ligne_erreurs,
                    "data": ligne_dict,
                }
            )

        lignes_valides.append(ligne_valide)

    # --------- Rapport console ---------
    affiche_outcome(
        name, "Toutes les lignes sont vérifiées, absence de champ invalide.", erreurs
    )
    # --------- Retour du DataFrame nettoyé ---------
    return pd.DataFrame(lignes_valides)
