"""Pipeline de référence en Python pur (sans orchestrateur)."""
import time, sys
from core import extract, clean, load, report

DB = sys.argv[1] if len(sys.argv) > 1 else "sqlite:///data/test.db"
t = time.perf_counter()
df = extract("data/raw/taxi_sample.csv");           print("extract ", len(df))
ok, ko = clean(df);                                 print("clean   ", len(ok), "ok /", len(ko), "rejetées")
ko.to_csv("data/reports/rejected.csv", index=False)
print("load    ", load(ok, DB))
print("report  ", report(DB, "data/reports/daily.csv"))
print(f"total {time.perf_counter()-t:.1f}s")
