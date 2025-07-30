import pytest
import pandas as pd
from unittest.mock import patch

from scripts.transform_phase1 import transform_data_vide_df, transform_type_df


@pytest.mark.parametrize(
    "input_data, expected_output, expected_invalid_rows",
    [
        # Cas 1 : ligne complète, rien à corriger
        ([{"col1": "A", "col2": "B"}], [{"col1": "A", "col2": "B"}], 0),
        # Cas 2 : champ vide => remplace par "*"
        ([{"col1": None, "col2": "B"}], [{"col1": "*", "col2": "B"}], 1),
        # Cas 3 : ligne trop courte (suppression)
        ([{"col1": "A", "col2": "B"}, {"col1": "C"}], [{"col1": "A", "col2": "B"}], 1),
    ],
)
@patch("scripts.transform_phase1.affiche_outcome")
def test_transform_data_vide_df(
    mock_outcome, input_data, expected_output, expected_invalid_rows
):
    df_input = pd.DataFrame(input_data)
    df_result = transform_data_vide_df("test", df_input)

    assert df_result.to_dict(orient="records") == expected_output
    # Vérifie que `affiche_outcome` a été appelée avec le bon nombre d'erreurs
    if expected_invalid_rows > 0:
        args, _ = mock_outcome.call_args
        erreurs = args[2]
        assert len(erreurs) == expected_invalid_rows
    else:
        mock_outcome.assert_called_once()


@pytest.mark.parametrize(
    "input_data, expected_data",
    [
        (  # Cas 1 : toutes données correctes
            [
                {
                    "production_id": "123",
                    "cout_unitaire": "12.5",
                    "commande_date": "2023-01-01",
                    "product_name": "Produit X",
                    "numero_commande": "CMD-20230101-001",
                }
            ],
            [
                {
                    "production_id": 123,
                    "cout_unitaire": 12.5,
                    "commande_date": "2023-01-01",
                    "product_name": "Produit X",
                    "numero_commande": "CMD-20230101-001",
                }
            ],
        ),
        (  # Cas 2 : champ entier non convertible
            [
                {
                    "production_id": "abc",
                    "cout_unitaire": "12.5",
                    "commande_date": "01/01/2023",
                    "product_name": "Produit",
                    "numero_commande": "CMD20230101.001",
                }
            ],
            [
                {
                    "production_id": "abc",  # erreur
                    "cout_unitaire": 12.5,
                    "commande_date": "2023-01-01",  # corrigée
                    "product_name": "Produit",
                    "numero_commande": "CMD-20230101-001",  # corrigé
                }
            ],
        ),
        (  # Cas 3 : texte sans lettres → remplacé par "*"
            [
                {
                    "production_id": "456",
                    "cout_unitaire": "10",
                    "commande_date": "2023-02-01",
                    "product_name": "1234",  # pas valide
                    "numero_commande": "CMD-20230201-002",
                }
            ],
            [
                {
                    "production_id": 456,
                    "cout_unitaire": 10.0,
                    "commande_date": "2023-02-01",
                    "product_name": "*",  # remplacé
                    "numero_commande": "CMD-20230201-002",
                }
            ],
        ),
    ],
)
@patch("scripts.transform_phase1.affiche_success_ligne")
@patch("scripts.transform_phase1.affiche_outcome")
@patch("scripts.transform_phase1.corriger_ocr", side_effect=lambda val, ref: val)
@patch(
    "scripts.transform_phase1.corriger_date",
    side_effect=lambda val: (
        ("2023-01-01", False) if val == "01/01/2023" else (val, False)
    ),
)
@patch(
    "scripts.transform_phase1.nettoyer_texte", side_effect=lambda val, ref: (val, False)
)
@patch(
    "scripts.transform_phase1.nettoyer_typographie",
    side_effect=lambda val, ref: (val, False),
)
@patch(
    "scripts.transform_phase1.nettoyer_numero_commande",
    side_effect=lambda val, ref: (
        ("CMD-20230101-001", False) if val == "CMD20230101.001" else (val, False)
    ),
)
def test_transform_type_df(
    mock_numero,
    mock_typo,
    mock_texte,
    mock_date,
    mock_ocr,
    mock_outcome,
    mock_success,
    input_data,
    expected_data,
):
    df_input = pd.DataFrame(input_data)
    df_result = transform_type_df("test", df_input)
    assert df_result.to_dict(orient="records") == expected_data
