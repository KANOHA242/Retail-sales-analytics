import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path(__file__).resolve().parents[2]/ "data" / "raw"

def load_data(path):
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    return pd.read_csv(path, encoding="cp1252")
       
        
def profile_data(data):
    shape = data.shape
    colonnes = data.columns.tolist()
    dtypes = data.dtypes.astype(str).to_dict()
    valeurs_manquantes = data.isna().sum().to_dict()
    doublons= int(data.duplicated().sum())
    profile = {
        "shape": shape,
        "columns": colonnes,
        "dtypes": dtypes,
        "valeurs_manquantes": valeurs_manquantes,
        "doublons": doublons
    }

    return profile

def print_report(profile):
    print("Profilage des données :")
    print(f"Forme : {profile['shape']}")
    print(f"Colonnes : {profile['columns']}")
    print(f"Types de données : {profile['dtypes']}")
    print(f"Valeurs manquantes : {profile['valeurs_manquantes']}")
    print(f"Doublons : {profile['doublons']}")

if __name__ == "__main__":
    data_path = RAW_DATA_DIR / "superstore.csv"
    data = load_data(data_path)
    profile = profile_data(data)
    print_report(profile)