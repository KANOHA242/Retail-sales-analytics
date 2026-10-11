# Insights — Sample Superstore (2014–2017)

Constats tirés de l'analyse SQL (DuckDB) des données nettoyées `data/processed/superstore_clean.parquet`.
Chaque constat indique la requête qui le produit, ce que les données **montrent**, et ce qu'elles **ne permettent pas** de conclure.

---

## Synthèse

> L'entreprise est rentable (12,5 % de marge) et en croissance, mais une partie importante de son profit est perdue à cause de **remises plus élevées que ce que certains produits peuvent absorber**. Ce problème est concentré sur la sous-catégorie **Tables** et sur la région **Central**.

| Constat | Chiffre clé |
|---------|-------------|
| Les remises ≥ 30 % sont toutes déficitaires | **−135 376 $** de profit sur 1 393 lignes |
| Furniture vend beaucoup mais rapporte peu | 32 % des ventes, **6 % du profit** |
| Tables est la sous-catégorie la plus déficitaire | **−17 725 $** (marge −8,6 %) |
| Central est la région la moins rentable | marge **7,9 %**, remise moyenne **24 %** |

---

## 1. Vue d'ensemble

*Requêtes : `kpis.sql`, `sales_by_month.sql`*

| KPI | Valeur |
|-----|--------|
| Ventes totales | 2 297 201 $ |
| Profit total | 286 397 $ |
| Marge | 12,5 % |
| Commandes | 5 009 |
| Clients | 793 |
| Panier moyen | 458,61 $ |

**Évolution annuelle**

| Année | Ventes | Profit | Marge | Commandes |
|-------|--------|--------|-------|-----------|
| 2014 | 484 248 $ | 49 544 $ | 10,2 % | 969 |
| 2015 | 470 533 $ | 61 619 $ | 13,1 % | 1 038 |
| 2016 | 609 206 $ | 81 795 $ | 13,4 % | 1 315 |
| 2017 | 733 215 $ | 93 439 $ | 12,7 % | 1 687 |

- Entre 2014 et 2017, les ventes progressent de **+51 %** et le profit de **+89 %** : le profit croît plus vite que les ventes.
- 2015 est la seule année où les ventes reculent légèrement (−2,8 %), alors que le profit augmente.
- Deux mois sont déficitaires : **juillet 2014** (−841 $) et **janvier 2015** (−3 281 $, marge −18 %). Non expliqué à ce stade.

## 2. Saisonnalité

*Requête : `sales_seasonality.sql`*

- Les ventes sont concentrées en fin d'année : le **4ᵉ trimestre représente 38 %** des ventes, contre 16 % pour le 1ᵉʳ.
- Les mois les plus forts sont **novembre, décembre et septembre** ; le plus faible est **février**.

⚠️ Les données montrent *quand* les ventes ont lieu, pas *pourquoi*. Aucune cause (fêtes, rentrée, budgets d'entreprise…) ne peut être affirmée à partir de ce dataset.

## 3. Performance par région

*Requête : `sales_by_region.sql`*

| Région | Ventes | Profit | Marge | Remise moyenne |
|--------|--------|--------|-------|----------------|
| West | 725 458 $ | 108 418 $ | 14,9 % | 10,9 % |
| East | 678 781 $ | 91 523 $ | 13,5 % | 14,5 % |
| Central | 501 240 $ | 39 706 $ | **7,9 %** | **24,0 %** |
| South | 391 722 $ | 46 749 $ | 11,9 % | 14,7 % |

- **Central** est 3ᵉ en ventes mais dernière en marge, et dégage moins de profit que South alors qu'elle vend 110 k$ de plus.
- C'est aussi la région qui remise le plus : **24 %** en moyenne, et **28 % de ses lignes** ont une remise ≥ 30 % (contre 4 % pour West).
- Sans remise, Central a une marge de **31 %**, la plus élevée des quatre régions. Sa faible rentabilité ne semble donc pas venir de ses produits ou de ses prix, mais de **sa politique de remise**.

## 4. Performance par catégorie et sous-catégorie

*Requêtes : `sales_by_category.sql`, `profit_by_subcategory.sql`*

| Catégorie | Ventes | Profit | Marge | Part des ventes | Part du profit |
|-----------|--------|--------|-------|-----------------|----------------|
| Technology | 836 154 $ | 145 455 $ | 17,4 % | 36 % | 51 % |
| Office Supplies | 719 047 $ | 122 491 $ | 17,0 % | 31 % | 43 % |
| Furniture | 742 000 $ | 18 451 $ | **2,5 %** | 32 % | **6 %** |

- **Furniture** génère un tiers des ventes mais seulement 6 % du profit.
- Le problème n'est pas toute la catégorie : il est concentré sur **Tables** (−17 725 $) et **Bookcases** (−3 473 $). Chairs (8,1 %) et Furnishings (14,2 %) restent rentables.
- 3 sous-catégories sur 17 sont déficitaires : **Tables, Bookcases, Supplies**.
- **Machines** est techniquement rentable mais sa marge est presque nulle (1,8 % sur 189 k$ de ventes).

## 5. Remises et rentabilité

*Requête : `profit_by_discount.sql`*

| Remise | Lignes | Marge |
|--------|--------|-------|
| 0 % | 4 798 | +29,5 % |
| 10 – 20 % | 3 803 | +5 % à +17 % |
| 30 – 50 % | 537 | −10 % à −45 % |
| 60 – 80 % | 856 | −89 % à −180 % |

- La marge diminue à mesure que la remise augmente, et **devient négative dès 30 % de remise**.
- Les remises ≥ 30 % concernent **1 393 lignes (14 %)** et représentent une perte cumulée de **135 376 $**, soit l'équivalent de 47 % du profit total.
- Ces niveaux ne sont pas marginaux : la remise de 70 % concerne à elle seule 418 lignes (−40 075 $).

## 6. Pourquoi certaines remises font perdre de l'argent

*Requête : `profit_by_subcategory.sql` (colonnes `avg_discount` et `margin_no_discount`)*

Une forte remise ne mène pas toujours à une perte. Ce qui compte, c'est **la remise par rapport à la marge de base du produit** (marge mesurée sur les ventes sans remise).

| Sous-catégorie | Marge sans remise | Remise moyenne | Marge réelle | Diagnostic |
|----------------|-------------------|----------------|--------------|------------|
| Tables | 18,6 % | 26,1 % | −8,6 % | remise > marge de base → perte |
| Bookcases | 19,0 % | 21,1 % | −3,0 % | remise > marge de base → perte |
| Supplies | 5,4 % | 7,7 % | −2,5 % | marge de base trop faible |
| Binders | 48,0 % | 37,2 % | +14,9 % | marge de base élevée, absorbe la remise |

**Règle observée : une sous-catégorie devient déficitaire lorsque sa remise moyenne dépasse sa marge de base.**

Deux problèmes distincts apparaissent :
- **Tables et Bookcases** sont rentables sans remise : ce sont **les remises** qui les font basculer en perte.
- **Supplies** a une marge de base de seulement 5 % : même de faibles remises suffisent. Le problème est **structurel** (prix ou coût).

---

## Recommandations

| # | Recommandation | Justification |
|---|----------------|---------------|
| 1 | **Plafonner les remises** à 20 % maximum (aucune remise ≥ 30 % n'est rentable) | 135 k$ perdus sur les remises ≥ 30 % |
| 2 | **Encadrer les remises sur Tables et Bookcases** sous leur marge de base (~19 %) | ces sous-catégories sont rentables sans remise |
| 3 | **Revoir la politique de remise de la région Central** | remise moyenne de 24 %, alors que sa marge sans remise est la plus élevée des 4 régions (31 %) |
| 4 | **Revoir le prix ou le coût d'achat de Supplies** | marge de base de 5 %, le problème ne vient pas des remises |
| 5 | **Surveiller Machines** | 1,8 % de marge avec 31 % de remise moyenne |

---

## Limites de l'analyse

- **Pas de coût d'achat dans le dataset** : la « marge sans remise » est estimée à partir des ventes non remisées, ce n'est pas un coût réel.
- **Association, pas causalité** : les données montrent que les fortes remises sont *associées* aux pertes. Elles ne disent pas pourquoi ces remises ont été accordées (déstockage, fidélisation, concurrence…), ni ce qui se serait passé sans elles (ventes perdues ?).
- **`AVG(discount)` est une moyenne par ligne**, non pondérée par le montant des ventes.
- **Les commandes ne s'additionnent pas entre catégories** : une commande peut contenir des produits de plusieurs catégories (7 050 au total par catégorie contre 5 009 commandes réelles).

## Pistes non explorées

- Pourquoi janvier 2015 est-il déficitaire ?
- Analyse par segment client (Consumer, Corporate, Home Office) — prévue pour le Dashboard 4.
- Top / flop produits au sein de Tables.
