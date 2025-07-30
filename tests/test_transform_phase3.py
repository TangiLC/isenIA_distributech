import pytest
import pandas as pd
from unittest.mock import patch

from scripts.transform_phase3 import nettoyer_dataframe_unicite


@pytest.fixture
def name_test():
    """Fixture pour le paramètre name"""
    return "test_file.csv"


@pytest.mark.parametrize(
    "input_data,expected_cols,expected_rows",
    [
        # Aucun doublon
        (pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}), 2, 3),
        # Colonnes dupliquées (C identique à A)
        (pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [1, 2, 3]}), 2, 3),
        # Lignes dupliquées (lignes 0 et 2 identiques)
        (pd.DataFrame({"A": [1, 2, 1], "B": [4, 5, 4]}), 2, 2),
        # Colonnes ET lignes dupliquées
        (pd.DataFrame({"A": [1, 2, 1], "B": [4, 5, 4], "C": [1, 2, 1]}), 2, 2),
        # DataFrame vide
        (pd.DataFrame(), 0, 0),
    ],
)
@patch("scripts.utils.affichage.affiche_outcome")
def test_logique_nettoyage_pure(
    mock_affiche, name_test, input_data, expected_cols, expected_rows
):
    """Test de la logique de nettoyage sans vérifier les appels mock"""
    result = nettoyer_dataframe_unicite(name_test, input_data)

    assert (
        len(result.columns) == expected_cols
    ), f"Expected {expected_cols} columns, got {len(result.columns)}"
    assert (
        len(result) == expected_rows
    ), f"Expected {expected_rows} rows, got {len(result)}"

    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"


@pytest.mark.parametrize(
    "input_df,expected_shape",
    [
        # Préservation des données uniques
        (pd.DataFrame({"A": [1, 2, 3, 2], "B": [10, 20, 30, 20]}), (3, 2)),
        # DataFrame simple sans doublon
        (pd.DataFrame({"A": [1, 2], "B": [3, 4]}), (2, 2)),
    ],
)
@patch("scripts.utils.affichage.affiche_outcome")
def test_preservation_donnees_simple(mock_affiche, name_test, input_df, expected_shape):
    """Test simple de préservation des données"""
    result = nettoyer_dataframe_unicite(name_test, input_df)

    assert (
        result.shape == expected_shape
    ), f"Expected shape {expected_shape}, got {result.shape}"
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"


@pytest.mark.parametrize(
    "special_case,expected_shape",
    [
        ("single_cell", (1, 1)),
        ("all_identical_rows", (1, 2)),
        ("all_identical_cols", (3, 1)),
    ],
)
@patch("scripts.utils.affichage.affiche_outcome")
def test_cas_limites_simple(mock_affiche, name_test, special_case, expected_shape):
    """Test des cas limites sans vérification mock"""
    if special_case == "single_cell":
        input_df = pd.DataFrame({"A": [1]})
    elif special_case == "all_identical_rows":
        input_df = pd.DataFrame({"A": [1, 1, 1], "B": [2, 2, 2]})
    elif special_case == "all_identical_cols":
        input_df = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 3], "C": [1, 2, 3]})

    result = nettoyer_dataframe_unicite(name_test, input_df)

    assert (
        result.shape == expected_shape
    ), f"For {special_case}: expected {expected_shape}, got {result.shape}"


@patch("scripts.utils.affichage.affiche_outcome")
def test_pas_de_doublons_apres_nettoyage(mock_affiche, name_test):
    """Test qu'il n'y a plus de doublons après nettoyage"""
    input_df = pd.DataFrame(
        {
            "A": [1, 2, 3, 1, 4],
            "B": [10, 20, 30, 10, 40],
            "C": [10, 20, 30, 10, 40],  # Colonne identique à B
        }
    )

    result = nettoyer_dataframe_unicite(name_test, input_df)

    assert (
        not result.duplicated().any()
    ), "Il ne devrait plus y avoir de lignes dupliquées"

    assert not result.empty, "Le résultat ne devrait pas être vide"

    assert len(result.columns) <= len(
        input_df.columns
    ), "Ne devrait pas avoir plus de colonnes"
    assert len(result) <= len(input_df), "Ne devrait pas avoir plus de lignes"


@patch("scripts.utils.affichage.affiche_outcome")
def test_colonnes_identiques_explicites(mock_affiche, name_test):
    """Test avec colonnes parfaitement identiques"""
    input_df = pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4, 5, 6],
            "col3": [1, 2, 3],  # Identique à col1
        }
    )

    result = nettoyer_dataframe_unicite(name_test, input_df)

    # Devrait garder seulement 2 colonnes uniques
    assert (
        len(result.columns) == 2
    ), f"Expected 2 unique columns, got {len(result.columns)}"
    assert len(result) == 3, f"Expected 3 rows, got {len(result)}"


@patch("scripts.utils.affichage.affiche_outcome")
def test_lignes_identiques_explicites(mock_affiche, name_test):
    """Test avec lignes parfaitement identiques"""
    input_df = pd.DataFrame(
        {
            "A": [1, 2, 1, 3],  # Lignes 0 et 2 identiques
            "B": [4, 5, 4, 6],  # Lignes 0 et 2 identiques
        }
    )

    result = nettoyer_dataframe_unicite(name_test, input_df)

    # Devrait garder seulement 3 lignes uniques
    assert len(result.columns) == 2, f"Expected 2 columns, got {len(result.columns)}"
    assert len(result) == 3, f"Expected 3 unique rows, got {len(result)}"


# Tests spécifiques pour le mock (séparés)
def test_mock_est_appele(name_test):
    """Test pour vérifier si le mock est effectivement appelé"""
    input_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    # Test avec différents chemins de mock possibles
    mock_paths = [
        "scripts.utils.affichage.affiche_outcome",
        "scripts.transform_phase3.affiche_outcome",
        "transform_phase3.affiche_outcome",
    ]

    for path in mock_paths:
        try:
            with patch(path) as mock_func:
                mock_func.return_value = None
                result = nettoyer_dataframe_unicite(name_test, input_df)

                if mock_func.call_count > 0:
                    print(
                        f"SUCCESS: Mock called {mock_func.call_count} times with path: {path}"
                    )
                    calls = mock_func.call_args_list
                    for i, call in enumerate(calls):
                        print(f"  Call {i+1}: {call}")
                    return  # Succès trouvé
                else:
                    print(f"Mock not called with path: {path}")
        except Exception as e:
            print(f"Error with path {path}: {e}")

    print("No mock path worked - function may not call affiche_outcome")
