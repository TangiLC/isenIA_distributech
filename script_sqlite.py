import sqlite3

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
    (3, "Auvergne–Rhône-Alpes"),
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
    (102, "Chargeur USB-C", 19.90),
    (103, "Enceinte Portable", 89.90),
    (104, "Batterie Externe", 24.90),
    (105, "Montre Connectée", 129.90),
    (106, "Webcam HD", 49.90),
    (107, "Hub USB 3.0", 34.90),
    (108, "Clavier sans fil", 44.90),
    (109, "Souris ergonomique", 39.90),
    (110, "Station d’accueil", 109.90),
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
