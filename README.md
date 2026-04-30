# POC Data Pipeline - Avantages sportifs

## 1. Contexte

Dans ce projet, j’ai réalisé un Proof of Concept (POC) d’un pipeline data permettant d’analyser l’impact de l’activité sportive des salariés sur des avantages RH.

L’objectif est de transformer des données brutes en indicateurs exploitables pour la prise de décision, notamment autour :

* de la prime sportive
* des jours de bien-être
* de l’engagement des salariés

---

## 2. Sources de données

J’ai utilisé deux sources principales :

* un fichier RH contenant les informations des salariés (salaire, moyen de transport, etc.)
* un fichier d’activités sportives simulées généré via Python

Ces données sont chargées dans PostgreSQL pour être traitées.

---

## 3. Architecture du projet

Le pipeline suit les étapes suivantes :

### 1. Extract

* chargement des fichiers Excel dans PostgreSQL
* génération d’un historique sportif simulé

### 2. Transform

* nettoyage des données
* normalisation des formats
* application des règles métier :

  * éligibilité à la prime sportive
  * calcul du montant de la prime
  * calcul du nombre d’activités sportives
  * éligibilité aux jours bien-être

### 3. Load

* stockage des données transformées dans la table finale `employee_benefits`

### 4. Export

* export des données vers des fichiers CSV pour Tableau Public

---

## 4. Stack technique

* Python (Pandas)
* PostgreSQL
* Docker
* Kestra (orchestration)
* Redpanda (simulation temps réel - POC)
* Tableau Public (visualisation)
* GitHub (versioning)

---

## 5. Dashboard

J’ai réalisé un dashboard interactif dans Tableau Public permettant de visualiser :

* le nombre de salariés
* le nombre d’éligibles aux avantages
* le coût total des primes
* le taux d’éligibilité
* la répartition des activités sportives

Le dashboard permet également de filtrer par :

* type de sport
* niveau d’activité

👉 Lien du dashboard :
(AJOUTER ICI TON LIEN TABLEAU PUBLIC)

---

## 6. Résultats

Ce projet permet de :

* mesurer l’engagement sportif des salariés
* estimer le coût des avantages RH
* identifier les profils les plus actifs
* faciliter la prise de décision

---

## 7. Intégration Slack

Dans ce projet, j’ai implémenté une simulation d’intégration Slack afin de répondre au besoin métier suivant :

> Chaque activité sportive doit générer une notification automatique pour encourager l’engagement des salariés.

J’ai développé un script Python qui :

* récupère la dernière activité sportive depuis PostgreSQL
* construit un message personnalisé (nom, activité, distance, durée)
* envoie ce message vers un channel Slack via un webhook

Lorsque le webhook n’est pas configuré, le message est affiché dans le terminal pour simuler le fonctionnement.

Exemple de message :

```text
Bravo Caroline Olivier ! Tu viens de faire 5.8 km en 199 min en Randonnée ! 🔥🏅
```

Cela permet de simuler un flux événementiel simple dans un contexte POC.

---

## 8. Améliorations possibles

* connexion à une API réelle (ex : Strava)
* mise en place d’un vrai pipeline temps réel
* automatisation complète via Kestra
* ajout de contrôles qualité avancés
* intégration complète avec Slack (webhook actif)

---

## 9. Lancement du projet

```bash
docker compose up -d
python src/load/load_excel_to_postgres.py
python src/extract/generate_sport_history.py
python src/transform/transform_business_rules.py
python src/load/export_for_tableau.py
python src/slack/send_slack_activity.py
```

---

## 10. Sécurité

Les informations sensibles (identifiants PostgreSQL, webhook Slack) sont stockées dans un fichier `.env` non versionné.

---

## 11. Auteur

Projet réalisé par Samir Belasri dans le cadre du parcours Data Engineer.
