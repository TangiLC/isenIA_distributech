import pandas as pd


def verifier_unicite_colonne(df, nom_colonne):

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

    colonnes_a_verifier = ["numero_commande", "revendeur_id", "region_id", "product_id"]
    doublons_detectes = {}

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
