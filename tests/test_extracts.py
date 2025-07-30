import pytest
import pandas as pd
import os
import sqlite3
from unittest.mock import patch, MagicMock
from pathlib import Path

from scripts.extracts import (
    get_list_of_files,
    save_to_logs,
    extract_csv_to_df,
    extract_sqlite_to_df,
    anonymize_name,
    move_file_to_target,
)


def test_get_list_of_files(tmp_path):
    # Création des fichiers de test
    (tmp_path / "fichier.csv").write_text("col1,col2\nval1,val2")
    (tmp_path / "base.sqlite").write_text("fichier vide mais extension bonne")
    (tmp_path / "autre.txt").write_text("non pris en compte")

    result = get_list_of_files(str(tmp_path))
    assert "csv" in result
    assert "sqlite" in result
    assert "txt" not in result
    assert result["csv"] == ["fichier.csv"]


@patch("scripts.extracts.print")
def test_save_to_logs(mock_print, tmp_path):
    df = pd.DataFrame({"a": [1], "b": [2]})
    result_path = save_to_logs(df, "testfile", logs_dir=str(tmp_path))

    assert Path(result_path).exists()
    assert result_path.startswith(str(tmp_path))
    assert result_path.endswith(".csv")


@patch("scripts.extracts.insert_into_bddlogs", return_value=123)
def test_extract_csv_to_df(mock_insert, tmp_path):
    test_csv = tmp_path / "test_commande.csv"
    test_csv.write_text("col1,col2\nval1,val2")

    name, df = extract_csv_to_df(str(test_csv), logs_dir=str(tmp_path))

    assert name[0] == "test_commande"
    assert name[1] == 123
    assert not df.empty


@patch("scripts.extracts.insert_into_bddlogs", return_value=456)
def test_extract_sqlite_to_df(mock_insert, tmp_path):
    # Crée une base SQLite avec une table "production"
    db_path = tmp_path / "base.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE production (id INTEGER, qty INTEGER);")
    conn.execute("INSERT INTO production VALUES (1, 10);")
    conn.commit()
    conn.close()

    result = extract_sqlite_to_df(str(db_path), logs_dir=str(tmp_path))

    assert isinstance(result, list)
    assert result[0][0][0] == "production"
    assert isinstance(result[0][1], pd.DataFrame)


@pytest.mark.parametrize(
    "id, expected",
    [
        (1, "revendeur_001"),
        (12, "revendeur_012"),
        (123, "revendeur_123"),
    ],
)
def test_anonymize_name(id, expected):
    assert anonymize_name(id) == expected


def test_move_file_to_target(tmp_path):
    source_file = tmp_path / "fichier.csv"
    source_file.write_text("test")

    target_dir = tmp_path / "archive"
    move_file_to_target(str(source_file), str(target_dir))

    moved_file = target_dir / "fichier.csv"
    assert moved_file.exists()
    assert not source_file.exists()
