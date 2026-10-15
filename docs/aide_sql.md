# 🗄️ Fiche complète PostgreSQL / PostGIS 

> Aide-mémoire de l'AUDC 51 pour interroger, modifier, sécuriser et sauvegarder une base de données géographique.
> Chaque requête est expliquée, avec ses pièges, ses variantes et, quand c'est utile, une illustration.

[🔗 Documentation officielle PostgreSQL](https://www.postgresql.org/docs/)  
[🔗 Documentation officielle PostGIS](https://postgis.net/documentation/)  
[🔗 Cours IDGEO 2025/2026](https://supports.idgeo.fr/cpgeom/2025-2027/A3-Admin_bdd/co/BDD_PGIS_tables_distantes.html)

---

## À qui s'adresse cette fiche et comment l'utiliser

Cette fiche est écrite pour les **géomaticiens et chargés d'études de l'agence**. Elle suppose que l'on connaît les bases du SQL (`SELECT`, `WHERE`, `JOIN`) et qu'une base PostgreSQL avec l'extension PostGIS est disponible.

Elle a été **réorganisée** pour suivre un fil logique : comprendre les notions de base, choisir la bonne fonction, écrire une requête efficace, modifier les données, puis les protéger (droits, sauvegardes).

| Je veux... | Section |
|------------|---------|
| Vérifier le SRID ou le type de mes données | 1 |
| Savoir quelle fonction PostGIS utiliser | 2 |
| Écrire une requête rapide et fiable | 3 |
| Découper, tamponner, mesurer, compter | 4 à 9 |
| Créer des tables et modifier des données | 10 |
| Importer ou exporter des données (Shapefile, CSV) | 11 |
| Changer de projection | 12 |
| Accélérer une requête lente | 15 |
| Donner ou retirer des droits à un collègue | 16 |
| Sauvegarder ou restaurer une base | 17 |
| Consulter une autre base ou un service WFS | 19 |
| Comprendre un message d'erreur | 20 |

### Ma démarche pour écrire une requête spatiale

<img width="1920" height="660" alt="sql_demarche" src="https://github.com/user-attachments/assets/1f9ac1a9-e4ea-4905-830e-8b4bf1233a5a" />

*Les six étapes à suivre pour une requête fiable. Les sections 3, 15 et 21 détaillent chacune d'elles.*

### Conventions utilisées dans la fiche

- Les mots-clés SQL sont en **majuscules**, les tables sont **préfixées par leur schéma** (`public.regions`).
- La colonne géométrique s'appelle **`geom`** et le système de projection est le **Lambert-93 (EPSG:2154)**, dont l'unité est le **mètre**.
- Les tables d'exemple viennent de cas réels de l'agence. **Remplace-les par les tiennes** :

| Table d'exemple | Contenu |
|-----------------|---------|
| `public.regions`, `public.communes_france` | Limites administratives |
| `departement.departements` | Départements |
| `public.zps` | Zones de protection spéciale (Natura 2000) |
| `public.pav` | Points d'apport volontaire (collecte des déchets) |
| `public.ecole_elem_matern` | Écoles élémentaires et maternelles |
| `public.filaire_de_voirie`, `public.jour_collect` | Voirie et secteurs de collecte |
| `carthage.cours` | Cours d'eau |
| `cadastre_tlse.parcelles`, `cadastre_tlse.batiments` | Cadastre |

Les encadrés signalent les points importants :

> 💡 **Conseil** : une astuce qui fait gagner du temps.

> ⚠️ **Attention** : un piège qui peut fausser un résultat ou abîmer des données.

> ✅ **À retenir** : la règle essentielle de la section.

---

## 1. Prérequis et notions de base

### 1.1 Activer PostGIS dans une base

L'extension doit être activée **une fois par base de données** :

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Vérifier la version installée
SELECT PostGIS_Full_Version();
```

### 1.2 Comprendre le SRID (système de projection)

Chaque géométrie porte un **SRID**, le code EPSG de son système de coordonnées. Mélanger deux SRID dans une même requête provoque une erreur (voir section 20).

| SRID | Nom | Unité | Usage |
|------|-----|-------|-------|
| 2154 | Lambert-93 | mètres | Référence en France métropolitaine : mesures, surfaces, distances |
| 4326 | WGS 84 | degrés | GPS, GeoJSON, échanges de données |
| 3857 | Web Mercator | mètres (déformés) | Fonds de carte web (tuiles) |

> ⚠️ **Attention** : une distance ou une surface calculée en **4326** est exprimée en **degrés**, donc inexploitable. Pour mesurer, reprojeter d'abord en 2154 (section 12).

### 1.3 Les types de géométrie

| Type | Description | Exemple |
|------|-------------|---------|
| `POINT` | Un point | Une école, un arbre |
| `LINESTRING` | Une ligne | Un tronçon de route |
| `POLYGON` | Une surface | Une parcelle |
| `MULTIPOINT`, `MULTILINESTRING`, `MULTIPOLYGON` | Plusieurs éléments du même type en un seul objet | Une commune composée de plusieurs îlots |

### 1.4 Inspecter une base ou une table

```sql
-- Toutes les couches géographiques de la base
SELECT f_table_schema, f_table_name, f_geometry_column, type, srid
FROM geometry_columns
ORDER BY f_table_schema, f_table_name;

-- SRID et types réellement présents dans une table
SELECT ST_SRID(geom) AS srid, GeometryType(geom) AS type, COUNT(*) AS nb
FROM public.regions
GROUP BY 1, 2;
```

### 1.5 Les schémas

Un **schéma** est un dossier qui regroupe des tables (`public`, `cadastre_tlse`, `carthage`...). Pour éviter de le répéter à chaque requête, on peut le déclarer :

```sql
SET search_path TO cadastre_tlse, public;
```

### 1.6 Commandes `psql` utiles

| Commande | Effet |
|----------|-------|
| `\l` | Lister les bases |
| `\c nom_base` | Se connecter à une base |
| `\dn` | Lister les schémas |
| `\dt schema.*` | Lister les tables d'un schéma |
| `\d schema.table` | Décrire une table (colonnes, index, contraintes) |
| `\du` | Lister les rôles |
| `\dp schema.table` | Afficher les droits d'une table |
| `\dx` | Lister les extensions installées |
| `\q` | Quitter |

---

## 2. Aide-mémoire des fonctions PostGIS

Une règle simple permet de s'y retrouver :

- les fonctions qui répondent **vrai ou faux** (`ST_Intersects`, `ST_Contains`...) se placent dans **`WHERE`** ou dans **`JOIN ... ON`** ;
- les fonctions qui **fabriquent ou mesurent** quelque chose (`ST_Buffer`, `ST_Area`...) se placent dans **`SELECT`**.

### 2.1 Relations spatiales (vrai / faux)

<img width="1920" height="1380" alt="sql_relations_spatiales" src="https://github.com/user-attachments/assets/cbcbd5fc-e812-4d2c-a0bf-94d701ac600a" />

*Les relations spatiales renvoient VRAI ou FAUX. A est en rose, B en bleu.*

| Fonction | Rôle |
|----------|------|
| `ST_Intersects(A, B)` | Au moins un point commun. **La plus utilisée**, elle exploite l'index. |
| `ST_Contains(A, B)` | A contient entièrement B |
| `ST_Within(A, B)` | A est entièrement dans B (l'inverse de `ST_Contains`) |
| `ST_Touches(A, B)` | Contact par le bord seulement |
| `ST_Disjoint(A, B)` | Aucun point commun |
| `ST_DWithin(A, B, d)` | Distance entre A et B inférieure ou égale à `d` |
| `ST_Overlaps(A, B)` | Chevauchement partiel de deux surfaces de même dimension |
| `ST_Crosses(A, B)` | Une ligne traverse une autre ligne ou une surface |

### 2.2 Géotraitements (nouvelle géométrie)

<img width="1920" height="1344" alt="sql_geotraitements" src="https://github.com/user-attachments/assets/63d93bde-d364-43a8-bb44-bb11de43ea40" />

*Les géotraitements renvoient une nouvelle géométrie.*

| Fonction | Rôle |
|----------|------|
| `ST_Buffer(geom, d)` | Zone tampon à `d` mètres |
| `ST_Intersection(A, B)` | Partie commune |
| `ST_Difference(A, B)` | Partie de A qui n'est pas dans B |
| `ST_Union(A, B)` | Fusion de géométries (existe aussi en agrégat) |
| `ST_Centroid(geom)` | Centre géométrique (peut tomber hors de l'objet) |
| `ST_PointOnSurface(geom)` | Point garanti à l'intérieur de la surface |
| `ST_Simplify(geom, tol)` | Simplifie le tracé |

### 2.3 Mesures

| Fonction | Résultat (en Lambert-93) |
|----------|--------------------------|
| `ST_Area(geom)` | Surface en m² |
| `ST_Length(geom)` | Longueur en m |
| `ST_Perimeter(geom)` | Périmètre en m |
| `ST_Distance(A, B)` | Distance en m |

### 2.4 Construction, conversion et contrôle

| Fonction | Rôle |
|----------|------|
| `ST_Transform(geom, srid)` | Reprojette (recalcule les coordonnées) |
| `ST_SetSRID(geom, srid)` | Déclare le SRID sans recalculer |
| `ST_MakePoint(x, y)` | Crée un point |
| `ST_GeomFromText('POINT(x y)', srid)` | Crée une géométrie depuis du texte WKT |
| `ST_Multi(geom)` | Convertit en géométrie multiple |
| `ST_CollectionExtract(geom, type)` | Extrait les points (1), lignes (2) ou polygones (3) |
| `ST_Dump(geom)` | Éclate une géométrie multiple en parties |
| `ST_Collect(geom)` | Regroupe des géométries sans les fusionner |
| `ST_AsText(geom)`, `ST_AsGeoJSON(geom)` | Exporte en texte lisible ou en GeoJSON |
| `ST_IsValid(geom)`, `ST_IsValidReason(geom)` | Teste la validité et en donne la raison |
| `ST_MakeValid(geom)` | Tente de réparer une géométrie |
| `ST_IsEmpty(geom)` | Teste si la géométrie est vide |

> ✅ **À retenir** : `ST_Intersects` répond à la question « est-ce que ça se touche ? », `ST_Intersection` renvoie « la zone commune ». On filtre d'abord avec la première, on calcule ensuite avec la seconde.

---

## 3. Bonnes pratiques de requêtage spatial

Ces cinq réflexes évitent la majorité des erreurs et des lenteurs.

### 3.1 Vérifier le SRID avant de croiser deux couches

```sql
(SELECT 'zps' AS couche, ST_SRID(geom) AS srid FROM public.zps LIMIT 1)
UNION ALL
(SELECT 'regions', ST_SRID(geom) FROM public.regions LIMIT 1);
```

Si les SRID diffèrent, reprojeter l'une des deux couches avec `ST_Transform` (section 12).

### 3.2 Créer un index spatial sur chaque colonne `geom`

Sans index, PostgreSQL compare chaque objet avec tous les autres. Avec un index **GiST**, il ne regarde que les objets proches (détail en section 15).

```sql
CREATE INDEX idx_zps_geom ON public.zps USING GIST (geom);
```

### 3.3 Préférer `ST_DWithin` à `ST_Distance` dans une condition

```sql
-- ❌ Lent : la distance est calculée pour toutes les paires possibles
JOIN public.ecole_elem_matern e ON ST_Distance(e.geom, p.geom) <= 100

-- ✅ Rapide : l'index spatial est utilisé
JOIN public.ecole_elem_matern e ON ST_DWithin(e.geom, p.geom, 100)
```

`ST_Distance` reste utile **dans le `SELECT`** pour afficher ou trier la distance.

### 3.4 Contrôler la validité des géométries

Une géométrie invalide (polygone qui se croise lui-même, par exemple) provoque des erreurs de type `TopologyException` dans les traitements.

```sql
-- Repérer les géométries invalides et connaître la raison
SELECT id, ST_IsValidReason(geom) AS raison
FROM public.zps
WHERE NOT ST_IsValid(geom);

-- Les réparer (à faire sur une copie ou dans une transaction)
UPDATE public.zps
SET geom = ST_Multi(ST_CollectionExtract(ST_MakeValid(geom), 3))
WHERE NOT ST_IsValid(geom);
```

> 💡 **Conseil** : `ST_MakeValid` peut renvoyer un mélange de types. `ST_CollectionExtract(..., 3)` ne garde que les polygones, et `ST_Multi` remet le résultat au bon type de colonne.

### 3.5 Écrire des requêtes lisibles avec `WITH` (CTE)

Une **CTE** donne un nom à une étape intermédiaire. On lit la requête de haut en bas, comme une recette, et on peut tester chaque étape séparément.

```sql
WITH etape_1 AS (
    SELECT ...
),
etape_2 AS (
    SELECT ... FROM etape_1
)
SELECT ... FROM etape_2;
```

### 3.6 Tester avant de modifier

Pour toute commande qui **modifie** des données (`UPDATE`, `DELETE`, `ALTER`) :

```sql
BEGIN;                    -- ouvre une transaction

UPDATE public.regions SET ...;

SELECT COUNT(*) FROM public.regions WHERE ...;   -- vérifier le résultat

ROLLBACK;                 -- annule tout ; remplacer par COMMIT pour valider
```

> ⚠️ **Attention** : sans `BEGIN`, chaque commande est validée immédiatement et ne peut plus être annulée. Avant une opération massive, faites une copie : `CREATE TABLE public.regions_sauv AS SELECT * FROM public.regions;`

---

## 4. Géotraitements

### 4.1 Intersection (découpe) : surface totale de ZPS dans une région

**Objectif** : calculer la surface de zones de protection spéciale (ZPS) située à l'intérieur d'une région.

**Méthode** : on découpe chaque ZPS avec la région (`ST_Intersection`), on mesure les morceaux (`ST_Area`), puis on additionne.

```sql
WITH req AS (
   -- Étape 1 : découper les ZPS avec la région choisie
   SELECT sitecode, sitename,
          ST_CollectionExtract(
               ST_Multi(ST_Intersection(r.geom, z.geom)), 3
          )::geometry(MultiPolygon, 2154) AS geom_inter
   FROM public.zps AS z
   JOIN public.regions AS r ON ST_Intersects(r.geom, z.geom)
   WHERE r.code_reg = '72'
),
req_1 AS (
   -- Étape 2 : surface de chaque morceau, convertie de m² en km²
   SELECT sitecode, sitename,
          ST_Area(geom_inter) / 1000000 AS surface_km2
   FROM req
)
-- Étape 3 : somme
SELECT SUM(surface_km2) AS total_surface_km2
FROM req_1;
```

| Élément | Explication |
|---------|-------------|
| `ST_Intersects` dans le `JOIN` | Filtre rapide : ne garde que les ZPS qui touchent la région |
| `ST_Intersection` | Calcule la zone commune, plus coûteux, donc appliqué après le filtre |
| `ST_Multi` + `ST_CollectionExtract(..., 3)` | Force un résultat de type `MultiPolygon` et élimine les lignes ou points parasites |
| `/ 1000000` | Passage des m² aux km² |

> 💡 **Conseil** : adapter le code région (`'72'`) au référentiel utilisé, les codes ont changé avec la réforme des régions.

### 4.2 Différence + Buffer : zones non couvertes par un service

**Objectif** : trouver, pour chaque commune, les secteurs situés à **plus de 500 m** d'un point d'apport volontaire.

```sql
WITH req AS (
   -- Zone couverte : union de tous les tampons de 500 m
   SELECT ST_Union(ST_Buffer(pav.geom, 500)) AS buffered_union
   FROM public.pav
)
SELECT commune.geom AS commune_geom,
       ST_Difference(commune.geom, req.buffered_union) AS zone_non_couverte
FROM public.communes_france AS commune, req
WHERE ST_Intersects(commune.geom, req.buffered_union);
```

Lecture : *commune* moins *zone couverte* = *zone non couverte*.

> ⚠️ **Attention** : `ST_Union` sur un très grand nombre de tampons peut être long. En cas de lenteur, filtrer d'abord les PAV (par département, par exemple).

### 4.3 Distance entre objets : les 5 couples les plus proches

**Objectif** : lister les écoles situées à moins de 100 m d'un point d'apport volontaire, classées par distance.

Version d'origine, qui fonctionne mais calcule la distance pour toutes les paires :

```sql
SELECT DISTINCT e.id, p.commune, p.code_postal,
       ST_Distance(e.geom, p.geom) AS distance
FROM public.pav p
JOIN public.ecole_elem_matern e
     ON ST_Distance(e.geom, p.geom) <= 100
GROUP BY e.id, p.commune, p.code_postal, e.geom, p.geom
ORDER BY distance ASC
LIMIT 5;
```

Version recommandée, plus rapide grâce à l'index spatial :

```sql
SELECT e.id, p.commune, p.code_postal,
       ST_Distance(e.geom, p.geom) AS distance
FROM public.pav AS p
JOIN public.ecole_elem_matern AS e
     ON ST_DWithin(e.geom, p.geom, 100)
ORDER BY distance ASC
LIMIT 5;
```

---

## 5. Regrouper et compter : `GROUP BY`

**Objectif** : combien d'écoles se trouvent à moins de 50 m d'un point d'apport volontaire de type « textile » ?

```sql
SELECT p.type_flux,
       COUNT(DISTINCT e.id) AS nb_ecoles
FROM public.pav AS p
JOIN public.ecole_elem_matern AS e
     ON ST_DWithin(e.geom, p.geom, 50)
WHERE p.type_flux = 'textile'
GROUP BY p.type_flux;
```

> ⚠️ **Attention** : `COUNT(DISTINCT e.id)` compte chaque école **une seule fois**, même si plusieurs PAV sont proches. Un simple `COUNT(e.id)` la compterait autant de fois qu'il y a de PAV.

Variante avec une CTE, plus lisible quand la requête se complexifie :

```sql
WITH req AS (
   SELECT DISTINCT e.id, p.type_flux
   FROM public.pav p
   JOIN public.ecole_elem_matern e ON ST_DWithin(e.geom, p.geom, 50)
   WHERE p.type_flux = 'textile'
)
SELECT type_flux, COUNT(id) AS nb_ecoles
FROM req
GROUP BY type_flux;
```

### Fonctions d'agrégation courantes

| Fonction | Rôle |
|----------|------|
| `COUNT(*)`, `COUNT(DISTINCT col)` | Compter les lignes ou les valeurs distinctes |
| `SUM`, `AVG`, `MIN`, `MAX` | Somme, moyenne, minimum, maximum |
| `STRING_AGG(col, ', ')` | Concaténer des valeurs dans un texte |
| `ARRAY_AGG(col)` | Rassembler des valeurs dans un tableau |
| `ST_Union(geom)` | Fusionner des géométries |
| `ST_Collect(geom)` | Regrouper des géométries sans les fusionner |

`HAVING` filtre **après** le regroupement, alors que `WHERE` filtre **avant** :

```sql
SELECT p.commune, COUNT(*) AS nb_pav
FROM public.pav AS p
GROUP BY p.commune
HAVING COUNT(*) >= 5
ORDER BY nb_pav DESC;
```

---

## 6. Jointures avancées

### 6.1 Rappel des types de jointures

| Jointure | Résultat |
|----------|----------|
| `INNER JOIN` | Uniquement les lignes qui ont une correspondance des deux côtés |
| `LEFT JOIN` | Toutes les lignes de gauche, même sans correspondance |
| `CROSS JOIN` ou `ON TRUE` | Toutes les combinaisons possibles |
| `CROSS JOIN LATERAL` | Sous-requête exécutée pour chaque ligne de gauche |

### 6.2 Le plus proche voisin avec `ON TRUE` et `DISTINCT ON`

**Objectif** : trouver, pour chaque école, le point d'apport volontaire le plus proche.

```sql
SELECT DISTINCT ON (e.id)
       e.id AS ecole_id, p.id AS pav_id,
       p.commune, p.code_postal,
       ST_Distance(e.geom, p.geom) AS distance
FROM public.pav p
JOIN public.ecole_elem_matern e
     ON TRUE
ORDER BY e.id, distance ASC;
```

`ON TRUE` associe **chaque école à chaque PAV**, puis `DISTINCT ON (e.id)` garde la première ligne par école, donc la plus proche grâce au tri.

> ⚠️ **Attention** : le nombre de lignes intermédiaires est le produit des deux tables (1 000 écoles × 5 000 PAV = 5 millions). Acceptable sur de petites tables, pénalisant sur de grosses.

### 6.3 Version performante : `LATERAL` et opérateur `<->`

L'opérateur `<->` classe par distance en s'appuyant sur l'index spatial. Combiné à `LATERAL`, il évite de tout comparer :

```sql
SELECT e.id AS ecole_id, p.id AS pav_id,
       p.commune, p.code_postal,
       ST_Distance(e.geom, p.geom) AS distance
FROM public.ecole_elem_matern AS e
CROSS JOIN LATERAL (
    SELECT id, commune, code_postal, geom
    FROM public.pav
    ORDER BY geom <-> e.geom
    LIMIT 1
) AS p
ORDER BY e.id;
```

> 💡 **Conseil** : cette version suppose un index GiST sur `public.pav.geom`. Pour trouver les **3** plus proches, remplacer `LIMIT 1` par `LIMIT 3`.

### 6.4 `ST_DWithin` : écoles avec ou sans point d'apport textile

**Objectif** : répartir les écoles entre celles qui ont un PAV textile à moins de 50 m et les autres.

```sql
WITH req AS (
   SELECT COUNT(DISTINCT e.id) AS ecole_textile
   FROM public.pav p
   JOIN public.ecole_elem_matern e
       ON ST_DWithin(e.geom, p.geom, 50)
   WHERE p.type_flux ILIKE '%textile%'
)
SELECT
   (SELECT COUNT(*) FROM public.ecole_elem_matern) - req.ecole_textile AS ecoles_sans_pav_textile,
   req.ecole_textile AS ecoles_avec_pav_textile
FROM req;
```

`ILIKE '%textile%'` cherche le mot « textile » n'importe où dans le texte, sans tenir compte des majuscules.

Pour **lister** les écoles sans PAV textile, une jointure négative avec `NOT EXISTS` :

```sql
SELECT e.id
FROM public.ecole_elem_matern AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM public.pav AS p
    WHERE p.type_flux ILIKE '%textile%'
      AND ST_DWithin(e.geom, p.geom, 50)
);
```

---

## 7. `ST_Intersects` ou `ST_Intersection` ?

| Fonction | Rôle | Se place dans |
|----------|------|---------------|
| `ST_Intersects()` | Vrai / Faux | `WHERE` ou `ON` |
| `ST_Intersection()` | Zone commune (géométrie) | `SELECT` |

**Exemple** : longueur de voirie située dans les secteurs de collecte.

```sql
SELECT SUM(ST_Length(ST_Intersection(t1.geom, t2.geom))) / 1000 AS length_km
FROM public.filaire_de_voirie t1
JOIN public.jour_collect t2
   ON ST_Intersects(t1.geom, t2.geom);
```

`ST_Intersects` écarte rapidement les couples qui ne se touchent pas. `ST_Intersection` découpe ensuite les tronçons, `ST_Length` les mesure (en mètres), et la division par 1000 donne des kilomètres.

---

## 8. Découper un linéaire par département

**Objectif** : obtenir la portion d'un cours d'eau dans chaque département qu'il traverse.

```sql
SELECT d.code_insee,
       d.nom AS departement,
       c.nomentiteh AS cours_eau,
       ST_Intersection(c.geom, d.geom) AS segment_geom,
       ST_Length(ST_Intersection(c.geom, d.geom)) / 1000 AS longueur_km
FROM departement.departements AS d
JOIN carthage.cours AS c
   ON ST_Intersects(c.geom, d.geom)
WHERE c.nomentiteh = 'La Garonne'
  AND NOT ST_IsEmpty(ST_Intersection(c.geom, d.geom));
```

- La condition spatiale est dans le `ON`, le filtre sur le nom dans le `WHERE`.
- `NOT ST_IsEmpty(...)` écarte les cas où le contact est trop ponctuel pour produire un segment.
- Pour obtenir **un enregistrement par tronçon** au lieu d'un objet multiple, appliquer `ST_Dump` : `(ST_Dump(ST_Intersection(c.geom, d.geom))).geom`.

---

## 9. Distance depuis un point

**Objectif** : distance moyenne entre un point donné et les PAV d'une commune.

```sql
WITH req AS (
   SELECT commune,
          ST_Distance(geom, ST_GeomFromText('POINT(574103 6279386)', 2154)) AS distance
   FROM public.pav
   WHERE commune = 'Toulouse'
)
SELECT AVG(distance) AS average_distance
FROM req;
```

Le point est défini en **Lambert-93** (X Y, en mètres). Deux écritures équivalentes :

```sql
ST_GeomFromText('POINT(574103 6279386)', 2154)
ST_SetSRID(ST_MakePoint(574103, 6279386), 2154)
```

Pour partir de coordonnées GPS (longitude, latitude), il faut reprojeter :

```sql
ST_Transform(ST_SetSRID(ST_MakePoint(1.4442, 43.6047), 4326), 2154)
```

> 💡 **Conseil** : un `ORDER BY` à l'intérieur d'une CTE n'apporte rien quand le résultat final est une moyenne. Il a été retiré ici.

---
## 10. Créer et modifier des données

### 10.1 Créer une table (`CREATE TABLE`)

```sql
CREATE TABLE public.arbre (
   id_arbre  integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   diametre  real CHECK (diametre >= 0),
   hauteur   real CHECK (hauteur >= 0),
   geom      geometry(Point, 2154) NOT NULL
);

-- Toujours créer l'index spatial avec la table
CREATE INDEX idx_arbre_geom ON public.arbre USING GIST (geom);

-- Documenter la table et ses colonnes
COMMENT ON TABLE public.arbre IS 'Inventaire des arbres';
COMMENT ON COLUMN public.arbre.diametre IS 'Diamètre du tronc';
```

| Élément | Explication |
|---------|-------------|
| `GENERATED ALWAYS AS IDENTITY` | Numérotation automatique de l'identifiant |
| `PRIMARY KEY` | Identifiant unique, indispensable pour ouvrir la table dans QGIS |
| `CHECK (...)` | Règle de validité vérifiée à chaque écriture |
| `geometry(Point, 2154)` | Type de géométrie et SRID : PostGIS **refuse** toute géométrie qui ne correspond pas |
| `NOT NULL` | Interdit les objets sans géométrie |

### 10.2 Ajouter des lignes (`INSERT INTO`)

```sql
-- Plusieurs lignes d'un coup
INSERT INTO public.etat (type)
VALUES ('sain'), ('malade'), ('casse'), ('mort');

-- Une ligne avec une géométrie
INSERT INTO public.arbre (diametre, hauteur, geom)
VALUES (35.5, 12.0, ST_SetSRID(ST_MakePoint(574103, 6279386), 2154));

-- Depuis une autre table (même structure)
INSERT INTO public.arbre_archive (id_arbre, diametre, hauteur, geom)
SELECT id_arbre, diametre, hauteur, geom
FROM public.arbre
WHERE hauteur > 20;
```

### 10.3 Modifier des lignes (`UPDATE`, `CAST`, `ROUND`)

**Objectif** : stocker le périmètre de chaque région, en kilomètres arrondis à deux décimales.

```sql
-- 1. Créer la colonne si elle n'existe pas
ALTER TABLE public.regions
ADD COLUMN IF NOT EXISTS perimetre_km numeric(10, 2);

-- 2. La remplir
UPDATE public.regions
SET perimetre_km = ROUND((ST_Perimeter(geom) / 1000)::numeric, 2);
```

> ⚠️ **Attention** : `ROUND(x, 2)` exige un type `numeric`. Il faut donc convertir **le résultat entier** avec des parenthèses : `(ST_Perimeter(geom) / 1000)::numeric`. Écrire `ST_Perimeter(geom) / 1000::numeric` ne convertit que le `1000` et peut provoquer l'erreur `function round(double precision, integer) does not exist`.

> ⚠️ **Attention** : un `UPDATE` ou un `DELETE` **sans `WHERE`** modifie ou supprime **toutes** les lignes. Toujours vérifier d'abord avec un `SELECT` équivalent, et travailler dans une transaction (section 3.6).

### 10.4 Modifier la structure (`ALTER TABLE`)

| Action | Commande |
|--------|----------|
| Ajouter une colonne | `ALTER TABLE public.arbre ADD COLUMN essence varchar(100);` |
| Renommer une colonne | `ALTER TABLE public.arbre RENAME COLUMN essence TO espece;` |
| Changer le type | `ALTER TABLE public.arbre ALTER COLUMN espece TYPE varchar(150);` |
| Supprimer une colonne | `ALTER TABLE public.arbre DROP COLUMN espece;` |
| Ajouter une contrainte | `ALTER TABLE public.arbre ADD CONSTRAINT chk_hauteur CHECK (hauteur < 100);` |
| Renommer la table | `ALTER TABLE public.arbre RENAME TO arbre_inventaire;` |

---

## 11. Importer et exporter des données

### 11.1 Importer un Shapefile avec GDAL (`ogr2ogr`)

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=GDAL user=postgres host=localhost port=5434" "C:\path\REGION.shp" -nln public.regions -nlt MULTIPOLYGON -t_srs EPSG:2154 -lco GEOMETRY_NAME=geom -progress
```

| Option | Rôle |
|--------|------|
| `-f "PostgreSQL"` | Format de destination |
| `PG:"dbname=... user=... host=... port=..."` | Paramètres de connexion à la base |
| `-nln public.regions` | Nom de la table créée (avec son schéma) |
| `-nlt MULTIPOLYGON` | Force le type de géométrie (`PROMOTE_TO_MULTI` s'adapte automatiquement) |
| `-t_srs EPSG:2154` | Reprojette pendant l'import |
| `-lco GEOMETRY_NAME=geom` | Nomme la colonne géométrique `geom` |
| `-overwrite` / `-append` | Remplace la table / ajoute à la table existante |
| `-progress` | Affiche l'avancement |

> ⚠️ **Attention** : ne jamais écrire le **mot de passe en clair** dans la commande ou dans un document partagé. Deux solutions :
> 
> - une variable d'environnement le temps de la session (PowerShell : `$env:PGPASSWORD = "..."`) ;
> - un fichier de mots de passe : `%APPDATA%\postgresql\pgpass.conf` sous Windows, `~/.pgpass` sous Linux (droits `600`).

### 11.2 Alternative : `shp2pgsql`

```bash
shp2pgsql -I -s 2154 -W UTF-8 REGION.shp public.regions | psql -h localhost -p 5434 -U postgres -d GDAL
```

`-I` crée l'index spatial, `-s` fixe le SRID, `-W` indique l'encodage du fichier.

### 11.3 Importer un CSV puis construire les géométries

**Étape 1 : charger le fichier.** La table doit exister avec les mêmes colonnes que le CSV, dans le même ordre.

```sql
COPY public.faune_auvergne_temp
FROM 'C:/chemin/faune.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'UTF8');
```

> 💡 **Conseil** : `COPY` lit le fichier **sur le serveur** et demande des droits élevés. Depuis son poste, utiliser `\copy` dans `psql` (sur une seule ligne) :
> `\copy public.faune_auvergne_temp FROM 'C:/chemin/faune.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'UTF8')`
>
> Dans les chemins Windows, utiliser des `/` (ou doubler les `\`) pour éviter qu'un `\f` soit lu comme un saut de page.

**Étape 2 : ajouter la colonne géométrique.**

```sql
ALTER TABLE public.faune_auvergne_temp
ADD COLUMN geom geometry(Point, 2154);
```

**Étape 3 : la remplir.** Deux cas selon la source.

*Cas A : la géométrie existe dans une autre table, on la récupère par identifiant.*

```sql
UPDATE public.faune_auvergne_temp f
SET geom = (
   SELECT t.geom
   FROM public.faune_auvergne t
   WHERE t.id = f.id_num
)
WHERE EXISTS (
   SELECT 1
   FROM public.faune_auvergne t
   WHERE t.id = f.id_num
);
```

Le `WHERE EXISTS` évite d'écraser avec `NULL` les lignes sans correspondance. L'identifiant `t.id` doit être unique.

*Cas B : le CSV contient des colonnes X et Y.*

```sql
UPDATE public.faune_auvergne_temp
SET geom = ST_SetSRID(ST_MakePoint(x_l93, y_l93), 2154)
WHERE x_l93 IS NOT NULL AND y_l93 IS NOT NULL;
```

### 11.4 Exporter des données

```bash
# Une table entière vers un GeoPackage
ogr2ogr -f GPKG "C:\export\regions.gpkg" PG:"dbname=GDAL user=postgres host=localhost port=5434" public.regions

# Le résultat d'une requête
ogr2ogr -f GPKG "C:\export\pav_textile.gpkg" PG:"dbname=GDAL user=postgres host=localhost port=5434" -sql "SELECT id, commune, geom FROM public.pav WHERE type_flux = 'textile'" -nln pav_textile
```

```sql
-- Un CSV sans géométrie (à lancer dans psql, sur une seule ligne)
\copy (SELECT id, commune, ST_AsText(geom) AS wkt FROM public.pav) TO 'pav.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')
```

---

## 12. Reprojection : `ST_Transform` et `ST_SetSRID`

| Fonction | Ce qu'elle fait | Quand l'utiliser |
|----------|-----------------|------------------|
| `ST_SetSRID(geom, srid)` | **Déclare** le SRID sans toucher aux coordonnées | Le SRID est absent ou faux (0, par exemple), mais les coordonnées sont bonnes |
| `ST_Transform(geom, srid)` | **Recalcule** les coordonnées dans un autre système | Passer de 4326 à 2154, par exemple |

### Créer une nouvelle table reprojetée

```sql
CREATE TABLE public.table_reproj AS
SELECT id, nom, ST_Transform(geom, 4326)::geometry(Point, 4326) AS geom
FROM public.table_originale;

CREATE INDEX idx_table_reproj_geom ON public.table_reproj USING GIST (geom);
```

> ⚠️ **Attention** : écrire `SELECT ST_Transform(geom, 4326) AS geom, *` produit l'erreur `column "geom" specified more than once`, car `*` reprend aussi l'ancienne colonne `geom`. **Lister les colonnes voulues.**

### Reprojeter une table en place

```sql
ALTER TABLE public.table_originale
   ALTER COLUMN geom TYPE geometry(Point, 4326)
   USING ST_Transform(geom, 4326);
```

L'index spatial est reconstruit automatiquement. Faire une copie de sauvegarde avant, l'opération est irréversible une fois validée.

---

## 13. Générer des séries : dates disponibles avec `generate_series`

**Objectif** : lister les jours de mars 2025 où la salle n° 3 n'est pas réservée.

```sql
SELECT jour
FROM generate_series(
   '2025-03-01'::date,
   '2025-03-31'::date,
   '1 day'::interval
) AS jour
WHERE jour NOT IN (
   SELECT date_location::date
   FROM louer
   WHERE id_salle = '3'
     AND EXTRACT(YEAR FROM date_location) = 2025
     AND EXTRACT(MONTH FROM date_location) = 3
);
```

`generate_series` fabrique une ligne par jour, puis le `WHERE` retire les jours déjà réservés.

> ⚠️ **Attention** : si la sous-requête de `NOT IN` renvoie **une seule valeur `NULL`**, le résultat est **vide**. `NOT EXISTS` n'a pas ce défaut :

```sql
SELECT jour::date AS jour_libre
FROM generate_series('2025-03-01'::date, '2025-03-31'::date, '1 day'::interval) AS jour
WHERE NOT EXISTS (
   SELECT 1
   FROM louer AS l
   WHERE l.id_salle = '3'
     AND l.date_location::date = jour::date
);
```

`generate_series` sert aussi à produire des nombres : `SELECT n FROM generate_series(1, 10) AS n;`

---

## 14. Triggers (déclencheurs)

Un **trigger** exécute automatiquement une fonction quand une ligne est insérée, modifiée ou supprimée. On le crée en **deux temps** : la fonction, puis le trigger qui l'appelle.

| Élément | Signification |
|---------|---------------|
| `BEFORE` / `AFTER` | La fonction s'exécute avant ou après l'écriture |
| `INSERT`, `UPDATE`, `DELETE` | L'événement surveillé |
| `FOR EACH ROW` | Une exécution par ligne concernée |
| `NEW` / `OLD` | La ligne après / avant modification |

### 14.1 Date de création automatique

```sql
-- La colonne doit exister
ALTER TABLE public.test_mobilier
ADD COLUMN IF NOT EXISTS date_creation timestamp;

CREATE OR REPLACE FUNCTION fn_set_date_creation()
RETURNS trigger AS $$
BEGIN
   NEW.date_creation := NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_date_creation
BEFORE INSERT ON public.test_mobilier
FOR EACH ROW
EXECUTE FUNCTION fn_set_date_creation();
```

### 14.2 Surface calculée automatiquement

```sql
CREATE OR REPLACE FUNCTION update_area()
RETURNS TRIGGER AS $$
BEGIN
   NEW.surface_m2 := ST_Area(NEW.geom);
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_update_area
BEFORE INSERT OR UPDATE ON zones
FOR EACH ROW
EXECUTE FUNCTION update_area();
```

La surface est en **m²** si la géométrie est en Lambert-93. Pour remplir les lignes **déjà présentes** : `UPDATE zones SET geom = geom;` (le trigger recalcule la surface).

### 14.3 Gérer ses triggers

```sql
-- Lister les triggers de la base
SELECT tgname, tgrelid::regclass AS table_cible
FROM pg_trigger
WHERE NOT tgisinternal;

-- Désactiver / réactiver temporairement
ALTER TABLE public.test_mobilier DISABLE TRIGGER trg_set_date_creation;
ALTER TABLE public.test_mobilier ENABLE TRIGGER trg_set_date_creation;

-- Supprimer
DROP TRIGGER IF EXISTS trg_set_date_creation ON public.test_mobilier;
```

> 💡 **Conseil** : préfixer les noms (`trg_` pour un trigger, `fn_` pour une fonction) permet de les retrouver facilement.

---

## 15. Index et performance

### 15.1 Index spatial (GiST)

Il accélère `ST_Intersects`, `ST_DWithin`, `ST_Contains`, l'opérateur `<->` et toutes les jointures spatiales.

```sql
CREATE INDEX idx_parcelles_geom
ON cadastre_tlse.parcelles USING GIST (geom);

ANALYZE cadastre_tlse.parcelles;
```

### 15.2 Index sur les colonnes ordinaires (B-tree)

```sql
-- Index classique
CREATE INDEX idx_parcel_numpar ON village.parcel (numpar);

-- Index partiel : ne concerne que les lignes qui respectent la condition
CREATE INDEX idx_parcel_numpar_c10436
ON village.parcel (numpar)
WHERE numpar ILIKE 'c10436';
```

Un index partiel est petit et rapide, mais **n'est utilisé que si la requête contient la même condition**.

### 15.3 Comprendre pourquoi une requête est lente : `EXPLAIN`

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM public.pav AS p
JOIN public.ecole_elem_matern AS e
  ON ST_DWithin(e.geom, p.geom, 50);
```

| Ce que l'on lit | Signification |
|-----------------|---------------|
| `Seq Scan` | Lecture complète de la table : lent sur une grosse table |
| `Index Scan`, `Bitmap Index Scan` | Un index est utilisé : bon signe |
| `Execution Time` | Durée réelle de la requête |
| `rows=` estimé et réel très différents | Statistiques périmées : lancer `ANALYZE` |

> ⚠️ **Attention** : `EXPLAIN ANALYZE` **exécute vraiment** la requête. Pour un `UPDATE` ou un `DELETE`, l'entourer de `BEGIN` ... `ROLLBACK`.

### 15.4 Maintenance

```sql
-- Mettre à jour les statistiques et nettoyer (surtout après un gros import ou une restauration)
VACUUM (ANALYZE) public.pav;

-- Reconstruire un index
REINDEX INDEX idx_arbre_geom;
```

PostgreSQL le fait seul en tâche de fond (*autovacuum*), mais un `ANALYZE` manuel après un gros chargement évite des plans de requête mal calculés.

### 15.5 Connaître la taille des tables et de la base

```sql
SELECT relname AS "Table",
       pg_size_pretty(pg_total_relation_size(relid)) AS "Size",
       pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS "External Size"
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Taille de la base entière
SELECT pg_size_pretty(pg_database_size(current_database())) AS taille_base;
```

`Size` est la taille totale (données + index + données volumineuses). `External Size` est la part hors table : index et stockage annexe.

---
## 16. Droits, rôles et groupes

<img width="1920" height="1120" alt="sql_roles_droits" src="https://github.com/user-attachments/assets/313a22b1-0d39-4c7a-8257-676ec862472f" />

*Les droits sont donnés aux groupes, et les utilisateurs rejoignent les groupes dont ils ont besoin.*

### 16.1 Définitions

Un **privilège** est un droit sur un objet de la base, attribué à un **rôle**. Les privilèges se règlent finement, à plusieurs niveaux :

- la **base de données** ;
- le **schéma** ;
- la **table** (relation) ;
- la **colonne** (attribut).

Un utilisateur peut ainsi recevoir un privilège sur toute une base, sur le contenu d'un schéma, sur quelques tables seulement, ou sur quelques colonnes de certaines tables.

Dans PostgreSQL, **tout est un rôle** : un rôle avec `LOGIN` est un **utilisateur** (une personne ou une application), un rôle sans `LOGIN` sert de **groupe**.

### 16.2 Les cinq règles d'attribution des privilèges

| Règle | Principe | Dans la pratique |
|-------|----------|------------------|
| **n°0 : un mot de passe pour chacun** | Tous les utilisateurs (personnes et applications) ont un mot de passe | Mots de passe longs, uniques, jamais partagés dans un mail ou un document |
| **n°1 : moindre privilège** | Chacun n'a que les droits strictement nécessaires à ses tâches. Les droits évoluent avec les besoins | Éviter de créer plusieurs comptes administrateurs |
| **n°2 : contrôle de la population** | Les droits doivent suivre la réalité des équipes : départs, arrivées, changements de poste | Supprimer ou désactiver les comptes des personnes qui partent ou changent de tâche |
| **n°3 : supervision de la délégation** | Un administrateur peut déléguer l'attribution de droits (`WITH GRANT OPTION`). Un contrôle a posteriori vérifie que le résultat respecte la politique choisie | Auditer régulièrement qui possède quels droits (section 16.9) |
| **n°4 : contrôle physique des connexions** | La connexion est possible depuis n'importe où via Internet : il faut la restreindre à des hôtes connus | Configurer le fichier `pg_hba.conf` (section 16.11) |

### 16.3 Créer des utilisateurs et des groupes

```sql
-- Un utilisateur : il peut se connecter
CREATE ROLE lea LOGIN PASSWORD 'UnMotDePasseLongEtUnique';

-- Des groupes : ils ne se connectent pas, ils portent des droits
CREATE ROLE gr_visu NOLOGIN;
CREATE ROLE gr_gestion_parcelles NOLOGIN;
CREATE ROLE gr_gestion_batiments NOLOGIN;
CREATE ROLE gr_dessin_cadastre NOLOGIN;
CREATE ROLE gr_maj_type_bati NOLOGIN;
```

> ⚠️ **Attention** : PostgreSQL met en **minuscules** les noms non entourés de guillemets (`Lea` devient `lea`). Écrire tous les noms en minuscules évite les surprises. Le mot de passe `'toto'` des exemples de cours ne doit **jamais** être utilisé en production.

> 💡 **Conseil** : pour définir ou changer un mot de passe sans qu'il apparaisse dans l'historique des commandes, utiliser la commande `psql` `\password lea`.

### 16.4 Autoriser l'accès au schéma

Pour utiliser les tables d'un schéma, un rôle a besoin du droit **`USAGE` sur le schéma**, en plus des droits sur les tables. C'est l'oubli le plus fréquent (erreur `permission denied for schema`).

```sql
GRANT USAGE ON SCHEMA cadastre_tlse
TO gr_visu, gr_gestion_parcelles, gr_gestion_batiments, gr_dessin_cadastre, gr_maj_type_bati;
```

### 16.5 Les privilèges disponibles

| Privilège | Autorise | Objets concernés |
|-----------|----------|------------------|
| `SELECT` | Lire les colonnes de la table, ou seulement celles listées. Permet aussi `COPY TO`. Nécessaire pour référencer des valeurs existantes dans un `UPDATE` ou un `DELETE` | Table, vue, séquence |
| `INSERT` | Ajouter des lignes (éventuellement sur certaines colonnes, les autres prennent leur valeur par défaut). Permet aussi `COPY FROM` | Table |
| `UPDATE` | Modifier les colonnes de la table ou celles listées. Une commande `UPDATE` demande **aussi** `SELECT`, car elle doit lire les colonnes pour repérer les lignes | Table |
| `DELETE` | Supprimer des lignes. Demande **aussi** `SELECT` | Table |
| `TRUNCATE` | Vider entièrement la table | Table |
| `REFERENCES` | Créer une clé étrangère. Requis sur les colonnes qui référencent et les colonnes référencées | Table, colonnes |
| `TRIGGER` | Créer un déclencheur sur la table | Table |
| `CREATE` | **Base** : créer des schémas. **Schéma** : créer des objets dedans (renommer un objet demande d'en être propriétaire et d'avoir ce droit sur le schéma). **Tablespace** : y créer tables, index et fichiers temporaires | Base, schéma, tablespace |
| `CONNECT` | Se connecter à la base (en plus des règles de `pg_hba.conf`) | Base |
| `TEMPORARY`, `TEMP` | Créer des tables temporaires dans la base | Base |
| `EXECUTE` | Utiliser une fonction ou un opérateur. Seul droit applicable aux fonctions (y compris les agrégats) | Fonction |
| `USAGE` | Accéder au contenu d'un schéma, ou utiliser une séquence | Schéma, séquence |
| `ALL PRIVILEGES` | Tous les droits disponibles en une seule fois (le mot `PRIVILEGES` est facultatif sous PostgreSQL mais exigé par le standard SQL) | Tous |

### 16.6 La commande `GRANT` (attribuer des droits)

Syntaxe générale :

```sql
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
```

Accorder des privilèges **sur des colonnes** :

```sql
GRANT { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
```

`WITH GRANT OPTION` permet au bénéficiaire de **transmettre** ce droit à d'autres : à réserver aux administrateurs (règle n°3).

**Exemples simples** :

```sql
-- Un utilisateur qui ne doit que consulter
GRANT SELECT ON TABLE parcelles TO utilisateur;
GRANT SELECT ON TABLE proprio TO utilisateur;

-- Droits de lecture-écriture pour un opérateur de saisie
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE parcelles TO operateur_saisie;
```

### 16.7 Mettre en place une organisation par groupes

C'est la méthode à privilégier : **un groupe par profil**, puis on y place les personnes.

**Étape 1 : donner les droits aux groupes**

```sql
-- Lecture de tout le schéma
GRANT SELECT ON ALL TABLES IN SCHEMA cadastre_tlse TO gr_visu;

-- Gestion complète des parcelles et des bâtiments
GRANT SELECT, INSERT, UPDATE, DELETE ON cadastre_tlse.parcelles TO gr_gestion_parcelles;
GRANT SELECT, INSERT, UPDATE, DELETE ON cadastre_tlse.batiments TO gr_gestion_batiments;

-- Redessiner uniquement la géométrie des parcelles
GRANT UPDATE (geom) ON cadastre_tlse.parcelles TO gr_dessin_cadastre;

-- Mettre à jour uniquement le type de bâtiment (adapter le nom de la colonne)
GRANT UPDATE (type_bati) ON cadastre_tlse.batiments TO gr_maj_type_bati;
```

**Étape 2 : placer les personnes dans les groupes**

```sql
GRANT gr_visu TO lea;
GRANT gr_dessin_cadastre TO lea;
```

**Étape 3 (facultative) : prévoir les tables futures**

Les droits ne s'appliquent qu'aux tables **existantes**. Pour que les tables créées plus tard soient lisibles par `gr_visu` :

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA cadastre_tlse
GRANT SELECT ON TABLES TO gr_visu;
```

Cette règle s'applique aux objets créés par le rôle qui l'exécute (ajouter `FOR ROLE proprietaire` pour cibler un autre créateur). Pour les colonnes de type `serial`, il faut aussi : `GRANT USAGE ON ALL SEQUENCES IN SCHEMA cadastre_tlse TO gr_gestion_parcelles;`

**Résultat attendu** :

| Groupe | Table `parcelles` | Table `batiments` |
|--------|-------------------|-------------------|
| `gr_visu` | Lecture | Lecture |
| `gr_gestion_parcelles` | Lecture, ajout, modification, suppression | Aucun droit propre |
| `gr_gestion_batiments` | Aucun droit propre | Lecture, ajout, modification, suppression |
| `gr_dessin_cadastre` | Modification de `geom` | Aucun droit propre |
| `gr_maj_type_bati` | Aucun droit propre | Modification de `type_bati` |

> 💡 **Conseil** : donner un droit directement à une personne reste possible, par exemple pour des colonnes précises, mais devient vite ingérable. Exemple, à réserver aux cas particuliers :

```sql
GRANT SELECT (fid, geom), UPDATE (geom)
ON TABLE cadastre_tlse.parcelles, cadastre_tlse.batiments
TO lea;
```

### 16.8 Retirer des droits (`REVOKE`)

La commande `REVOKE` enlève un ou plusieurs privilèges à un rôle.

```sql
REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    FROM { [ GROUP ] role_name | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]
```

| Option | Effet |
|--------|-------|
| `GRANT OPTION FOR` | Seule la **possibilité de transmettre** le droit est retirée, pas le droit lui-même |
| `FROM PUBLIC` | Concerne tous les utilisateurs auxquels le droit a été donné via le mot-clé `PUBLIC` |
| `CASCADE` | Retire aussi les droits que le bénéficiaire avait redistribués |
| `RESTRICT` | Refuse l'opération s'il existe des droits dépendants (comportement par défaut) |

```sql
-- Retirer un droit à un groupe
REVOKE DELETE ON cadastre_tlse.parcelles FROM gr_gestion_parcelles;

-- Retirer une personne d'un groupe
REVOKE gr_visu FROM lea;
```

> 💡 **Conseil** : depuis PostgreSQL 15, tout le monde n'a plus le droit de créer des objets dans le schéma `public`. Sur une version plus ancienne, retirer ce droit : `REVOKE CREATE ON SCHEMA public FROM PUBLIC;`

### 16.9 Vérifier qui a quels droits

```sql
-- Droits d'une table (dans psql)
\dp cadastre_tlse.parcelles

-- Un utilisateur a-t-il ce droit ?
SELECT has_table_privilege('lea', 'cadastre_tlse.parcelles', 'SELECT');

-- Tous les droits d'un schéma, par rôle
SELECT grantee, table_schema, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'cadastre_tlse'
ORDER BY grantee, table_name;
```

La commande `\du` affiche la liste des rôles et leurs attributs.

### 16.10 Suivre la vie d'un compte

```sql
-- Changer un mot de passe
ALTER ROLE lea PASSWORD 'NouveauMotDePasseLong';

-- Désactiver un compte sans le supprimer (congé long, par exemple)
ALTER ROLE lea NOLOGIN;

-- Supprimer définitivement (départ de l'agence) : dans cet ordre
REASSIGN OWNED BY lea TO postgres;   -- transfère les objets que lea possédait
DROP OWNED BY lea;                   -- retire ses droits
DROP ROLE lea;
```

### 16.11 Restreindre les connexions (`pg_hba.conf`)

Ce fichier du serveur liste **qui peut se connecter, depuis où, et comment**. Chaque ligne est une règle, lue de haut en bas.

```text
# TYPE  BASE    UTILISATEUR  ADRESSE            METHODE
host    all     all          192.168.1.0/24     scram-sha-256
host    mabase  lea          10.0.0.15/32       scram-sha-256
```

- La première règle autorise tout le réseau interne `192.168.1.0/24`.
- La seconde n'autorise `lea` que depuis une machine précise, vers la base `mabase`.
- Après modification, recharger la configuration : `SELECT pg_reload_conf();`
- Pour retrouver l'emplacement du fichier : `SHOW hba_file;`

> ⚠️ **Attention** : éviter les règles trop larges comme `0.0.0.0/0`, qui ouvrent la base à tout Internet. Seul un administrateur du serveur peut modifier ce fichier.

---

## 17. Sauvegarder et restaurer une base PostgreSQL

<img width="1920" height="800" alt="sql_sauvegarde" src="https://github.com/user-attachments/assets/31ace920-c1ad-48a9-88f9-2f63670caa23" />

*Le circuit complet : on sauvegarde, on conserve plusieurs copies, et on teste régulièrement la restauration.*

### 17.1 Principe

L'objectif est de produire un **fichier de sauvegarde** (« dump ») qui, renvoyé au serveur, recrée une base de données **identique** à celle sauvegardée. PostgreSQL fournit pour cela le programme **`pg_dump`**.

Les extractions peuvent prendre la forme de **scripts** ou de **fichiers d'archive** :

| Format | Option | Extension courante | Se restaure avec | Particularités |
|--------|--------|--------------------|------------------|----------------|
| Script texte | `-F p` (par défaut) | `.sql` | `psql` | Lisible et modifiable. Contient les commandes SQL qui reconstruisent la base |
| Archive « custom » | `-F c` | `.dump` | `pg_restore` | Compressé. Permet de choisir et réordonner les éléments à restaurer, et la restauration en parallèle |
| Archive « directory » | `-F d` | un dossier | `pg_restore` | Compressé. **Seul format** qui permet de sauvegarder en parallèle (`-j`) |
| Archive « tar » | `-F t` | `.tar` | `pg_restore` | Non compressé, moins pratique |

> 💡 **Conseil** : pour l'usage courant, le format **custom** (`-F c`) est le meilleur compromis : compact, fiable, et restaurable partiellement.

### 17.2 Avec l'interface pgAdmin 4

- **Sauvegarder** : clic droit sur la base, puis **Backup...**
- **Restaurer** : clic droit sur la base (ou sur une base vide), puis **Restore...**, et choisir le fichier de sauvegarde.

Après la restauration, **tout est recréé** : schémas, tables avec leurs colonnes (y compris `geom`), index, etc.

### 17.3 Sauvegarder en ligne de commande (`pg_dump`)

```bash
pg_dump base_de_donnees > fichier_sauvegarde
```

Exemple complet, ici sous Linux. Le fichier est créé dans le dossier courant (`/home/idgeo`) :

```bash
idgeo@GS8:~$ pg_dump -f rugby_sauv.sql -d rugby_top -p 5432 -U postgres
```

| Option | Rôle |
|--------|------|
| `-h` | Hôte du serveur (`localhost`, nom ou adresse IP) |
| `-p` | Port (5432 par défaut) |
| `-U` | Utilisateur |
| `-d` | Base à sauvegarder |
| `-f` | Fichier de sortie |
| `-F` | Format (`p`, `c`, `d`, `t`) |
| `-n` | Ne sauvegarder qu'un schéma |
| `-t` | Ne sauvegarder qu'une table |
| `-s` | Structure seule, sans les données |
| `-a` | Données seules, sans la structure |
| `-j` | Nombre de tâches en parallèle (format `d` uniquement) |

**Exemples utiles** :

```bash
# Toute la base, au format custom
pg_dump -U postgres -p 5432 -F c -f sauv_base.dump nom_base

# Un seul schéma
pg_dump -U postgres -n cadastre_tlse -F c -f sauv_cadastre.dump nom_base

# Une seule table
pg_dump -U postgres -t public.regions -F c -f sauv_regions.dump nom_base

# La structure uniquement (modèle de données)
pg_dump -U postgres -s -f structure.sql nom_base

# Format dossier, 4 tâches en parallèle (grosses bases)
pg_dump -U postgres -F d -j 4 -f sauv_dossier nom_base
```

### 17.4 Restaurer une sauvegarde

**Étape 1 : créer une base vide** dans laquelle on va restaurer :

```bash
psql -U postgres -p 5432 -c "CREATE DATABASE idgeo_locale;"
```

**Étape 2 : activer PostGIS** (indispensable si la base contient des données géographiques) :

```bash
psql -U postgres -p 5432 -d idgeo_locale -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

**Étape 3 : restaurer le fichier**, selon son format :

```bash
# Script texte (.sql)
psql -U postgres -p 5432 -d idgeo_locale -f sauv_idgeo.sql

# Archive custom ou dossier (.dump)
pg_restore -U postgres -p 5432 -d idgeo_locale -j 4 sauv_base.dump
```

> 💡 **Conseil** : l'écriture `psql ... < fichier.sql` fonctionne sous Linux, mais pas sous **PowerShell** (Windows). L'option **`-f`** marche partout.

**Étape 4 : se reconnecter pour vérifier** :

```bash
psql -U postgres -p 5432 -d idgeo_locale
```

**Étape 5 : recalculer les statistiques** (voir section 15.4) :

```sql
ANALYZE;
```

Pour **remplacer** des objets existants lors d'une restauration depuis une archive : `pg_restore -c --if-exists ...`

> ⚠️ **Attention** : tous les utilisateurs qui possèdent des objets, ou qui ont des droits sur les objets de la base sauvegardée, doivent **exister avant la restauration**. Sinon la création de ces objets échoue. Voir `pg_dumpall --globals-only` ci-dessous pour sauvegarder les rôles.

**À savoir** :

- `pg_dump` permet de restaurer une base sur une version **plus récente** du serveur.
- C'est aussi la seule méthode qui fonctionne pour transférer une base vers une machine d'une **architecture différente** (par exemple d'un serveur 32 bits à un serveur 64 bits).

### 17.5 Sauvegarder tout le serveur (`pg_dumpall`)

`pg_dumpall` sauvegarde **tout un cluster** : toutes les bases, les rôles et les tablespaces.

```bash
pg_dumpall -U postgres -f sauv_cluster.sql

# Seulement les rôles et les tablespaces (à conserver avec les sauvegardes de bases)
pg_dumpall -U postgres --globals-only -f sauv_roles.sql
```

Pour restaurer un fichier `.sql` dans une nouvelle base PostGIS :

```bash
psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE nombase;"
psql -h localhost -p 5432 -U postgres -d nombase -c "CREATE EXTENSION postgis;"
psql -h localhost -p 5432 -U utilisateur -d nombase -f chemin\complet\du\fichier.sql
```

> ⚠️ **Attention** : il est préférable d'avoir les droits de **superutilisateur** pour obtenir une sauvegarde complète. Il faut **obligatoirement** ce profil pour restaurer une sauvegarde faite avec `pg_dumpall`, afin de pouvoir recréer les rôles et les tablespaces. Si des tablespaces sont utilisés, vérifier que leurs chemins conviennent à la nouvelle installation.

### 17.6 Copier une base directement d'un serveur à un autre

```bash
pg_dump -h serveur1 base_de_donnees | psql -h serveur2 base_de_donnees
```

La base de destination doit déjà exister (créée vide, avec PostGIS activé).

### 17.7 Automatiser la sauvegarde

Selon la taille de l'infrastructure, des sauvegardes interviennent à plusieurs niveaux. Souvent, le **serveur hôte** de PostgreSQL est déjà sauvegardé. On peut y ajouter une sauvegarde **propre à la base**, à un rythme adapté : régulier pour des données qui changent souvent, plus espacé pour un modèle qui évolue peu.

**Étape 1 : écrire le script** (`sauvegarde_bdd.sh`, à placer par exemple dans `/usr/local/bin/`)

```bash
#!/bin/bash
# Sauvegarde d'un schéma PostgreSQL (format custom) avec suppression des anciennes copies

DB_USER="postgres"                  # utilisateur PostgreSQL
DB_NAME="ma_base"                   # base à sauvegarder
DB_SCHEMA="mon_schema"              # schéma à sauvegarder (retirer l'option -n pour toute la base)
BACKUP_DIR="/home/xxx/sauv_bdd"     # dossier de destination
RETENTION_JOURS=30                  # durée de conservation

DATE=$(date +%Y-%m-%d_%Hh%M)
BACKUP_FILE="${BACKUP_DIR}/sauv_${DB_NAME}_${DB_SCHEMA}_${DATE}.dump"

mkdir -p "$BACKUP_DIR"

if ! pg_dump -U "$DB_USER" -F c -n "$DB_SCHEMA" -f "$BACKUP_FILE" "$DB_NAME"; then
    echo "ECHEC : la sauvegarde de ${DB_NAME} a échoué" >&2
    exit 1
fi

echo "Sauvegarde OK : ${BACKUP_FILE}"

# Supprimer les sauvegardes plus vieilles que RETENTION_JOURS
find "$BACKUP_DIR" -name "sauv_${DB_NAME}_*.dump" -mtime +"$RETENTION_JOURS" -delete
```

**Étape 2 : éviter le mot de passe en clair.** Créer le fichier `~/.pgpass` (droits `600`, soit `chmod 600 ~/.pgpass`) avec une ligne :

```text
localhost:5432:ma_base:postgres:le_mot_de_passe
```

**Étape 3 : rendre le script exécutable**

```bash
chmod +x /usr/local/bin/sauvegarde_bdd.sh
```

**Étape 4 : planifier avec `crontab`**

```bash
crontab -e
```

Ajouter une ligne dans le fichier qui s'ouvre :

```text
# m  h  dom mon dow   commande
20   *  *   *   *     /usr/local/bin/sauvegarde_bdd.sh >> /home/xxx/sauv_bdd/sauvegarde.log 2>&1
```

**Comment régler le rythme ?** Les cinq champs se lisent ainsi :

```text
# .---------------- minute (0 - 59)
# |  .------------- heure (0 - 23)
# |  |  .---------- jour du mois (1 - 31)
# |  |  |  .------- mois (1 - 12) ou jan, feb, mar...
# |  |  |  |  .---- jour de la semaine (0 - 6) (dimanche = 0 ou 7) ou sun, mon, tue...
# |  |  |  |  |
# *  *  *  *  *  commande à exécuter
```

| Exemple | Signification |
|---------|---------------|
| `20 * * * *` | Toutes les heures, à la minute 20 |
| `0 2 * * *` | Tous les jours à 2 h |
| `0 3 * * 0` | Tous les dimanches à 3 h |
| `*/15 * * * *` | Toutes les 15 minutes |

[🔗 Cron et crontab : le planificateur de tâches (LinuxTricks)](https://www.linuxtricks.fr/wiki/cron-et-crontab-le-planificateur-de-taches)

> ⚠️ **Attention** : `cron` s'exécute avec un environnement minimal. Utiliser des **chemins complets** dans le script, et conserver la redirection vers un fichier journal (`>> ... 2>&1`) pour comprendre un éventuel échec.

**Exemple d'essai rapide sous Ubuntu (Terminal)**

On crée le fichier avec :

```bash
idgeo@GS8:~$ nano script_sauv_bdd.sh
```

Dans l'éditeur, on écrit :

```bash
#!/bin/bash
pg_dump -f sauv_bdd_auto.sql -U postgres -p 5432 -d idgeo_locale
```

On enregistre (Ctrl + O puis Entrée) et on quitte (Ctrl + X). On rend ensuite le script exécutable :

```bash
idgeo@GS8:~$ chmod a+x script_sauv_bdd.sh
```

Puis on planifie :

```bash
idgeo@GS8:~$ crontab -e
```

Pour **tester sans attendre**, on choisit une minute proche de l'heure actuelle. Il est 16 h 56 : on programme 16 h 58 :

```text
58 * * * * /home/idgeo/script_sauv_bdd.sh
```

On enregistre, on quitte, et à 16 h 58 le fichier `sauv_bdd_auto.sql` doit apparaître.

> 💡 **Conseil** : sous **Windows**, le même principe s'applique avec le **Planificateur de tâches** qui lance `pg_dump.exe`.

### 17.8 Les bonnes pratiques de sauvegarde

| Pratique | Pourquoi |
|----------|----------|
| **Règle 3-2-1** : 3 copies, sur 2 supports différents, dont 1 hors site | Une seule copie ne protège pas d'un incident matériel, d'un vol ou d'un incendie |
| **Tester la restauration** sur une base vide, au moins une fois par trimestre | Une sauvegarde jamais restaurée peut se révéler inutilisable le jour où l'on en a besoin |
| **Sauvegarder aussi les rôles** (`--globals-only`) | Sinon les droits sont perdus à la restauration |
| **Protéger les fichiers** de sauvegarde | Ils contiennent toutes les données : limiter l'accès |
| **Supprimer les anciennes copies** automatiquement | Évite de saturer le disque |
| **Surveiller le journal** de la sauvegarde | Un échec silencieux n'est découvert qu'au moment du besoin |
| **Sauvegarder avant toute opération risquée** (migration, mise à jour massive) | Permet de revenir en arrière |

---

## 18. Vues et vues matérialisées

| Objet | Contient | Données à jour ? | Rapidité |
|-------|----------|------------------|----------|
| **Table** | Les données elles-mêmes | Oui | Rapide |
| **Vue** | Une requête enregistrée | Oui, toujours | Même vitesse que la requête |
| **Vue matérialisée** | Le **résultat** de la requête, stocké | Non : à rafraîchir | Rapide, et indexable |

```sql
-- Vue simple : toujours à jour, mais recalculée à chaque lecture
CREATE VIEW public.v_pav_textile AS
SELECT id, commune, code_postal, geom
FROM public.pav
WHERE type_flux ILIKE '%textile%';

-- Vue matérialisée : résultat stocké sur le disque
CREATE MATERIALIZED VIEW public.mv_pav_textile AS
SELECT id, commune, code_postal, geom
FROM public.pav
WHERE type_flux ILIKE '%textile%'
WITH DATA;

-- On peut indexer une vue matérialisée
CREATE INDEX idx_mv_pav_textile_geom ON public.mv_pav_textile USING GIST (geom);

-- La mettre à jour quand les données sources changent
REFRESH MATERIALIZED VIEW public.mv_pav_textile;
```

> 💡 **Conseil** : `REFRESH MATERIALIZED VIEW CONCURRENTLY ...` met à jour **sans bloquer les lectures**, mais exige un **index unique** sur la vue matérialisée.

> 💡 **Conseil** : pour ouvrir une vue dans QGIS, elle doit contenir une colonne d'identifiant **unique** (ici `id`).

---

## 19. Connexions distantes (Foreign Data Wrappers)

Un **FDW** (*Foreign Data Wrapper*) présente des **données externes comme des tables locales**, que l'on interroge en SQL.

| Source | Extension | Accès |
|--------|-----------|-------|
| Autre base PostgreSQL | `postgres_fdw` | Lecture / écriture |
| Oracle, MySQL | `oracle_fdw`, `mysql_fdw` | Lecture / écriture |
| Fichiers CSV ou à largeur fixe | `file_fdw` | Lecture |
| Services et fichiers géographiques (WFS, Shapefile, GeoPackage...) | `ogr_fdw` | Lecture (écriture selon le format) |
| ODBC, JDBC, Multicorn, NoSQL (CouchDB, Redis) | extensions dédiées | Selon le pilote |

Le FDW standard de PostgreSQL, `postgres_fdw`, permet d'accéder aux tables de serveurs PostgreSQL distants de manière très transparente. Il permet aussi à la **géométrie PostGIS** de passer des hôtes distants aux hôtes locaux, ce qui est très pratique.

### 19.1 Lire une table d'une autre base PostgreSQL

```sql
-- 0. Activer l'extension (une fois par base)
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 1. Création d'un lien vers la base de données bd_test_postgis
CREATE SERVER foreign_bd
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host 'localhost', port '5434', dbname 'bd_test_postgis');

-- 2. Associer un utilisateur de la base distante à un utilisateur local
CREATE USER MAPPING FOR postgres          -- utilisateur local
        SERVER foreign_bd
        OPTIONS (user 'postgres', password 'postgres');   -- utilisateur distant

-- 3. Création d'une table ayant la même structure que la table distante
CREATE FOREIGN TABLE foreign_parkings (
    osm_id integer NOT NULL,
    date_heure timestamp without time zone,
    nom character varying,
    type_obj character varying,
    xcoord double precision,
    ycoord double precision,
    geom geometry(Point, 2154)
)
    SERVER foreign_bd
        OPTIONS (schema_name 'parkings', table_name 't_parking');

-- 4. Utilisation
SELECT * FROM foreign_parkings LIMIT 10;
```

**Variante rapide** : importer d'un coup la structure des tables distantes.

```sql
IMPORT FOREIGN SCHEMA parkings
LIMIT TO (t_parking)
FROM SERVER foreign_bd
INTO public;
```

> ⚠️ **Attention** : le mot de passe du `USER MAPPING` est stocké dans la base. Utiliser un **compte distant dédié, en lecture seule**, et jamais un compte administrateur.

> 💡 **Conseil** : l'accès aux données des tables étrangères est **plus lent**, et il est **impossible de créer un index** sur une table étrangère. Elles conviennent à des accès occasionnels. Pour des usages fréquents, **encapsuler les tables distantes dans des vues matérialisées** (section 18) qui stockent les données en local.

```sql
CREATE MATERIALIZED VIEW public.mv_parkings AS
SELECT * FROM foreign_parkings
WITH DATA;

CREATE INDEX idx_mv_parkings_geom ON public.mv_parkings USING GIST (geom);
```

### 19.2 Lire un service WFS (exemple des données de l'INPN)

Jouons avec les données de l'INPN : `http://ws.carmencarto.fr/WFS/119/fxx_inpn`

**Étape 1 : activer les extensions.** `ogr_fdw` est indispensable (il était prévu dans le modèle de base de données). On peut aussi ajouter `postgres_fdw` et `file_fdw`.

```sql
CREATE EXTENSION IF NOT EXISTS ogr_fdw;
```

**Étape 2 : créer le serveur.**

```sql
DROP SERVER IF EXISTS fdw_ogr_inpn_metropole;
```

```sql
CREATE SERVER fdw_ogr_inpn_metropole
FOREIGN DATA WRAPPER ogr_fdw
OPTIONS (
   datasource 'WFS:http://ws.carmencarto.fr/WFS/119/fxx_inpn?',
   format 'WFS'
);
```

**Étape 3 : créer un schéma dédié.**

```sql
CREATE SCHEMA IF NOT EXISTS inpn_metropole;
```

**Étape 4 : récupérer l'ensemble des couches WFS comme des tables** dans le schéma `inpn_metropole`.

```sql
IMPORT FOREIGN SCHEMA ogr_all
FROM SERVER fdw_ogr_inpn_metropole
INTO inpn_metropole
OPTIONS (
   -- mettre le nom des tables en minuscules et sans caractères spéciaux
   launder_table_names 'true',
   -- mettre le nom des champs en minuscules
   launder_column_names 'true'
);
```

**Résultat** : le schéma `inpn_metropole` contient maintenant des **tables étrangères** (*Foreign Tables*), visibles dans pgAdmin.

> 💡 **Conseil d'usage** : pour la vitesse de lecture, créer une **vue matérialisée** (section 18) avec les seules tables qui t'intéressent.

---

## 20. Dépannage : erreurs fréquentes

| Message d'erreur | Cause probable | Solution |
|------------------|----------------|----------|
| `Operation on mixed SRID geometries` | Deux couches ont des SRID différents | Reprojeter l'une avec `ST_Transform` (section 12) |
| `Geometry type (Polygon) does not match column type (MultiPolygon)` | Le type inséré ne correspond pas à la colonne | Appliquer `ST_Multi(geom)` |
| `Geometry has Z dimension but column does not` | Géométrie 3D dans une colonne 2D | Appliquer `ST_Force2D(geom)` |
| `GEOSIntersects: TopologyException` ou erreur similaire | Géométrie invalide | `ST_MakeValid` (section 3.4) |
| `relation "xxx" does not exist` | Mauvais nom, schéma oublié, ou casse des majuscules | Préfixer par le schéma, vérifier avec `\dt schema.*` |
| `permission denied for table xxx` | Droit `SELECT`, `INSERT`... manquant | `GRANT` sur la table (section 16.7) |
| `permission denied for schema xxx` | Droit `USAGE` sur le schéma manquant | `GRANT USAGE ON SCHEMA ...` (section 16.4) |
| `role "xxx" does not exist` pendant une restauration | Les rôles n'existent pas sur le serveur cible | Les créer avant, ou restaurer `--globals-only` |
| `column "geom" specified more than once` | `SELECT ..., *` qui répète une colonne | Lister les colonnes explicitement (section 12) |
| `function round(double precision, integer) does not exist` | `ROUND` appliqué à un nombre non `numeric` | `(expression)::numeric` (section 10.3) |
| `could not open file ... for reading: Permission denied` avec `COPY` | Le serveur ne peut pas lire le fichier | Utiliser `\copy` depuis `psql` (section 11.3) |
| `password authentication failed` | Mauvais mot de passe, ou règle `pg_hba.conf` | Vérifier le compte et la section 16.11 |
| `could not connect to server` | Service arrêté, mauvais port, pare-feu | Vérifier l'hôte, le port (5432 par défaut) et l'état du serveur |
| Requête qui ne se termine pas | Pas d'index spatial, `ST_Distance` dans un `JOIN` | Sections 3.3 et 15 |

---

## 21. Checklists d'équipe

### Avant de modifier des données

- ☐ J'ai sauvegardé la table ou la base.
- ☐ J'ai lancé le `SELECT` équivalent pour voir les lignes concernées.
- ☐ Mon `UPDATE` ou `DELETE` contient un `WHERE`.
- ☐ Je travaille dans une transaction (`BEGIN` ... `ROLLBACK` puis `COMMIT`).

### Avant de livrer une table ou une couche

- ☐ Le SRID est correct (2154 pour la France métropolitaine).
- ☐ Toutes les géométries sont valides (`ST_IsValid`).
- ☐ Une clé primaire et un index spatial existent.
- ☐ Les colonnes et la table sont documentées (`COMMENT ON`).
- ☐ Les droits sont attribués aux groupes concernés.

### Avant d'attribuer un droit

- ☐ Le besoin est précis et justifié (moindre privilège).
- ☐ Le droit est donné à un groupe, pas à une personne isolée.
- ☐ Le droit `USAGE` sur le schéma est prévu.

### Régulièrement

- ☐ Une sauvegarde automatique tourne et son journal est consulté.
- ☐ Une restauration de test a été réalisée récemment.
- ☐ Les comptes des personnes parties ont été désactivés ou supprimés.
- ☐ `ANALYZE` a été lancé après un gros chargement de données.

### Conventions de nommage proposées

| Objet | Convention | Exemple |
|-------|------------|---------|
| Tables, colonnes | minuscules, sans accent, avec `_` | `ecole_elem_matern` |
| Colonne géométrique | `geom` | `geom` |
| Identifiant | `id` ou `id_nomtable` | `id_arbre` |
| Index | `idx_table_colonne` | `idx_arbre_geom` |
| Trigger / fonction | `trg_...` / `fn_...` | `trg_set_date_creation` |
| Vue / vue matérialisée | `v_...` / `mv_...` | `mv_pav_textile` |
| Groupe de droits | `gr_...` | `gr_visu` |

---

## 22. Glossaire et ressources

### Glossaire

| Terme | Définition |
|-------|------------|
| **SGBD** | Système de gestion de bases de données (ici PostgreSQL) |
| **PostGIS** | Extension de PostgreSQL qui ajoute les types et fonctions géographiques |
| **SRID / EPSG** | Code d'un système de coordonnées (2154 = Lambert-93) |
| **GiST** | Type d'index adapté aux données spatiales |
| **CTE** | *Common Table Expression* : étape nommée dans une clause `WITH` |
| **Schéma** | Regroupement de tables au sein d'une base |
| **Rôle** | Utilisateur (avec `LOGIN`) ou groupe (sans `LOGIN`) |
| **GRANT / REVOKE** | Attribuer / retirer un privilège |
| **Dump** | Fichier de sauvegarde produit par `pg_dump` |
| **FDW** | *Foreign Data Wrapper* : accès à des données externes comme à des tables |
| **WFS** | Service web qui diffuse des objets géographiques vectoriels |
| **Vue matérialisée** | Résultat d'une requête stocké sur le disque et rafraîchissable |
| **PAV** | Point d'apport volontaire (collecte des déchets) |
| **ZPS** | Zone de protection spéciale (Natura 2000) |

### Ressources

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation PostGIS](https://postgis.net/documentation/)
- [Documentation GDAL : `ogr2ogr`](https://gdal.org/programs/ogr2ogr.html)
- [Cours IDGEO 2025/2026 : administration de bases de données](https://supports.idgeo.fr/cpgeom/2025-2027/A3-Admin_bdd/co/BDD_PGIS_tables_distantes.html)
- [Cron et crontab (LinuxTricks)](https://www.linuxtricks.fr/wiki/cron-et-crontab-le-planificateur-de-taches)

---

*Dernière mise à jour : 15 octobre 2026. Une remarque ou une erreur à signaler ? Utilisez le bouton « Une remarque ? » en bas à gauche de la page.*
