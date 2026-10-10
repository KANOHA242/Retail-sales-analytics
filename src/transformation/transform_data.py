import pandas as pd
from pathlib import Path
from src.ingestion.load_data import load_data, RAW_DATA_DIR

PROCESSED_DATA_DIR = Path(__file__).resolve().parents[2]/ "data" / "processed"

#Fonction pour renommer les colonnes
def rename_columns(data):
    data.columns = data.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
    return data

def convert_types(data):
    data['order_date'] = pd.to_datetime(data['order_date'], format="%m/%d/%Y")
    data['ship_date'] = pd.to_datetime(data['ship_date'], format="%m/%d/%Y")
    data['postal_code'] = data['postal_code'].astype(str).str.zfill(5)  
    return data

def add_features(data):
    data['order_year'] = data['order_date'].dt.year
    data['order_month'] = data['order_date'].dt.month
    data['shipping_days'] = (data['ship_date'] - data['order_date']).dt.days
    return data

def transform(data):
    data = rename_columns(data)
    data = convert_types(data)
    data = add_features(data)
    return data


if __name__ == "__main__":
    # Charger les données brutes
    df = load_data(RAW_DATA_DIR / "superstore.csv")
    df = transform(df)
    # Sauvegarder les données transformées
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / "superstore_clean.parquet"
    df.to_parquet(output_path, index=False)
    print(f"Données transformées sauvegardées dans {output_path}")
    print(f"Nombre de lignes : {len(df)}")
