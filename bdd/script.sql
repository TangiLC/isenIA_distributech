CREATE DATABASE IF NOT EXISTS distributech;
USE distributech;

CREATE TABLE IF NOT EXISTS region (
    region_id INT PRIMARY KEY,
    region_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS revendeur (
    revendeur_id INTEGER PRIMARY KEY,
    revendeur_name TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);

CREATE TABLE IF NOT EXISTS produit (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    cout_unitaire REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS log_commande_brut (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    log_date DATETIME,
    nom_fichier TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS log_production_brut (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    log_date DATETIME,
    nom_fichier TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS production (
    production_id INTEGER AUTO_INCREMENT PRIMARY KEY ,
    log_id INTEGER,
    FOREIGN KEY (log_id) REFERENCES log_production_brut(id),
    date_production DATE
);

CREATE TABLE IF NOT EXISTS produit_production (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    production_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (production_id) REFERENCES production(production_id),
    FOREIGN KEY (product_id) REFERENCES produit(product_id)
);

CREATE TABLE IF NOT EXISTS commande (
    commande_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    numero_commande VARCHAR(16),
    commande_date DATE,
    revendeur_id INT NOT NULL,
    log_id INTEGER,
    FOREIGN KEY (log_id) REFERENCES log_commande_brut(id),
    FOREIGN KEY (revendeur_id) REFERENCES revendeur(revendeur_id)
);

CREATE TABLE IF NOT EXISTS commande_produit (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    commande_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES produit(product_id),
    FOREIGN KEY (commande_id) REFERENCES commande(commande_id)
);

CREATE TABLE IF NOT EXISTS stock (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    stock_date DATE,
    product_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES produit(product_id)
);


