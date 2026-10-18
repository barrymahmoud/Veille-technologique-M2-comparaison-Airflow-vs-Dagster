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

## 2. Informations qu'il reste à relever (à compléter, sans les deviner)

| Information | Outil | Où la chercher | Résultat |
|---|---|---|---|
| Dernière version publiée et sa date | Airflow | page GitHub, rubrique « Releases » ; comparer avec la 3.3.2 utilisée | À COMPLÉTER |
| Dernière version publiée et sa date | Dagster | page GitHub, rubrique « Releases » ; comparer avec la 1.13.25 | À COMPLÉTER |
| Fuseau horaire des planifications | Airflow | documentation, recherche « timezone » | À COMPLÉTER |
| Fuseau horaire des planifications | Dagster | documentation, recherche « execution_timezone » | À COMPLÉTER |
| Gestion des secrets | Airflow | documentation, recherche « secrets backend » et « connections » | À COMPLÉTER |
| Gestion des secrets | Dagster | documentation, recherche « EnvVar » et « resources » | À COMPLÉTER |
| Exécuteurs / passage à l'échelle | Airflow | documentation, recherche « executor » | À COMPLÉTER |
| Déploiement / passage à l'échelle | Dagster | documentation, rubrique « Deployment » | À COMPLÉTER |
| Tests | Airflow | documentation, recherche « testing » | À COMPLÉTER |
| Tests | Dagster | documentation, recherche « testing » | À COMPLÉTER |

## 3. Précautions de rédaction

- Le nombre d'étoiles, de forks ou de commits ne mesure pas la qualité d'un outil : ne pas le présenter comme un avantage.
- Les phrases de positionnement viennent des éditeurs : les écrire comme « selon la documentation de Dagster », jamais comme un fait vérifié.
- Les exemples du README d'Airflow sur le versionnement sont en 2.x : ne pas en déduire le calendrier des versions 3.x.
- Chaque ligne du rapport qui s'appuie sur cette veille doit citer l'adresse et la date de consultation.
