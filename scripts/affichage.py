import sys
import time


def affiche_titre(title):
    """Affichage du titre avec animation barre de progression
    Args :
        titre (string)
    """

    style_prefix = "\033[30;44m "
    style_suffix = " \033[0m"

    debut = title[:45]
    fin = title[45:]

    sys.stdout.write(style_prefix + debut)
    sys.stdout.flush()
    for c in fin:
        time.sleep(0.01)
        sys.stdout.write(c)
        sys.stdout.flush()
    sys.stdout.write(style_suffix + "\n")
    sys.stdout.flush()


###############################################################################
def affiche_success_ligne(ref, transform_type, before, after):
    """Affichage du du message en fin de traitement ligne
    Args :
        ref (objet références du fichier/ligne/champ),
        transform_type (string) : information sur le traitement transform,
        before : élément avant correction,
        after : élément après correction
    Returns : null
    """
    reference = f"[{ref['name'].upper()}]>Ligne{ref['ligne']}|{ref['champ']}"
    colored_text = display_variation(str(before), str(after))
    print(f"✅ {reference}: Correction d{transform_type} dans : '{colored_text}'")


###############################################################################
def affiche_outcome(name, ok_message, erreurs):
    """Affichage du message en fin de traitement fichier
    Args:
        name (str): nom du fichier
        ok_message (str): alternative succès
        erreurs (obj): alternative echec, liste d'erreurs {ligne,erreur_type,erreur_data,champs}
    """
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
def afficher_tableau_horizontal(d, cles_invalides, indent=0, col_width=16):
    """Mise en page du tableau outcome
    Args:
        d (dict): dictionnaire à mettre en forme
        cles_invalides (key): clés invalides
        indent (int, optional): décalage initial du tableau,defaults to 0.
        col_width (int, optional): largeur de colonne, defaults to 16.
    """
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
def display_variation(original, edited):
    """Mise en évidence (fond rouge) des éléments corrigés
    Args:
        original (_type_): donnée brute
        edited (_type_): donnée corrigée
    Returns:
        str: string composite avec les éléments corrigés mis en évidence
    """
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
