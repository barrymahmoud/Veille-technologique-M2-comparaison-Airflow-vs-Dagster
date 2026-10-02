"""Logique métier du pipeline, indépendante de tout orchestrateur.
Airflow et Dagster appelleront ces mêmes fonctions : la comparaison porte
ainsi sur l'orchestration, pas sur le code métier."""
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

TIME_COLS = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def extract(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path, parse_dates=TIME_COLS)


def clean(df: pd.DataFrame, month_start="2024-01-01", month_end="2024-02-01"):
    """Retourne (lignes propres, lignes rejetées avec motif)."""
    rules = {
        "distance_invalide": df.trip_distance <= 0,
        "montant_invalide": (df.fare_amount <= 0) | (df.total_amount <= 0),
        "passagers_invalides": df.passenger_count.isna() | (df.passenger_count <= 0),
        "dates_incoherentes": df.tpep_dropoff_datetime < df.tpep_pickup_datetime,
        "hors_periode": ~df.tpep_pickup_datetime.between(month_start, month_end, inclusive="left"),
    }
    reason = pd.Series("", index=df.index)
    for name, mask in rules.items():
        reason = reason.where(~mask, reason + name + ";")
    bad = reason != ""
    rejected = df[bad].assign(motif_rejet=reason[bad])
    clean_df = df[~bad].copy()
    clean_df["duree_min"] = (
        clean_df.tpep_dropoff_datetime - clean_df.tpep_pickup_datetime
    ).dt.total_seconds() / 60
    return clean_df, rejected


def load(df: pd.DataFrame, db_url: str, table: str = "trips_clean") -> int:
    engine = create_engine(db_url)
    df.to_sql(table, engine, if_exists="replace", index=False, chunksize=10_000)
    return len(df)


def report(db_url: str, out_path: str, table: str = "trips_clean") -> str:
    engine = create_engine(db_url)
    df = pd.read_sql(f"SELECT * FROM {table}", engine, parse_dates=TIME_COLS)
    df["jour"] = df.tpep_pickup_datetime.dt.date
    daily = df.groupby("jour").agg(
        courses=("trip_distance", "size"),
        distance_moy=("trip_distance", "mean"),
        recette=("total_amount", "sum"),
    ).round(2)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(out_path)
    return out_path
