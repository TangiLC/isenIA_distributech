from scripts.utils.affichage import affiche_outcome


def nettoyer_dataframe_unicite(name, data_df):
    """Suppression des colonnes en doublon
        transposition .T du dataframe lignes/colonnes puis retour après suppression
    Args:
        name (lst): [nom du fichier csv, id du log]
        data_df (dataframe): données csv extraites en dataframe (Pandas)
    Returns:
        df corrigé(dataframe): données corrigées
    """
    # Étape 1 : Supprimer les colonnes en doublon (même contenu) Fonction T transpose
    colonnes_uniques = data_df.T.drop_duplicates().T
    colonnes_supprimees = set(data_df.columns) - set(colonnes_uniques.columns)
    if colonnes_supprimees:
        affiche_outcome(
            name, f"Colonnes dupliquées supprimées : {list(colonnes_supprimees)}", {}
        )
    else:
        affiche_outcome(name, "Aucune colonne dupliquée détectée.", {})

    # Étape 2 : Supprimer les lignes en doublon
    lignes_avant = colonnes_uniques.copy()
    index_avant = lignes_avant.index
    df_final = colonnes_uniques.drop_duplicates()
    index_apres = df_final.index
    index_supprimes = index_avant.difference(index_apres)

    if not index_supprimes.empty:
        affiche_outcome(
            name, f"ligne(s) dupliquée(s) supprimée(s):{list(index_supprimes)}", {}
        )
    else:
        affiche_outcome(name, "Aucune ligne dupliquée détectée.", {})

    return df_final
