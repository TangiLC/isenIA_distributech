import pandas as pd
from datetime import datetime, date

from scripts.requetes_sql import get_product_unit_prices, get_revendeur_region
from scripts.affichage import affiche_success_ligne, affiche_outcome


#########  TRANSFORM COHERENCE NUMERO COMMANDE ################################
# Validation des cohérences des colonnes du dataframe
# suppression de ligne en cas d'incohérence non corrigible
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_coherence_commande_df(name, data_df):
    erreurs = []
    lignes_valides = []

    if {"numero_commande", "commande_date"}.issubset(data_df.columns):

        for index, ligne in data_df.iterrows():
            ligne_dict = ligne.to_dict()
            numero_commande = ligne_dict.get("numero_commande")
            commande_date = ligne_dict.get("commande_date")
            ligne_coherente = ligne_dict.copy()
            ligne_erreurs = []

            try:
                parts = numero_commande.split("-")
                if len(parts) < 3:
                    date_commande_no = "19700101"
                else:
                    date_commande_no = parts[1]
                if isinstance(commande_date, str):
                    date_obj = datetime.strptime(commande_date, "%Y-%m-%d")
                    date_from_field = date_obj.strftime("%Y%m%d")
                else:
                    date_from_field = commande_date.strftime("%Y%m%d")

                # Vérifier la cohérence
                if date_commande_no != date_from_field:
                    # Corriger le numéro de commande avec la bonne date

                    nouveau_numero = f"CMD-{date_from_field}-***"

                    ref = {"name": name, "ligne": index + 2, "champ": "numero_commande"}
                    affiche_success_ligne(
                        ref,
                        "e cohérence commande/date",
                        numero_commande,
                        nouveau_numero,
                    )
                    ligne_coherente["numero_commande"] = nouveau_numero

            except ValueError as e:
                ligne_erreurs.append("commande_date")
                erreurs.append(
                    {
                        "ligne": index + 2,
                        "erreur": "Problème dans le traitement du numéro de commande",
                        "champs_erreurs": ["commande_date"],
                        "data": ligne_dict,
                    }
                )

            lignes_valides.append(ligne_coherente)

        affiche_outcome(
            name,
            "Toutes les lignes sont vérifiées, cohérence commande/date assurée.",
            erreurs,
        )
        return pd.DataFrame(lignes_valides)

    return data_df


#########  TRANSFORM COHERENCE REVENDEUR ######################################
# Validation des cohérences des colonnes du dataframe
# suppression de ligne en cas d'incohérence non corrigible
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_coherence_revendeur_df(name, data_df):
    # cohérence paire revendeur_id/region_id et existe
    # (Choix arbitraire: confiance revendeur_id)
    erreurs = []
    lignes_valides = []

    # Vérifie que les colonnes nécessaires sont présentes
    # Traitement uniquement si les deux colonnes sont présentes
    if {"revendeur_id", "region_id"}.issubset(data_df.columns):
        revendeur_region_map = get_revendeur_region()  # TO DO limiter requetes

        for index, ligne in data_df.iterrows():
            ligne_dict = ligne.to_dict()
            revendeur_id = ligne_dict.get("revendeur_id")
            region_id = ligne_dict.get("region_id")

            ligne_coherente = ligne_dict.copy()
            ligne_erreurs = []

            # Traitement uniquement si revendeur_id est connu
            if revendeur_id in revendeur_region_map:
                region_bdd = revendeur_region_map[revendeur_id]

                if region_bdd != region_id:
                    ref = {"name": name, "ligne": index + 2, "champ": "region_id"}
                    affiche_success_ligne(
                        ref, "e cohérence revendeur/region", region_id, region_bdd
                    )
                    ligne_coherente["region_id"] = region_bdd
                lignes_valides.append(ligne_coherente)
            else:
                ligne_erreurs.append("revendeur_id")
                erreurs.append(
                    {
                        "ligne": index + 2,
                        "erreur": "revendeur_id inconnu en base",
                        "champs_erreurs": ["revendeur_id"],
                        "data": ligne_dict,
                    }
                )

        affiche_outcome(
            name,
            "Toutes les lignes sont vérifiées, cohérence revendeur/region assurée.",
            erreurs,
        )

        return pd.DataFrame(lignes_valides)
    return data_df


#########  TRANSFORM COHERENCE PRIX UNITAIRE ##################################
# Validation des cohérences des colonnes du dataframe
# suppression de ligne en cas d'incohérence non corrigible
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_coherence_prix_unitaire_df(name, data_df):
    # cohérence paire cout_unitaire/unit_price et existe
    # (Choix arbitraire: confiance BDD cout_unitaire)
    erreurs = []
    lignes_valides = []

    if {"product_id", "unit_price"}.issubset(data_df.columns):
        product_price_map = get_product_unit_prices()  # TO DO limiter requetes

        for index, ligne in data_df.iterrows():
            ligne_dict = ligne.to_dict()
            product_id = ligne_dict.get("product_id")
            unit_price = ligne_dict.get("unit_price")

            ligne_coherente = ligne_dict.copy()
            ligne_erreurs = []

            if product_id in product_price_map:
                prix_ref = product_price_map[product_id]

                # Comparaison avec tolérance
                try:
                    prix_df = float(unit_price)
                    if abs(prix_df - prix_ref) > 0.01:  # Tolérance centime
                        ref = {"name": name, "ligne": index + 2, "champ": "unit_price"}
                        affiche_success_ligne(
                            ref, "e cohérence prix unitaire", prix_df, prix_ref
                        )
                        ligne_coherente["unit_price"] = prix_ref
                except:
                    ligne_erreurs.append("unit_price")
                    erreurs.append(
                        {
                            "ligne": index + 2,
                            "erreur": "unit_price invalide ou non numérique",
                            "champs_erreurs": ["unit_price"],
                            "data": ligne_dict,
                        }
                    )

            else:
                ligne_erreurs.append("product_id")
                erreurs.append(
                    {
                        "ligne": index + 2,
                        "erreur": "product_id inconnu en base",
                        "champs_erreurs": ["product_id"],
                        "data": ligne_dict,
                    }
                )

            lignes_valides.append(ligne_coherente)

        affiche_outcome(
            name,
            "Toutes les lignes sont vérifiées, cohérence prix unitaire assurée.",
            erreurs,
        )

        return pd.DataFrame(lignes_valides)

    # Pas de colonnes concernées
    return data_df


#########  TRANSFORM COHERENCE QUANTITE ##################################
# Validation des cohérences des colonnes du dataframe
# suppression de ligne en cas d'incohérence non corrigible
# Paramètre d'entrée : dataframe
# Sortie : dataframe corrigée
def transform_coherence_quantity_df(name, data_df):
    erreurs = []

    if "quantity" in data_df.columns:
        lignes_invalides = data_df[data_df["quantity"] <= 0]

        for index, ligne in lignes_invalides.iterrows():
            erreurs.append(
                {
                    "ligne": index + 2,
                    "erreur": "quantity doit être strictement positif",
                    "champs_erreurs": ["quantity"],
                    "data": ligne.to_dict(),
                }
            )

        affiche_outcome(
            name,
            "Toutes les lignes sont vérifiées, cohérence quantité assurée.",
            erreurs,
        )

        return data_df[data_df["quantity"] > 0]

    # Colonne manquante
    return data_df
