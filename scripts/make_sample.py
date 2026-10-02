"""Échantillon reproductible de 100 000 lignes (à lancer une seule fois)."""
import sys
from pathlib import Path
import pandas as pd

src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw/yellow_tripdata_2024-01.parquet")
out = Path("data/raw/taxi_sample.csv")
df = pd.read_parquet(src)
df.sample(n=100_000, random_state=42).to_csv(out, index=False)
print(f"{len(df)} lignes source -> {out} (100000 lignes)")
