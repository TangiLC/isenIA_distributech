import sys
import time

###############################################################################
# Affichage du titre avec animation barre de progression
# Paramètre d'entrée : titre
# Affichage progressif


def affiche_titre(title: str):

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
# Affichage du message en fin de traitement ligne
# Paramètre d'entrée : message ok et liste d'erreurs
# Affichage des messages succès/echec


def affiche_success_ligne(ref, transform_type, before, after):

    colored_text = display_variation(str(before), str(after))
    print(
        f"✅ [{ref['name'].upper()}]>Ligne{ref['ligne']}|{ref['champ']}: Correction d{transform_type} dans : '{colored_text}'"
    )


###############################################################################
# Affichage du message en fin de traitement fichier
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
