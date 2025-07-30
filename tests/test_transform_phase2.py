import pytest
import pandas as pd
from unittest.mock import patch
from scripts.transform_phase2 import (
    transform_coherence_commande_df,
    transform_coherence_revendeur_df,
    transform_coherence_prix_unitaire_df,
    transform_coherence_quantity_df,
    transform_coherence_historique_df,
)


@pytest.mark.parametrize(
    "numero_commande, commande_date, expected_num",
    [
        ("CMD-20240101-001", "2024-01-01", "CMD-20240101-001"),  # cohérent
        ("CMD-20220101-001", "2024-01-01", "CMD-20240101-***"),  # non cohérent
        ("CMD-XYZ", "2024-01-01", "CMD-20240101-***"),  # mal formé
    ],
)
def test_transform_coherence_commande_df(numero_commande, commande_date, expected_num):
    df = pd.DataFrame(
        [{"numero_commande": numero_commande, "commande_date": commande_date}]
    )
    result = transform_coherence_commande_df("test.csv", df)
    assert result.loc[0, "numero_commande"] == expected_num


@pytest.mark.parametrize(
    "revendeur_id, region_id, expected_region, should_be_present",
    [
        (1, 1, 1, True),  # cohérent
        (1, 2, 1, True),  # incohérent, correction attendue
        (99, 1, 0, False),  # revendeur inconnu, ligne rejetée
    ],
)
@patch("scripts.transform_phase2.get_revendeur_region", return_value={1: 1})
def test_transform_coherence_revendeur_df(
    mock_get, revendeur_id, region_id, expected_region, should_be_present
):
    df = pd.DataFrame(
        [{"revendeur_id": int(revendeur_id), "region_id": int(region_id)}]
    )
    result = transform_coherence_revendeur_df("test.csv", df)

    if should_be_present:
        assert not result.empty
        assert result.iloc[0]["region_id"] == expected_region
    else:
        assert result.empty


@pytest.mark.parametrize(
    "product_id, unit_price, expected_price",
    [
        ("P001", 10.0, 10.0),  # cohérent
        ("P001", 11.5, 10.0),  # correction
        ("P002", "NaN", "NaN"),  # non numérique
        ("XXX", 9.0, 9.0),  # produit inconnu
    ],
)
@patch("scripts.transform_phase2.get_product_unit_prices", return_value={"P001": 10.0})
def test_transform_coherence_prix_unitaire_df(
    mock_get, product_id, unit_price, expected_price
):
    df = pd.DataFrame([{"product_id": product_id, "unit_price": unit_price}])
    result = transform_coherence_prix_unitaire_df("test.csv", df)

    if product_id == "XXX":
        assert result.loc[0, "product_id"] == product_id
    elif product_id == "P002":
        assert result.loc[0, "unit_price"] == unit_price
    else:
        assert result.loc[0, "unit_price"] == expected_price


@pytest.mark.parametrize(
    "quantity, should_be_present",
    [
        (5, True),  # valide
        (0, False),  # rejeté
        (-2, False),  # rejeté
    ],
)
def test_transform_coherence_quantity_df(quantity, should_be_present):
    df = pd.DataFrame([{"quantity": quantity}])
    result = transform_coherence_quantity_df("test.csv", df)
    assert (not result.empty) == should_be_present


@pytest.mark.parametrize(
    "numero_commande, product_id, exists, should_be_present",
    [
        ("CMD-1", "P001", False, True),
        ("CMD-2", "P002", True, False),
    ],
)
@patch("scripts.transform_phase2.check_commande_already_exists")
def test_transform_coherence_historique_df_commande(
    mock_check, numero_commande, product_id, exists, should_be_present
):
    mock_check.return_value = exists
    df = pd.DataFrame([{"numero_commande": numero_commande, "product_id": product_id}])
    result = transform_coherence_historique_df("test.csv", df)
    assert (not result.empty) == should_be_present
