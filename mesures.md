# Tableau des mesures : Airflow vs Dagster

Sources : captures du dossier `captures/` (numéro indiqué entre crochets). Aucune valeur n'est interprétée ici.
Environnement : Windows 10, Docker Desktop (moteur Docker 29.7.2, Compose v5.5.0, 7,6 GiB alloués),
Airflow 3.3.2 (CeleryExecutor, Python 3.13 d'après les traces), Dagster 1.13.25 en mode `dagster dev` (Python 3.12).
Données : taxis jaunes NYC, janvier 2024, échantillon de 100 000 lignes (seed 42) : 91 813 conservées, 8 187 rejetées.

## 1. Durées (100 000 lignes lues, environnement `prod`)

| Configuration | Run 1 | Run 2 | Run 3 | Médiane | Remarque |
|---|---|---|---|---|---|
| Python pur → SQLite (4 runs, 2 oct.) | 4,1 s | 3,7 s | 3,6 s (+ 4,1 s) | 3,9 s | base différente : non comparable [02] |
| Python pur → PostgreSQL (5 oct.) | 27,2 s | 25,6 s | 27,9 s | **27,2 s** | exécuté dans le conteneur Dagster [27] |
| Dagster, run complet `prod` (5 oct.) | 60 s | 52 s | 50 s | **52 s** | durée affichée par l'interface [28] |
| Airflow, run complet `prod` (5 oct.) | 43,8 s | 65 s | 59,3 s | **59,3 s** | `env=prod` confirmé pour 20:29 (fichier `daily_prod.csv` modifié à 20:30) et 20:39 (colonne Configuration, capture 31) ; run de 20:42 à confirmer [29] |

Mesures isolées d'une autre session (4 oct.) : Airflow `dev` 15,9 s [06], Airflow `prod` 47,8 s [07], Dagster `dev` 18 s [17], Dagster `prod` 34 s [18].
Runs planifiés Dagster en `dev` : 33 s chacun [24]. Ne pas les comparer aux runs `prod`.

Durée par étape (une seule mesure par outil) :

| Étape | Airflow (run de 59,3 s) | Dagster (run de 50 s) |
|---|---|---|
| extraction | 2,4 s | non relevé |
| nettoyage | 1,7 s | non relevé |
| chargement PostgreSQL | 49,5 s | 22,2 s |
| rapport | 3,2 s | 3,1 s |

## 2. Mémoire (`docker stats --no-stream`, une mesure instantanée)

| | Airflow, 4 oct. [13] | Airflow, 5 oct. [30] | Dagster, 4 oct. [26] |
|---|---|---|---|
| Conteneurs de l'outil | 7 | 7 | 1 |
| Mémoire totale de l'outil | ≈ 2 394 MiB | ≈ 1 902 MiB | 699 MiB |
| Base cible `warehouse` (non comptée) | 53 MiB | 66 MiB | 53 MiB |

Le CPU relevé par `--no-stream` n'est pas fiable : non retenu.

## 3. Code (même règle de comptage : lignes totales / lignes utiles, sans lignes vides ni commentaires)

| | Airflow (`taxi_pipeline.py`) | Dagster (`definitions.py`) |
|---|---|---|
| Lignes totales | 82 | 88 |
| Lignes utiles | 66 | 65 |

Dagster déclare en plus la ressource, le job et la planification dans ce fichier.

## 4. Installation et démarrage

| | Airflow | Dagster |
|---|---|---|
| Initialisation | `airflow-init` : 58,5 s [03] | build de l'image : 180,1 s [Dagster, étape build] |
| Démarrage des services | apiserver healthy après 153,7 s [04] ; 288,8 s au démarrage du 18 oct. | warehouse healthy 19,3 s, dagster started 18,0 s |
| Conteneurs lancés | 8 (dont `warehouse`) | 2 (dont `warehouse`) |
| Temps de mise en œuvre total | À COMPLÉTER (en heures, incidents compris) | À COMPLÉTER |

## 5. Panne provoquée (arrêt de la base `warehouse` pendant un run `prod`)

| | Airflow [09, 10, 11, 12] | Dagster [20, 21, 22, 22b, 22c, 22e] |
|---|---|---|
| Étapes réussies avant la panne | `extract`, `clean` (essai 1) | `raw_trips`, `clean_trips` |
| Étape en échec | `load` après 2 essais ; `report` : « échec en amont » | `loaded_trips` après `max_retries=1` ; `daily_report` non exécuté |
| Durée du run en échec | 38,5 s | 43 s |
| Cause trouvée dans les logs | recherche du mot `OperationalError` : trouvée | recherche `OperationalError` : rien ; filtre `type:STEP_FAILURE` : trouvée |
| Temps pour trouver la cause | non chronométré | non chronométré |
| Relance uniquement des étapes en échec | « effacer » `load` + aval, même run, `prod` conservé ; `load` à l'essai 3 ; `extract`/`clean` inchangés (14:38) | reprise « From failure » (page détaillée du run) : `prod` conservé, 2 assets, 42 s ; matérialisation manuelle sélective : repart en `dev` (22 s) |
| Incident constaté après la panne | aucun | serveur de code injoignable (erreur gRPC UNAVAILABLE), résolu par `docker compose restart dagster` ; cause non établie |

## 6. Planification

| | Airflow [14] | Dagster [23b, 23c, 24] |
|---|---|---|
| Essai à 2 minutes | runs « Planifié » déclenchés seuls (15:00 à 15:22), versions du DAG v1 → v2 → v3 | ticks à 19:26 et 19:28 UTC, 2 runs de 33 s |
| Planification d'origine (`0 6 * * *`) | run planifié observé le 5 oct. (démarré 20:23:49, 1 min 30 s) et le 6 oct. (démarré 07:07, 24 s) | 06:00 UTC ; interrupteur éteint par défaut |
| Fuseau | à vérifier dans la documentation | UTC (affiché) |
| Paramètres des runs planifiés | `env=dev` (valeur par défaut) | `env=dev` (valeur par défaut) |

## 7. Secrets (valeurs lues dans l'environnement du conteneur)

| | Airflow [15, non publiée] | Dagster [25, non publiée] |
|---|---|---|
| Où est défini le secret | `airflow/.env`, exclu de Git | `dagster/docker-compose.yaml`, versionné |
| Visible en clair dans le conteneur | mot de passe de la base, `FERNET_KEY` | mot de passe de la base |
| Lecture dans le code | `os.environ.get(...)` | `dg.EnvVar(...)` |

## 8. Incidents d'exploitation à reporter dans le journal

- Docker Desktop : erreur API 500 après le build Dagster, puis au redémarrage du PC (redémarrage de Docker Desktop nécessaire).
- Airflow : fichiers créés vides à l'installation (`.env`, DAG), corrigés ; `FERNET_KEY` obligatoire.
- Dagster : bouton « Re-execute » grisé pendant l'erreur du serveur de code ; l'option « From failure » n'apparaît que sur la page détaillée du run, pas dans la liste des runs.

## 9. Limites de l'étude à écrire

- Un seul PC, 3 runs par outil et par configuration : les étendues se recouvrent, aucune conclusion de vitesse.
- Dagster en mode `dagster dev` (1 conteneur) : pas équivalent à un déploiement de production.
- Versions de Python différentes dans les conteneurs (3.12 / 3.13).
- Définition de la « durée » différente dans les deux interfaces.
- Temps de diagnostic non chronométré.
