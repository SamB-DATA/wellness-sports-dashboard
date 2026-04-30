# POC Data Pipeline - Avantages sportifs

## 1. Contexte

Dans ce projet, j’ai réalisé un Proof of Concept (POC) d’un pipeline data permettant d’analyser l’impact de l’activité sportive des salariés sur des avantages RH, notamment :

* la prime sportive
* les jours de bien-être

L’objectif est de transformer des données brutes en indicateurs exploitables pour la prise de décision.

---

## 2. Sources de données

J’ai utilisé deux sources principales :

* un fichier RH contenant les informations des salariés (salaire, moyen de transport, etc.)
* un fichier d’activités sportives simulées généré via Python

Ces données sont chargées dans PostgreSQL pour être traitées.

---

## 3. Architecture du projet

Le pipeline suit les étapes suivantes :

1. **Extract**

   * chargement des fichiers Excel dans PostgreSQL

2. **Transform**

   * nettoyage des données
   * normalisation des champs
   * calcul des règles métier :

     * éligibilité à la prime sportive
     * calcul du montant de la prime
     * calcul du nombre d’activités sportives
     * éligibilité aux jours bien-être

3. **Load**

   * stockage dans une table finale `employee_benefits`

4. **Export**

   * export des données vers des fichiers CSV pour Tableau Public

---

## 4. Stack technique

* Python (Pandas)
* PostgreSQL
* Docker
* Kestra (orchestration)
* Redpanda (simulation temps réel - POC)
* Tableau Public (visualisation)

---

## 5. Dashboard

J’ai réalisé un dashboard interactif dans Tableau Public permettant de visualiser :

* le nombre de salariés
* le nombre d’éligibles aux avantages
* le coût total des primes
* le taux d’éligibilité
* la répartition des activités sportives

Le dashboard permet également de filtrer par type de sport et niveau d’activité.

---

## 6. Résultats

Ce projet permet de :

* mesurer l’engagement sportif des salariés
* estimer le coût des avantages RH
* identifier les profils les plus actifs
* faciliter la prise de décision

---

## 7. Améliorations possibles

* connexion à une API réelle (ex : Strava)
* mise en place d’un vrai pipeline temps réel
* ajout de contrôles qualité avancés
* automatisation complète via Kestra

---

## 8. Lancement du projet

```bash
docker compose up -d
python src/load/load_excel_to_postgres.py
python src/extract/generate_sport_history.py
python src/transform/transform_business_rules.py
python src/load/export_for_tableau.py
```
