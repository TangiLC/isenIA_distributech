import pandas as pd


#########  TRANSFORM ELEMENT VIDE  #############################################
# Transformation des éléments vides d'une dataframe
# ajout de '*' en cas d'élément manquant
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_data_vide_df(name, data_df):

    champs_obligatoires = data_df.columns.tolist()
    print(f"[{name.upper()}]Champs attendus : {champs_obligatoires}", end=">")
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
                    "données": ligne_dict,
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
        champs_manquants = [
            champ for champ, val in ligne_complete.items() if val == "*"
        ]

        if champs_manquants:
            erreurs.append(
                {
                    "ligne": index + 2,
                    "erreur": "Champs manquants",
                    "champs_manquants": champs_manquants,
                    "données": ligne_complete,
                }
            )

        lignes_valides.append(ligne_complete)

    # Afficher les erreurs à l'écran : à vérifier plus tard comment le rendre plus précis
    if erreurs:
        print(f"\n\033[91m⚠️ Lignes avec problèmes détectées :\033[0m")
        for err in erreurs:
            if err["erreur"] == "Longueur de ligne incorrecte":
                print(
                    f"\033[35mLigne {err['ligne']} → ligne ignorée (longueur incorrecte)\033[0m"
                )
            else:
                print(
                    f"\033[34mLigne {err['ligne']} → champs manquants : {err['champs_manquants']}\033[0m"
                )
    else:
        print(f"\033[32m✅ Toutes les lignes sont valides.\033[0m")

    # On crée un nouveau fichier avec uniquement les lignes valides.
    df_valide = pd.DataFrame(lignes_valides)

    return df_valide

# Transformation des dates d'une dataframe
# # Paramètre d'entrée : dataframe
# Sortie : date corrigée


def corriger_date(date_str):
    """
    Tente de corriger une chaîne représentant une date
    vers le format standard YYYY-MM-DD.
    Retourne '*' si la date est invalide ou non corrigeable.
    """
    if pd.isnull(date_str) or not isinstance(date_str, str):
        return "*"

    # Essai de plusieurs formats possibles
    formats_possibles = [
        "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d",
        "%Y%m%d", "%d%m%Y", "%m-%d-%Y", "%d %b %Y", "%d %B %Y"
    ]

    for fmt in formats_possibles:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return "*"

    