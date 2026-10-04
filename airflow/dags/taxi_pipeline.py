"""DAG Airflow : extraction -> nettoyage -> chargement -> rapport.
La logique métier est dans src/core.py (identique pour Dagster).
Chaque étape lit/écrit des fichiers dans data/staging : on peut ainsi relancer
une seule étape sans refaire les précédentes."""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, "/opt/airflow/src")
import core  # noqa: E402

try:  # Airflow 3
    from airflow.sdk import Param, dag, task
except ImportError:  # Airflow 2
    from airflow.decorators import dag, task
    from airflow.models.param import Param

DATA = "/opt/airflow/data"
STAGING = f"{DATA}/staging"
DB_URL = os.environ.get("WAREHOUSE_DB_URL", "sqlite:////opt/airflow/data/airflow_test.db")


def _env(ctx):
    return ctx["params"]["env"]


def _maybe_fail(step, ctx):
    if ctx["params"]["fail_at"] == step:
        raise RuntimeError(f"Erreur injectée volontairement à l'étape '{step}'")


@dag(
    dag_id="taxi_pipeline",
    schedule="0 6 * * *",              # tous les jours à 06:00
    start_date=datetime(2026, 10, 1),
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=10)},
    params={
        "env": Param("dev", enum=["dev", "prod"]),       # dev = 10 000 lignes, prod = tout
        "fail_at": Param("none", enum=["none", "extract", "clean", "load", "report"]),
    },
    tags=["veille", "comparaison"],
)
def taxi_pipeline():
    @task
    def extract(**ctx):
        _maybe_fail("extract", ctx)
        Path(STAGING).mkdir(parents=True, exist_ok=True)
        df = core.extract(f"{DATA}/raw/taxi_sample.csv")
        if _env(ctx) == "dev":
            df = df.head(10_000)
        df.to_parquet(f"{STAGING}/{_env(ctx)}_raw.parquet", index=False)
        return len(df)

    @task
    def clean(n_extracted, **ctx):
        _maybe_fail("clean", ctx)
        df = pd.read_parquet(f"{STAGING}/{_env(ctx)}_raw.parquet")
        ok, ko = core.clean(df)
        ok.to_parquet(f"{STAGING}/{_env(ctx)}_clean.parquet", index=False)
        ko.to_csv(f"{DATA}/reports/rejected_{_env(ctx)}.csv", index=False)
        return len(ok)

    @task
    def load(n_clean, **ctx):
        _maybe_fail("load", ctx)
        ok = pd.read_parquet(f"{STAGING}/{_env(ctx)}_clean.parquet")
        return core.load(ok, DB_URL, table=f"trips_clean_{_env(ctx)}")

    @task
    def report(n_loaded, **ctx):
        _maybe_fail("report", ctx)
        return core.report(DB_URL, f"{DATA}/reports/daily_{_env(ctx)}.csv",
                           table=f"trips_clean_{_env(ctx)}")

    report(load(clean(extract())))


taxi_pipeline()