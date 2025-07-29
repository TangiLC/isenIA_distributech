import pandas as pd
import unicodedata
import re  # lecture du regex
from datetime import datetime

from scripts.affichage import affiche_success_ligne


def corriger_ocr(val, ref):
    """Correction des chiffres interprétés en lettre proche (OCR)
    Args:
        val (str): donnée à corriger
        ref (dict): données d'identification du fichier, ligne, champ

    Returns:
        corrigé (str): un chiffre modifié selon les paires de correction
    """
    if not isinstance(val, str):
        return val

    corrections = {
        "O": "0",
        "D": "0",
        "Q": "0",
        "l": "1",
        "I": "1",
        "i": "1",
        "t": "1",
        "|": "1",
        "Z": "2",
        "z": "2",
        "E": "3",
        "A": "4",
        "h": "4",
        "S": "5",
        "s": "5",
        "G": "6",
        "b": "6",
        "C": "6",
        "T": "7",
        "L": "7",
        "B": "8",
        "R": "8",
        "g": "9",
        "q": "9",
        "p": "9",
    }

    val_corrige = "".join(corrections.get(c, c) for c in val)

    if val_corrige != val:
        affiche_success_ligne(ref, "es nombres interprétés en lettre", val_corrige, val)

    return val_corrige


###############################################################################
def nettoyer_texte(texte, ref):
    """Nettoyage des espaces, retour ligne
    Args:
        texte (str): texte brut à nettoyer
        ref (dict): données d'identification du fichier, ligne, champ

    Returns:
        nettoyé (str): texte sans espaces et retour ligne
    """
    if pd.isnull(texte):
        return "*", True  # Valeur, Erreur

    temp_texte = str(texte)
    temp_texte = temp_texte.strip()  # enlève espaces début/fin
    temp_texte = temp_texte.replace("\xa0", " ")  # espace insécable -> espace normal
    temp_texte = temp_texte.replace("\r", "")
    temp_texte = temp_texte.replace("\n", "")  # supprime saut de ligne

    if repr(temp_texte) != repr(texte):
        affiche_success_ligne(ref, "e l'espacement", texte, temp_texte)

    return temp_texte, False  # Valeur corrigée, Pas d'erreur


###############################################################################
def nettoyer_typographie(texte, ref):
    """Nettoyage des guillemets, apostrophes, tirets
    Args:
        texte (str): texte brut à nettoyer
        ref (dict): données d'identification du fichier, ligne, champ

    Returns:
        nettoyé (str): texte nettoyé
    """
    temp_texte = str(texte)
    remplacements = {
        "'": "'",  # apostrophe courbe vers droite
        """: '"',
        """: '"',
        "«": '"',
        "»": '"',
        "–": "-",  # tiret moyen
        "—": "-",  # tiret long
    }
    for mauvais, bon in remplacements.items():
        temp_texte = temp_texte.replace(mauvais, bon)

    if temp_texte != texte:
        affiche_success_ligne(ref, "e la typographie", texte, temp_texte)

    return temp_texte, False  # Valeur corrigée, Pas d'erreur


###############################################################################
def nettoyer_typographie_agressif(texte):
    # TO DO : Reflexion sur l'utilité de ce traitement
    """Nettoyage des caractères accentués et spéciaux
    Args:
        texte (str): texte brut à nettoyer
        ref (dict): données d'identification du fichier, ligne, champ

    Returns:
        nettoyé (str): texte nettoyé
    """
    texte = unicodedata.normalize("NFD", texte)  # sépare caractères + accents
    texte = texte.encode("ascii", "ignore").decode("utf-8")  # enlève accents
    return texte


###############################################################################
# Transformation des dates d'une dataframe
# # Paramètre d'entrée : dataframe
# Sortie : date corrigée, booléen d'erreur
def corriger_date(date_str):
    """Transformation d'un format non-conventionnel de date en date
    Args:
        date_str (str): texte brut à nettoyer

    Returns:
        corrigé (date): date nettoyée / '*' en cas d'impossibilité de correction
    """
    if pd.isnull(date_str) or not isinstance(date_str, str):
        print(f"❌ Entrée invalide ou nulle : {date_str}")
        return "*", True  # Valeur, Erreur

    # Essai de plusieurs formats possibles
    formats_possibles = [
        "%Y_%m_%d",
        "%d/%m/%Y",
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
            return dt.strftime("%Y-%m-%d"), False  # Date corrigée, Pas d'erreur
        except ValueError:
            continue

    print(f"❌ Aucun format valide trouvé pour : {date_str}")
    return "*", True  # Valeur invalide, Erreur


##############################################################################
def nettoyer_numero_commande(numero, ref):
    """Nettoyage du format numéro de commande, objectif CMD-YYYYMMDD-nnn
    Args:
        numero (str): numéro de commande brut à nettoyer
        ref (dict): données d'identification du fichier, ligne, champ

    Returns:
        nettoyé (str): numéro de commande valide nettoyé si possible, initial sinon
    """

    original_numero = str(numero)

    # Retire les espaces mal placés, remplace les "." et "_" par des "-"
    numero_clean = (
        original_numero.strip().replace(" ", "-").replace(".", "-").replace("_", "-")
    )
    numero_clean = re.sub(r"-{2,}", "-", numero_clean)

    # Vérification du format avec une expression régulière
    # Format attendu : CMD-8 chiffres-3 chiffres
    pattern = r"^CMD-\d{8}-\d{3}$"
    est_valide_format = bool(re.match(pattern, numero_clean))

    # Si le format ne correspond pas après nettoyage, c'est une erreur irréparable
    if not est_valide_format:
        return numero_clean, True

    # Vérification de la validité de la date dans le numéro
    parts = numero_clean.split("-")
    if len(parts) == 3 and len(parts[1]) == 8:
        date_in_numero = parts[1]
        try:
            datetime.strptime(date_in_numero, "%Y%m%d")
            # Si on arrive ici, le numéro est valide
            # Détermine si c'était une correction ou pas
            correction_effectuee = numero_clean != original_numero
            if correction_effectuee:
                affiche_success_ligne(
                    ref, "u format numéro commande", numero_clean, original_numero
                )
            return numero_clean, False
        except Exception:

            return numero_clean, True

    return numero_clean, True
