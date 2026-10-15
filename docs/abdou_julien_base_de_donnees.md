# Scripts SQL / PostGIS fréquents en géomatique 

> **Public** : équipe géomatique / urbanisme (AUDC 51) · **SGBD** : PostgreSQL + PostGIS · **Clients** : pgAdmin, DBeaver, QGIS (DB Manager)
> **Objet** : bibliothèque de requêtes **commentées, testées dans leur logique et corrigées**, avec pour chacune l'objectif, le principe, les pièges et une illustration.
> Les illustrations sont dans le dossier `img/` (fichiers PNG réutilisables dans vos présentations).

---

## Comment utiliser cette page

Chaque fiche suit le même plan, pour qu'on retrouve toujours l'information au même endroit :

| Bloc | Contenu |
|---|---|
| **Objectif** | La question métier à laquelle la requête répond |
| **Principe** | Les fonctions utilisées et pourquoi |
| **Prérequis** | Ce qu'il faut vérifier avant (SRID, index, validité) |
| **Code SQL** | Version robuste, prête à adapter |
| **Lecture du résultat** | Comment interpréter ce qu'on obtient |
| **Pièges** | Les erreurs classiques |

**Conventions de lecture**

- Les noms de schémas, tables et colonnes (`village.parcel`, `carthage.cours`, `geom`…) sont ceux de notre base. Adaptez-les si besoin.
- Une valeur entre `/* … */` ou un commentaire `-- À ADAPTER` signale un paramètre à vérifier (code de zone, SRID…).
- Les numéros de fiche (1 à 17) sont **conservés** par rapport à l'ancienne version ; les fiches **18 à 26** sont nouvelles ou réorganisées.

### Jeu de données utilisé

| Schéma | Table | Contenu | Type de géométrie |
|---|---|---|---|
| `village` | `parcel` | Parcelles cadastrales (`numpar`) | Polygones |
| `village` | `bati` | Bâtiments | Polygones |
| `village` | `o_usees` | Réseau d'eaux usées | Lignes |
| `village` | `pos` | Zonage PLU (zones ND…) | Polygones |
| `carthage` | `cours` | Cours d'eau BD Carthage (`nomentiteh`, `classe`) | Lignes |
| `corine` | `clc` | Corine Land Cover (`code_18`) | Polygones |
| `departement` | `departements` | Départements (`code_insee`, `nom`) | Polygones |
| `arbres` | `mobilier` | Mobilier urbain (`id_parcelle`, `id_type_mobilier`) | Points / attributaire |

### Sommaire des fiches

| Partie | Fiches |
|---|---|
| **A. Préparer et contrôler la base** | 1 Index · 2 Vue matérialisée simplifiée · 3 SRID · 19 Inventaire des couches · 20 Validité des géométries |
| **B. Mesurer** | 4 Longueur du réseau · 5 Périmètre des zones ND |
| **C. Sélectionner par relation spatiale** | 6 Parcelles traversées · 7 Parcelles bâties · 8 Départements traversés · 9 Parcelles voisines · 10 Zones autour des tourbières |
| **D. Distances et proximité** | 11 Zones industrielles / Garonne · 12 Bâtiment le plus proche · 21 Tampons |
| **E. Fabriquer de nouvelles géométries** | 13 Périmètre non touché · 14 Découpage par département · 15 Segments de 10 km · 22 Fusion (dissolve) · 24 Centroïdes |
| **F. Compter et agréger** | 16 Comptages avancés · 23 Bâtiments par parcelle |
| **G. Automatiser** | 17 Triggers · 18 Fonctions temporelles |
| **H. Diffuser et optimiser** | 25 Vue pour QGIS · 26 Lire un plan d'exécution |
| **Annexes** | Erreurs fréquentes · Check-list · Glossaire · Journal des corrections |

---

## 0. Les fondamentaux avant d'écrire une requête

### 0.1 La démarche en 7 étapes

<img width="1987" height="878" alt="01_demarche_requete" src="https://github.com/user-attachments/assets/8b848329-f098-4ba7-a1cc-cbac9f5ea858" />

1. **Question** : formuler ce qu'on veut mesurer ou sélectionner, avec l'unité attendue (m, km, ha, nombre).
2. **Couches** : identifier schéma, table et colonne géométrique.
3. **SRID** : connaître le système de coordonnées (fiche 3) pour savoir dans quelle unité sortent les mesures.
4. **Géométries** : vérifier qu'elles sont valides (fiche 20).
5. **Index** : s'assurer qu'un index GIST existe sur chaque colonne géométrique.
6. **Requête** : écrire en CTE lisibles, avec le prédicat adapté (voir 0.4).
7. **Contrôle** : `EXPLAIN ANALYZE` (fiche 26), puis publier une vue pour QGIS (fiche 25).

### 0.2 SRID et unités : la source d'erreurs n°1

<img width="1987" height="908" alt="04_srid_unites" src="https://github.com/user-attachments/assets/730d9101-5540-437e-8331-8c94a3d37aec" />

`ST_Length`, `ST_Area`, `ST_Perimeter`, `ST_Distance`, `ST_DWithin`, `ST_Simplify` et `ST_Buffer` **travaillent dans l'unité du SRID** de la géométrie.

| SRID | Unité | Conséquence |
|---|---|---|
| 2154 (Lambert-93) | mètre | Les mesures sont directement en m / m² |
| 3035 (ETRS89-LAEA) | mètre | Idem (projection de Corine Land Cover) |
| 4326 (WGS 84) | **degré** | Une « tolérance de 20 » = 20 degrés. Il faut reprojeter ou utiliser `geography` |

Deux couches de SRID différents ne peuvent pas être comparées directement (`Operation on mixed SRID geometries`). On reprojette **un seul côté**, de préférence la plus petite couche :

```sql
ST_Transform(c.geom, Find_SRID('corine', 'clc', 'geom'))
```

> ⚠️ `ST_Transform(colonne, …)` dans une jointure empêche l'utilisation de l'index sur cette colonne. Si la requête est fréquente, créez une vue ou une colonne déjà reprojetée.

### 0.3 Comment PostGIS accélère les requêtes : l'index GIST

<img width="1841" height="920" alt="02_index_gist_deux_etapes" src="https://github.com/user-attachments/assets/c4b01cf3-8bea-47e5-9a8e-edd431ec6ea7" />

PostGIS procède en **deux temps** :

1. **Filtre rapide** : l'index GIST compare uniquement les rectangles englobants (*bounding boxes*) et élimine l'immense majorité des entités.
2. **Test exact** : le prédicat (`ST_Intersects`, `ST_Contains`…) n'est calculé que sur les candidates restantes.

Sans index, l'étape 2 est lancée sur **toutes** les entités : sur des couches de plusieurs centaines de milliers d'objets, la différence se compte en minutes.

Modèle à copier pour chaque couche :

```sql
CREATE INDEX IF NOT EXISTS idx_parcel_geom ON village.parcel USING GIST (geom);
VACUUM ANALYZE village.parcel;   -- met à jour les statistiques du planificateur
```

### 0.4 Quel prédicat ou quelle fonction choisir ?

<img width="2062" height="1118" alt="12_arbre_decision_fonctions" src="https://github.com/user-attachments/assets/69252f49-24b6-4d26-8ff5-44aa31c49fd0" />

<img width="1836" height="1258" alt="03_predicats_spatiaux" src="https://github.com/user-attachments/assets/597b2b74-4cb7-4f45-8b50-4ca7dbf138cd" />

| Question posée | Fonction | Remarque |
|---|---|---|
| Les deux objets se croisent ou se touchent ? | `ST_Intersects(a, b)` | Le plus général, utilise l'index |
| B est-il entièrement dans A ? | `ST_Contains(a, b)` / `ST_Within(b, a)` | Un bâtiment à cheval sur deux parcelles n'est contenu dans aucune |
| Contact par la bordure uniquement ? | `ST_Touches(a, b)` | Exclut les chevauchements |
| Recouvrement partiel ? | `ST_Overlaps(a, b)` | Même dimension requise (polygone / polygone) |
| À moins de X unités ? | `ST_DWithin(a, b, X)` | **À préférer** à `ST_Distance(...) < X` (index) |
| Aucun point commun ? | `NOT ST_Intersects(a, b)` | Préférer à `ST_Disjoint` (index) |
| Distance exacte ? | `ST_Distance(a, b)` | Ne pas filtrer dessus : utiliser `ST_DWithin` |
| Objet le plus proche ? | `ORDER BY a.geom <-> b.geom LIMIT 1` | Avec `LATERAL` (fiche 12) |

---

## A. Préparer et contrôler la base

### 1. Création d'index

#### Objectif

Accélérer les recherches de parcelles par leur numéro (`numpar`), en particulier la parcelle `c10436`.

#### Principe

Un index **B-Tree** accélère les comparaisons d'égalité et d'ordre sur du texte. Mais :

- `ILIKE` (insensible à la casse) **n'utilise pas** un index B-Tree classique ;
- un index **partiel** (`WHERE …`) est plus petit, mais n'est utilisé que si la requête contient **exactement le même prédicat**.

Trois options selon le besoin :

| Besoin | Solution |
|---|---|
| Recherche exacte, insensible à la casse | Index sur `lower(numpar)` (**recommandé**) |
| Recherche très ciblée sur une seule parcelle | Index partiel (version d'origine) |
| Recherche « contient » (`ILIKE '%436%'`) | Index trigramme `pg_trgm` |

#### Code SQL

```sql
-- Option 1 (recommandée) : index fonctionnel insensible à la casse
CREATE INDEX IF NOT EXISTS idx_parcel_numpar_lower
    ON village.parcel (lower(numpar));

-- La requête doit utiliser la MÊME expression pour profiter de l'index
SELECT *
FROM village.parcel
WHERE lower(numpar) = 'c10436';
```

```sql
-- Option 2 : index partiel (version d'origine, corrigée : les instructions étaient collées sur une ligne)
CREATE INDEX IF NOT EXISTS idx_parcel_numpar_c10436
    ON village.parcel (numpar)
    WHERE numpar ILIKE 'c10436';

-- Utilisé uniquement si la requête reprend le même prédicat
SELECT * FROM village.parcel WHERE numpar ILIKE 'c10436';
```

```sql
-- Option 3 : recherche partielle (ILIKE '%…%')
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX IF NOT EXISTS idx_parcel_numpar_trgm
    ON village.parcel USING GIN (numpar gin_trgm_ops);
```

#### Vérification

```sql
EXPLAIN SELECT * FROM village.parcel WHERE lower(numpar) = 'c10436';
-- On doit lire « Index Scan using idx_parcel_numpar_lower » et non « Seq Scan »
```

#### Pièges

- Sur une table de quelques centaines de lignes, PostgreSQL préfère parfois le `Seq Scan` : c'est normal.
- Pensez à `VACUUM ANALYZE village.parcel;` après création.

---

### 2. Vue matérialisée simplifiée

#### Objectif
Fournir à QGIS une couche des cours d'eau **allégée** pour accélérer l'affichage à petite échelle.

#### Principe

- `ST_Simplify(geom, tolérance)` supprime des sommets (algorithme de Douglas-Peucker). La tolérance est **dans l'unité du SRID** : 20 = 20 m en Lambert-93.
- Une **vue matérialisée** stocke physiquement le résultat : lecture rapide, mais à **rafraîchir** quand la source change.
- L'index spatial doit être créé **sur la vue matérialisée** (et non sur la table source, erreur de l'ancienne version).

<img width="1702" height="1319" alt="05_simplify_tolerance" src="https://github.com/user-attachments/assets/96292f6e-34d6-4635-8065-326e63d20f21" />

#### Prérequis

Vérifier le SRID (fiche 3). Si la couche est en 4326, **ne pas** utiliser une tolérance de 20.

#### Code SQL

```sql
-- 1) Contrôle de l'unité : doit renvoyer 2154 (mètres) pour une tolérance de 20 m
SELECT Find_SRID('carthage', 'cours', 'geom');

-- 2) Création de la vue matérialisée
CREATE MATERIALIZED VIEW IF NOT EXISTS carthage.cours_eau_simplifiee AS
SELECT gid,
       cdentitehy,
       nomentiteh,
       candidat,
       classe,
       ST_Multi(ST_Simplify(geom, 20)) AS geom     -- 20 m en Lambert-93
FROM carthage.cours
WHERE geom IS NOT NULL
WITH DATA;

-- 3) Index spatial SUR LA VUE (pas sur la table source)
CREATE INDEX IF NOT EXISTS idx_cours_eau_simplifiee_geom
    ON carthage.cours_eau_simplifiee USING GIST (geom);

-- 4) Identifiant unique : obligatoire pour QGIS et pour REFRESH ... CONCURRENTLY
CREATE UNIQUE INDEX IF NOT EXISTS idx_cours_eau_simplifiee_gid
    ON carthage.cours_eau_simplifiee (gid);

-- 5) Rafraîchir après mise à jour de carthage.cours
REFRESH MATERIALIZED VIEW CONCURRENTLY carthage.cours_eau_simplifiee;
```

#### Lecture du résultat

Comparez le nombre de sommets avant / après :

```sql
SELECT (SELECT SUM(ST_NPoints(geom)) FROM carthage.cours)                     AS sommets_origine,
       (SELECT SUM(ST_NPoints(geom)) FROM carthage.cours_eau_simplifiee)      AS sommets_simplifie;
```

#### Pièges

- Pour des **polygones**, préférer `ST_SimplifyPreserveTopology` : `ST_Simplify` peut produire des géométries invalides.
- Une vue matérialisée **ne se met pas à jour toute seule**.

---

### 3. Connaître le SRID d'une couche

#### Objectif

Identifier le système de référence spatiale d'une couche, donc l'unité de ses mesures.

#### Code SQL

```sql
-- SRID déclaré dans les métadonnées PostGIS
SELECT Find_SRID('carthage', 'cours', 'geom');

-- SRID réellement porté par les objets (peut différer en cas d'import défectueux)
SELECT DISTINCT ST_SRID(geom) FROM carthage.cours;

-- Détail du système (nom, unité) à partir du SRID
SELECT srid, auth_name, srtext
FROM spatial_ref_sys
WHERE srid = Find_SRID('carthage', 'cours', 'geom');
```

#### Lecture du résultat

- `2154` ou `3035` : unités en **mètres**.
- `4326` : unités en **degrés** → reprojeter (`ST_Transform`) avant toute mesure.
- `0` : SRID **non défini** → à corriger avec `ST_SetSRID` (sans reprojection) après avoir identifié le vrai système.

---

### 4. Inventaire des couches de la base *(nouveau)*

#### Objectif

Dresser en une requête la liste des couches, leur SRID, leur type de géométrie, et repérer celles qui n'ont **pas d'index spatial**.

#### Code SQL

```sql
-- 1) Inventaire des couches géométriques
SELECT f_table_schema AS schema,
       f_table_name   AS table,
       f_geometry_column AS colonne_geom,
       srid,
       type,
       coord_dimension AS dim
FROM geometry_columns
WHERE f_table_schema IN ('village', 'carthage', 'corine', 'departement', 'arbres')
ORDER BY f_table_schema, f_table_name;
```

```sql
-- 2) Colonnes géométriques SANS index (à indexer en priorité)
SELECT n.nspname AS schema,
       c.relname AS table,
       a.attname AS colonne_geom
FROM pg_attribute a
JOIN pg_class c      ON c.oid = a.attrelid
JOIN pg_namespace n  ON n.oid = c.relnamespace
JOIN pg_type t       ON t.oid = a.atttypid
WHERE t.typname IN ('geometry', 'geography')
  AND c.relkind IN ('r', 'm')                       -- tables et vues matérialisées
  AND a.attnum > 0 AND NOT a.attisdropped
  AND n.nspname NOT IN ('pg_catalog', 'information_schema', 'topology', 'tiger')
  AND NOT EXISTS (
        SELECT 1 FROM pg_index i
        WHERE i.indrelid = c.oid AND a.attnum = ANY (i.indkey)
  )
ORDER BY 1, 2;
```

```sql
-- 3) Cohérence entre SRID déclaré et SRID réel (doit renvoyer 0)
SELECT COUNT(*) AS objets_incoherents
FROM village.parcel
WHERE ST_SRID(geom) <> Find_SRID('village', 'parcel', 'geom');
```

---

### 5. Validité des géométries *(nouveau)*

#### Objectif

Détecter et corriger les géométries invalides (auto-intersections, anneaux ouverts…) qui provoquent l'erreur `TopologyException` dans `ST_Intersection`, `ST_Union`, etc.

#### Code SQL

```sql
-- 1) Repérer les géométries invalides et la raison
SELECT gid, ST_IsValidReason(geom) AS raison
FROM village.parcel
WHERE NOT ST_IsValid(geom);

-- 2) Repérer vides et NULL
SELECT COUNT(*) FILTER (WHERE geom IS NULL)       AS nb_null,
       COUNT(*) FILTER (WHERE ST_IsEmpty(geom))   AS nb_vides
FROM village.parcel;
```

```sql
-- 3) Correction, SUR UNE COPIE (sauvegarde préalable obligatoire)
CREATE TABLE village.parcel_backup AS TABLE village.parcel;

UPDATE village.parcel
SET geom = ST_Multi(ST_CollectionExtract(ST_MakeValid(geom), 3))   -- 3 = polygones
WHERE NOT ST_IsValid(geom);
```

#### Pièges

- `ST_MakeValid` peut renvoyer une **collection** (polygones + lignes) : `ST_CollectionExtract(…, 3)` ne garde que les polygones (`2` = lignes, `1` = points).
- Sans correction, utilisez ponctuellement `ST_MakeValid(geom)` **dans** la requête, sans modifier les données.

---

## B. Mesurer

### 1. Longueur du réseau d'eaux usées

#### Objectif

Calculer la longueur totale du réseau d'assainissement.

#### Principe

`ST_Length(geom)` renvoie la longueur dans l'unité du SRID ; `SUM()` additionne toutes les lignes.

#### Code SQL

```sql
-- SRID métrique (2154) : résultat en mètres, présenté aussi en km
SELECT ROUND(SUM(ST_Length(geom))::numeric, 1)          AS longueur_m,
       ROUND((SUM(ST_Length(geom)) / 1000)::numeric, 2) AS longueur_km
FROM village.o_usees;
```

```sql
-- Variante si la couche est en 4326 (degrés) : mesure sur l'ellipsoïde
SELECT ROUND((SUM(ST_Length(geom::geography)) / 1000)::numeric, 2) AS longueur_km
FROM village.o_usees;
```

#### Pièges

- En 4326 sans `::geography`, le résultat est en **degrés** et n'a aucun sens métier.
- `ST_Length` ignore les polygones : utiliser `ST_Perimeter` (fiche 5).

---

### 2. Périmètre des zones PLU « ND »

#### Objectif

Calculer le périmètre total des zones ND du PLU, en kilomètres.

#### Principe et correction

- Le périmètre est une **longueur** : on le convertit en km en divisant par **1 000** (et non 10 000).
- Diviser par 10 000 convertit des **m² en hectares**, donc seulement valable pour une **surface**.
- L'ancienne version contenait la requête en double et ne filtrait pas sur les zones ND.

#### Code SQL

```sql
-- Périmètre en km (SRID métrique)
SELECT ROUND((SUM(ST_Perimeter(geom)) / 1000)::numeric, 2) AS perimetre_km
FROM village.pos
WHERE typezone = 'ND';      -- À ADAPTER : nom de la colonne et valeur du zonage
```

```sql
-- Pour comparaison : la SURFACE se convertit en hectares avec / 10000
SELECT ROUND((SUM(ST_Area(geom)) / 10000)::numeric, 2) AS surface_ha
FROM village.pos
WHERE typezone = 'ND';
```

#### Lecture du résultat

Ordre de grandeur : un carré de 100 m de côté a un périmètre de 400 m (0,4 km) et une surface de 10 000 m² (1 ha).

---

## C. Sélectionner par relation spatiale

### 1. Parcelles traversées par le réseau d'eaux usées

#### Objectif

Trouver les parcelles dont la géométrie intersecte le réseau.

#### Principe

`ST_Intersects(a, b)` est vrai si les géométries se croisent ou se touchent. On utilise **`EXISTS`** plutôt que `JOIN + DISTINCT` : chaque parcelle n'est évaluée qu'une fois, sans comparer des géométries entières pour dédoublonner.

#### Code SQL

```sql
SELECT p.*
FROM village.parcel p
WHERE EXISTS (
    SELECT 1
    FROM village.o_usees o
    WHERE ST_Intersects(o.geom, p.geom)
);
```

```sql
-- Variante : longueur de réseau présente dans chaque parcelle
SELECT p.numpar,
       ROUND(SUM(ST_Length(ST_Intersection(o.geom, p.geom)))::numeric, 1) AS longueur_reseau_m
FROM village.parcel p
JOIN village.o_usees o ON ST_Intersects(o.geom, p.geom)
GROUP BY p.numpar
ORDER BY longueur_reseau_m DESC;
```

#### Pièges

- `SELECT DISTINCT p.*` fonctionne, mais devient très lent avec des géométries volumineuses.
- Un réseau qui longe la limite de parcelle est compté (contact = intersection). Pour l'exclure, utiliser `ST_Crosses` ou `NOT ST_Touches`.

---

### 2. Parcelles bâties

#### Objectif

Sélectionner les parcelles contenant au moins un bâtiment.

#### Principe

`ST_Contains(p.geom, b.geom)` n'est vrai que si le bâtiment est **entièrement** dans la parcelle. Un bâtiment à cheval sur deux parcelles n'est donc rattaché à aucune. Selon le besoin, on choisit :

| Besoin | Fonction |
|---|---|
| Bâtiment strictement à l'intérieur | `ST_Contains` |
| Bâtiment dont le contour peut toucher la limite | `ST_Covers` |
| Bâtiment même partiellement dans la parcelle | `ST_Intersects` |

#### Code SQL

```sql
SELECT p.*
FROM village.parcel p
WHERE EXISTS (
    SELECT 1
    FROM village.bati b
    WHERE ST_Contains(p.geom, b.geom)
);
```

```sql
-- Bâtiments non rattachés à une parcelle par ST_Contains (à cheval ou hors parcelle) : contrôle qualité
SELECT b.id
FROM village.bati b
WHERE NOT EXISTS (
    SELECT 1 FROM village.parcel p WHERE ST_Contains(p.geom, b.geom)
);
```

---

### 3. Départements traversés par la Garonne

#### Objectif

Lister les départements que La Garonne intersecte.

#### Principe

On croise `departement.departements` et `carthage.cours`, en filtrant sur le **nom** et sur la **classe 1** (cours principal, pour ne pas intégrer les petits bras et affluents homonymes).

#### Prérequis
Les deux couches doivent avoir le **même SRID** (fiche 3). Sinon : `ST_Transform(c.geom, ST_SRID(d.geom))`.

#### Code SQL

```sql
SELECT DISTINCT d.code_insee, d.nom
FROM departement.departements d
JOIN carthage.cours c
  ON ST_Intersects(c.geom, d.geom)
WHERE c.nomentiteh = 'La Garonne'
  AND c.classe = 1
ORDER BY d.code_insee;
```

#### Pièges

- L'ancienne version contenait une ligne `SELECT DISTINCT d.code_in` tronquée au début : à supprimer.
- Un département simplement tangent au cours d'eau est inclus (contact = intersection). Pour mesurer la longueur réellement dans chaque département, voir la fiche 14.

---

### 4. Parcelles voisines d'une parcelle donnée

#### Objectif

Trouver les parcelles qui touchent la parcelle `c10436`.

#### Principe

`ST_Touches` détecte un contact par la **frontière** sans recouvrement des intérieurs. La parcelle de référence ne se touche pas elle-même : elle est donc exclue automatiquement.

#### Code SQL

```sql
WITH req AS (
    SELECT geom
    FROM village.parcel
    WHERE lower(numpar) = 'c10436'
)
SELECT p2.*
FROM village.parcel p2
JOIN req ON ST_Touches(p2.geom, req.geom);
```

```sql
-- Variante tolérante aux défauts de topologie (micro-vides ou micro-chevauchements entre parcelles)
WITH req AS (
    SELECT numpar, geom
    FROM village.parcel
    WHERE lower(numpar) = 'c10436'
)
SELECT p2.*
FROM village.parcel p2
JOIN req ON ST_DWithin(p2.geom, req.geom, 0.05)     -- 5 cm de tolérance
        AND p2.numpar <> req.numpar;
```

#### Pièges

- Si deux parcelles ne se touchent pas exactement (vide de quelques millimètres), `ST_Touches` les ignore : c'est le rôle de la variante.
- Si elles se chevauchent légèrement, `ST_Touches` est **faux** (c'est un recouvrement) : la variante les récupère.

---

### 5. Zones d'occupation du sol au contact des tourbières (code 412)

#### Objectif

Compter les zones Corine Land Cover qui touchent des tourbières (code 412) et calculer leur surface moyenne.

#### Principe et correction

La version d'origine utilisait un `JOIN` direct : une zone qui touche **deux** tourbières était comptée **deux fois**, et les tourbières voisines d'autres tourbières étaient incluses. On dédoublonne et on exclut le code 412.

#### Prérequis

Le SRID de `corine.clc` doit être métrique (3035 ou 2154) pour que `ST_Area` soit en m².

#### Code SQL

```sql
WITH tourbieres AS (
    SELECT geom
    FROM corine.clc
    WHERE code_18 = '412'
),
voisines AS (
    SELECT DISTINCT c.id,
           c.code_18,
           ST_Area(c.geom) / 1000000 AS surface_km2
    FROM corine.clc c
    JOIN tourbieres t ON ST_Touches(c.geom, t.geom)
    WHERE c.code_18 <> '412'
)
SELECT COUNT(*)                                  AS nombre_zone_ocsol,
       ROUND(AVG(surface_km2)::numeric, 2)       AS surface_moyenne_km2
FROM voisines;
```

```sql
-- Variante : détail par type d'occupation du sol voisin
WITH tourbieres AS (SELECT geom FROM corine.clc WHERE code_18 = '412'),
voisines AS (
    SELECT DISTINCT c.id, c.code_18, ST_Area(c.geom) / 1000000 AS surface_km2
    FROM corine.clc c
    JOIN tourbieres t ON ST_Touches(c.geom, t.geom)
    WHERE c.code_18 <> '412'
)
SELECT code_18,
       COUNT(*)                            AS nb_zones,
       ROUND(AVG(surface_km2)::numeric, 2) AS surface_moyenne_km2
FROM voisines
GROUP BY code_18
ORDER BY nb_zones DESC;
```

---

## D. Distances et proximité

### 1. Distance des zones industrielles (121) à la Garonne

#### Objectif

Calculer, pour chaque zone industrielle Corine (code 121) située à **moins de 10 km** de La Garonne, la distance au cours d'eau.

#### Principe

- `ST_DWithin(a, b, 10000)` filtre via l'index (rapide) ; `ST_Distance` calcule ensuite la distance exacte.
- La Garonne est composée de **plusieurs tronçons** : sans agrégation, une même zone apparaît une fois par tronçon. On garde la **distance minimale** avec `MIN()`.
- Les deux couches n'ont généralement pas le même SRID : on reprojette la Garonne (petite couche) dans le SRID de Corine.

<img width="1912" height="998" alt="07_dwithin_rayon" src="https://github.com/user-attachments/assets/0a56815e-3805-4e90-8e85-8759d0daafe7" />

#### Code SQL

```sql
WITH garonne AS (
    SELECT ST_Transform(geom, Find_SRID('corine', 'clc', 'geom')) AS geom
    FROM carthage.cours
    WHERE nomentiteh = 'La Garonne'
      AND classe = 1
)
SELECT z.id,
       z.code_18,
       ROUND((MIN(ST_Distance(z.geom, g.geom)) / 1000)::numeric, 2) AS distance_km,
       ROUND((ST_Area(z.geom) / 1000000)::numeric, 2)               AS surface_km2,
       z.geom
FROM corine.clc z
JOIN garonne g
  ON ST_DWithin(z.geom, g.geom, 10000)          -- 10 km
WHERE z.code_18 = '121'
GROUP BY z.id, z.code_18, z.geom
ORDER BY distance_km;                            -- du plus proche au plus éloigné
```

#### Lecture du résultat

Une distance de `0.00` signifie que la zone **touche ou chevauche** le cours d'eau.

#### Pièges

- Le tri d'origine était décroissant (`DESC`) : changez-le selon l'usage (les plus proches d'abord pour un diagnostic de risque).
- `ST_DWithin` prend son seuil dans l'unité du SRID : 10 000 = 10 km seulement en SRID métrique.

---

### 2. Bâtiment le plus proche du réseau d'eaux usées

#### Objectif

Pour chaque bâtiment, trouver le tronçon de réseau le plus proche et la distance correspondante.

#### Principe

- `CROSS JOIN LATERAL` exécute la sous-requête **pour chaque bâtiment**.
- `ORDER BY b.geom <-> o.geom LIMIT 1` utilise l'**index GIST** pour trouver directement le voisin le plus proche (recherche *KNN*), sans calculer la distance à tous les tronçons.
- `ST_ShortestLine` permet de dessiner le branchement dans QGIS.

<img width="1912" height="998" alt="06_plus_proche_voisin" src="https://github.com/user-attachments/assets/c91f8f64-6524-4781-b55b-1658bc367365" />

#### Prérequis

Index GIST sur `village.o_usees.geom` (voir 0.3).

#### Code SQL

```sql
SELECT b.id,
       b."type",
       ROUND(ST_Distance(b.geom, n.geom)::numeric, 1) AS distance_m,
       ST_ShortestLine(b.geom, n.geom)                AS ligne_branchement,
       b.geom
FROM village.bati AS b
CROSS JOIN LATERAL (
    SELECT o.geom
    FROM village.o_usees AS o
    ORDER BY b.geom <-> o.geom
    LIMIT 1
) AS n
ORDER BY distance_m ASC;
```

```sql
-- Variante : uniquement les bâtiments à plus de 100 m du réseau (non raccordables facilement)
SELECT b.id, ROUND(d.distance_m::numeric, 1) AS distance_m, b.geom
FROM village.bati b
CROSS JOIN LATERAL (
    SELECT ST_Distance(b.geom, o.geom) AS distance_m
    FROM village.o_usees o
    ORDER BY b.geom <-> o.geom
    LIMIT 1
) d
WHERE d.distance_m > 100;
```

#### Pièges

- Sans index GIST, la requête reste correcte mais devient très lente.
- Si la table `o_usees` pouvait être vide, remplacer `CROSS JOIN LATERAL` par `LEFT JOIN LATERAL (…) n ON true` pour ne pas perdre les bâtiments.

---

### 3. Tampons autour d'objets *(nouveau)*

#### Objectif

Sélectionner les parcelles à moins de 50 m du réseau, ou produire une zone tampon unique.

#### Principe

- Pour **sélectionner**, `ST_DWithin` est plus rapide qu'un `ST_Buffer` suivi d'un `ST_Intersects`.
- Pour **produire** une géométrie (cartographie), on utilise `ST_Buffer`. Fusionner avant de bufferiser (`ST_Union` puis `ST_Buffer`) évite des milliers de petits polygones qui se recouvrent.

#### Code SQL

```sql
-- Sélection : parcelles à moins de 50 m du réseau
SELECT p.*
FROM village.parcel p
WHERE EXISTS (
    SELECT 1 FROM village.o_usees o
    WHERE ST_DWithin(p.geom, o.geom, 50)
);
```

```sql
-- Production : zone tampon unique de 50 m   (remplacer 2154 par le SRID de la couche)
SELECT 1 AS fid,
       ST_Multi(ST_Buffer(ST_Union(geom), 50))::geometry(MultiPolygon, 2154) AS geom
FROM village.o_usees;
```

---

## E. Fabriquer de nouvelles géométries

### 1. Pourcentage de périmètre non touché par d'autres départements

#### Objectif

Pour chaque département, calculer :

1. son **périmètre total** ;
2. la **longueur de frontière partagée** avec d'autres départements ;
3. la longueur **sans contact** avec un autre département ;
4. le **pourcentage** de périmètre non touché.

Cette analyse permet de repérer les départements **enclavés** (pourcentage proche de 0), **côtiers**, ou en **limite internationale**.

<img width="1987" height="1028" alt="08_frontiere_partagee" src="https://github.com/user-attachments/assets/9f6ef5d9-9ba1-45e2-9b0d-28ade35d2641" />

#### Principe étape par étape

| Étape | Fonction | Rôle |
|---|---|---|
| 1 | `ST_Boundary` + `ST_CollectionExtract(…, 2)` | Extrait le contour du polygone et ne garde que les lignes |
| 1 | `ST_Transform(…, 2154)` | Garantit des mesures en mètres |
| 2 | `ST_Intersection` | Extrait la portion commune entre deux frontières |
| 2 | `ST_Union` | Rassemble les frontières partagées d'un même département |
| 3 | `ST_Length` | Longueur de la frontière partagée |
| 4 | Calcul | `non touché = périmètre − partagé`, puis `% = non touché / périmètre × 100` |

#### Prérequis

Couche départements **sans trou ni chevauchement** entre voisins (voir fiche 20). Le SRID 2154 est adapté à la France métropolitaine ; les DROM nécessitent leur projection locale.

#### Code SQL

```sql
WITH dep AS (
    -- 1) Contour et périmètre de chaque département, en Lambert-93
    SELECT d.code_insee,
           d.nom,
           ST_CollectionExtract(ST_Boundary(ST_Transform(d.geom, 2154)), 2) AS boundary_2154,
           ST_Perimeter(ST_Transform(d.geom, 2154))                         AS perimeter_m
    FROM departement.departements d
),
shared AS (
    -- 2) Frontière commune avec chaque voisin, fusionnée par département
    SELECT d.code_insee,
           ST_Union(
               ST_CollectionExtract(ST_Intersection(d.boundary_2154, d2.boundary_2154), 2)
           ) AS shared_geom
    FROM dep d
    JOIN dep d2
      ON d2.code_insee <> d.code_insee
     AND ST_DWithin(d.boundary_2154, d2.boundary_2154, 0.001)
    GROUP BY d.code_insee
),
shared_len AS (
    -- 3) Longueur partagée (0 si aucun voisin)
    SELECT d.code_insee,
           d.nom,
           d.perimeter_m,
           COALESCE(ST_Length(s.shared_geom), 0) AS shared_border_m
    FROM dep d
    LEFT JOIN shared s ON s.code_insee = d.code_insee
)
-- 4) Part de périmètre non touchée
SELECT code_insee,
       nom,
       ROUND(perimeter_m::numeric, 0)                                         AS perimeter_m,
       ROUND(shared_border_m::numeric, 0)                                     AS shared_border_m,
       ROUND(GREATEST(perimeter_m - shared_border_m, 0)::numeric, 0)          AS non_touching_m,
       ROUND((100.0 * GREATEST(perimeter_m - shared_border_m, 0)
              / NULLIF(perimeter_m, 0))::numeric, 2)                          AS pct_non_touching
FROM shared_len
ORDER BY pct_non_touching DESC;
```

#### Lecture du résultat

- `pct_non_touching` proche de **0 %** : département enclavé, entouré de voisins.
- Valeur élevée : département côtier ou frontalier.
- Pour contrôle, la somme des pourcentages n'a pas de sens ; vérifiez plutôt un département connu (exemple : un département côtier doit avoir un pourcentage notable).

#### Pièges

- `ST_Intersection` sur des lignes exige que les sommets coïncident. Si les contours des départements ne sont pas parfaitement jointifs, la frontière partagée est **sous-estimée**. Dans ce cas, remplacer l'intersection par `ST_Intersection(d.boundary_2154, ST_Buffer(d2.boundary_2154, 1))` (tolérance de 1 m).
- Les CTE `dep` ne sont pas indexées : correct pour une centaine de départements, à matérialiser et indexer pour des communes.
- `ST_LineMerge` et `ST_UnaryUnion` de l'ancienne version ne sont plus nécessaires : `ST_Union` agrégé dissout déjà les recouvrements.

---

### 2. Découper la Garonne par département

#### Objectif

Obtenir, pour chaque département traversé, le tronçon de La Garonne qui s'y trouve, avec sa longueur.

#### Principe

`ST_Intersection(c.geom, d.geom)` découpe la ligne à la limite du département. Le résultat peut contenir des **points** (simples contacts) : `ST_CollectionExtract(…, 2)` ne garde que les lignes. `LATERAL` calcule l'intersection **une seule fois** par couple au lieu de trois dans l'ancienne version.

#### Code SQL

```sql
SELECT d.code_insee,
       d.nom                                     AS departement,
       c.nomentiteh                              AS cours_eau,
       ST_Multi(x.g)                             AS segment_geom,
       ROUND((ST_Length(x.g) / 1000)::numeric, 1) AS longueur_km     -- SRID métrique
FROM departement.departements d
JOIN carthage.cours c
  ON ST_Intersects(c.geom, d.geom)
CROSS JOIN LATERAL (
    SELECT ST_CollectionExtract(ST_Intersection(c.geom, d.geom), 2) AS g
) x
WHERE c.nomentiteh = 'La Garonne'
  AND c.classe = 1
  AND NOT ST_IsEmpty(x.g);
```

#### Pour obtenir une ligne par département (somme des tronçons)

```sql
SELECT d.code_insee,
       d.nom AS departement,
       ROUND((SUM(ST_Length(x.g)) / 1000)::numeric, 1) AS longueur_km
FROM departement.departements d
JOIN carthage.cours c ON ST_Intersects(c.geom, d.geom)
CROSS JOIN LATERAL (
    SELECT ST_CollectionExtract(ST_Intersection(c.geom, d.geom), 2) AS g
) x
WHERE c.nomentiteh = 'La Garonne' AND c.classe = 1
GROUP BY d.code_insee, d.nom
ORDER BY longueur_km DESC;
```

---

### 3. Découper la Garonne en segments de 10 km

#### Objectif

Découper la Garonne en segments réguliers de 10 km, pour les styliser séparément dans QGIS (dégradé, numérotation, étiquettes).

#### Principe

1. Extraire les lignes de la Garonne, les **fusionner** (`ST_Union` puis `ST_LineMerge`) et les mettre en 2D.
2. **Reprojeter** en 2154 pour travailler en mètres.
3. Calculer la longueur de chaque partie.
4. Générer la série `0 … CEIL(longueur / 10 000) − 1` avec `generate_series`.
5. Pour chaque indice, extraire la portion de ligne avec `ST_LineSubstring`, dont les bornes sont des **fractions** (0 à 1) de la longueur totale.

<img width="1987" height="878" alt="09_segments_10km" src="https://github.com/user-attachments/assets/eb00c332-193f-4694-a712-079323221d2f" />

Le pas (10 000 m) est isolé dans une CTE `params` : on le modifie en un seul endroit.

#### Code SQL

```sql
WITH params AS (
    SELECT 10000.0 AS pas_m                       -- longueur des segments, en mètres
),
src AS (
    SELECT ST_CollectionExtract(ST_Force2D(c.geom), 2) AS geom
    FROM carthage.cours AS c
    WHERE c.nomentiteh ILIKE 'La Garonne'
      AND c.classe = 1
),
merged AS (
    SELECT (ST_Dump(ST_LineMerge(ST_Union(geom)))).geom AS geom
    FROM src
),
g2154 AS (
    SELECT ST_Transform(geom, 2154) AS geom
    FROM merged
),
parts AS (
    SELECT ROW_NUMBER() OVER () AS part_id,
           geom,
           ST_Length(geom)      AS len_m
    FROM g2154
),
segs AS (
    SELECT p.part_id,
           seg_idx,
           ST_LineSubstring(
               p.geom,
               (seg_idx * pr.pas_m) / p.len_m,
               LEAST(((seg_idx + 1) * pr.pas_m) / p.len_m, 1.0)
           ) AS geom_2154
    FROM parts p
    CROSS JOIN params pr
    CROSS JOIN LATERAL generate_series(
        0,
        GREATEST(CEIL(p.len_m / pr.pas_m)::int - 1, 0)
    ) AS seg_idx
)
SELECT ROW_NUMBER() OVER ()                                   AS fid,       -- identifiant unique pour QGIS
       part_id,
       seg_idx,
       'La Garonne'::text                                     AS cours_eau,
       ROUND((ST_Length(geom_2154) / 1000)::numeric, 2)       AS longueur_km,
       ST_Multi(geom_2154)::geometry(MultiLineString, 2154)   AS geom
FROM segs
WHERE NOT ST_IsEmpty(geom_2154);
```

#### Lecture du résultat

Tous les segments font 10 km, **sauf le dernier de chaque partie**, plus court : c'est le reste de la division. Vérification :

```sql
-- à ajouter à la suite : somme des segments = longueur de la Garonne
-- SELECT SUM(longueur_km) FROM (<la requête ci-dessus>) t;
```

#### Pièges

- `ST_LineSubstring` n'accepte que des **LineString** : d'où le `ST_Dump` après `ST_LineMerge`.
- Si la Garonne est en plusieurs parties non jointives (bras, lacunes de saisie), la numérotation redémarre à 0 pour chaque `part_id`.
- Le dernier segment peut avoir une longueur quasi nulle si la longueur est un multiple presque exact du pas ; filtrer avec `WHERE ST_Length(geom_2154) > 1` si nécessaire.

---

### 4. Fusionner des entités (dissolve) *(nouveau)*

#### Objectif

Regrouper les polygones d'un même zonage en une géométrie unique, avec la surface totale.

#### Code SQL

```sql
SELECT typezone,                                             -- À ADAPTER : colonne de regroupement
       ST_Multi(ST_Union(geom))                              AS geom,
       ROUND((SUM(ST_Area(geom)) / 10000)::numeric, 2)       AS surface_ha
FROM village.pos
GROUP BY typezone
ORDER BY surface_ha DESC;
```

#### Pièges

- `ST_Union` agrégé sur de grosses couches est coûteux. Ajouter un `WHERE` pour restreindre au secteur d'étude.
- `ST_Union` échoue si une géométrie est invalide : voir fiche 20.

---

### 5. Centroïde ou point garanti dans le polygone *(nouveau)*

#### Objectif

Placer un point par parcelle (étiquette, symbole, jointure).

#### Principe

| Fonction | Garantie | Usage |
|---|---|---|
| `ST_Centroid` | Centre de gravité, **peut tomber hors** du polygone (forme en U, en L) | Calculs statistiques |
| `ST_PointOnSurface` | Point **toujours à l'intérieur** | Étiquettes, jointures spatiales |

#### Code SQL

```sql
SELECT numpar,
       ST_Centroid(geom)       AS centroide,
       ST_PointOnSurface(geom) AS point_interieur
FROM village.parcel;
```

---

## F. Compter et agréger

### 1. Comptages avancés (mobilier par parcelle / type)

#### Objectif

Compter le mobilier :

1. par parcelle ;
2. par type ;
3. par parcelle **et** par type ;
4. avec le **total général** sur chaque ligne.

#### Principe

Les CTE organisent le calcul en blocs lisibles :

| CTE | Rôle |
|---|---|
| `req` | total par parcelle |
| `req1` | total par type |
| `req2` | total par couple (type, parcelle) |
| `total` | total général |

<img width="1987" height="938" alt="10_pipeline_cte" src="https://github.com/user-attachments/assets/bef6b836-d04d-464e-835a-be97118ebde7" />

#### Version 1 : CTE (pédagogique)

```sql
WITH req AS (
    SELECT id_parcelle, COUNT(*) AS nbre_par_parcelle
    FROM arbres.mobilier
    GROUP BY id_parcelle
),
req1 AS (
    SELECT id_type_mobilier, COUNT(*) AS nbre_par_type
    FROM arbres.mobilier
    GROUP BY id_type_mobilier
),
req2 AS (
    SELECT id_type_mobilier, id_parcelle, COUNT(*) AS nbre_par_parcelle_type
    FROM arbres.mobilier
    GROUP BY id_type_mobilier, id_parcelle
),
total AS (
    SELECT COUNT(*) AS total_mobilier
    FROM arbres.mobilier
)
SELECT req2.id_parcelle,
       req.nbre_par_parcelle,
       req2.id_type_mobilier,
       req1.nbre_par_type,
       req2.nbre_par_parcelle_type,
       total.total_mobilier
FROM req2
LEFT JOIN req  ON req.id_parcelle        = req2.id_parcelle
LEFT JOIN req1 ON req1.id_type_mobilier  = req2.id_type_mobilier
CROSS JOIN total
ORDER BY req2.id_parcelle, req2.id_type_mobilier;
```

> Corrections : les `ORDER BY` à l'intérieur des CTE étaient inutiles (seul le tri final compte) ; `id_parcelle` est maintenant lu depuis `req2`, qui contient toutes les combinaisons, et non depuis `req`.

#### Version 2 : fonctions de fenêtre (plus courte)

```sql
SELECT id_parcelle,
       id_type_mobilier,
       COUNT(*)                                          AS nbre_par_parcelle_type,
       SUM(COUNT(*)) OVER (PARTITION BY id_parcelle)::int       AS nbre_par_parcelle,
       SUM(COUNT(*)) OVER (PARTITION BY id_type_mobilier)::int  AS nbre_par_type,
       SUM(COUNT(*)) OVER ()::int                               AS total_mobilier
FROM arbres.mobilier
GROUP BY id_parcelle, id_type_mobilier
ORDER BY id_parcelle, id_type_mobilier;
```

#### Version 3 : sous-totaux avec `GROUPING SETS` (tableau de synthèse)

```sql
SELECT id_parcelle,
       id_type_mobilier,
       COUNT(*) AS nombre,
       CASE
           WHEN GROUPING(id_parcelle) = 0 AND GROUPING(id_type_mobilier) = 0 THEN 'parcelle + type'
           WHEN GROUPING(id_parcelle) = 0                                    THEN 'sous-total parcelle'
           WHEN GROUPING(id_type_mobilier) = 0                               THEN 'sous-total type'
           ELSE 'total général'
       END AS niveau
FROM arbres.mobilier
GROUP BY GROUPING SETS ((id_parcelle, id_type_mobilier), (id_parcelle), (id_type_mobilier), ())
ORDER BY niveau, id_parcelle, id_type_mobilier;
```

---

### 2. Compter les bâtiments par parcelle *(nouveau)*

#### Objectif

Associer à chaque parcelle le nombre de bâtiments et l'emprise bâtie, **sans compter deux fois** un bâtiment à cheval sur deux parcelles.

#### Principe

On rattache chaque bâtiment à la parcelle qui contient son `ST_PointOnSurface` (un point unique, donc une seule parcelle). `LEFT JOIN` conserve les parcelles sans bâtiment (0).

#### Code SQL

```sql
SELECT p.numpar,
       COUNT(b.id)                                        AS nb_batiments,
       ROUND(COALESCE(SUM(ST_Area(b.geom)), 0)::numeric, 1) AS emprise_m2,
       ROUND((COALESCE(SUM(ST_Area(b.geom)), 0)
              / NULLIF(ST_Area(p.geom), 0) * 100)::numeric, 1)   AS taux_emprise_pct
FROM village.parcel p
LEFT JOIN village.bati b
       ON ST_Intersects(p.geom, ST_PointOnSurface(b.geom))
GROUP BY p.numpar, p.geom
ORDER BY nb_batiments DESC;
```

---

## G. Automatiser

### 1. Triggers : ajout automatique de la date de création

#### Objectif

Renseigner automatiquement `date_creation` à chaque insertion dans `test_mobilier`.

#### Principe

Un trigger **`BEFORE INSERT`** déclenche une fonction qui modifie la ligne `NEW` **avant** son écriture.

<img width="1987" height="757" alt="11_trigger_before_insert" src="https://github.com/user-attachments/assets/0e0799a1-adbc-46be-9142-ccbe0e615ad4" />

> 💡 Si l'on veut seulement une date par défaut, `DEFAULT now()` sur la colonne suffit et c'est plus simple. Le trigger est utile quand on veut **imposer** la valeur (même si l'utilisateur en fournit une) ou enchaîner d'autres traitements.

#### Code SQL

**1. Création de la table**

```sql
CREATE TABLE IF NOT EXISTS public.test_mobilier (
    id_mobilier       SERIAL PRIMARY KEY,
    id_parcelle       INTEGER,
    id_type_mobilier  INTEGER,
    date_creation     TIMESTAMP,
    date_modification TIMESTAMP
);
```

**2. Fonction du trigger**

```sql
CREATE OR REPLACE FUNCTION public.fn_set_date_creation()
RETURNS trigger AS $$
BEGIN
    NEW.date_creation := NOW();
    RETURN NEW;                      -- indispensable
END;
$$ LANGUAGE plpgsql;
```

**3. Création du trigger** (*bloc de code correctement fermé, il ne l'était pas dans l'ancienne version*)

```sql
DROP TRIGGER IF EXISTS trg_set_date_creation ON public.test_mobilier;

CREATE TRIGGER trg_set_date_creation
BEFORE INSERT ON public.test_mobilier
FOR EACH ROW
EXECUTE FUNCTION public.fn_set_date_creation();
```

**4. Insertion de test**

```sql
INSERT INTO public.test_mobilier (id_mobilier, id_parcelle, id_type_mobilier)
SELECT id_mobilier, id_parcelle, id_type_mobilier
FROM arbres.mobilier;

-- Les identifiants ont été fournis explicitement : on recale la séquence pour les prochaines insertions
SELECT setval(pg_get_serial_sequence('public.test_mobilier', 'id_mobilier'),
              (SELECT MAX(id_mobilier) FROM public.test_mobilier));
```

**5. Vérification**

```sql
SELECT *
FROM public.test_mobilier
ORDER BY id_mobilier
LIMIT 20;
```

#### Extension : date de modification automatique

```sql
CREATE OR REPLACE FUNCTION public.fn_set_date_modification()
RETURNS trigger AS $$
BEGIN
    NEW.date_modification := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_date_modification
BEFORE UPDATE ON public.test_mobilier
FOR EACH ROW
EXECUTE FUNCTION public.fn_set_date_modification();
```

#### Nettoyage

```sql
DROP TRIGGER IF EXISTS trg_set_date_creation     ON public.test_mobilier;
DROP TRIGGER IF EXISTS trg_set_date_modification ON public.test_mobilier;
DROP TABLE   IF EXISTS public.test_mobilier;
```

#### Pièges

- Oublier `RETURN NEW` dans un trigger `BEFORE` annule l'opération.
- `NOW()` renvoie l'heure de **début de transaction** : toutes les lignes d'une même transaction ont la même date. Pour l'heure réelle de chaque ligne, utiliser `clock_timestamp()`.
- Utiliser `TIMESTAMPTZ` plutôt que `TIMESTAMP` si plusieurs fuseaux horaires sont possibles.

---

### 2. Fonctions temporelles (PostgreSQL)

#### Objectif

Disposer d'un aide-mémoire fiable des fonctions de date, **en distinguant PostgreSQL (notre base) de MySQL**.

> ⚠️ L'ancienne liste mélangeait les deux : `YEAR()`, `MONTH()`, `DATEDIFF()`, `DATE_ADD()`, `LAST_DAY()`… **n'existent pas dans PostgreSQL**. Voici les équivalents.

#### Table de correspondance

| Besoin | PostgreSQL ✅ | MySQL (pour info) |
|---|---|---|
| Date du jour | `CURRENT_DATE` | `CURDATE()` |
| Date + heure actuelles | `CURRENT_TIMESTAMP` ou `NOW()` | `NOW()` |
| Année | `EXTRACT(YEAR FROM d)` | `YEAR(d)` |
| Mois (1-12) | `EXTRACT(MONTH FROM d)` | `MONTH(d)` |
| Jour du mois | `EXTRACT(DAY FROM d)` | `DAY(d)` |
| Heure / minute / seconde | `EXTRACT(HOUR \| MINUTE \| SECOND FROM d)` | `HOUR(d)`, `MINUTE(d)`, `SECOND(d)` |
| Partie quelconque | `EXTRACT(part FROM d)` ou `date_part('part', d)` | `EXTRACT(part FROM d)` |
| Début de période | `DATE_TRUNC('month', d)` | – |
| Mise en forme | `TO_CHAR(d, 'YYYY-MM')` | `DATE_FORMAT(d, '%Y-%m')` |
| Ajouter une période | `d + INTERVAL '1 month'` | `DATE_ADD(d, INTERVAL 1 MONTH)` |
| Retirer une période | `d - INTERVAL '1 month'` | `DATE_SUB(d, INTERVAL 1 MONTH)` |
| Différence en jours | `d1::date - d2::date` | `DATEDIFF(d1, d2)` |
| Différence en années / mois | `AGE(d1, d2)` | `TIMESTAMPDIFF(unit, d1, d2)` |
| Dernier jour du mois | `(DATE_TRUNC('month', d) + INTERVAL '1 month - 1 day')::date` | `LAST_DAY(d)` |
| Jour de la semaine | `EXTRACT(ISODOW FROM d)` (1 = lundi … 7 = dimanche) | `DAYOFWEEK(d)` (1 = dimanche) |
| Numéro de semaine | `EXTRACT(WEEK FROM d)` (semaine ISO) | `WEEK(d)` |

#### Exemples appliqués à la table `test_mobilier`

```sql
-- Nombre de mobiliers créés par mois
SELECT DATE_TRUNC('month', date_creation)::date AS mois,
       COUNT(*)                                  AS nb
FROM public.test_mobilier
GROUP BY 1
ORDER BY 1;

-- Créations des 30 derniers jours
SELECT *
FROM public.test_mobilier
WHERE date_creation >= CURRENT_DATE - INTERVAL '30 days';

-- Ancienneté en jours
SELECT id_mobilier,
       CURRENT_DATE - date_creation::date AS anciennete_jours
FROM public.test_mobilier;

-- Calendrier de dates continues (utile pour combler les mois sans données)
SELECT generate_series('2025-01-01'::date, '2025-12-01'::date, INTERVAL '1 month')::date AS mois;
```

#### Pièges

- `EXTRACT(DOW …)` renvoie 0 pour dimanche ; `ISODOW` renvoie 7. Privilégier `ISODOW`.
- Une date est `d1 - d2` = **entier de jours** ; un `timestamp - timestamp` = un **intervalle**.
- Filtrer avec `date_creation >= … AND date_creation < …` plutôt qu'avec `EXTRACT(...)` pour garder l'usage d'un index.

---

## H. Diffuser et optimiser

### 1. Publier une couche propre pour QGIS *(nouveau)*

#### Objectif

Fournir aux collègues une **vue** stable, typée et avec identifiant unique, que QGIS charge sans avertissement.

#### Principe

QGIS a besoin de : une **clé unique** (entier), une **géométrie typée** (type et SRID) et, idéalement, un **index spatial** sur les tables sources.

#### Code SQL

```sql
CREATE OR REPLACE VIEW village.v_parcelles_traversees AS
SELECT ROW_NUMBER() OVER ()::int                        AS fid,        -- clé unique pour QGIS
       p.numpar,
       ST_Multi(p.geom)::geometry(MultiPolygon, 2154)   AS geom        -- À ADAPTER : type et SRID
FROM village.parcel p
WHERE EXISTS (
    SELECT 1 FROM village.o_usees o WHERE ST_Intersects(o.geom, p.geom)
);

COMMENT ON VIEW village.v_parcelles_traversees
    IS 'Parcelles intersectées par le réseau d''eaux usées. Mise à jour automatique.';
```

#### Dans QGIS

1. *Couche → Ajouter une couche → Ajouter une couche PostGIS*.
2. Sélectionner la vue, cocher **Utiliser la clé primaire / colonne unique** = `fid`.
3. Pour une **requête libre** : *DB Manager → Fenêtre SQL → Charger en tant que nouvelle couche*, en renseignant colonne **Id unique** et colonne **Géométrie**.

#### Pièges

- Une vue ordinaire se recalcule à chaque affichage : pour un calcul lourd, utiliser une **vue matérialisée** (fiche 2) avec un index unique.
- `ROW_NUMBER() OVER ()` n'est pas stable d'une exécution à l'autre : à éviter si l'on conserve des styles liés à l'identifiant. Préférer une vraie clé (`gid`) quand elle existe.

---

### 2. Lire un plan d'exécution *(nouveau)*

#### Objectif

Comprendre pourquoi une requête est lente et vérifier qu'un index est bien utilisé.

#### Code SQL

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.numpar
FROM village.parcel p
WHERE EXISTS (SELECT 1 FROM village.o_usees o WHERE ST_Intersects(o.geom, p.geom));
```

#### Lecture

| Ce qu'on lit | Signification | Action |
|---|---|---|
| `Seq Scan on …` sur une grande table | Parcours complet, pas d'index | Créer l'index GIST ou aligner les SRID |
| `Index Scan` / `Bitmap Heap Scan` | Index utilisé | ✅ |
| `Nested Loop` + `Index Scan` interne | Jointure spatiale efficace | ✅ |
| `rows=` estimé très différent du réel | Statistiques périmées | `VACUUM ANALYZE table;` |
| `Execution Time` | Durée totale | À comparer avant / après optimisation |

#### Entretien courant

```sql
VACUUM ANALYZE village.parcel;
VACUUM ANALYZE village.o_usees;
```

---

## Annexes

### Erreurs fréquentes et solutions

| Message / symptôme | Cause probable | Solution |
|---|---|---|
| `Operation on mixed SRID geometries` | Deux couches de SRID différents | `ST_Transform` d'un côté (voir 0.2) |
| `TopologyException` / `GEOSIntersects` | Géométrie invalide | Fiche 20 : `ST_MakeValid` |
| Longueurs ≈ 0,0x | Couche en 4326 (degrés) | `::geography` ou `ST_Transform(…, 2154)` |
| Tolérance `ST_Simplify` sans effet ou destructrice | Unité du SRID mal comprise | Vérifier le SRID (fiche 3) |
| Doublons après jointure spatiale | Une entité touche plusieurs entités | `EXISTS`, `DISTINCT` ou agrégation |
| Requête spatiale très lente | Pas d'index GIST, ou `ST_Transform` sur la colonne | Fiches 19 et 26 |
| `column … must appear in the GROUP BY clause` | Colonne non agrégée dans un `GROUP BY` | L'ajouter au `GROUP BY` ou l'agréger |
| `function year(timestamp) does not exist` | Syntaxe MySQL | `EXTRACT(YEAR FROM …)` (fiche 18) |
| Le trigger « ne fait rien » | `RETURN NEW` oublié, mauvais événement (`INSERT` / `UPDATE`) | Fiche 17 |
| QGIS : « pas de clé primaire » | Vue sans identifiant unique | Fiche 25 |

### Check-list avant de livrer une requête

- [ ] Le **SRID** des couches est connu et identique (ou reprojeté).
- [ ] L'**unité** du résultat est indiquée (m, km, m², ha).
- [ ] Les **géométries** sont valides (`ST_IsValid`).
- [ ] Un **index GIST** existe sur chaque colonne géométrique utilisée.
- [ ] Le **prédicat** est adapté (`Contains` ≠ `Intersects` ≠ `Touches`).
- [ ] Pas de **doublons** involontaires (`EXISTS`, `DISTINCT`, `GROUP BY`).
- [ ] Les paramètres modifiables (seuil, code, SRID) sont **en tête** de requête ou commentés.
- [ ] `EXPLAIN ANALYZE` ne montre pas de `Seq Scan` sur les grosses tables.
- [ ] Le résultat est **contrôlé sur un cas connu** (une parcelle, un département).
- [ ] La requête est **commentée** et enregistrée dans cette page.

### Glossaire

| Terme | Définition |
|---|---|
| **SRID** | Identifiant du système de coordonnées (2154 = Lambert-93, 4326 = WGS 84) |
| **GIST** | Type d'index adapté aux données spatiales (arbre de rectangles englobants) |
| **Bounding box** | Plus petit rectangle contenant une géométrie, utilisé pour le filtre rapide |
| **CTE** | *Common Table Expression* : bloc `WITH nom AS (…)` réutilisable dans la requête |
| **LATERAL** | Sous-requête pouvant référencer les colonnes des tables qui la précèdent dans le `FROM` |
| **KNN** | *K-nearest neighbours* : recherche des voisins les plus proches (opérateur `<->`) |
| **Vue matérialisée** | Résultat de requête stocké physiquement, à rafraîchir |
| **Trigger** | Fonction exécutée automatiquement lors d'un `INSERT`, `UPDATE` ou `DELETE` |
| **Dissolve** | Fusion de plusieurs entités en une seule (`ST_Union`) |
| **Topologie** | Cohérence des contacts entre entités (pas de vides ni de chevauchements) |

### Journal des corrections par rapport à l'ancienne version

| Fiche | Correction |
|---|---|
| Titre | Faute « Queslques » corrigée |
| 1 | Instructions SQL collées sur une ligne ; l'index B-Tree n'accélère pas `ILIKE` → 3 options documentées |
| 2 | L'index spatial était créé sur la table source au lieu de la vue ; ajout de `WITH DATA`, de l'index unique et du `REFRESH` ; avertissement sur l'unité de la tolérance |
| 5 | Périmètre divisé par 10 000 (conversion m² → ha) au lieu de 1 000 (m → km) ; requête dupliquée ; filtre ND ajouté |
| 6, 7 | `JOIN + DISTINCT p.*` remplacé par `EXISTS` ; explication du choix `Contains` / `Covers` / `Intersects` |
| 8 | Ligne tronquée `SELECT DISTINCT d.code_in` supprimée |
| 9 | Variante tolérante aux défauts de topologie |
| 10 | Doublons de comptage (zone touchant plusieurs tourbières) et inclusion du code 412 corrigés |
| 11 | Une ligne par tronçon de Garonne → agrégation `MIN()` ; reprojection automatique vers le SRID de Corine |
| 12 | Alias dupliqué `o` clarifié ; ajout de `ST_ShortestLine` |
| 13 | `ST_CollectionExtract` appliqué aussi à l'intersection ; `ST_LineMerge` / `ST_UnaryUnion` superflus retirés ; tolérance de topologie documentée |
| 14 | Jointure avec filtres déplacés ; intersection calculée une fois (`LATERAL`) ; ajout de la longueur |
| 15 | Pas paramétré (`params`) ; `ST_Force2D` ; géométrie typée pour QGIS ; commentaires parasites retirés |
| 16 | `ORDER BY` inutiles retirés ; `id_parcelle` lu depuis `req2` ; versions fenêtre et `GROUPING SETS` ajoutées |
| 17 | Bloc de code non fermé (le titre « 4. Insertion de test » était dans le bloc SQL) ; recalage de la séquence ; trigger de modification |
| 18 (ex-« 20 ») | Titre renuméroté ; fonctions MySQL séparées des fonctions PostgreSQL |
| 19 à 26 | Nouvelles fiches : inventaire, validité, tampons, dissolve, bâtiments par parcelle, centroïdes, vue QGIS, plan d'exécution |
