# Readme pour la dockerisation du projet

## DockerHub

recherche des images officielles cohérentes avec le projet

- MySQL
- Adminer
- Python Back
- Python Front Flask

## Dossier à cibler

identifier les dossiers/fichiers à mettre dans chaque image

- Python Back : etl.py + ./scripts + ./data (volume) -> lancer etl.py
- Python front : ./front -> lancer front.py

## Dockerignore

créer le `.dockerignore`

## Image Backend

créer l'image du backend (Dockerfile)

## Image Frontend

créer l'image du frontend (Dockerfile)

## Orchestration

orchestrer les images dans docker-compose.yml (inclure Adminer, MySQL)

## Rédiger ce ReadMe...

et penser à la récursivité

## Mode d'emploi

1- Démarrer le container pour le back-end en arrière plan

```bash
docker-compose up -d
```

2- Dans un nouveau terminal, build le projet

```bash
docker-compose build --no-cache
```

3- Déplacer les données vers le volume /data

```bash
docker cp ./data/. etl_dt:/dtech/data/
```

4- Lancer l'appli etl

```bash
docker-compose exec etl python3 etl.py
```

les étapes 3 et 4 peuvent être recommancées avec les nouvelles données dans /data

5- Lancer le front

```bash
docker-compose exec etl python3 ./front/front.py
```
