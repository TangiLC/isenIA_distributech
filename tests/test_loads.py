import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from scripts.loads import (
    insert_commande_product,
    insert_production_product,
    update_stock_produit,
    load_commande_produit,
    load_production_produit,
)


@patch("scripts.loads.init_connection")
def test_insert_commande_product_success(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 42

    success = insert_commande_product(
        1,
        {
            "numero_commande": "CMD-20240101-001",
            "commande_date": "2024-01-01",
            "revendeur_id": 10,
            "product_id": 100,
            "quantity": 5,
        },
    )
    assert success is True
    assert mock_cursor.execute.call_count == 2


@patch("scripts.loads.init_connection")
def test_insert_production_product_success(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 21

    success = insert_production_product(
        2,
        {
            "production_id": "PROD001",
            "date_production": "2024-06-01",
            "product_id": 200,
            "quantity": 10,
        },
    )
    assert success is True
    assert mock_cursor.execute.call_count == 2


@patch("scripts.loads.init_connection")
def test_update_stock_produit_success(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (50,)  # stock précédent = 50

    stock_dict = {
        "stock_date": "2024-06-01",
        "product_id": 101,
        "movement": 10,
        "operator_id": 3,
    }

    success = update_stock_produit(stock_dict, 1)
    assert success is True
    mock_cursor.execute.assert_any_call(
        """SELECT quantity FROM stock WHERE product_id=%s
            ORDER BY stock_date DESC LIMIT 1;
        """,
        (101,),
    )
    mock_cursor.execute.assert_any_call(
        """INSERT INTO stock (stock_date,product_id,movement,quantity,operator_id)
        VALUES (%s,%s,%s,%s,%s)
        """,
        ("2024-06-01", 101, 10, 60, 3),
    )


@patch("scripts.loads.insert_commande_product", return_value=True)
@patch("scripts.loads.update_stock_produit")
def test_load_commande_produit(mock_update_stock, mock_insert_commande):
    data = pd.DataFrame(
        [
            {
                "numero_commande": "CMD-20240101-001",
                "commande_date": "2024-01-01",
                "revendeur_id": 10,
                "product_id": 100,
                "quantity": 5,
            }
        ]
    )
    load_commande_produit(["fichier.csv", 1], data)
    mock_insert_commande.assert_called_once()
    mock_update_stock.assert_called_once_with(
        {
            "stock_date": "2024-01-01",
            "product_id": 100,
            "movement": 5,
            "operator_id": 10,
        },
        -1,
    )


@patch("scripts.loads.insert_production_product", return_value=True)
@patch("scripts.loads.update_stock_produit")
def test_load_production_produit(mock_update_stock, mock_insert_prod):
    data = pd.DataFrame(
        [
            {
                "production_id": "PROD001",
                "date_production": "2024-06-01",
                "product_id": 200,
                "quantity": 10,
            }
        ]
    )
    load_production_produit(["fichier.csv", 2], data)
    mock_insert_prod.assert_called_once()
    mock_update_stock.assert_called_once_with(
        {
            "stock_date": "2024-06-01",
            "product_id": 200,
            "movement": 10,
            "operator_id": None,
        },
        1,
    )
