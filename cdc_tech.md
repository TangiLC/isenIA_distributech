# Cahier des charges techniques

## 1️⃣ Vision produit

**Objectif :** Cadrer rapidement le sens du projet IA

**Contenu :**

Pour pallier le manque de suivi logistique fiable et en temps réel, un pipeline ETL a été mis en place pour intégrer les données de commandes (CSV) et de stocks (SQLite) dans une base MySQL centralisée. Celle-ci permet de suivre l’historique des commandes, visualiser les stocks par région et piloter efficacement les opérations commerciales et logistiques.

Cette architecture simple, robuste, évolutive et maîtrisable par les équipes en place permet de fiabiliser rapidement les données tout en posant une base solide pour les usages futurs.

**Checklist / Questions clés :**

- [ ] Quel problème métier cherchons-nous à résoudre ?
- [ ] Quelle valeur pour l’utilisateur final ?
- [ ] Pourquoi une IA plutôt qu’une autre solution ?

**Agile :**

- Résumée en une phrase, revue à chaque grand jalon produit

---

## 2️⃣ User Stories

**Objectif :** Traduire les besoins en fonctionnalités concrètes

**Exemples :**

**User Story no. 1** En tant que _commercial terrain_, je veux un _fichier commande nettoyé_ afin _d'améliorer le traitement du process de commande_.

Critères d’acceptation mesurables :

- Le fichier ne contient aucune ligne vide ni doublon.
- Les formats de date sont homogènes (ex. AAAA-MM-JJ).
- n>95 % des champs obligatoires sont remplis (client, produit, quantité).

**User Story no. 2** En tant que _responsable commercial_, je veux _récupérer un rapport hebdomadaire des stocks\*\* afin d'avoir une vision à jour des tendances et tensions logistiques_.

Critères d’acceptation mesurables :

- Le rapport hebdomadaire est généré automatiquement.
- Il contient les stocks par produit et par région à la date de génération.
- Le fichier au format csv est accessible dans un dossier.

**User Story no. 3** En tant que _responsable commercial_, je veux _integrer les commandes et les productions dans un stock centralisé_ afin de _garder à jour des stocks cohérents et piloter efficacement les opérations commerciales_.

Critères d’acceptation mesurables :

- n>95 % des commandes validées sont intégrées au stock central.
- Toutes les entrées et sorties de stock sont historisées avec date, origine et quantité.
- Les stocks sont cohérents entre les différentes sources (aucun écart supérieur à 1 %).
- Les données sont accessibles dans un fichier csv et mise à jour est hebdomadaire.

**Checklist / Questions clés :**

- [ ] En tant que… je veux… afin de… ?
- [ ] Quels bénéfices utilisateurs ?
- [ ] Critères d’acceptation mesurables définis ?

**Agile :**

- Prioriser avec le Product Owner à chaque sprint

---

## 3️⃣ Rédaction itérative

**Objectif :** Permettre l’évolution naturelle du projet

**Contenu :**

_Révision continue des besoins à chaque sprint :_
À l’issue de chaque sprint, les exigences fonctionnelles et techniques sont réévaluées en tenant compte des retours du terrain, des échanges avec les commerciaux et des données collectées. Cette démarche garantit une adaptation progressive du système à son environnement réel d’exploitation.

_Intégration des apprentissages POC, MVP et tests terrain :_
Les enseignements tirés du POC (validation des sources et du pipeline), du MVP (structure minimale fonctionnelle de la base et du script ETL), ainsi que des tests terrain (exploitabilité par les commerciaux et fiabilité des données de stock) sont systématiquement intégrés aux itérations suivantes. Ces retours permettent d’optimiser la robustesse du système, d’affiner la logique métier et de renforcer la maintenabilité de la solution.

**Checklist / Questions clés :**

- [ ] Revoir les besoins et contraintes à chaque sprint
- [ ] Inclure apprentissages du POC, MVP, tests terrain

**Agile :**

- Mises à jour fréquentes, versionnées

---

## 4️⃣ Spécifications techniques

**Objectif :** Poser les bases technologiques sans figer

**Contenu :**

- Python 3.12, MySQL 8, Pandas 2.3
- Connexion MySQL via mysql-connector 9.3
- Docker + Adminer pour BDD
- Tests Pytest(v8.4) + Pytest-cov(v6.2)
- Données d’entrée : CSV & SQLite

**Checklist / Questions clés :**

- [ ] Langage / framework IA défini
- [ ] Données nécessaires (type, volume, accès, RGPD)
- [ ] Contraintes techniques (perfs, compatibilité, stockage)

**Agile :**

- Ajouter les specs par briques fonctionnelles au fil des itérations

---

## 5️⃣ KPI & critères d’acceptation

**Objectif :** Valider la qualité et l’utilité des livrables

**Exemples de KPI :**

User Story no. 1 KPIs:

- Taux de doublons : 2 % (aucune ligne en double dans le fichier).
- Taux de lignes vides : 2 % (chaque ligne contient des données utiles).
- Taux de complétude : 100 % des lignes doivent avoir les champs obligatoires renseignés (client, produit, quantité).
- Taux de formats conformes (dates) : 100 % des dates au format AAAA-MM-JJ.

User Story no. 2 KPIs:

- Taux d’erreurs d’accès : 0 % (le fichier CSV est bien généré et accessible dans le bon dossier).
- Taux de complétude du rapport : tous les produits et toutes les régions doivent être représentés.
- Temps de génération du rapport : < 1 seconde.
- Format de fichier conforme : CSV bien structuré (lisible, séparateur correct, encodage UTF-8).

User Story no. 3 KPIs:

- Taux d’intégration des commandes validées : 100 %.
- Taux de mouvements historisés : 100 % des entrées/sorties doivent être enregistrées avec date, origine, quantité.
- Écart de cohérence entre sources : ≤ 1 % entre le stock théorique et les données d’entrée (commandes, production).
- Fichier export disponible : chaque mise à jour génère un fichier CSV complet et lisible.

  **Checklist / Questions clés :**

- [ ] Précision / rappel / F1-score
- [ ] Temps de réponse acceptable
- [ ] Taux de faux positifs / négatifs

**Agile :**

- Définis pour chaque User Story, évalués en fin de sprint

---

## 6️⃣ Organisation agile du projet

**Objectif :** Structurer l’avancement en mode collaboratif

**Contenu :**

- 3 sprints courts (1 semaine)
- Rituels : daily, sprint planning, review, rétrospective
- Suivi via Notion (retroplanning, tickets, documentation, RGPD)

**Checklist / Questions clés :**

- [ ] Sprints courts définis (1-3 semaines)
- [ ] Rituels agiles respectés (planning, daily, review, rétro)
- [ ] Suivi backlog (Jira, Trello, Notion...)

**Agile :**

- Responsabiliser l’équipe, suivre l'avancement de façon visuelle

---

## 7️⃣ Points de vigilance IA

**Objectif :** Anticiper les pièges spécifiques aux projets IA

**Risques & Préventions :**

1. Sur-nettoyage des données

   Risque : suppression involontaire de données valides jugées ""anormales"", insertion de données érronnées dans la BDD centralisée

   Conséquence : perte d'informations utiles, résultats faussés.

   Prévention : valider les règles de nettoyage avec les utilisateurs métier.

2. Données biaisées

   Risque : les données reflètent des pratiques locales ou des périodes spécifiques, ""Boite noire"" règles de transformation non-explicables

   Conséquence : analyses non généralisables, décisions faussées.

   Prévention : vérifier la représentativité des données (produits, régions, revendeurs, etc.).

3. Manque d’explicabilité

   Risque : traitements ou règles métier opaques, Manque de log des traitements

   Conséquence : incompréhension, difficulté à corriger ou justifier les résultats.

   Prévention : documenter clairement chaque transformation, privilégier des règles simples et traçables.

4. Absence de versioning

   Risque : perte de maîtrise sur les versions de code ou de données.

   Conséquence : résultats incohérents, erreurs non reproductibles.

   Prévention : versionner le code (Git), horodater les fichiers sources, documenter les évolutions de schéma.

5. Tests insuffisants en conditions réelles

   Risque : pipeline testé uniquement sur des cas simplifiés.

   Conséquence : erreurs silencieuses en production, instabilité.

   Prévention : tester sur des données réelles, puis sur des volumes complets avant mise en production.

**Checklist / Questions clés :**

- [ ] Données biaisées identifiées ?
- [ ] Explicabilité du modèle assurée ?
- [ ] Versioning ?
- [ ] Tests sur données réelles ?

**Agile :**

- Maintenir checklist IA spécifique à jour à chaque étape
