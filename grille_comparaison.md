# Grille de comparaison pondérée : Airflow vs Dagster

Note de 0 à 5 par critère. Score = somme (note × poids) / 5. Total des poids = 100.
Chaque note doit être justifiée par une preuve (mesure, capture, source officielle).

| # | Famille | Critère | Définition | Méthode de test | Poids | Airflow | Dagster | Preuve |
|---|---|---|---|---|---|---|---|---|
| 1 | Fonctionnalités | Couverture du besoin | Le pipeline E-T-L-R est réalisé complètement | Pipeline exécuté de bout en bout | 8 | | | capture |
| 2 | Fonctionnalités | Planification | Exécution automatique (cron) fiable | Schedule quotidien, vérifier 2 déclenchements | 6 | | | capture |
| 3 | Fonctionnalités | Paramétrage / environnements | dev et prod sans changer le code | Même code, 2 configs | 7 | | | diff de config |
| 4 | Fonctionnalités | Reprise sur erreur | Relancer seulement l'étape en échec | Erreur provoquée dans `load` | 10 | | | logs avant/après |
| 5 | Technique | Installation | Effort pour obtenir un environnement fonctionnel | Chrono + nb de commandes | 6 | | | chrono |
| 6 | Technique | Modèle de programmation | Lisibilité et maintenabilité du code | Lignes de code, nb de concepts à apprendre | 8 | | | `wc -l` |
| 7 | Technique | Performance | Surcoût d'orchestration | Temps total vs `run_plain.py` (3 runs, médiane) | 6 | | | tableau de mesures |
| 8 | Technique | Tests | Tester le pipeline sans l'orchestrateur complet | Écrire 1 test unitaire par outil | 5 | | | code du test |
| 9 | Exploitation | Observabilité / diagnostic | Trouver la cause d'une panne rapidement | Chrono : temps pour localiser l'erreur injectée | 10 | | | capture UI + chrono |
| 10 | Exploitation | Secrets | Gestion des identifiants BD | Lecture de la doc + test réel | 6 | | | capture |
| 11 | Exploitation | Ressources | RAM et CPU au repos et en exécution | `docker stats` | 6 | | | `docker stats` |
| 12 | Exploitation | Passage à l'échelle | Exécuteurs, distribution, parallélisme | Analyse de la doc officielle | 5 | | | sources |
| 13 | Écosystème | Licence et coût | Licence, coût d'exploitation | Doc officielle | 3 | | | lien |
| 14 | Écosystème | Documentation et communauté | Qualité de la doc, activité du dépôt | Dernier release, issues ouvertes, étoiles (date de relevé) | 4 | | | lien + date |
| 15 | Écosystème | Pérennité | Gouvernance, rythme d'évolution | Historique des versions | 4 | | | lien |
| 16 | Décision | Adéquation par scénario | Voir scénarios A et B du rapport | Synthèse | 6 | | | rapport |
| | | **Total** | | | **100** | | | |

## Scénarios de décision
- **A. Petite équipe (1 à 3 personnes)** : priorité aux critères 5, 6, 8, 9.
- **B. Grande plateforme (nombreuses équipes, centaines de pipelines)** : priorité aux critères 10, 11, 12, 15.

## Journal de temps de mise en œuvre
| Étape | Outil | Début | Fin | Durée | Remarques / blocages |
|---|---|---|---|---|---|
