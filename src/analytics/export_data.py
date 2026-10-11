from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql" / "analytics"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "superstore_clean.parquet"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"

def export_query(sql_file):
    query = sql_file.read_text(encoding="utf-8")
    duckdb.sql(query)
    result = duckdb.sql(query).df()
    export_file = EXPORT_DIR / f"{sql_file.stem}.csv"
    result.to_csv(export_file, index=False)
    print(f"Exporté : {export_file.name}")

def export_clean_table():
    df = duckdb.sql(f"SELECT * FROM '{PROCESSED_FILE}'").df()
    export_file = EXPORT_DIR / "superstore_clean.csv"
    df.to_csv(export_file, index=False)
    print(f"Exporté : {export_file.name}")


if __name__ == "__main__":
    # créer EXPORT_DIR s'il n'existe pas
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        export_query(sql_file)
    export_clean_table()

