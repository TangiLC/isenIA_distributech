# 🧪 Projet ETL Python – Suivi des commandes revendeurs

## 🎓 Présentation

Ce projet est un **Proof of Concept (PoC)** académique développé dans le cadre du module _Extraction, Transformation, Chargement (ETL)_ de la formation **Développeur IA** ISEN / Simplon.co.

Il a pour but de concevoir un pipeline **ETL automatisé en Python**, permettant l'intégration des données de commandes revendeurs (au format CSV) et de stocks/production (via une base SQLite), dans une **base de données MySQL centralisée**. L'aboutissement du pipeline est la mise à jour de la base stock, avec création de fichiers csv pour le suivi des stocks par produits et par revendeur. Le tout est actuellement **sans interface graphique**, en interaction terminal uniquement.

Le développement de ce projet a suivi une méthodologie Agile, avec ticketing et feuille de route sur
[Notion](https://www.notion.so/ba8a83033c684aa798eb9e7c6e2e2ed6).

---

![Python 3.12](https://img.shields.io/badge/Python-3.12%2B-yellow?logo=python&logoColor=yellow)
![Pandas](https://img.shields.io/badge/Pandas-2.3-150458?logo=pandas&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.2-0A9EDC?logo=pytest&logoColor=white)
![Ubuntu 24](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=E95420)
![SQLite 3.4](https://img.shields.io/badge/SQLite-3.4-pink?logo=sqlite&logoColor=003B57)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-v3-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-V27-2496ED?logo=docker&logoColor=2496ED)
![VSCode](https://img.shields.io/badge/VSCode-1.10-007ACC?logo=visualstudiocode&logoColor=007ACC)

![tests](https://img.shields.io/badge/coverage-89%-green?logo=pytest&logoColor=white&style=for-the-badge)

## 🧾 Objectif pédagogique

- Concevoir une base SQL relationnelle orientée gestion logistique (revendeurs, produits, régions, commandes, stocks),
- Développer un pipeline ETL pour :
  - Extraire les données CSV & SQLite,
  - Valider et nettoyer les données (cohérence, format, doublons...),
  - Charger les données dans une base **MySQL conteneurisée**,
- Générer un rapport CSV de l’état des stocks à date,
- Automatiser le traitement dans une architecture modulaire.

---

## 🧑‍💻 Stack technique

| Outil / Techno          | Version / Remarques                         |
| ----------------------- | ------------------------------------------- |
| Python                  | ≥ 3.12                                      |
| Pandas                  | 2.3 Manipulation de données structurées     |
| mysql-connector         | 9.3 Bibliothèque d'interaction avec MySQL   |
| python-dotenv           | chargement des variables d'environnement    |
| pytest (et pytest-cov)  | Bibliothèques de test et couverture         |
| Docker / Docker Compose | Conteneurisation de la base MySQL + Adminer |
| MySQL                   | 8.0+ BDD relationnelle (Port 3307)          |
| Adminer                 | Interface web pour MySQL (Port 8081)        |
| SQLite                  | Base légère Stock source                    |
| CSV                     | Fichier Commandes des revendeur             |
| VSCode                  | IDE de développement local                  |

---

## ⚙️ Installation & mise en route

### 1. Pré-requis

- Python 3.12+
- Docker + Docker Compose installés
- `pip`, `venv` disponibles en ligne de commande

### 2. Clonage du dépôt

```bash
git clone https://github.com/TangiLC/isenIA_distributech.git
cd etl
```

Ce projet est réalisé en trinôme, les contributeurs sont :

_Carole_ <a href="https://github.com/Carole-N" target="_blank">
<img src="https://avatars.githubusercontent.com/Carole-N" width="50" height="50" style="border-radius: 50%;" alt="CaroleN" />
</a>
_Gosia_ <a href="https://github.com/go2375" target="_blank">
<img src="https://avatars.githubusercontent.com/go2375" width="50" height="50" style="border-radius: 50%;" alt="Gosia" />
</a>
_Tangi_ <a href="https://github.com/TangiLC" target="_blank">
<img src="https://avatars.githubusercontent.com/TangiLC" width="50" height="50" style="border-radius: 50%;" alt="TangiLC" />
</a>

### 3. Création du fichier d'environnement et de la base de données

Un fichier contenant les données d'environnement de votre BDD est nécessaire à la racine du projet.
Créer et personnalisez le fichier `.env` selon ce schéma ou copier/renommer le fichier `.env.template`:

```bash
BDD_HOST=votre-adresse-host (localhost)
BDD_PORT=votre-port-mysql (3307)
MYSQL_USER=votre-nom-user-mysql
MYSQL_PASSWORD=votre-mot-de-passe-mysql
MYSQL_DATABASE=votre-nom-de-bdd (distributech)
```

### 4. Création de l’environnement virtuel Python

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 6. Lancement de la base de données

Les fichiers `bdd/script.sql` et `bdd/populate_init.sql` permettent d'initialiser votre base de données.

Alternativement, Dans le dossier `bdd/`, un fichier docker-compose permet de conteneuriser une bdd :

```bash
docker-compose up -d

```

> 📌 La base **MySQL** sera alors accessible sur le port `3307`  
> 🖥 L'interface **Adminer** est disponible via [http://localhost:8081](http://localhost:8081)

Lancer les scripts d'initialisation depuis l'interface Adminer.

---

## 🧬 Pipeline ETL

-Schéma
![Schéma du pipeline ETL](schema_etl_pipe.png)

### 📤 Extract

- Chargement des **commandes revendeurs** depuis un ou plusieurs fichiers `.csv` au format :

```
numero_commande,commande_date,revendeur_id,region_id,product_id,quantity,unit_price
```

- Connexion à une base **SQLite** pour lire :
  - Liste des produits
  - Répartition des revendeurs par région
  - Stock actuel

### 🧹 Transform

- Validation des données (formats de date, types, cohérence produit/revendeur)
- Nettoyage des doublons
- Normalisation (majuscule/minuscule, encodage, etc.)

### 📥 Load

- Mise à jour de la base MySQL cible via `mysql-connector-python`
- Génération des fichiers `.csv` récapitulatif de l’état des stocks à date
- Déplacement des fichiers sources traités

---

## ✓✓ Tests unitaires (pytest)

Les bibliothèques _pytest_ et _pytest-cov_ est configurée avec pytest.ini et .coveragerc.
Les tests sont à lancer à la racine du projet avec la commande suivante :

```
pytest --cov=scripts --cov-report=term --cov-report=html:tests/htmlcov --cov-config=.coveragerc
```

Le coverage sera affiché dans le terminal, avec un objectif >80%.
Le rapport se trouve dans `/tests/htmlcov`. (page principale `index.html`)

---

## 🗃 Structure du projet

```
distributech/
├── etl.py                   # Script principal du pipeline (main)
├── scripts/
│   ├── extracts.py          # Scripts pour les étapes Extract
│   ├── transform_xx.py      # Scripts pour les étapes Transform
│   ├── loads.py             # Scripts pour les étapes Load
│   ├── generate_report.py   # Scripts pour la génération de l'état des Stocks
│   └─utils/                 # Scripts annexes (mise en forme, requêtes...)
├── bdd/
│   ├── script.sql           # Script de création des tables pour mySQL
│   ├── populate_init.sql    # Script d'alimentation initiale de la BDD (produits, régions)
│   └── docker-compose.yml   # Lancement base MySQL + Adminer en container
├── data/
│   ├── commandes_xxx.csv    # source CSV (Commandes)
│   ├── base_stock.sqlite    # Base SQLite (production/réapprovisionnement)
|   └──archived/             # Dossier archive des fichiers antérieurs
├── sql/
│   └── schema.sql           # Script de création des tables pour mySQL
├── tests/
│   └── test_xxxx.py         # Scripts de tests unitaires pour l'ensemble des fonctions
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier 😄
├── env.template             # template du .env à personnaliser
├── pytest.ini, .coveragerc  # Fichiers de configuration de l'outil pytest
└── .gitignore               # Liste des répertoires ou fichiers non suivis
```

---

## 📤 Données manipulées

- **Commandes** : `numero_commande`, `commande_date`, `revendeur_id`, `region_id`, `product_id`, `quantity`, `unit_price`
- **Stocks** : mouvements (entrées/sorties), calcul des niveaux à date
- **Revendeurs** : `revendeur_id`, `revendeur_name`, `region_id`
- **Régions** : `region_id`, `region_name`
- **Produits** : `product_id`, `product_name`, `cout_unitaire`

---

## ✅ Livrables attendus

- Scripts Python du pipeline ETL (`etl.py`) et annexes (`/scripts/`)
- Fichier SQL ([script.sql](./bdd/script.sql)) pour initialiser la base, et fichier de population ([populate_init.sql](./bdd/populate_init.sql))
- Fichier `.csv` généré de l’état des stocks à date dans un dossier `/exports`
- Documentation fonctionnelle (ce `README.md`)
- Cahier des charges ([fichier cdc.md](./cdc.md))

---

## 📜 Licence

Ce projet est sous licence **MIT** – voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📌 À venir

- Factorisation et sécurisation
- Tests de robustesse sur les différentes étapes ETL
- Affiner les vues BDD selon les exigences métier

---

**Bonne lecture !**
