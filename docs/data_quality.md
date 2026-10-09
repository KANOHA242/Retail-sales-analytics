# Data Quality Report — Sample Superstore

Diagnostic de qualité du fichier brut, établi **avant toute transformation**.
Il sert de référence pour les étapes de validation et de transformation du pipeline.

## 1. Source

| Élément | Valeur |
|---------|--------|
| Dataset | Superstore Dataset (Kaggle) — fichier d'origine `Sample - Superstore.csv` |
| Lien | https://www.kaggle.com/datasets/vivek468/superstore-dataset-final |
| Téléchargé le | 2026-10-09 |
| Emplacement | `data/raw/superstore.csv` (renommé, contenu jamais modifié) |
| Encodage | `cp1252` (Windows-1252), pas UTF-8 |

**Pourquoi l'encodage compte :** le fichier contient des caractères non ASCII
(espaces insécables, lettres accentuées comme dans `Französisch`, guillemets typographiques `“ ”`).
Lu en UTF-8, le chargement échoue (`UnicodeDecodeError`). `latin-1` permet de le lire,
mais décode mal les guillemets `“ ”` (octets `0x93` / `0x94`), qui deviennent des caractères de contrôle invisibles.
`cp1252` décode correctement tous les caractères du fichier.

## 2. Vue d'ensemble

| Indicateur | Valeur |
|------------|--------|
| Lignes | 9 994 |
| Colonnes | 21 |
| Période des commandes | 03/01/2014 → 30/12/2017 (4 années complètes) |
| Pays | 1 (United States) |
| Commandes distinctes | 5 009 |
| Clients distincts | 793 |
| Produits distincts (`Product ID`) | 1 862 |

**Granularité : une ligne = un produit dans une commande** (ligne de commande).
Une commande contient en moyenne 2 lignes (de 1 à 14).
`Order ID` n'est donc **pas** unique par ligne.

Répartition des lignes par année : 2014 : 1 993 · 2015 : 2 102 · 2016 : 2 587 · 2017 : 3 312.

## 3. Dictionnaire des colonnes

| Colonne | Type brut | Description | Remarque |
|---------|-----------|-------------|----------|
| Row ID | int64 | Numéro de ligne (1 à 9 994) | Identifiant technique, sans valeur métier |
| Order ID | str | Identifiant de commande | Non unique : plusieurs lignes par commande |
| Order Date | str | Date de commande | Texte au format `M/D/YYYY` → à convertir |
| Ship Date | str | Date d'expédition | Texte au format `M/D/YYYY` → à convertir |
| Ship Mode | str | Mode de livraison | 4 valeurs : Standard Class, Second Class, First Class, Same Day |
| Customer ID | str | Identifiant client | 793 clients |
| Customer Name | str | Nom du client | Donnée personnelle, inutile pour l'analyse |
| Segment | str | Segment client | 3 valeurs : Consumer, Corporate, Home Office |
| Country | str | Pays | Une seule valeur (United States), aucun intérêt analytique |
| City | str | Ville | 531 villes |
| State | str | État | 49 États |
| Postal Code | int64 | Code postal | Identifiant stocké comme nombre → zéros initiaux perdus |
| Region | str | Région | 4 valeurs : Central, East, South, West |
| Product ID | str | Identifiant produit | Pas parfaitement cohérent avec `Product Name` (voir §5) |
| Category | str | Catégorie | 3 valeurs : Furniture, Office Supplies, Technology |
| Sub-Category | str | Sous-catégorie | 17 valeurs |
| Product Name | str | Nom du produit | 1 850 noms distincts |
| Sales | float64 | Chiffre d'affaires de la ligne | De 0,44 à 22 638,48 |
| Quantity | int64 | Quantité | De 1 à 14 |
| Discount | float64 | Taux de remise | De 0 à 0,8 (12 niveaux distincts) |
| Profit | float64 | Profit de la ligne | De -6 599,98 à 8 399,98, négatif possible |

## 4. Contrôles effectués

| Contrôle | Résultat | Commentaire |
|----------|----------|-------------|
| Valeurs manquantes | 0 dans toutes les colonnes | Aucun traitement nécessaire |
| Doublons (lignes complètes) | 0 | Peu significatif : `Row ID` rend chaque ligne unique |
| Doublons (hors `Row ID`) | **1 paire** (Row ID 3406 et 3407) | Commande `US-2014-150119`, même produit, mêmes valeurs |
| Unicité de `Row ID` | OK | 1 à 9 994, sans trou |
| Cohérence des dates | OK | `Ship Date` ≥ `Order Date` sur toutes les lignes ; délai de 0 à 7 jours |
| Cohérence au niveau commande | OK | Un `Order ID` a toujours le même client, la même date et le même mode de livraison |
| `Customer ID` ↔ `Customer Name` | OK | Un nom par identifiant |
| `Product ID` ↔ `Product Name` | **Incohérent** | 32 `Product ID` ont plusieurs noms ; 16 noms ont plusieurs `Product ID` |
| Valeurs numériques | OK | `Sales` > 0, `Quantity` ≥ 1, `Discount` entre 0 et 0,8 |
| Profits négatifs | 1 871 lignes (18,7 %) | Attendu dans ce dataset, pas une erreur : à analyser, pas à supprimer |

## 5. Problèmes identifiés et actions prévues

| Problème | Impact | Action (étape transformation) |
|----------|--------|-------------------------------|
| `Order Date` et `Ship Date` en texte | Impossible d'analyser par mois/année ou de calculer un délai | Convertir en date avec le format explicite `%m/%d/%Y` |
| `Postal Code` stocké en nombre | 449 codes de Nouvelle-Angleterre / New Jersey perdent leur zéro initial (`02108` → `2108`) | Convertir en texte sur 5 caractères avec zéros à gauche |
| Doublon potentiel (Row ID 3406 / 3407) | Ventes et profit comptés deux fois si c'est une erreur | À trancher : vrai doublon ou deux lignes légitimes ? Documenter la décision |
| `Product ID` non unique par nom | Un « top produits » par `Product ID` peut mélanger deux produits | Pour le classement des produits, regrouper sur `Product ID` + `Product Name` |
| `Row ID`, `Country` sans valeur analytique | Bruit dans les tables | Peuvent être exclues des tables analytiques |
| Noms de colonnes avec espaces et tirets | Requêtes SQL (DuckDB) moins pratiques | Renommer en `snake_case` (`order_date`, `sub_category`…) |
| Encodage `cp1252` | Caractères corrompus si mal lu | Toujours lire avec `encoding="cp1252"` |

## 6. Points d'attention pour l'analyse

- **Nombre de commandes** = nombre de `Order ID` **distincts** (5 009), pas le nombre de lignes (9 994).
- **Nombre de clients** = nombre de `Customer ID` distincts (793).
- **Panier moyen** (Average Order Value) = ventes totales ÷ nombre de commandes distinctes.
- **Profit moyen par commande** : même logique, diviser par les commandes distinctes.
- **Marge** = profit total ÷ ventes totales (calcul sur les totaux, pas moyenne des marges par ligne).
- **Croissance du volume** : le nombre de lignes passe de 1 993 (2014) à 3 312 (2017), à garder en tête en comparant les années.
