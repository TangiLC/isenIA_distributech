import pytest
from unittest.mock import patch, MagicMock, mock_open, call
from datetime import datetime
import mysql.connector
import os


from scripts.generate_report import extraire_stock


@patch("scripts.generate_report.mysql.connector.connect")
@patch("scripts.generate_report.open", new_callable=mock_open)
@patch("scripts.generate_report.os.makedirs")
@patch("scripts.generate_report.print")
def test_extraire_stock_success(mock_print, mock_makedirs, mock_openfile, mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "Produit A", 50)]
    mock_cursor.description = [("id",), ("nom",), ("stock",)]
    mock_connect.return_value.cursor.return_value = mock_cursor

    extraire_stock()

    # On vérifie que la connexion et la requête ont bien eu lieu
    assert mock_cursor.execute.call_count == 2  # une fois pour chaque vue
    assert mock_openfile.call_count == 2  # un fichier CSV par vue
    assert mock_print.call_args_list[0][0][0].startswith(
        "✅ Le fichier CSV du Stock Final Produit"
    )


@patch(
    "scripts.generate_report.mysql.connector.connect",
    side_effect=mysql.connector.Error("Connexion échouée"),
)
@patch("scripts.generate_report.print")
def test_extraire_stock_mysql_fail(mock_print, mock_connect):
    result = extraire_stock()
    assert result is None
    assert "❌ Échec de l'extraction des données" in mock_print.call_args[0][0]
