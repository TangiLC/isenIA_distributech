# 🧪 Projet ETL Python – Suivi des commandes revendeurs

## 🎓 Présentation

Ce projet est un **Proof of Concept (PoC)** académique développé dans le cadre du module *Extraction, Transformation, Chargement (ETL)* de la formation **Développeur IA** ISEN / Simplon.co.

Il a pour but de concevoir un pipeline **ETL automatisé en Python**, permettant l'intégration des données de commandes revendeurs (au format CSV) et de stocks/production (via une base SQLite), dans une **base de données MySQL centralisée**. Le tout est actuellement **sans interface graphique**, en interaction terminale uniquement.

Le développement de ce projet a suivi une méthodologie Agile, avec ticketing et feuille de route sur
[Notion](https://www.notion.so/ba8a83033c684aa798eb9e7c6e2e2ed6).

---
![Python 3.12](https://img.shields.io/badge/Python-3.12%2B-yellow?logo=python&logoColor=white)
![Ubuntu 24](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)
![SQLite 3.4](https://img.shields.io/badge/SQLite-3.4-pink?logo=sqlite&logoColor=003B57)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3-150458?logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-V27-2496ED?logo=docker&logoColor=white)
![VSCode](https://img.shields.io/badge/VSCode-1.10-007ACC?logo=visualstudiocode&logoColor=white)


## 🧾 Objectif pédagogique

- Concevoir une base SQL relationnelle orientée gestion logistique (revendeurs, produits, régions, commandes, stocks),
- Développer un pipeline ETL pour :
  - Extraire les données CSV & SQLite,
  - Valider et nettoyer les données (cohérence, format, doublons),
  - Charger les données dans une base **MySQL conteneurisée**,
- Générer un rapport CSV de l’état des stocks à date,
- Automatiser le traitement dans une architecture modulaire.

---

## 🧑‍💻 Stack technique

| Outil / Techno      | Version / Remarques                  |
|---------------------|--------------------------------------|
| Python              | ≥ 3.12                               |
| Docker / Docker Compose | Conteneurisation de la base MySQL + Adminer |
| MySQL               | 8.0+ – Port 3307                     |
| Adminer             | Interface DB web – Port 8081         |
| SQLite              | Stock source                         |
| CSV                 | Commandes des revendeurs             |
| VSCode              | Développement local                  |

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

*Carole* <a href="https://github.com/Carole-N" target="_blank">
  <img src="https://avatars.githubusercontent.com/Carole-N" width="50" height="50" style="border-radius: 50%;" alt="CaroleN" />
</a>
*Gosia* <a href="https://github.com/go2375" target="_blank">
  <img src="https://avatars.githubusercontent.com/go2375" width="50" height="50" style="border-radius: 50%;" alt="Gosia" />
</a>
*Tangi* <a href="https://github.com/TangiLC" target="_blank">
  <img src="https://avatars.githubusercontent.com/TangiLC" width="50" height="50" style="border-radius: 50%;" alt="TangiLC" />
</a>


### 3. Création de l’environnement virtuel Python

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancement de la base de données

Dans le dossier `bdd/`, lancer :

```bash
docker-compose up -d
```

> 📌 La base **MySQL** sera accessible sur le port `3307`  
> 🖥 L'interface **Adminer** est disponible via [http://localhost:8081](http://localhost:8081)

---

## 🧬 Pipeline ETL

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
- Génération d’un fichier `.csv` récapitulatif de l’état des stocks à date

---

## 🗃 Structure du projet

```
etl-revendeurs/
├── etl.py                   # Script principal du pipeline (main)
├── /scripts/
│   ├── extracts.py          # Scripts pour l'étape Extract
│   ├── transforms.py        # Scripts pour l'étape Transform
│   └── loads.py             # Scripts pour l'étape Load
├── /bdd/
│   └── docker-compose.yml   # Lancement base MySQL + Adminer
├── /data/
│   ├── commandes_X.csv      # Commandes hebdo (source CSV)
│   └── stocks.sqlite        # Base SQLite (stock de départ)
├── /sql/
│   └── schema.sql           # Script de création des tables pour mySQL
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier 😄
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
- Fichier SQL (`schema.sql`) pour initialiser la base
- Fichier `.csv` généré de l’état des stocks à date
- Documentation fonctionnelle (ce `README.md`)

---

## 📌 À venir

- Factorisation et sécurisation
- try/except affinés
- Tests de robustesse sur les étapes `Transform`

---

**Bonne lecture !**
