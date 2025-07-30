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
    production_ref INTEGER,
    log_id INTEGER,
    FOREIGN KEY (log_id) REFERENCES log_production_brut(id),
    date_production DATE
);

CREATE TABLE IF NOT EXISTS production_produit (
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
    movement INT NOT NULL,
    operator_id INT,
    FOREIGN KEY (operator_id) REFERENCES revendeur(revendeur_id),
    FOREIGN KEY (product_id) REFERENCES produit(product_id)
);

-- INDEXES pour optimiser les requêtes
CREATE INDEX idx_revendeur_region ON revendeur(region_id);
CREATE INDEX idx_production_log ON production(log_id);
CREATE INDEX idx_commande_log ON commande(log_id);
CREATE INDEX idx_commande_revendeur ON commande(revendeur_id);
CREATE INDEX idx_production_produit_pid ON production_produit(production_id);
CREATE INDEX idx_production_produit_produit ON production_produit(product_id);
CREATE INDEX idx_commande_produit_commande ON commande_produit(commande_id);
CREATE INDEX idx_commande_produit_produit ON commande_produit(product_id);
CREATE INDEX idx_stock_product ON stock(product_id);
CREATE INDEX idx_production_date ON production(date_production);
CREATE INDEX idx_commande_date ON commande(commande_date);
CREATE INDEX idx_stock_date ON stock(stock_date);

---- CREATION VIEW : une vue du stock final par produit et une vue du stock final par revendeur
-- Une vue du stock final par produit

CREATE OR REPLACE VIEW vue_stock_final_produit AS
SELECT s.stock_date, s.product_id, p.product_name, s.quantity, 
    COALESCE(r.revendeur_name, 'Distributech') AS operateur,
    CASE WHEN s.operator_id IS NULL THEN s.movement
        ELSE -1 * s.movement END AS mouvement
    FROM stock s
    JOIN produit p ON s.product_id = p.product_id
    JOIN (
    SELECT product_id, MAX(stock_date) AS last_date
    FROM stock
    GROUP BY product_id
) latest
ON s.product_id = latest.product_id AND s.stock_date = latest.last_date
LEFT JOIN revendeur r ON s.operator_id = r.revendeur_id; -- LEFT JOIN revendeur permet de ne pas perdre de données produits, même sans revendeur.

-- Une vue du stock final par revendeur

CREATE OR REPLACE VIEW vue_stock_final_revendeur AS
SELECT s.stock_date, s.product_id, p.product_name, s.quantity, 
    COALESCE(r.revendeur_name, 'Distributech') AS operateur,
    CASE WHEN s.operator_id IS NULL THEN s.movement
        ELSE -1 * s.movement END AS mouvement
    FROM stock s
    JOIN produit p ON s.product_id = p.product_id
    JOIN (
    SELECT product_id, MAX(stock_date) AS last_date
    FROM stock
    GROUP BY product_id, operator_id
) latest
ON s.product_id = latest.product_id AND s.stock_date = latest.last_date AND s.operateur <=> latest.operateur  -- <=> signifie en MySQL égalité NULL-safe et permet que les lignes où operator_id est NULL soient correctement appariées dans la jointure.
LEFT JOIN revendeur r ON s.operator_id = r.revendeur_id; --  LEFT JOIN revendeur permets d'inclure aussi les stocks sans revendeur (par ex. gérés directement en futur par Distributech)