import pytest
import sys
import time
from scripts.utils.affichage import (
    affiche_outcome,
    affiche_success_ligne,
    affiche_titre,
    afficher_tableau_horizontal,
)

import re


def strip_ansi(text):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


def test_affiche_titre(capfd, monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda _: None)

    titre = ("A" * 40).ljust(110)
    affiche_titre(titre)

    out, err = capfd.readouterr()

    assert len(out) == 110 + 15
    # ajout de 15 caractères Ansi (9 prefix, 6 suffix) pour le style
    assert out.startswith("\033[30;44m AAA")
    assert out.endswith("   \033[0m\n")
    assert err == ""


@pytest.mark.parametrize(
    "ref, transform_type, before, after, expected_text",
    [
        (  # référence classique
            {"name": "test1", "ligne": 42, "champ": "test"},
            "e type test",
            "73",
            "37",
            "37",
        ),
        (  # référence avec types exotiques
            {"name": 3.14159, "ligne": "B", "champ": 33},
            "e type test",
            666,
            999,
            "999",
        ),
    ],
)
def test_affiche_success_line(capfd, ref, transform_type, before, after, expected_text):
    affiche_success_ligne(ref, transform_type, before, after)
    out, err = capfd.readouterr()
    out_clean = strip_ansi(out)

    expected_prefix = (
        f"✅ [{str(ref['name']).upper()}]>Ligne{ref['ligne']}|{ref['champ']}"
    )
    assert expected_prefix in out_clean
    assert f"Correction d{transform_type}" in out_clean
    assert expected_text in out_clean
    assert err == ""


@pytest.mark.parametrize(
    "name, ok_message, erreurs, expected_lines",
    [
        (  # Cas succès
            "fichier1",
            "Aucune erreur détectée.",
            [],
            ["[FICHIER1]", "✅ Aucune erreur détectée."],
        ),
        (  # Cas avec erreur sur la longueur
            "error_file",
            "",
            [
                {
                    "ligne": 12,
                    "erreur": "test erreur",
                    "data": ["abc", "def"],
                    "champs_erreurs": ["champ1", "champ2"],
                }
            ],
            [
                "[ERROR_FILE]",
                "⚠️ Lignes avec problèmes détectées",
                "Ligne 12 → test erreur\n",
            ],
        ),
    ],
)
def test_affiche_outcome_param(
    capfd, monkeypatch, name, ok_message, erreurs, expected_lines
):
    monkeypatch.setattr(
        "scripts.utils.affichage.afficher_tableau_horizontal",
        lambda data, champs: print(f"[TABLE] {data} / {champs}"),
    )

    affiche_outcome(name, ok_message, erreurs)

    out, err = capfd.readouterr()
    clean = strip_ansi(out)

    for expected in expected_lines:
        assert expected in clean

    assert err == ""


@pytest.mark.parametrize(
    "d, cles_invalides, expected_parts",
    [
        # 1. Tableau vide
        ({}, [], ["|  |", "|  |"]),
        # 2. Tableau simple
        ({"nom": "Toto", "age": 30}, [], ["nom", "Toto", "age", "30"]),
        # 3. Pas une instance dictionnaire
        ("not dict", None, ["not dict"]),
        (  # 4. Clé ou valeur trop longue
            {"nom_super_long_qui_dépasse": "val_super_longue"},
            [],
            ["nom_super_long_qui_dépasse", "val_super_longue"],
        ),
        (  # 5. Clé marquée invalide
            {"nom": "Durand", "ville": "Paris"},
            ["ville"],
            ["nom", "Durand", "\033[30;41mville", "\033[30;41mParis"],
        ),
    ],
)
def test_afficher_tableau_horizontal(capfd, d, cles_invalides, expected_parts):
    afficher_tableau_horizontal(d, cles_invalides)
    out, _ = capfd.readouterr()

    for fragment in expected_parts:
        assert fragment in out or strip_ansi(out).find(fragment) != -1
