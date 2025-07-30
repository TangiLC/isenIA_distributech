import pytest
from unittest.mock import patch
from scripts.utils.utils import (
    corriger_ocr,
    nettoyer_texte,
    nettoyer_typographie,
    corriger_date,
    nettoyer_numero_commande,
)


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("OQZ", "002"),
        ("SlG", "516"),
        ("123", "123"),
        ("", ""),
        (None, None),
    ],
)
@patch("scripts.utils.utils.affiche_success_ligne")
def test_corriger_ocr(mock_affiche, input_str, expected):
    ref = {"name": "test", "ligne": 1, "champ": "val"}
    result = corriger_ocr(input_str, ref)
    assert result == expected


@pytest.mark.parametrize(
    "texte, expected_result, expected_error",
    [
        ("  test \n", "test", False),
        ("\n  hello\r", "hello", False),
        ("ok", "ok", False),
        (None, "*", True),
    ],
)
@patch("scripts.utils.utils.affiche_success_ligne")
def test_nettoyer_texte(mock_affiche, texte, expected_result, expected_error):
    ref = {"name": "test", "ligne": 1, "champ": "texte"}
    result, error = nettoyer_texte(texte, ref)
    assert result == expected_result
    assert error == expected_error


@pytest.mark.parametrize(
    "texte, expected_result",
    [
        ("«Bonjour»", '"Bonjour"'),
        ("C’est l’été — enfin", "C'est l'été - enfin"),
        ("Test", "Test"),
    ],
)
@patch("scripts.utils.utils.affiche_success_ligne")
def test_nettoyer_typographie(mock_affiche, texte, expected_result):
    ref = {"name": "test", "ligne": 1, "champ": "texte"}
    result, error = nettoyer_typographie(texte, ref)
    assert result == expected_result
    assert error is False


@pytest.mark.parametrize(
    "date_str, expected, is_error",
    [
        ("2023_01_15", "2023-01-15", False),
        ("15/01/2023", "2023-01-15", False),
        ("20230115", "2023-01-15", False),
        ("31-12-2023", "2023-12-31", False),
        ("invalid", "*", True),
        (None, "*", True),
    ],
)
def test_corriger_date(date_str, expected, is_error):
    result, error = corriger_date(date_str)
    assert result == expected
    assert error == is_error


@pytest.mark.parametrize(
    "numero, expected_result, is_error",
    [
        (" CMD_20240101.001 ", "CMD-20240101-001", False),
        ("CMD20240101-001", "CMD20240101-001", True),
        ("CMD-20241301-001", "CMD-20241301-001", True),  # date M>12
        ("CMD--20240101--001", "CMD-20240101-001", False),
        ("CMD-20240101-001", "CMD-20240101-001", False),
    ],
)
@patch("scripts.utils.utils.affiche_success_ligne")
def test_nettoyer_numero_commande(mock_affiche, numero, expected_result, is_error):
    ref = {"name": "test", "ligne": 1, "champ": "numero_commande"}
    result, error = nettoyer_numero_commande(numero, ref)
    assert result == expected_result
    assert error == is_error
