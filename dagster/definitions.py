"""Pipeline taxi avec Dagster : modèle « actifs de données » (assets).
La logique métier est dans src/core.py (identique à la version Airflow).
Chaque actif écrit son résultat dans data/staging : on peut donc re-matérialiser
uniquement `loaded_trips` et ce qui en dépend, sans refaire les étapes précédentes."""
import os
import sys
from pathlib import Path

import dagster as dg
import pandas as pd

PROJECT = os.environ.get("PROJECT_DIR", "/opt/project")
sys.path.insert(0, f"{PROJECT}/src")
import core  # noqa: E402

DATA = f"{PROJECT}/data"
STAGING = f"{DATA}/staging"


class PipelineConfig(dg.Config):
    env: str = "dev"          # dev = 10 000 lignes, prod = tout
    fail_at: str = "none"     # none | extract | clean | load | report


class Warehouse(dg.ConfigurableResource):
    db_url: str


def _maybe_fail(step: str, config: PipelineConfig):
    if config.fail_at == step:
        raise RuntimeError(f"Erreur injectée volontairement à l'étape '{step}'")


RETRY = dg.RetryPolicy(max_retries=1, delay=10)   # même politique que sous Airflow


@dg.asset(group_name="taxi", retry_policy=RETRY)
def raw_trips(config: PipelineConfig) -> dg.MaterializeResult:
    _maybe_fail("extract", config)
    Path(STAGING).mkdir(parents=True, exist_ok=True)
    df = core.extract(f"{DATA}/raw/taxi_sample.csv")
    if config.env == "dev":
        df = df.head(10_000)
    df.to_parquet(f"{STAGING}/{config.env}_raw.parquet", index=False)
    return dg.MaterializeResult(metadata={"lignes": len(df)})


@dg.asset(deps=[raw_trips], group_name="taxi", retry_policy=RETRY)
def clean_trips(config: PipelineConfig) -> dg.MaterializeResult:
    _maybe_fail("clean", config)
    df = pd.read_parquet(f"{STAGING}/{config.env}_raw.parquet")
    ok, ko = core.clean(df)
    ok.to_parquet(f"{STAGING}/{config.env}_clean.parquet", index=False)
    Path(f"{DATA}/reports").mkdir(parents=True, exist_ok=True)
    ko.to_csv(f"{DATA}/reports/rejected_{config.env}.csv", index=False)
    return dg.MaterializeResult(metadata={"lignes_conservees": len(ok), "lignes_rejetees": len(ko)})


@dg.asset(deps=[clean_trips], group_name="taxi", retry_policy=RETRY)
def loaded_trips(config: PipelineConfig, warehouse: Warehouse) -> dg.MaterializeResult:
    _maybe_fail("load", config)
    ok = pd.read_parquet(f"{STAGING}/{config.env}_clean.parquet")
    n = core.load(ok, warehouse.db_url, table=f"trips_clean_{config.env}")
    return dg.MaterializeResult(metadata={"lignes_chargees": n})


@dg.asset(deps=[loaded_trips], group_name="taxi", retry_policy=RETRY)
def daily_report(config: PipelineConfig, warehouse: Warehouse) -> dg.MaterializeResult:
    _maybe_fail("report", config)
    path = core.report(warehouse.db_url, f"{DATA}/reports/daily_{config.env}.csv",
                       table=f"trips_clean_{config.env}")
    return dg.MaterializeResult(metadata={"fichier": path})


taxi_job = dg.define_asset_job("taxi_job", selection=dg.AssetSelection.all())

taxi_schedule = dg.ScheduleDefinition(
    job=taxi_job,
    cron_schedule="0 6 * * *",                       # tous les jours à 06:00
    default_status=dg.DefaultScheduleStatus.STOPPED,  # à activer dans l'interface
)

defs = dg.Definitions(
    assets=[raw_trips, clean_trips, loaded_trips, daily_report],
    jobs=[taxi_job],
    schedules=[taxi_schedule],
    resources={"warehouse": Warehouse(db_url=dg.EnvVar("WAREHOUSE_DB_URL"))},
)
