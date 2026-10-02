# Orchestration : Airflow vs Dagster

## Données
Taxis jaunes NYC, janvier 2024 (TLC). Placer `yellow_tripdata_2024-01.parquet` dans `data/raw/` (ignoré par Git), puis :

    pip install pandas pyarrow sqlalchemy
    python scripts/make_sample.py          # produit data/raw/taxi_sample.csv (100 000 lignes, seed 42)
    python src/run_plain.py                # pipeline de référence (SQLite par défaut)

Résultat de référence : 100 000 lignes lues, 91 813 conservées, 8 187 rejetées (data/reports/rejected.csv).
