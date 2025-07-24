import pandas as pd

def verifier_unicite_colonne(df, nom_colonne):
    """
    🔍 Vérifie que les valeurs d'une colonne donnée dans un DataFrame sont uniques.

    ➕ Paramètres :
    - df : le DataFrame contenant les données à vérifier
    - nom_colonne : nom de la colonne à analyser (string)

    📦 Retour :
    - Liste des valeurs dupliquées dans la colonne (liste vide si aucune duplication)
    """

    if nom_colonne not in df.columns:
        print(f"⚠️ La colonne '{nom_colonne}' n'existe pas dans le DataFrame.")
        return []

    # Compte combien de fois chaque valeur apparaît dans la colonne
    comptage = df[nom_colonne].value_counts()

    # Sélectionne les valeurs avec au moins 2 occurrences
    duplicatas = comptage[comptage > 1].index.tolist()

    if duplicatas:
        print(f"\n🚨 Doublons détectés dans la colonne '{nom_colonne}':")
        for valeur in duplicatas:
            print(f"- {valeur}")
    else:
        print(f"✅ Toutes les valeurs de la colonne '{nom_colonne}' sont uniques.")

    return duplicatas


def verifier_unicites_globales(df):
    """
    🔎 Lance les vérifications d’unicité sur les colonnes critiques du projet Distributech.

    Vérifie :
    - numero_commande
    - revendeur_id
    - region_id
    - product_id

    📦 Retourne :
    Un dictionnaire contenant les colonnes et leurs valeurs dupliquées (le cas échéant)
    """

    colonnes_a_verifier = ["numero_commande", "revendeur_id", "region_id", "product_id"]
    doublons_detectes = {}

    print("\n=== Vérification globale de l’unicité des identifiants ===")

    for col in colonnes_a_verifier:
        duplicatas = verifier_unicite_colonne(df, col)
        if duplicatas:
            doublons_detectes[col] = duplicatas

    if not doublons_detectes:
        print("\n🎉 Toutes les colonnes critiques sont uniques.")
    else:
        print("\n⚠️ Résumé des duplications par colonne :")
        for col, dups in doublons_detectes.items():
            print(f"→ {col} : {len(dups)} doublon(s) détecté(s)")

    return doublons_detectes
