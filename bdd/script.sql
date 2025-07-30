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
SELECT s.product_id, s.stock_date, p.product_name, s.quantity, 
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
LEFT JOIN revendeur r ON s.operator_id = r.revendeur_id; 
-- LEFT JOIN revendeur permet de ne pas perdre de données produits, même sans revendeur.


-- Une vue du stock final par revendeur

CREATE OR REPLACE VIEW vue_stock_final_revendeur AS
SELECT COALESCE(r.revendeur_name, 'Distributech') AS operateur,
    s.stock_date, s.product_id, p.product_name, s.quantity, 
    CASE WHEN s.operator_id IS NULL THEN s.movement
        ELSE -1 * s.movement END AS mouvement
    FROM stock s
    JOIN produit p ON s.product_id = p.product_id
    JOIN (
    SELECT product_id,operator_id, MAX(stock_date) AS last_date
    FROM stock
    GROUP BY product_id, operator_id
) latest
ON s.product_id = latest.product_id 
AND s.stock_date = latest.last_date 
AND (
        s.operator_id = latest.operator_id 
        OR (s.operator_id IS NULL AND latest.operator_id IS NULL)
    )
LEFT JOIN revendeur r ON s.operator_id = r.revendeur_id; 



CREATE OR REPLACE VIEW vue_historique_stock_par_revendeur AS
SELECT
    COALESCE(reg.region_name, 'Distributech') AS region,
    COALESCE(r.revendeur_name, 'Distributech') AS operateur,
    s0.product_id,
    p.product_name,
    COALESCE(s2.movement, 0) AS movement_2,
    COALESCE(s2.stock_date, '2020-01-01') AS date_2,
    COALESCE(s1.movement, 0) AS movement_1,
    COALESCE(s1.stock_date, '2020-01-01') AS date_1,
    s0.movement AS movement_0,
    s0.stock_date AS latest_date
FROM (
    -- Les 3 derniers enregistrements par produit/opérateur
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY product_id, COALESCE(operator_id, 0) ORDER BY stock_date DESC) AS rn
    FROM stock
) ranked
-- Stock le plus récent (rn = 1)
JOIN (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY product_id, COALESCE(operator_id, 0) ORDER BY stock_date DESC) AS rn
        FROM stock
    ) sub
    WHERE rn = 1
) s0 ON ranked.product_id = s0.product_id 
    AND COALESCE(ranked.operator_id, 0) = COALESCE(s0.operator_id, 0)
-- Stock précédent (rn = 2)
LEFT JOIN (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY product_id, COALESCE(operator_id, 0) ORDER BY stock_date DESC) AS rn
        FROM stock
    ) sub
    WHERE rn = 2
) s1 ON ranked.product_id = s1.product_id 
    AND COALESCE(ranked.operator_id, 0) = COALESCE(s1.operator_id, 0)
-- Stock d'avant (rn = 3)
LEFT JOIN (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY product_id, COALESCE(operator_id, 0) ORDER BY stock_date DESC) AS rn
        FROM stock
    ) sub
    WHERE rn = 3
) s2 ON ranked.product_id = s2.product_id 
    AND COALESCE(ranked.operator_id, 0) = COALESCE(s2.operator_id, 0)
-- Jointures avec les tables de référence
JOIN produit p ON s0.product_id = p.product_id
LEFT JOIN revendeur r ON s0.operator_id = r.revendeur_id
LEFT JOIN region reg ON r.region_id = reg.region_id
-- Filtrer pour ne garder qu'une ligne par produit/opérateur
WHERE ranked.rn = 1
ORDER BY region, s0.operator_id, s0.product_id;