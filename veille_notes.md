# Notes de veille : Airflow et Dagster

Date de consultation de toutes les sources de ce tableau : 06/10/2026.
Les chiffres de GitHub sont une photo instantanée à cette date.

## 1. Informations relevées (avec la source)

| Information | Outil | Ce que dit la source | Adresse de la page |
|---|---|---|---|
| Dépôt officiel | Airflow | Dépôt public sous l'organisation Apache. Description : « Apache Airflow - A platform to programmatically author, schedule, and monitor workflows » | https://github.com/apache/airflow |
| Licence | Airflow | Onglet « Apache-2.0 license » affiché sur la page du dépôt | https://github.com/apache/airflow |
| Activité | Airflow | 41 805 commits ; dernier commit affiché « 4 minutes ago » ; 47,1k étoiles ; 18k forks | https://github.com/apache/airflow |
| Versionnement | Airflow | Le README décrit un versionnement MAJOR / MINOR / PATCH : MAJOR en cas de changements incompatibles, MINOR pour de nouvelles fonctions, PATCH pour des corrections et la documentation. Les versions mineures sont publiées depuis une branche dédiée (exemples du README en 2.x) | https://github.com/apache/airflow (README) |
| Documentation | Airflow | La page d'index présente Airflow Core (webserver, scheduler, CLI), airflowctl (interface en ligne de commande qui passe par l'API REST) et des plugins Mypy | https://airflow.apache.org/docs/ |
| Dépôt officiel | Dagster | Dépôt public `dagster-io/dagster`. Description : « An orchestration platform for the development, production, and observation of data assets » | https://github.com/dagster-io/dagster |
| Licence | Dagster | « Dagster is Apache 2.0 licensed » (section License du README) ; onglet « Apache-2.0 license » | https://github.com/dagster-io/dagster |
| Activité | Dagster | 28 080 commits ; dernier commit affiché « 14 hours ago » ; 16,2k étoiles ; 2,3k forks | https://github.com/dagster-io/dagster |
| Version | Dagster | La documentation affiche « Latest (1.13.25) », la version utilisée pour les tests | https://dagster.io/docs |
| Positionnement (affirmation de l'éditeur) | Dagster | « a data orchestrator built for data engineers, with integrated lineage, observability, a declarative programming model, and best-in-class testability » | https://dagster.io/docs |
| Offre commerciale | Dagster | La documentation met en avant « Dagster+ » (bouton « Try Dagster+ », quickstarts Hybrid et Serverless) à côté de l'open source | https://dagster.io/docs |
| Communauté | Dagster | Le README renvoie vers un Slack, des archives Slack, les GitHub Discussions et un guide de contribution | https://github.com/dagster-io/dagster (README) |

## 2. Informations relevées dans la documentation (à vérifier en ouvrant chaque page)

Lecture faite par recherche web (extraits de pages, parfois d'une version précédente de la documentation). : [06/10/2026].

| Information | Outil | Résultat (reformulé) | Adresse | Source |
|---|---|---|---|---|
| Dernière version publiée | Airflow | La page des versions marque la 3.3.2 comme dernière version (publiée le 17 septembre, année non affichée) : version testée identique | https://github.com/apache/airflow/releases/tag/3.3.2 | officielle |
| Dernière version publiée | Dagster | La documentation affiche 1.13.25 comme « Latest » : version testée identique. Publiée le 1er octobre 2026 à 18 h 17 (GMT), d'après la page des versions. | https://dagster.io/docs et https://github.com/dagster-io/dagster/releases | officielle |
| Fuseau horaire | Airflow | Dates stockées en UTC ; `default_timezone` dans `[core]`, `utc` par défaut, modifiable ; un `start_date` sans fuseau reçoit le fuseau par défaut (lecture des pages 3.1.x et 2.x) | https://airflow.apache.org/docs/apache-airflow/3.3.2/authoring-and-scheduling/timezone.html | officielle |
| Fuseau horaire | Dagster | Sans fuseau défini, planification en UTC ; paramètre `execution_timezone` ; un changement manuel dans l'interface prend le pas sur le statut par défaut du code | https://dagster.io/docs/guides/automate/schedules/customizing-execution-timezone | officielle |
| Gestion des secrets | Airflow | Connexions et variables lues dans les variables d'environnement puis dans la base de métadonnées ; backend de secrets alternatif possible, et backend séparé pour les workers en version 3 (page de la 3.0.1) | https://airflow.apache.org/docs/apache-airflow/3.0.1/security/secrets/secrets-backend/index.html | officielle |
| Gestion des secrets | Dagster | `EnvVar` alimente les champs d'une ressource, valeur évaluée au lancement du run ; secrets non visibles dans le code ni le launchpad | https://docs.dagster.io/guides/build/external-resources/configuring-resources | officielle |
| Exécuteurs | Airflow | LocalExecutor par défaut ; autres exécuteurs possibles ; plusieurs exécuteurs combinables depuis la 2.10 ; exécuteurs hybrides retirés en 3.0 | https://airflow.apache.org/docs/apache-airflow/3.3.2/core-concepts/executor/index.html | officielle |
| Déploiement | Dagster | `dagster dev` réservé au développement local ; `-f` déconseillé en production ; production : plusieurs répliques du serveur web, daemon redémarré automatiquement | https://docs.dagster.io/guides/running-dagster-locally | officielle |
| Tests | Airflow | `dag.test()` et `airflow dags test` ; tests de validation avec un lanceur Python ; page non mise à jour pour Airflow 3 | guide Astronomer (à confirmer sur la page Best Practices d'Airflow) | éditeur tiers |
| Tests | Dagster | Tests unitaires d'actifs, un par un plutôt que des jobs entiers ; ressources simulables | https://docs.dagster.io/next/guides/test/unit-testing-assets-and-ops | officielle |

## 3. Précautions de rédaction

- Le nombre d'étoiles, de forks ou de commits ne mesure pas la qualité d'un outil : ne pas le présenter comme un avantage.
- Les phrases de positionnement viennent des éditeurs : les écrire comme « selon la documentation de Dagster », jamais comme un fait vérifié.
- Les exemples du README d'Airflow sur le versionnement sont en 2.x : ne pas en déduire le calendrier des versions 3.x.
- Chaque ligne du rapport qui s'appuie sur cette veille doit citer l'adresse et la date de consultation.
- Dans notre montage, Airflow utilise le CeleryExecutor du fichier Compose officiel alors que la documentation indique le LocalExecutor comme exécuteur par défaut : la comparaison de mémoire (7 conteneurs contre 1) compare deux configurations différentes, pas deux minimums.
- Dagster a été testé avec `dagster dev -f`, que la documentation réserve au développement local.
- Les pages lues pour les fuseaux (Airflow) et les secrets (Airflow) datent de versions plus anciennes que la 3.3.2 : à confirmer sur la bonne version.
