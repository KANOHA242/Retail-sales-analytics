import sys

import pandas as pd

from src.ingestion.load_data import load_data, RAW_DATA_DIR

EXPECTED_COLUMNS = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 'State', 'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']
DATE_FORMAT = "%m/%d/%Y"


def check_expected_columns(df):
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    return {
        "check": "Colonnes attendues présentes",
        "level": "error",
        "passed": len(missing_columns) == 0,
        "details": missing_columns,
    }


def check_no_missing_values(df):
    missing = df.isna().sum()
    columns_with_missing = missing[missing > 0].to_dict()
    return {
        "check": "Aucune valeur manquante",
        "level": "error",
        "passed": len(columns_with_missing) == 0,
        "details": columns_with_missing,
    }


def check_row_id_unique(df):
    return {
        "check": "Row ID unique",
        "level": "error",
        "passed": df['Row ID'].is_unique,
        "details": None,
    }


def check_duplicates(df):
    # Row ID est différent sur chaque ligne : on l'exclut, sinon aucun doublon ne peut être trouvé
    duplicated = df.drop(columns="Row ID").duplicated(keep=False)
    return {
        "check": "Aucun doublon (hors Row ID)",
        "level": "warning",
        "passed": not duplicated.any(),
        "details": df.loc[duplicated, "Row ID"].tolist(),
    }


def check_numeric_ranges(df):
    invalid = {
        "Sales <= 0": int((df['Sales'] <= 0).sum()),
        "Quantity < 1": int((df['Quantity'] < 1).sum()),
        "Discount hors [0, 1]": int((~df['Discount'].between(0, 1)).sum()),
    }
    invalid = {rule: count for rule, count in invalid.items() if count > 0}
    return {
        "check": "Valeurs numériques valides",
        "level": "error",
        "passed": len(invalid) == 0,
        "details": invalid,
    }


def check_ship_after_order(df):
    # Conversion locale : la conversion des colonnes est le rôle de la transformation
    order_date = pd.to_datetime(df['Order Date'], format=DATE_FORMAT)
    ship_date = pd.to_datetime(df['Ship Date'], format=DATE_FORMAT)
    invalid = ship_date < order_date
    return {
        "check": "Ship Date >= Order Date",
        "level": "error",
        "passed": not invalid.any(),
        "details": df.loc[invalid, "Row ID"].tolist(),
    }


def check_one_customer_per_order(df):
    customers_per_order = df.groupby('Order ID')['Customer ID'].nunique()
    invalid_orders = customers_per_order[customers_per_order > 1]
    return {
        "check": "Un seul client par commande",
        "level": "error",
        "passed": invalid_orders.empty,
        "details": invalid_orders.index.tolist(),
    }


def check_one_name_per_product(df):
    names_per_product = df.groupby('Product ID')['Product Name'].nunique()
    invalid_products = names_per_product[names_per_product > 1]
    return {
        "check": "Un seul nom par Product ID",
        "level": "warning",
        "passed": invalid_products.empty,
        "details": f"{len(invalid_products)} Product ID avec plusieurs noms",
    }


def run_all_checks(df):
    return [
        check_expected_columns(df),
        check_no_missing_values(df),
        check_row_id_unique(df),
        check_duplicates(df),
        check_numeric_ranges(df),
        check_ship_after_order(df),
        check_one_customer_per_order(df),
        check_one_name_per_product(df),
    ]


def print_results(results):
    for result in results:
        if result["passed"]:
            status = "PASS"
        elif result["level"] == "error":
            status = "ERREUR"
        else:
            status = "AVERTISSEMENT"
        print(f"[{status}] {result['check']}")
        if not result["passed"]:
            print(f"    Détails: {result['details']}")


def has_errors(results):
    return any(result["level"] == "error" and not result["passed"] for result in results)


if __name__ == "__main__":
    df = load_data(RAW_DATA_DIR / "superstore.csv")

    # Sans les colonnes attendues, les autres contrôles planteraient
    columns_result = check_expected_columns(df)
    if not columns_result["passed"]:
        print_results([columns_result])
        sys.exit(1)

    results = run_all_checks(df)
    print_results(results)

    if has_errors(results):
        print("\nValidation échouée.")
        sys.exit(1)
    print("\nValidation réussie.")
