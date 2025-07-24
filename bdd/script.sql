CREATE DATABASE IF NOT EXISTS distributech;
USE distributech;

CREATE TABLE IF NOT EXISTS region (
    region_id INT PRIMARY KEY,
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
    --product_id INTEGER NOT NULL,
    --quantity INTEGER NOT NULL,
    date_production TEXT NOT NULL, 
    --FOREIGN KEY (product_id) REFERENCES produit(product_id)
);

CREATE TABLE produit_production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    production_id  INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (production_id) REFERENCES production(production_id),
    FOREIGN KEY (product_id) REFERENCES produit(product_id)    
);

CREATE TABLE commande (
    commande_id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_commande VARCHAR(16) NOT NULL,
    commande_date DATE NOT NULL,
    revendeur_id INT NOT NULL,
    --product_id INT NOT NULL,
    --quantity INT NOT NULL,
    --cout_unitaire REAL NOT NULL,
    FOREIGN KEY (revendeur_id) REFERENCES revendeur(revendeur_id)
);

CREATE TABLE commande_produit (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    product_id INT NOT NULL,
    commande_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES produit(product_id),
    FOREIGN KEY (commande_id) REFERENCES commande(commande_id)
);

CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_date DATE,
    product_id INT NOT NULL,
    quantity INT, -- Pas NOT NULL parce que le flux de stock peut être 0.
    FOREIGN KEY (product_id) REFERENCES produit(product_id)
);

CREATE TABLE log_commande_brut (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date DATETIME,
    nom text NOT NULL
);

CREATE TABLE log_production_brut (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date DATETIME,
    nom text NOT NULL
);



