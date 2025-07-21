import sqlite3

# Ajout debut#
import pandas as pd

# Ajout fin#

sqlite_path = "./data/base_stock.sqlite"
conn = sqlite3.connect(sqlite_path)
cur = conn.cursor()

# Création des tables
cur.executescript(
    """
DROP TABLE IF EXISTS production;
DROP TABLE IF EXISTS revendeur;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS produit;
 
CREATE TABLE region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL
);
 
CREATE TABLE revendeur (
    revendeur_id INTEGER PRIMARY KEY,
    revendeur_name TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);
 
CREATE TABLE produit (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    cout_unitaire REAL NOT NULL
);
 
CREATE TABLE production (
    production_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    date_production TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES produit(product_id)
);
"""
)

# Insertion des régions
regions = [
    (1, "Île-de-France"),
    (2, "Occitanie"),
    (3, "Auvergne-Rhône-Alpes"),
    (4, "Bretagne"),
]
cur.executemany("INSERT INTO region VALUES (?, ?);", regions)

# Insertion des revendeurs
revendeurs = [
    (1, "TechExpress", 1),
    (2, "ElectroZone", 1),
    (3, "SudTech", 2),
    (4, "GadgetShop", 2),
    (5, "Connectik", 3),
    (6, "Domotik+", 3),
    (7, "BreizhTech", 4),
    (8, "SmartBretagne", 4),
    (9, "HighNord", 1),
    (10, "OuestConnect", 4),
]
cur.executemany("INSERT INTO revendeur VALUES (?, ?, ?);", revendeurs)

# Insertion des produits
produits = [
    (101, "Casque Bluetooth", 59.90),
    (102, "Chargeur USB-C", 19.90),
    (103, "Enceinte Portable", 89.90),
    (104, "Batterie Externe", 24.90),
    (105, "Montre Connectée", 129.90),
    (106, "Webcam HD", 49.90),
    (107, "Hub USB 3.0", 34.90),
    (108, "Clavier sans fil", 44.90),
    (109, "Souris ergonomique", 39.90),
    (110, "Station d'accueil", 109.90),
]
cur.executemany("INSERT INTO produit VALUES (?, ?, ?);", produits)

# Insertion de production (réapprovisionnement)
production = [
    (101, 50, "2025-07-01"),
    (102, 80, "2025-07-01"),
    (103, 40, "2025-07-02"),
    (104, 60, "2025-07-02"),
    (105, 20, "2025-07-03"),
    (106, 35, "2025-07-03"),
    (107, 25, "2025-07-04"),
    (108, 30, "2025-07-04"),
    (109, 45, "2025-07-05"),
    (110, 15, "2025-07-05"),
]
cur.executemany(
    "INSERT INTO production (product_id, quantity, date_production) VALUES (?, ?, ?);",
    production,
)

conn.commit()
conn.close()

sqlite_path

# Ajout debut : je lis csv
df = pd.read_csv("./data/commande_revendeur_tech_express.csv")
# Je vérifie import des données csv
print(df.head())
# Ajout fin#
# Ticket no.1

# Je définis les champs obligatoires en prenant les noms de colonnes comme champs obligatoires :
# df.columns : récupère tous les noms de colonnes dans le fichier CSV (la ligne d'en-tête)
# .tolist() : transforme ça en liste Python.

champs_obligatoires = df.columns.tolist()
print(champs_obligatoires)
# Je prépare une liste vide pour y stocker les lignes qui posent problème.
erreurs = []

# Je vérifie ligne par ligne notre csv:
# df.iterrows() permet de parcourir chaque ligne du CSV une par une.
# index = numéro de la ligne (commence à 0)
# ligne = données de cette ligne, sous forme de dictionnaire

for index, ligne in df.iterrows():
    # Pour chaque champ obligatoire, on regarde :
    # Est-ce que la cellule correspondante dans cette ligne est vide (NaN) ?
    # pd.isnull(...) retourne True si la valeur est absente ou nulle.
    champs_manquants = [
        champ for champ in champs_obligatoires if pd.isnull(ligne.get(champ))
    ]
    # On crée une liste champs_manquants avec tous les noms de colonnes qui sont manquants dans cette ligne.
    # Si la ligne est incomplète (il manque des champs) :
    # On ajoute un dictionnaire dans erreurs qui contient :
    # ligne: le numéro réel de la ligne dans le fichier CSV (on ajoute +2 car :
    # Python commence à 0
    # Et la première ligne est l’en-tête)
    # champs_manquants: liste des champs manquants
    # données: les données complètes de cette ligne

    if champs_manquants:
        erreurs.append(
            {
                "ligne": index + 2,  # +2 pour tenir compte de l'en-tête (ligne 1)
                "champs_manquants": champs_manquants,
                "données": ligne.to_dict(),
            }
        )

# Afficher les erreurs à l'écran : à vérifier plus tard comment le rendre plus précis
if erreurs:
    print("Lignes avec des champs manquants :")
    for err in erreurs:
        print(
            f"Ligne {err['ligne']} → Champs manquants : {', '.join(err['champs_manquants'])}"
        )
else:
    print("✅ Toutes les lignes sont valides.")
