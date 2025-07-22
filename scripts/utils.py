import pandas as pd
import unicodedata
from datetime import datetime


#########  TRANSFORM : Nettoyage des espaces, caractères et typographies  #####
# Transformation des espaces, caractères speciaux et typographies
# Partie. 1 Nettoyer les espaces et les sauts de lignes
def nettoyer_texte(texte):
    temp_texte = str(texte)
    temp_texte = temp_texte.strip()  # enlève espaces début/fin
    temp_texte = temp_texte.replace("\xa0", " ")  # espace insécable -> espace normal
    temp_texte = temp_texte.replace("\r", "")
    temp_texte = temp_texte.replace("\n", "")  # supprime saut de ligne
    if temp_texte != texte:
        colored_text = display_variation(texte, temp_texte)
        print(f"✅ Correction des espaces dans : '{colored_text}'")
    if pd.isnull(texte):
        return "*"
    return texte


# Partie. 2 Nettoyer la typographie classique (guillemets, tirets)
def nettoyer_typographie(texte):
    temp_texte = str(texte)
    remplacements = {
        "’": "'",  # apostrophe courbe vers droite
        "“": '"',
        "”": '"',
        "«": '"',
        "»": '"',
        "–": "-",  # tiret moyen
        "—": "-",  # tiret long
    }
    for mauvais, bon in remplacements.items():
        temp_texte = temp_texte.replace(mauvais, bon)
    if temp_texte != texte:
        colored_text = display_variation(texte, temp_texte)
        print(f"✅ Correction de la typographie dans : '{colored_text}'")
    return texte


# Partie. 3 Nettoyer en supprimant accents et caractères spéciaux
# la typographie classique (guillemets, tirets)
def nettoyer_typographie_agressif(texte):

    texte = unicodedata.normalize("NFD", texte)  # sépare caractères + accents
    texte = texte.encode("ascii", "ignore").decode("utf-8")  # enlève accents
    return texte


###############################################################################
# Transformation des dates d'une dataframe
# # Paramètre d'entrée : dataframe
# Sortie : date corrigée


def corriger_date(date_str):

    if pd.isnull(date_str) or not isinstance(date_str, str):
        print(f"❌ Entrée invalide ou nulle : {date_str}")
        return "*"

    # Essai de plusieurs formats possibles
    formats_possibles = [
        "%Y_%m_%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y%m%d",
        "%d%m%Y",
        "%m-%d-%Y",
        "%d %b %Y",
        "%d %B %Y",
        "%Y %m %d",
        "%Y %b %d",
    ]

    for fmt in formats_possibles:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            colored_text = display_variation(dt.strftime("%Y-%m-%d"), date_str)
            print(
                f"✅ Correction réussie : '{colored_text}' avec format '{fmt}' → {dt.strftime('%Y-%m-%d')}"
            )
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            # print(f"⛔ Format invalide pour '{date_str}' avec '{fmt}'")
            continue

    print(f"❌ Aucun format valide trouvé pour : {date_str}")
    return "*"


###############################################################################
# Affichage du message en fin de traitement
# Paramètre d'entrée : message ok et liste d'erreurs
# Affichage des messages succès/echec


def affiche_outcome(name, ok_message, erreurs):
    print(f"[{name.upper()}]", end="")
    if erreurs:
        print(f"\033[91m⚠️ Lignes avec problèmes détectées :\033[0m")
        for err in erreurs:
            ligne = err.get("ligne", "?")
            erreur_type = err.get("erreur", "Erreur inconnue")
            erreur_data = err.get("data", "Problème de données")
            champs = err.get("champs_erreurs", [])

            if erreur_type == "Longueur de ligne incorrecte":
                print(
                    f"\033[35mLigne {ligne} → ligne ignorée (longueur incorrecte)\033[0m"
                )

            else:
                print(f"\033[33mLigne {ligne} → {erreur_type}\033[0m")
            afficher_tableau_horizontal(erreur_data, champs)
    else:
        print(f"\033[32m✅ {ok_message}\033[0m")


#########################################################################
### mise en forme tableau outcome #######################################


def afficher_tableau_horizontal(d, cles_invalides, indent=0, col_width=16):
    if not isinstance(d, dict):
        print(" " * indent + str(d))
        return
    if cles_invalides is None:
        cles_invalides = []
    cles = []
    valeurs = []

    for k, v in d.items():
        cle_str = str(k)
        val_str = str(v)

        if cle_str in cles_invalides:
            cle_str = f"\033[30;41m{cle_str.ljust(col_width)}\033[0m"
            val_str = f"\033[30;41m{val_str.ljust(col_width)}\033[0m"
        else:
            cle_str = cle_str.ljust(col_width)
            val_str = val_str.ljust(col_width)

        cles.append(cle_str)
        valeurs.append(val_str)

    ligne_cles = " | ".join(cles)
    ligne_valeurs = " | ".join(valeurs)

    print(" " * indent + f"| {ligne_cles} |")
    print(" " * indent + f"| {ligne_valeurs} |")


#########################################################################
### mise en forme mot corrigé ###########################################
def display_variation(original, edited):
    original = str(original)
    edited = str(edited)
    color = "\033[30;41m"
    reset = "\033[0m"
    result = ""
    max_len = max(len(original), len(edited))
    for i in range(max_len):
        c_orig = original[i] if i < len(original) else ""
        c_edit = edited[i] if i < len(edited) else ""

        if c_orig != c_edit:
            result += f"{color}{c_edit}{reset}"
        else:
            result += c_edit

    if not result.endswith(reset):
        result += reset

    return result
