"""Prépare airflow/ : patche docker-compose.yaml et complète .env.
À lancer UNE fois depuis le dossier airflow :  py setup_airflow.py
Sans effet si déjà appliqué. Une sauvegarde docker-compose.yaml.bak est créée."""
import base64, os, shutil
from pathlib import Path

COMPOSE, ENV = Path("docker-compose.yaml"), Path(".env")

WAREHOUSE = """  warehouse:
    image: postgres:16
    environment:
      POSTGRES_USER: warehouse
      POSTGRES_PASSWORD: warehouse
      POSTGRES_DB: warehouse
    ports:
      - "5433:5432"
    volumes:
      - warehouse-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "warehouse"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

"""

REPLACEMENTS = [
    ("AIRFLOW__CORE__LOAD_EXAMPLES: 'true'", "AIRFLOW__CORE__LOAD_EXAMPLES: 'false'"),
    ("    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins\n",
     "    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins\n"
     "    - ../src:/opt/airflow/src\n    - ../data:/opt/airflow/data\n"),
    ("\nservices:\n", "\nservices:\n" + WAREHOUSE.rstrip("\n") + "\n\n"),
    ("\nvolumes:\n  postgres-db-volume:", "\nvolumes:\n  postgres-db-volume:\n  warehouse-db-volume:"),
]

text = COMPOSE.read_text(encoding="utf-8")          # normalise CRLF -> LF
if "warehouse-db-volume" in text:
    print("docker-compose.yaml déjà patché : rien à faire.")
else:
    shutil.copy(COMPOSE, "docker-compose.yaml.bak")
    for old, new in REPLACEMENTS:
        if text.count(old) != 1:
            raise SystemExit(f"ERREUR : motif introuvable ou ambigu :\n{old!r}\n"
                             "Colle ton docker-compose.yaml dans le chat.")
        text = text.replace(old, new)
    COMPOSE.write_text(text, encoding="utf-8", newline="\n")
    print("docker-compose.yaml patché (4 modifications). Sauvegarde : .bak")

# --- .env : on ajoute seulement les clés manquantes ---
env = {}
if ENV.exists():
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v
defaults = {
    "AIRFLOW_UID": "50000",
    "AIRFLOW_PROJ_DIR": ".",
    "_PIP_ADDITIONAL_REQUIREMENTS": "pandas pyarrow sqlalchemy",
    "FERNET_KEY": base64.urlsafe_b64encode(os.urandom(32)).decode(),
    "WAREHOUSE_DB_URL": "postgresql+psycopg2://warehouse:warehouse@warehouse:5432/warehouse",
}
added = [k for k in defaults if k not in env]
for k in added:
    env[k] = defaults[k]
ENV.write_text("\n".join(f"{k}={v}" for k, v in env.items()) + "\n", encoding="utf-8", newline="\n")
print(".env : clés ajoutées ->", added or "aucune")

# --- .gitignore (racine du projet) ---
gi = Path("../.gitignore")
wanted = ["airflow/.env", "airflow/logs/", "airflow/docker-compose.yaml.bak", "data/staging/"]
cur = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
new = [w for w in wanted if w not in cur]
if new:
    gi.write_text("\n".join(cur + new) + "\n", encoding="utf-8", newline="\n")
    print(".gitignore : ajouté ->", new)