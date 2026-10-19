# Orchestration de pipelines : Airflow vs Dagster

Projet de veille technologique (Master Data Science - Génie logiciel, sujet 10).
Même pipeline (extraction, nettoyage, chargement PostgreSQL, rapport) implémenté avec Apache Airflow et Dagster.
La logique métier est dans `src/core.py`, appelée à l'identique par les deux outils.

## Contenu du dépôt

```
orchestration/
├── src/core.py              logique métier commune
├── src/run_plain.py         pipeline de référence sans orchestrateur
├── scripts/make_sample.py   génère l'échantillon de données
├── data/raw/taxi_sample.csv échantillon fourni (100 000 lignes, seed 42)
├── airflow/                 DAG, docker-compose, script de préparation
├── dagster/                 définitions, Dockerfile, docker-compose
├── captures/                preuves (numérotées)
├── mesures.md               toutes les mesures et leurs sources
├── veille_notes.md          notes de veille datées
└── grille_comparaison.md    grille pondérée
```

## Prérequis

- Windows avec Docker Desktop lancé (testé : moteur 29.7.2, Compose v5.5.0, 7,6 GiB alloués).
- Python 3 (commande `py`) pour la référence et le script de préparation d'Airflow.
- Environ 14 Go de disque utilisés par Docker lors des tests.

## Pipeline de référence (sans orchestrateur)

```powershell
py -m pip install pandas pyarrow sqlalchemy
py src\run_plain.py
```

Résultat attendu : 100 000 lignes lues, 91 813 conservées, 8 187 rejetées.

## Airflow (interface : http://localhost:8080, compte `airflow` / `airflow`)

Première installation, depuis le dossier `airflow` :

```powershell
cd airflow
py setup_airflow.py          # crée .env (avec FERNET_KEY) et complète le compose
docker compose up airflow-init
docker compose up -d
```

Démarrages suivants :

```powershell
cd airflow
docker compose up -d
docker compose ps           # attendre que les 8 services soient (healthy), environ 3 minutes
```

Arrêt (conserve les données) :

```powershell
docker compose stop
```

Paramètres au déclenchement du DAG `taxi_pipeline` : `env` (`dev` = 10 000 lignes, `prod` = tout), `fail_at` (`none`, `extract`, `clean`, `load`, `report`).
Planification : `0 6 * * *`. Le DAG est créé **en pause** (réglage du compose officiel) : l'activer avec l'interrupteur dans l'interface avant d'attendre une exécution planifiée.

## Dagster (interface : http://localhost:3000)

Première installation (construit l'image, environ 3 minutes) :

```powershell
cd dagster
docker compose up -d --build
```

Démarrages suivants :

```powershell
cd dagster
docker compose up -d
docker ps
```

Arrêt (conserve les données) :

```powershell
docker compose stop
```

En cas d'erreur « Code location error » dans l'interface :

```powershell
docker compose restart dagster
```

Lancer un run `prod` : menu **Jobs**, `taxi_job`, flèche à côté de « Materialize all », « Open launchpad », puis coller :

```yaml
ops:
  raw_trips:
    config: {env: prod, fail_at: none}
  clean_trips:
    config: {env: prod, fail_at: none}
  loaded_trips:
    config: {env: prod, fail_at: none}
  daily_report:
    config: {env: prod, fail_at: none}
```

La planification (`0 6 * * *`, fuseau UTC) est désactivée par défaut : l'activer dans le menu **Automation**.

## Vérifier les données chargées

Depuis le dossier de l'outil concerné (`airflow` ou `dagster`) :

```powershell
docker compose exec warehouse psql -U warehouse -d warehouse -c "SELECT count(*) FROM trips_clean_prod;"
```

Résultat attendu après un run `prod` : 91813.

## Provoquer une panne puis relancer

```powershell
docker compose stop warehouse      # puis lancer un run prod : l'étape de chargement échoue
docker compose start warehouse     # puis relancer uniquement les étapes en échec
```

- Airflow : ouvrir la tâche `load` en échec, « effacer » avec les tâches en aval.
- Dagster : page détaillée du run en échec, menu à côté de « Re-execute all (*) », « From failure ».

## Ports utilisés

| Service | Port |
|---|---|
| Airflow (interface) | 8080 |
| Dagster (interface) | 3000 |
| Base cible d'Airflow | 5433 |
| Base cible de Dagster | 5434 |

## Règles importantes

- Ne jamais lancer `docker compose down -v` : l'option `-v` supprime les volumes (historique des runs, données).
- Pour mesurer, lancer un seul outil à la fois et ne rien faire de lourd sur le PC.
- Le fichier `airflow/.env` (clé `FERNET_KEY`) et les captures `15_*` et `25_*` ne sont pas publiés.
- Les identifiants de la base (`warehouse`) sont des valeurs de développement local.

## Résultats et limites

Les mesures et leurs sources sont dans `mesures.md`, la veille dans `veille_notes.md`.
Limites : un seul PC, 3 mesures par outil et par configuration, Dagster testé en mode `dagster dev` (un seul conteneur), versions de Python différentes dans les conteneurs (3.12 pour Dagster, 3.13 pour Airflow).
