import pandas as pd
from datetime import datetime

from scripts.utils import (
    corriger_date,
    corriger_ocr,
    nettoyer_numero_commande,
    nettoyer_texte,
    nettoyer_typographie,
)

from scripts.affichage import affiche_success_ligne, affiche_outcome


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
    print(f"[{name.upper()}]Champs attendus : {champs_obligatoires}")
    erreurs = []
    lignes_valides = []

    for index, ligne in data_df.iterrows():
        ligne_dict = ligne.to_dict()
        valeurs = list(ligne_dict.values())

        # Vérification 1 : ligne avec un mauvais nombre de colonnes
        if len(valeurs) < len(champs_obligatoires) or pd.isnull(valeurs[-1]):
            # Créer une version basique nettoyée pour l'affichage d'erreur
            ligne_display = {}
            for champ, val in ligne_dict.items():
                if pd.isnull(val):
                    ligne_display[champ] = "*"
                else:
                    ligne_display[champ] = str(val).strip() if val != "" else "*"

            erreurs.append(
                {
                    "ligne": index + 2,  # +2 pour tenir compte de l'en-tête (ligne 1)
                    "erreur": "Longueur de ligne incorrecte",
                    "data": ligne_display,  # Version nettoyée basique
                }
            )
            continue

        ligne_valide = {}
        ligne_erreurs = []

        for champ, valeur in ligne_dict.items():
            # Gestion des valeurs nulles comme dans transform_data_vide_df
            if pd.isnull(valeur):
                ligne_valide[champ] = "*"
                ligne_erreurs.append(champ)
                continue

            val = str(valeur).strip()

            # --------- Champs de type ENTIER ---------
            if champ in [
                "production_id",
                "product_id",
                "quantity",
                "region_id",
                "revendeur_id",
            ]:
                try:
                    # voir inférence de type Pandas (doc)
                    ref = {"name": name, "ligne": index + 2, "champ": champ}
                    if isinstance(val, (int, float)):
                        val_float = float(val)
                    else:
                        val_str = str(val).strip()
                        val_corr = corriger_ocr(val_str, ref)
                        val_float = float(val_corr)
                    if val_float.is_integer():
                        val_int = int(val_float)
                        if val != str(val_int):
                            affiche_success_ligne(ref, "u type entier", val_int, val)
                        ligne_valide[champ] = val_int
                    else:
                        val_int = int(val_float)
                        ref = {"name": name, "ligne": index + 2, "champ": champ}
                        affiche_success_ligne(
                            ref, "u type entier /tronqué/", val_int, f"{val} (décimal)"
                        )
                        ligne_valide[champ] = val_int
                except (ValueError, TypeError):
                    ligne_valide[champ] = val
                    ligne_erreurs.append(champ)
                continue

            # --------- Champs de type FLOTTANT ---------
            if champ in ["cout_unitaire", "unit_price"]:
                try:
                    ref = {"name": name, "ligne": index + 2, "champ": champ}
                    if isinstance(valeur, (int, float)):
                        val_float = float(valeur)
                    else:
                        val_str = str(valeur).strip()
                        val_corr = corriger_ocr(val_str, ref)
                        val_float = float(val_corr)
                    if val_float <= 0:
                        raise ValueError("float <= 0")
                    ligne_valide[champ] = val_float
                    if val != str(val_float):
                        affiche_success_ligne(ref, "u type flottant", val, val_float)
                except:
                    val_clean = str(valeur).strip() if valeur is not None else "*"
                    ligne_valide[champ] = val_clean if val_clean else "*"
                    ligne_erreurs.append(champ)
                continue

            # --------- Champs de type DATE ---------
            if champ in ["date_production", "commande_date"]:
                try:
                    datetime.strptime(val, "%Y-%m-%d")
                    ligne_valide[champ] = val
                except:
                    date_corrigee, erreur_date = corriger_date(val)
                    ligne_valide[champ] = date_corrigee

                    if erreur_date:
                        ligne_erreurs.append(champ)
                    elif val != date_corrigee:
                        ref = {"name": name, "ligne": index + 2, "champ": champ}
                        affiche_success_ligne(ref, "u format date", date_corrigee, val)
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
                    ref = {"name": name, "ligne": index + 2, "champ": champ}

                    if champ != "numero_commande":
                        # Nettoyage du texte puis de la typographie
                        texte_nettoye, erreur_texte = nettoyer_texte(val, ref)
                        if erreur_texte:
                            ligne_valide[champ] = "*"
                            ligne_erreurs.append(champ)
                        else:
                            typo_nettoyee, erreur_typo = nettoyer_typographie(
                                texte_nettoye, ref
                            )
                            ligne_valide[champ] = typo_nettoyee
                            # Note: erreur_typo est généralement False car nettoyer_typographie corrige toujours
                    else:
                        # Traitement spécial pour numero_commande
                        numero_nettoye, erreur_numero = nettoyer_numero_commande(
                            val, ref
                        )
                        ligne_valide[champ] = numero_nettoye
                        if erreur_numero:
                            ligne_erreurs.append(champ)

                continue

            # --------- Champs inconnus (non référencés) ---------
            ligne_valide[champ] = val

        # Vérification : détection des champs marqués comme invalides
        if ligne_erreurs:
            erreurs.append(
                {
                    "ligne": index + 2,  # +2 pour prendre en compte l'en-tête
                    "erreur": "Champs invalides ou non conformes",
                    "champs_erreurs": ligne_erreurs,
                    "data": ligne_valide,  # Utilise les données nettoyées au lieu des originales
                }
            )

        lignes_valides.append(ligne_valide)

    # --------- Rapport console ---------
    affiche_outcome(
        name, "Toutes les lignes sont vérifiées, absence de champ invalide.", erreurs
    )
    # --------- Retour du DataFrame nettoyé ---------
    return pd.DataFrame(lignes_valides)
