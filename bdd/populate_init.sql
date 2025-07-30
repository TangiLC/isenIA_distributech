-- Insertion des régions
INSERT INTO region (region_id, region_name) VALUES
    (1, 'Île-de-France'),
    (2, 'Occitanie'),
    (3, 'Auvergne-Rhône-Alpes'),
    (4, 'Bretagne');

-- Insertion des revendeurs
INSERT INTO revendeur (revendeur_id, revendeur_name, region_id) VALUES
    (1, 'TechExpress', 1),
    (2, 'ElectroZone', 1),
    (3, 'SudTech', 2),
    (4, 'GadgetShop', 2),
    (5, 'Connectik', 3),
    (6, 'Domotik+', 3),
    (7, 'BreizhTech', 4),
    (8, 'SmartBretagne', 4),
    (9, 'HighNord', 1),
    (10, 'OuestConnect', 4);

-- Insertion des produits
INSERT INTO produit (product_id, product_name, cout_unitaire) VALUES
    (101, 'Casque Bluetooth', 59.90),
    (102, 'Chargeur USB-C', 19.90),
    (103, 'Enceinte Portable', 89.90),
    (104, 'Batterie Externe', 24.90),
    (105, 'Montre Connectée', 129.90),
    (106, 'Webcam HD', 49.90),
    (107, 'Hub USB 3.0', 34.90),
    (108, 'Clavier sans fil', 44.90),
    (109, 'Souris ergonomique', 39.90),
    (110, 'Station d’accueil', 109.90);

