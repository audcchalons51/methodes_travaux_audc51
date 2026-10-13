# Mise en place d'une base de données géographiques

<img width="245" height="100" alt="logo idgeo cmjn 400x100mm sans ombre" src="https://github.com/user-attachments/assets/1d4e1e65-f6bf-4856-b1cb-85316fe4651d" />

**Année:** 2025-2027

**Auteur:**
- GUENE Abdou Lahat (Alternant géomaticien AUDC 2025 - 2027)

<img width="2894" height="664" alt="logo-CPGEOM" src="https://github.com/user-attachments/assets/0c665be8-0b63-490f-8a1c-06b6ef74d991" />

---
## I \- Présentation du projet

### a) Commande

L’agglomération de Losse-en-Gelaisse, en tant qu’Autorité Organisatrice de la Mobilité dans le cadre de la Loi d'Orientation des Mobilités (LOM[^1]), souhaite se doter d’un dispositif complet permettant de mieux exploiter et piloter ses données d’accessibilité de la voirie (données « outdoor »).

La collectivité souhaite développer un outil web destiné à :

* analyser les problématiques d’accessibilité du territoire ;  
* croiser les données d’accessibilité avec l’offre de transport et la densité de population;  
* identifier et hiérarchiser les zones prioritaires d’intervention ;  
* produire des cartographies thématiques adaptées aux besoins internes (services techniques, SIG, voirie) ;  
* proposer un mode de consultation simplifié pour des présentations à destination des associations de personnes à mobilité réduite.

L’outil devra être responsive (web et mobile), partiellement conforme au RGAA (niveau supérieur à 85 %) et conçu pour être réutilisable par d’autres territoires.

La collectivité souhaite également intégrer dans la solution web un module dédié au suivi des travaux sur la voirie, permettant notamment :

* la visualisation des zones de travaux sur la voirie ;  
* l’intégration d’une dimension temporelle (date de début, date de fin, état d’avancement) ;  
* la visualisation cartographique des impacts sur l’accessibilité ;  
* l’analyse croisée entre accessibilité existante et perturbations temporaires.

La collectivité demande également au prestataire d’être force de proposition pour la rédaction d’une convention encadrant la mise à disposition des données d’accessibilité.

### b) Périmètre de travail

Le projet couvre des aspects techniques, méthodologiques et organisationnels liés à la mise en place et à l’exploitation d’une base de données géographiques dédiée à l’accessibilité.  
Le périmètre comprend notamment :

* l’analyse du MCD du standard CNIG Accessibilité afin d’évaluer son adéquation avec les besoins de l’outil web ;  
* la définition d’un MCD pour les zones de travaux, accompagnée d’une étude comparative des modèles utilisés par d’autres collectivités ;  
* la collecte, la structuration et l’intégration des données d’accessibilité dans une base PostgreSQL conforme au modèle CNIG ;  
* le développement d’un outil web open source dédié à l’exploration, à l’analyse et à la visualisation des données d’accessibilité, intégrant une interface responsive et conforme au RGAA ;  
* la mise en place d’une méthodologie de contrôle qualité des données, incluant des outils de vérification (conformité au modèle, cohérence spatiale, calculs de pente, détection d’anomalies) ;  
* la proposition d’enrichissements de la base de données par l’intégration de données complémentaires (démographie, réseau de transport, équipements publics) ;  
* la conception du cycle de vie des données ainsi que des mécanismes d’administration et de gestion des métadonnées afin de garantir la traçabilité et la pérennité de la base.

### c) Analyse des besoins

L’analyse des besoins vise à identifier les ressources nécessaires à la mise en œuvre du projet, tant en termes de données que d’outils et d’organisation.

#### 		c.1) Besoins en données

La réalisation du projet nécessite l’accès à différents jeux de données permettant d’analyser l’accessibilité du territoire et d’alimenter la base de données géographiques.

Tout d’abord, un accès complet à la base de données PostgreSQL/PostGIS existante de la collectivité est indispensable. Cette base contient les données d’accessibilité déjà collectées et structurées selon le modèle du standard CNIG Accessibilité. L’accès aux modèles conceptuels de données (MCD) utilisés par la collectivité est également nécessaire afin de comprendre la structure actuelle de la base et de garantir la cohérence avec les futurs développements.

Des données complémentaires devront également être mobilisées afin d’enrichir l’analyse et de permettre les croisements de données demandés par la collectivité. Parmi celles-ci figurent notamment :

* des données LiDAR ou des Modèles Numériques de Terrain (MNT) permettant d’analyser les pentes et dévers de la voirie ;  
* des données satellitaires ou issues de télédétection pouvant servir à identifier certains éléments de la voirie, tels que les passages piétons ;  
* des données relatives au réseau de transport (arrêts, lignes, desserte) afin d’analyser l’accessibilité en lien avec l’offre de mobilité ;  
* des données démographiques, utiles pour croiser l’accessibilité avec la densité de population et identifier les zones prioritaires d’intervention ;  
* les données produites par les prestataires chargés de la collecte des données d’accessibilité, qui devront être intégrées et contrôlées dans la base de données.

#### c.2) Besoins organisationnels

Afin de garantir une bonne coordination entre les différents acteurs du projet, il est nécessaire de désigner un référent technique au sein de la collectivité ainsi qu’un référent au sein de l’entreprise prestataire en charge de la collecte des données. Ces interlocuteurs auront pour rôle de faciliter les échanges, de valider les choix techniques et d’assurer le suivi de la production et de la qualité des données.

Cette organisation permettra d’assurer une communication efficace entre les différentes parties prenantes et de sécuriser les différentes étapes du projet.

#### 		c.3) Besoin logiciels

La mise en œuvre du projet nécessite l’utilisation de plusieurs outils spécialisés dans la gestion et le traitement des données géographiques. QGIS sera utilisé pour la visualisation et l’analyse des données. La base de données reposera sur PostgreSQL avec l’extension PostGIS, permettant le stockage et le traitement des données spatiales. Enfin, la modélisation des données sera réalisée avec Looping afin de concevoir les modèles conceptuels de données (MCD) nécessaires à la structuration de la base.

### d) Déroulement des travaux

Le déroulement de la mission s’articule en plusieurs phases successives :

- **Phase 1 : Cadrage du projet**  
* analyse du modèle CNIG Accessibilité ;  
* rédaction d’une convention de mise à disposition des données d’accessibilité.

-  **Phase 2 : Structuration et adaptation du modèle**  
* mise en place d’une base de données de travail sous PostgreSQL/PostGIS ;  
* analyse et éventuelle adaptation du modèle de données pour répondre aux besoins de l’outil web.

-  **Phase 3 : Définition de la méthodologie de contrôle qualité**  
* conception de règles de contrôle portant sur la conformité au modèle, la complétude et la cohérence spatiale des données ;  
* proposition d’outils d’analyse.

- **Phase 4 : Développement de l’outil web**  
* conception du back-office, du module de génération de cartographies et des interfaces de consultation ;  
* intégration des visualisations thématiques (accessibilité, zones de travaux) ;  
* réalisation de tests utilisateurs et ajustements.

-  **Phase 5 : Documentation et accompagnement**  
* rédaction de la documentation technique et fonctionnelle ;  
* formation des agents SIG et Voirie à l’administration de la base de données et à l’utilisation de l’outil web.

### e) Cadre législatif des données d’accessibilité

La mise en place et la gestion des données d’accessibilité s’inscrivent dans un cadre réglementaire national visant à améliorer l’accessibilité des transports et de l’espace public, notamment pour les personnes à mobilité réduite.  
Plusieurs textes législatifs et réglementaires encadrent la collecte, la structuration et la diffusion de ces données afin de garantir leur interopérabilité et leur exploitation à l’échelle nationale.

Les principaux dispositifs juridiques applicables au projet sont présentés ci-dessous.

#### e.1) La Loi d’Orientation des Mobilités (LOM)

La Loi d’Orientation des Mobilités (LOM), ou loi n°2019-1428 du 24 décembre 2019, constitue un texte structurant pour la politique nationale des transports. Elle vise notamment à améliorer l’accessibilité des mobilités et à favoriser le développement de solutions de transport plus durables et inclusives.  
Cette loi repose sur trois grands objectifs :

1. Investir plus et mieux dans les transports du quotidien, en priorisant l'entretien des réseaux et le désenclavement.  
2. Faciliter le déploiement de nouvelles solutions (covoiturage, navettes autonomes, transport à la demande) pour couvrir l'intégralité du territoire.  
3. Accélérer la révolution numérique et la transition écologique, afin de promouvoir une mobilité plus propre et connectée.

Dans ce cadre, la LOM impose également une meilleure structuration et diffusion des données de transport et d’accessibilité, afin de garantir leur interopérabilité et leur réutilisation dans différents services numériques.

Pour assurer cette cohérence à l’échelle nationale, plusieurs standards sont utilisés et encadrés par des groupes de travail spécialisés, notamment le GT7 de l’AFNOR dédié à l’information voyageurs. Parmi les principaux standards utilisés figurent :

* Norme NeTEx (CEN/TS 16614\) : Format d'échange européen de référence pour les données de transport.  
* Profil NeTEx Accessibilité France : Déclinaison nationale harmonisée permettant de décrire de manière harmonisée les informations des points d'arrêt, les véhicules et les services de transport.

#### e.2) Le Cadre Juridique de la Voirie et des Espaces Publics

Le « premier et dernier kilomètre » constitue souvent la partie la plus critique du déplacement pour les personnes à mobilité réduite (PMR). Afin de garantir une continuité de l’accessibilité entre les transports et l’espace public, la réglementation impose également la prise en compte de la voirie dans la collecte des données d’accessibilité.  
L’article L.141-13[^2] du Code de la voirie routière étend ainsi l’obligation de collecte de données à l’environnement proche des points d’arrêt de transport. Selon l’article, les gestionnaires de voirie doivent décrire les itinéraires principaux situés dans un rayon de 200 mètres à vol d’oiseau autour des points d’arrêt prioritaires.  
Cet itinéraire est mesuré à partir de la surface au sol délimitant l’arrêt, ou depuis chaque porte d’accès dans le cas des gares ferroviaires et routières.

#### e.3) Interopérabilité : L’Arrêté du 28 Mai 2024

L’arrêté du 28 mai 2024 vise à harmoniser les formats d’échange des données d’accessibilité et de transport à l’échelle nationale. Il consacre le standard NeTEx comme format de référence pour l’échange de ces données.

Dans ce cadre, les données d’accessibilité collectées sur la voirie selon le standard CNIG Accessibilité doivent pouvoir être converties vers le format NeTEx afin d’être exploitées par différents services numériques, notamment les calculateurs d’itinéraires. Cette conversion repose sur des passerelles permettant d’assurer l’interopérabilité entre les différents standards de données.

### f) Perspectives d’évolution

Plusieurs pistes d’évolution peuvent être envisagées afin d’améliorer et de faire évoluer la solution mise en place :

* interopérabilité avec les plateformes open data et les solutions régionales ;  
* intégration de flux de données en temps réel, tels que les informations relatives aux travaux en cours ou aux incidents impactant l’accessibilité ;  
* mise en place d’une API publique permettant la réutilisation des données et le développement d’applications par des acteurs tiers ;  
* contribution à l’évolution du standard national CNIG Accessibilité, notamment par des retours d’expérience et des propositions d’amélioration du modèle.

## II \- Etude des sources de données et analyse critique

### a) Données GTFS (General Transit Feed Specification)

Le GTFS est une norme ouverte pour diffuser des données sur les systèmes de transport en commun. Cette norme comprend deux formats différents : le GTFS Schedule et le GTFS Realtime. Les données de transport de Losse-en-Gelaisse étant exportées en format GTFS Schedule, le modèle de données “Transport” a été conçu sur la base de ce format.

Le GTFS Schedule est un format commun pour les informations statiques sur les transports publics. Il est composé d’un ensemble de fichiers texte (.txt) contenu dans un seul fichier zippé (.zip). Les sept fichiers de base du format GTFS Schedule sont les suivants : `agency.txt`, `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt`, `calendar.txt` et `calendar_dates.txt.` Des fichiers supplémentaires facultatifs peuvent également être ajoutés pour fournir par exemple des informations sur les tarifs ou les traductions.

La référence officielle GTFS [^3] a permis d’identifier le rôle de chacun de ces fichiers (Fig 1): 

* agency.txt regroupe les informations sur le service de transport (compagnies de transport, nom du réseau) ;  
* calendar.txt et calendar\_dates.txt qui contiennent le calendrier de circulation ;  
* routes.txt présente le nom et la direction des routes (terme anglais pour *lignes*, au sens d'une origine-destination) ;  
* stops.txt liste tous les points d'arrêt et propose d'éventuelles informations ;  
* trips.txt détaille les courses, sous la forme d'une table de liaison entre les services (agency), les routes et les régimes de circulation (calendar.txt et calendar\_dates.txt) ;  
* stops\_times.txt présente les horaires des courses aux points d'arrêt ;  
* transfers.txt présente les correspondances entre plusieurs points d'arrêt ;  
* shapes.txt permet le tracé d'une route sur une carte ;  
* frequencies.txt indique le temps entre deux courses d'une ligne (pour celles qui n'ont pas d'horaires fixes aux points d'arrêts) ;

Dans le cadre de ce projet, il a été convenu de considérer uniquement les fichiers du GTFS dont la présence est “Requise” et qui sont listés dans le tableau ci-dessous, issu de la documentation officielle du format.

<img width="835" height="644" alt="image" src="https://github.com/user-attachments/assets/93f016ea-26ec-49fe-8661-9b72d891ec6f" />

Figure 1 : Definitions des champs ; General Transit Feed Specification 

### b) Standard CNIG “Accessibilité”

La base de données d’accessibilité fournie par la collectivité est structurée selon le standard CNIG Accessibilité et stockée dans une base PostgreSQL/PostGIS. Ce modèle constitue le socle de travail du projet. Le Conseil National de l’Information Géolocalisée (CNIG) propose des standards de structuration des données géographiques destinés à harmoniser les pratiques des collectivités et à faciliter l’échange de données. Le standard CNIG Accessibilité vise ainsi à décrire de manière homogène les éléments de voirie impactant l’accessibilité, tels que les cheminements piétons, les obstacles, les pentes ou les équipements urbains (Fig 2 et fig 3).  
Ce standard s’inscrit également dans le cadre plus large des politiques européennes d’interopérabilité des données géographiques, notamment la directive INSPIRE[^5], qui vise à faciliter le partage et la diffusion des données géographiques au sein de l’Union européenne.

<img width="940" height="611" alt="image" src="https://github.com/user-attachments/assets/8afa3210-0d63-423b-86ed-9defb3d78c0d" />

Figure 2 : MCD accessibilité VOIRIE (partie 1\) ; CNIG

<img width="1013" height="607" alt="image" src="https://github.com/user-attachments/assets/31ef3796-5617-4616-92c1-428cc0917fd6" />

Figure 3 : MCD accessibilité VOIRIE (partie 2\) ; CNIG

Le choix de conserver ce modèle sans modification présente plusieurs avantages :

- **Conformité réglementaire**

L’utilisation du standard CNIG garantit l’alignement avec les recommandations nationales en matière de structuration des données d’accessibilité.

- **Interopérabilité des données**

 L’usage d’un modèle normalisé facilite :

* la réutilisation des données par d’autres collectivités ;  
* l’intégration dans des outils SIG couramment utilisés ;  
* l’échange de données avec différents prestataires.

Dans le contexte du projet, la collectivité souhaite que l’outil développé puisse être réutilisé par d’autres territoires. Le respect du standard CNIG constitue donc un levier essentiel d’interopérabilité.

- **Mutualisation et pérennité**

Le MCD du CNIG repose sur une structure stable et partagée, permettant de limiter les divergences de modélisation et de faciliter la maintenance de la base de données dans le temps.

Ainsi, ce modèle constitue une base fiable et pérenne pour la structuration et l’exploitation des données d’accessibilité dans le cadre du projet.

### c) Analyse critique des modèles comparatives (MCD Travaux) 

Pour construire notre MCD pour les zones de travaux , nous avons effectué une étude comparative des modèles existants : Open data Paris et Toulouse métropole.

#### c.1) Le Modèle de la Ville de Paris

Paris utilise un modèle très granulaire qui sépare strictement l'entité administrative de l'entité géographique qui se présente comme suit : 

* **structure :** Utilisation d'un identifiant unique de "chantier" lié à plusieurs "emprises" géométriques.  
* **points Forts :** Permet une gestion temporelle extrêmement précise (date de début/fin par emprise) et une classification par maître d'ouvrage (Ville, concessionnaires de réseaux, tiers).  
* **critique :** Modèle complexe qui nécessite une interface de saisie robuste pour ne pas décourager les agents de terrain.

#### c.2) Analyse du modèle “Rennes Métropole en accès libre” de  Rennes Métropole

La métropole de Rennes a développé un outil de suivi des chantiers sur son territoire qui  se présente comme suit : 

* **Structure des données :** Le modèle est plus "léger" et se concentre sur l'information utile au citoyen (Qui fait quoi ? Jusqu'à quand ?).  
* **Géométrie :** Principalement linéaire  ce qui simplifie la lecture sur smartphone mais perd en précision sur l'emprise réelle du chantier au sol.  
* **Point fort :** Une interopérabilité maximale. Les données sont conçues pour être "aspirées" par des services tiers (Waze, Google, …).  
* **Point faible :** Moins de précision sur l'impact spécifique aux PMR.

#### c.3) Analyse du modèle “Data Hub Métropole de Bordeaux”

Bordeaux s'appuie sur le logiciel *Litteralis*, qui transforme automatiquement les arrêtés de circulation signés par les élus en données géographiques.

* **Structure des données :** Le modèle est découpé en "Mesures" (ce que l'on impose : rue barrée, alternat, déviation).  
* **Géométrie :** C'est l'un des rares modèles à proposer une **triple géométrie native** (Point, Ligne, Polygone), ce qui valide exactement la structure de votre MCD.  
* **Point fort :** Une fiabilité juridique totale. Si un chantier est sur la carte, c'est qu'un arrêté officiel existe.  
* **Point faible :** Les données sont parfois "froides" et très administratives, moins orientées vers le ressenti de l'usager piéton.

#### c.4) Analyse du modèle "Chantiers (ORION)" \- Toulouse Métropole

Le modèle toulousain se structure autour d'une fiche chantier synthétique avec une forte composante géographique.

* **Structure des données :**  
- **Identification :** **`numero`** (n° de demande), **`declarant`** (structure demandeuse), **`entreprise`** (réalisateur).  
- **Temporalité :** **`datedebut`**, **`datefin`** et surtout un champ **`duree`** (durée maximale de l'autorisation en jours).  
- **Description métier :** Un champ **`libelle`** très riche qui agrège la nature des travaux (ex: "Éclairage", "Voirie", "Aménagement de sécurité").  
* **Points forts**   
- **Richesse du champ `circulation` :** Précise les impacts réels (Alternat, occupation piste cyclable, occupation du trottoir).  
- **Mixité géométrique :** La présence de **`geo_shape`** permet de décrire aussi bien une tranchée linéaire qu'un périmètre de chantier ou un chantier ponctuel.  
- **Fréquence de mise à jour :** Actualisation quotidienne, essentielle pour un outil web performant.  
* **Point faibles** :   
- **Données textuelles :** Les impacts sur le trottoir sont dans un champ texte libre, ce qui rend l'analyse automatisée difficile.  
- **Manque de lien CNIG :** Il n'y a pas de lien direct avec les données d'accessibilité PMR.  
- **Pas de spécialisation :** Pas de distinction stricte entre point, ligne et surface dans la structure de la table.

## III \- Contenu de la base de données

### a) Description des exigences générales

Le cahier des charges identifie clairement plusieurs besoins supplémentaires : 

* représenter les zones de travaux ;  
* intégrer la dimension temporelle (début, fin, état d’avancement) ;  
* croiser accessibilité et transports ;  
* analyser les zones prioritaires en lien avec la densité de population.   

Le MCD du CNIG ne prévoit naturellement aucune structure pour modéliser :   

* les travaux ;  
* les lignes ou arrêts GTFS ;  
* les perturbations temporaires ;  
* les impacts sur la mobilité. 

C’est pourquoi deux schémas complémentaires ont été créés.

### b) Modèles conceptuels de données

#### b.1) Modèle de données général

Le modèle conceptuel de données (MCD) retenu pour ce projet est composé de trois volets (Fig 4\) :

* le MCD du standard CNIG Accessibilité, déjà mis en œuvre par la collectivité ;  
* le MCD Travaux, modélisant les chantiers et leurs impacts ;  
* le MCD Transports, dérivé des données GTFS.

Cette architecture modulaire répond directement aux besoins exprimés par Losse‑en‑Gelaisse dans le cadre du développement d’un outil web dédié à l’analyse de l’accessibilité, de la mobilité et de la population.

<img width="997" height="421" alt="image" src="https://github.com/user-attachments/assets/4c365c4a-d4df-4253-b900-d28aa70f4281" />

Figure 4 : MCD général 

#### b.2) Modèle de données “Transport”

Les données concernant le réseau de transport public sont essentielles en complément des données d’accessibilité car elle permettent de mettre en place les fonctionnalités suivantes :

* mesurer l’accessibilité aux arrêts (rayon de 200 m),  
* analyser la desserte par ligne,  
* évaluer l’impact des travaux sur les arrêts et les itinéraires,  
* produire des cartes thématiques adaptées aux besoins internes.

Le MCD Transport complète donc le CNIG en apportant une véritable dimension mobilité.

Le MCD présenté synthétise l’organisation des services de transport en commun, sur la base du format GTFS Schedule. Il repose sur cinq entités principales liées par des relations de service, de temps et de hiérarchie spatiale. Nous avons choisi d’indiquer les noms des entités et de leurs attributs en anglais pour garder une cohérence avec la nomenclature internationale du GTFS (Fig 5).

<img width="872" height="692" alt="image" src="https://github.com/user-attachments/assets/5f8ee5f7-f1fe-4331-a833-b27adc142305" />

Figure 5 : MCD “Transport”

Ce modèle de données comporte les entités suivantes :

**AGENCY (Agence) :** Elle identifie l'autorité organisatrice ou l'entreprise de transport. Elle contient les données administratives comme le nom, l'URL et le fuseau horaire de référence.

**ROUTE (Ligne) :** Elle correspond à une ligne de transport (ex: "Ligne 1" ou "Métro B"). Elle regroupe les caractéristiques génériques de la ligne, notamment son nom et son mode de transport.

**TRIP (Trajet) :** C'est l'unité centrale de l'offre de transport. Un trajet représente un passage spécifique d'un véhicule sur une ligne, identifié par une direction et une destination.

**CALENDAR (Calendrier) :** Cette entité gère la temporalité de l'offre. Elle définit les jours de circulation (du lundi au dimanche) ainsi que la période de validité globale (dates de début et de fin).

**STOP (Arrêt) :** C'est l'entité géographique. Elle stocke la localisation précise (latitude et longitude) et le nom de chaque point d'arrêt ou station du réseau.

Les associations suivantes dictent comment les entités interagissent entre-elles dans le modèle conceptuel de données :

**Gérer (AGENCY \- ROUTE) :** Une agence peut gérer plusieurs lignes (**1,n**), mais une ligne peut théoriquement être partagée ou dépendre de plusieurs agences (**0,n**).

**Composer (ROUTE \- TRIP) :** Une ligne est composée de plusieurs trajets étalés sur la journée (**1,n**). À l'inverse, un trajet est obligatoirement rattaché à une seule et unique ligne (**1,1**).

**Planifier (CALENDAR \- TRIP) :** Cette relation associe chaque trajet à son calendrier d'exploitation. Un calendrier peut s'appliquer à une multitude de trajets (**1,n**), tandis qu'un trajet suit un planning unique (**1,1**).

**Desservir (TRIP \- STOP) :** Il s'agit d'une **association porteuse de données**. Elle fait le lien entre le mouvement (le trajet) et l'espace (l'arrêt). Cette association correspond au fichier **`stop_times.txt` dans le format GTFS**.

  * *Attributs spécifiques :* Elle un identifiant (**`stop_sequence`**) qui correpspond à la combinaison de l’identifiant de TRIP et de l’identifiant de STOP. Les attributs contiennent également les horaires précis (**`arrival_time`**, **`departure_time`**). Un trajet dessert plusieurs arrêts (**1,n**) et un arrêt est desservi par plusieurs trajets (**1,n**).  
* **Etre\_parent\_de (STOP \- STOP) :** C'est une **relation réflexive** (un arrêt lié à un autre arrêt).  
  * *Utilité :* Elle permet de créer une hiérarchie spatiale. Un arrêt "enfant" (par exemple un quai) peut être rattaché à un arrêt "parent" (une station ou une gare globale). Un arrêt enfant n'a qu'un seul arrêt parent (**0,1**), mais un arrêt parent peut avoir plusieurs arrêts enfants (**0,n**).

#### b.3) Modèle de donnée “Accessibilité”

Le présent modèle a été élaboré sur la base du standard CNIG relatif à l’accessibilité. Il a été complété et enrichi par l’intégration d’une table « Carroyage », spécifiquement ajoutée afin de répondre aux besoins méthodologiques de cette étude (Fig 6).

L’objectif principal est d’analyser le niveau d’accessibilité ainsi que les différentes formes qu’elle revêt sur le territoire de la commune de Losse-en-Gelaisses. Cette démarche vise également à identifier et localiser les secteurs où ces dispositifs d’accessibilité sont présents, avec une attention particulière portée aux quartiers prioritaires.

<img width="1055" height="980" alt="image" src="https://github.com/user-attachments/assets/16939dec-3c05-43f8-afc8-5764b8426935" />

Figure 6 : MCD “Accessibilité”

Ce modèle de données comporte les entités suivantes :

* **CHEMINEMENT (Cheminement) :** Cette entité représente un itinéraire entre deux points ou un parcours piéton structuré au sein du territoire étudié. Elle constitue une unité logique regroupant plusieurs tronçons successifs formant un parcours continu.  
* **TRONCON\_CHEMINEMENT (Tronçon de cheminement)** : Il s’agit de l’unité linéaire élémentaire composant un cheminement. Chaque tronçon est défini par ses caractéristiques géométriques (longueur, géométrie) et physiques (type, pente, dévers, statut de voie, accessibilité globale). Il est délimité par un nœud initial et un nœud final.  
* **NOEUD (Nœud)** : Cette entité correspond à un point géographique structurant du réseau (intersection, extrémité de tronçon, point d’accès). Elle stocke des informations altimétriques et fonctionnelles liées à l’accessibilité (abaissés de trottoir, bandes d’éveil, dispositifs de perception, etc.).  
* **OBSTACLE (Obstacle)** : Cette entité recense les éléments ponctuels susceptibles d’entraver la circulation (mobilier urbain, poteaux, etc.). Elle précise leurs dimensions, leur position et leur niveau de repérabilité visuelle.  
* **CIRCULATION (Zone de circulation)** : Cette entité décrit les espaces dédiés au déplacement sur une surface régulière (trottoirs, voies partagées, etc.). Elle contient des informations sur le revêtement, la largeur utile, l’éclairage, la transition ou encore le type de passage.  
* **TRAVERSEE (Traversée piétonne)** : Elle modélise les dispositifs permettant de franchir une voie (passage piéton). Les attributs décrivent l’état du revêtement, la signalisation, la présence de dispositifs sonores ou lumineux et la visibilité.  
* **RAMPE (Rampe d’accès)** : Cette entité caractérise les plans inclinés facilitant le franchissement d’un dénivelé. Elle intègre des informations sur la largeur, les dispositifs de sécurité (chasse-roue, palier de repos), la main courante et le poids supporté.  
* **ESCALIER (Escalier fixe)** : Elle décrit les escaliers classiques. Les attributs précisent le nombre de marches, la hauteur et le giron, la présence de mains courantes, les contrastes visuels et les dispositifs de vigilance.  
* **ESCALATOR (Escalier mécanique)** : Cette entité correspond aux escaliers mécaniques. Elle renseigne le sens de fonctionnement, la largeur utile, les dispositifs de détection et de supervision.  
* **TAPIS\_ROULANT (Tapis roulant)** : Elle modélise les dispositifs mécaniques horizontaux facilitant le déplacement. Les caractéristiques portent sur le sens, la largeur et les dispositifs de sécurité.  
* **QUAI (Quai)** : Cette entité représente un équipement d'un mode de transport permettant un accès au véhicule. Elle précise la hauteur, la largeur de passage, la signalisation et les espaces de manœuvre.  
* **ENTREE (Entrée d’établissement ou de bâtiment)** : Elle décrit les points d’accès aux bâtiments. Les attributs détaillent les équipements d’accessibilité (rampe, ascenseur, poignée, largeur de porte, signalétique, contrôle d’accès, etc.).  
* **PASSAGE\_SELECTIF (Passage sélectif)** : Cette entité représente le dispositif permettant le passage des piétons, mais dissuadant celui des cycles et des engins motorisés . Elle précise les dimensions, la profondeur et le repérage visuel.  
* **ELEVATEUR (Élévateur PMR)** : Elle modélise le système de franchissement d'une dénivellation muni d'une plate-forme ou d'une nacelle. Les attributs décrivent les dimensions, la charge maximale, les dispositifs de sécurité et l’autonomie d’utilisation.  
* **ASCENSEUR (Ascenseur)** : Cette entité décrit les ascenseurs classiques. Elle comprend les dimensions de cabine, les équipements (miroir, boutons en relief, annonces sonores, éclairage) et les dispositifs d’assistance.  
* **STATIONNEMENT\_PMR (Stationnement réservé PMR)** : Elle recense les places de stationnement adaptées aux personnes à mobilité réduite. Les attributs précisent les dimensions, la pente, la signalisation et le marquage au sol.  
* **CARROYAGE (Carroyage)** : Cette entité, issue des données de l’INSEE, représente une grille de 200 mètres de côté couvrant l’ensemble du territoire français. Chaque carreau renseigne le nombre d’individus qu’il contient, ainsi qu’une répartition par tranche d’âge. Ce carroyage permet d’analyser l’accessibilité du territoire et d’identifier les zones prioritaires.

Chaque cheminement est composé de un ou plusieurs tronçons (1,n), ce qui signifie qu’un cheminement n’existe que s’il comporte au moins un tronçon, et qu’un tronçon appartient à un et un seul cheminement (1,1). De même, chaque tronçon possède un nœud initial et un nœud final (1,1), tandis qu’un même nœud peut être partagé par plusieurs tronçons (0,n), ce qui permet de modéliser un réseau. 

Les cardinalités décrivent aussi la relation entre les tronçons et les éléments d’accessibilité. Un tronçon peut comporter zéro, un ou plusieurs obstacles, circulations ou équipements (rampe, escalier, escalator, tapis roulant, quai, etc.) (0,n), tandis qu’un obstacle ou un équipement est toujours rattaché à un seul tronçon (1,1) . Cela signifie qu’on peut représenter un tronçon sans obstacle, mais qu’un obstacle isolé sans tronçon n’a pas de sens dans le modèle. 

Les entités liées aux entrées, ascenseurs, élévateurs ou stationnements PMR sont connectées à des nœuds avec des cardinalités du type (0,n) côté nœud et (1,1) côté équipement : un nœud peut donner accès à plusieurs dispositifs, mais chaque dispositif est localisé sur un nœud unique. Ces cardinalités garantissent la cohérence spatiale du modèle en imposant qu’un équipement d’accessibilité soit toujours positionné sur un point du réseau.

Enfin, l’entité CARROYAGE permet d’associer au réseau des informations de population, utiles pour les futures analyses de densité et l’identification des quartiers prioritaires. Un carreau de carroyage est relié à l’entité NOEUD par une cardinalité (0,n), ce qui signifie qu’un carreau peut contenir zéro, un ou plusieurs nœuds. Réciproquement, chaque nœud est associé à un unique carreau par une cardinalité (1,1), indiquant qu’un nœud ne peut appartenir qu’à un seul carreau. 

#### b.4) Modèle de donnée “travaux”

Le modèle conceptuel de données (MCD) dédié aux zones de travaux a pour objectif de décrire les chantiers impactant la voirie et susceptibles d’affecter l’accessibilité des cheminements piétons. Il permet de structurer les informations relatives aux travaux afin de faciliter leur intégration dans la base de données et leur exploitation dans l’outil web.  
Dans ce modèle, les chantiers sont représentés sous forme de géométries surfaciques (polygones) permettant de localiser précisément les zones concernées. Le MCD intègre également une dimension temporelle, à travers des attributs décrivant les dates de début et de fin des travaux, les différentes phases du chantier ainsi que leur état d’avancement.  
Chaque chantier à un organisme responsable, ce qui permet d’identifier l’acteur en charge des travaux et de faciliter le suivi administratif. Le modèle prévoit également la description des impacts potentiels sur l’accessibilité, notamment pour les personnes à mobilité réduite.

<img width="860" height="509" alt="image" src="https://github.com/user-attachments/assets/c0b0c65d-b722-4969-948d-00d85bd76631" />

Figure 7 : MCD “Travaux”

Pour rendre les données exploitable , nous les avons organisées en quatre blocs (Fig 7\) : 

* le bloc administratif ( table **projet\_travaux**): elle renseigne sur l’identité du chantier , le prestataire et sur la personne à contacter en cas d’urgence, le contact ici peut être un numéro de téléphone ou un mail.

* le bloc temporel ( table **zone** ): c’est la table centrale du modèle qui permet le suivi. Pour chaque chantier , nous enregistrons la date de début et de fin , ce qui permettra aux élus d’avoir une carte de  l'état de l'agglomération à n'importe quelle date. Le champ statut sera constitué d’une liste déroulante ( prévu, en cours, terminé) qui permettra d’avoir un idée sur l'état d’avancement de chaque chantier.

* le bloc géographique ( tables **travaux**): nous dessinerons les travaux dans des tables géométriques en fonction de leurs natures. Ces dessins seront le plus précis possible pour ne pas bloquer inutilement des itinéraires de bus ou des trottoirs.

* le bloc accessibilité ( table **impact**): le modèle propose une table dédiée aux personnes à mobilité réduites , nous ne nous contenterons pas de dire seulement s’il y a des travaux ,  nous renseignerons également les impacts de ses travaux sur le déplacement des PMR et s’il y a des recommandations de déviation qui ont été mis en place.

Ce MCD pourra être facilement relié aux données GTFS via des requêtes spatiales qui seront utiles dans notre web-sig. On pourra par exemple informer les utilisateurs grâce à des alertes : *"Votre arrêt de bus est déplacé de 50m car une zone de travaux bloque le passage piéton".* 

### c) Contrôle et qualité des données

Les principaux objectifs liés à la qualité des informations géographiques nécessaires à l’accessibilité de la chaîne de déplacement reposent sur plusieurs dimensions essentielles. Il s’agit tout d’abord de garantir la précision géométrique des données, afin d’assurer une représentation fidèle des éléments du réseau. La qualité topologique constitue également un enjeu majeur, dans la mesure où elle permet d’assurer la cohérence des relations spatiales entre les objets et de rendre possible le calcul d’itinéraires fiables et pertinents.

Par ailleurs, une attention particulière doit être portée à la qualité descriptive des informations, qui permet de caractériser avec précision l’accessibilité de la chaîne de déplacement. Enfin, les données doivent respecter le modèle de données et le catalogue d’objets définis le standard CNIG , garantissant ainsi leur cohérence et leur interopérabilité.

Nous proposons divers contrôles qui ont pour but de vérifier la fiabilité des données intégrées par les prestataires lors des phases de collecte. Ces vérifications reposent sur deux principaux critères : d’une part, les critères d’analyse de la qualité définis par la norme ISO 19157 d’autre part, des contrôles spécifiques liés au calcul d’itinéraires, permettant de garantir la cohérence et l’exploitabilité des données dans les outils de calcul d’itinéraire.

#### 		c.1) Critères d’analyse de la qualité (norme ISO 19157\)

##### Contrôles de conformité au Modèle (MCD)

Ce contrôle relève de la qualité interne. Il s'agit de mesurer l'écart entre la donnée livrée par le prestataire et le standard **CNIG Accessibilité** .

* **Cohérence de format :** Vérifier que les tables possèdent les bons noms de colonnes, types (Integer, Varchar….) et encodages (UTF-8).

- outil : une inspection minutieuse du schéma postgreSQL ou une Commande ogrinfo nous permettront de déceler d'éventuelles anomalies.

* **Cohérence au domaine de valeur :** Les champs dont nous avons établies des listes prédéfinies doivent être respectés car une  analyse thématique peut être basée sur ces champs dans notre outil. Si ces champs sont remplis par des données hors liste, notre analyse thématique sera fausse.

- outil : Mettre en place des requêtes SQL pour identifier les valeurs hors liste (valeurs aberrantes).

- indicateur : **taux de non-conformité au domaine de valeur**.

- exemple métier : si un prestataire saisit "trotoir" au lieu de "trottoir", l'outil web ne pourra pas filtrer correctement les données.

* **Précision Sémantique :** Contrôle de l'invariance des identifiants . Il est important de veiller à ce que les identifiants des objets communs à plusieurs tables (tels que les tronçons de cheminement , les nœuds,etc...) restent constants pour l' ensemble des données afin d' assurer la bonne calculabilité des itinéraires de cheminement.

##### Contrôle d’exhaustivité

Le contrôle d’exhaustivité nous permettra de détecter s’il y a des omissions ou des excédents dans les données intégrées par les prestataires. Ce contrôle nous permettra de valider les données si elles sont dans le seuil de la LAQ ou de les rejeter si elles en sont hors. Un exemple de contrôle d’exhaustivité .

Ce contrôle mesure l'adéquation entre la couche “passages\_piétons” livrée par le prestataire (le **Lot à contrôler**) et la couche extraite par télédétection (le **Référentiel de contrôle**).

On distingue deux types d'erreurs : 

* **L'omission :** un passage piéton détecté sur l'image mais absent de la base du prestataire. (Risque : itinéraire impossible pour l'usager).   
* **L'Excédent :** un passage piéton saisi par le prestataire mais non détecté sur l’image (peut être une erreur de saisie ou un marquage effacé).

- outil : pour comparer ces deux sources, on utilise une méthode de croisement géographique (sous QGIS ou PostGIS). On crée une zone de tolérance (Buffer), on applique un tampon de 2 à 3 mètres autour des géométries du référentiel (télédétection) pour absorber les légers écarts de saisie. Ensuite on effectue une jointure spatiale pour avoir des données conformes, omises ou excédentaires.

- indicateur : on calcul alors le taux d’exhaustivité en appliquant la formule suivante[^10]: T \= 1 \- Nb Omissions \+ Nb Excédents /Nb Passages détectés par télédétection.

- analyse et seuil d'acceptation (LAQ) : Nous exigeons pour le calcul des itinéraires des PMR un seuil d’acceptation à 98% , un taux d’exhaustivité supérieur à 2 % rend la donnée non conforme. Le prestataire devra donc corriger sa saisie. 

##### Qualité temporelle

Ce critère assure que la donnée est "fraîche" et cohérente chronologiquement, surtout pour la gestion des zones de travaux.

* **Exactitude de la mesure temporelle :** Vérifier que les dates de relevés terrain sont cohérentes (ne peuvent pas être postérieures à la date de livraison).

* **Cohérence temporelle :** Pour les arrêtés de travaux qui bloquent l'accessibilité :

- contrôle de la règle : Date\_Debut \< Date\_Fin.

- vérifier que les dates sont au format ISO (AAAA-MM-JJ) pour être traitées par l'outil web.

* **Validité temporelle :** S'assurer que les données historiques (anciens aménagements avant travaux) sont bien archivées ou marquées comme obsolètes pour ne pas fausser le calcul d'itinéraire actuel.

#### c.2) Les contrôles spécifiques au calcul d'itinéraire

##### contrôles de cohérence topologique

Les contrôles de cohérence topologique représentent une étape essentielle pour garantir le bon fonctionnement du modèle de calcul d’itinéraires. En effet, une donnée peut sembler correcte d’un point de vue visuel tout en étant techniquement exploitable si les segments du réseau ne sont pas correctement connectés.

* **Connectivité :** Vérifier que tous les segments de voirie (trottoirs, passages piétons) sont parfaitement accrochés. Une erreur de quelques centimètres empêche l'algorithme de trouver un chemin.  
  \- outil : nombre de nœuds isolés ou de connexions manquantes.  
* **Absence de chevauchements et d'auto-intersections :** Deux surfaces (ex: deux zones de trottoirs) ne doivent pas se superposer.  
  \- outil : **vérificateur de topologie QGIS** (Règles :  "ne doit pas se chevaucher").  
* **Indice de compacité et d'épaisseur:**

On utilisera le coefficient d'épaisseur E \= 2 (Surface) / (Périmètre) pour détecter les "résidus" de numérisation ou les polygones trop étroits (\< 0.5m) qui ne correspondent pas à une réalité physique de cheminement PMR.

##### Précision de position (Altitudes et Pentes)

Dans le cadre de l'accessibilité, la précision Z (altitude) est plus critique que la précision XY. Une erreur de 5% de pente change radicalement l'accessibilité d'un tronçon surtout pour les fauteuils roulants.

* Contrôle Altimétrique via LiDAR / MNT :

Nous allons comparer les données collectées avec les  données issus du  LiDAR ou MNT. On échantillonne des tronçons. Pour chaque tronçon, on compare la pente saisie par le prestataire avec la pente calculée mathématiquement à partir du MNT (Modèle Numérique de Terrain). En suivant le standard du CNIG, nous imposons un un écart admissible de 3% , au-delà de ce seuil, la donnée est considérée comme fausse.

* Précision de position absolue :

On mesurera  l'écart (en mètres) entre des objets fixes saisis (ex: potelets, bordures) et le PCRS (Plan Corps de Rue Simplifié) si l'agglomération en dispose.

#### 		c.3) Outils de validation externe

Afin de garantir la qualité, la cohérence et l’interopérabilité des données produites, plusieurs outils de validation externe sont mobilisés. Ces outils permettent de vérifier la conformité des données de transport et de s’assurer qu’elles respectent les standards d’échange notamment le GTFS largement utilisé pour la diffusion et l’exploitation des données de mobilité.

* **Données de transport (GTFS)** : Les données relatives aux transports sont validées à l’aide d’outils de contrôle dédiés au format GTFS. Ces validateurs permettent de vérifier la conformité de la structure des fichiers, la cohérence des identifiants ainsi que l’intégrité des informations relatives aux arrêts, aux lignes et aux horaires. L’objectif est de garantir la qualité des données et leur compatibilité avec les plateformes de diffusion de données de transport.

* **Interopérabilité GTFS** : Une attention particulière est portée à la cohérence des identifiants et à la structure des données afin de faciliter leur intégration dans les différents outils de calcul d’itinéraires et applications de mobilité. L’utilisation du standard GTFS permet ainsi d’assurer 

## IV \- Structure-des-données

### a) Choix d’implémentation

Pour répondre aux exigences de la commande, le choix s’est porté sur le couple **PostgreSQL**, pour la gestion de la base de données relationnelle, et son extension spatiale **PostGIS**. Ce choix est stratégique pour plusieurs raisons :

* **Interopérabilité :** Les données d'accessibilité déjà collectées par la collectivité sont actuellement stockées sous PostgreSQL selon un modèle conforme au standard CNIG Accessibilité. L'utilisation de ce même SGBD garantit une transition fluide.

* **Capacités de traitement spatial :** Le projet nécessite des analyses complexes, telles que l'identification de zones d'intervention prioritaires. L'extension PostGIS offre les fonctions géométriques et topologiques nécessaires pour ces calculs.

* **Open Source :** L'agglomération exige que l'outil web et les outils de contrôle soient entièrement **open source** afin d'être mutualisables avec d'autres territoires. PostgreSQL étant le leader des SGBD libres, il est parfaitement adapté pour répondre aux besoin de ce projet.

### b) Livraison informatique

Le cœur de la livraison repose sur la fourniture d’un script SQL à l’agglomération de Losse-en-Gelaisse pour garantir le déploiement opérationnel de la solution. 

Ce script assure :

* **la création des schémas :** l'isolation des données en trois domaines distincts : **`accessibilite`**, **`transport`** et **`travaux`** ;

* **la structuration des tables :** La création de l'ensemble des tables nécessaires (ex: **`transport.STOP`**, **`accessibilite.Troncon_Cheminement`**, **`travaux.zone`**) avec un typage de données strict ;

* **l'implémentation des contraintes :** La mise en place des clés primaires, des clés étrangères pour la cohérence relationnelle et des contraintes d'unicité (ex: lien unique entre un nœud et une entrée d'ERP).

Le script SQL complet est consultable en annexe (annexe n°2).

### c) Implémentation physique

#### c.1) Organisation en schémas

Pour assurer une gestion structurée et sécurisée des accès multi-utilisateurs, la base de données est organisée en **trois schémas distincts**, correspondant aux domaines thématiques du projet :

* **accessibilité :** contient l'intégralité du socle conforme au standard CNIG (tronçons, nœuds, obstacles, cheminements) ;

* **transport :** contient les données de l'offre de transport au format GTFS (arrêts, lignes, calendriers) ;

* **travaux :** gère le suivi temporel et géographique des chantiers impactant la voirie.

#### c.2) Contraintes structurelles

* **clés primaires (PRIMARY KEY) :** Chaque table dispose d'un identifiant unique (ex: **`idTroncon`**, **`stop_id, Id_zone`**) garantissant l'unicité de chaque objet.

* **clés étrangères (FOREIGN KEY) :** Elles assurent la **cohérence relationnelle** entre les tables. Par exemple, un **`Noeud`** d'accessibilité ne peut exister que s'il est rattaché à un **`Troncon_Cheminement`** valide via une clé étrangère. De même, la table de liaison **`donner_acces_a`** assure le pont technique entre le monde du transport (**`stop_id`**) et celui de l'accessibilité (**`idNoeud`**).

* **contraintes d'unicité (UNIQUE) :** Pour les relations de type 1:1, comme entre un nœud et une entrée d'ERP, une contrainte **`UNIQUE`** est appliquée sur la clé étrangère pour empêcher qu'une même entrée ne soit rattachée à plusieurs nœuds.

* **contraintes de non-nullité (NOT NULL) :** Les champs critiques, notamment les géométries (**`geom`**) et les identifiants de liaison, sont paramétrés en **`NOT NULL`** pour éviter les données inexploitables d’un point de vue spatial.

#### c.3) Contraintes de domaine et qualité des données

Pour garantir que les données saisies sont conformes aux attentes métiers (standard CNIG), des **contraintes de domaine** sont définies :

* **typage de données strict :** Utilisation de types adaptés comme **`DOUBLE PRECISION`** ou **`REAL`** pour les mesures physiques (pentes, largeurs), **`BOOLEAN`** pour les équipements (présence d'ascenseur) et **`DATE`** pour la gestion temporelle des travaux.

* **standardisation des listes de valeurs :** L'utilisation de types énumérés (ex: **`geostandard.enum5`**) pour des champs comme l'état du revêtement ou la présence de dispositifs de vigilance permet de forcer la saisie de valeurs prédéfinies, empêchant ainsi les erreurs de saisie manuelle.

* **intégrité spatiale :** Les géométries sont contraintes par des types spécifiques (ex: **`POLYGON`** pour les zones de travaux) et associées au système de référence spatial **SRID 2154** (Lambert 93).

### d) Représentation graphique

A partir des modèles conceptuels de données et des différentes contraintes déjà présentés, un schéma relationnel de base de donnée a été réalisé, montrant l'organisation physique des tables et assurant que la base soit opérationnelle et exploitable. Les tables, colonnes, clés primaires et relations qui composent la base sont exposées ci-dessous (Fig 8, 9 et 10).

<img width="671" height="556" alt="image" src="https://github.com/user-attachments/assets/9b8a2587-131d-4a92-95fd-7b5cedb391a5" />

Figure 8 : Modèle relationnel du schéma “Travaux”

<img width="924" height="586" alt="image" src="https://github.com/user-attachments/assets/7200d306-45d1-4421-b08d-785d8072f880" />

Figure 9 : Modèle relationnel du schéma “Transport”

<img width="1146" height="881" alt="image" src="https://github.com/user-attachments/assets/614deb50-04a6-47ab-86f6-16727e2cd953" />

Figure 10 : Modèle relationnel du schéma “Accessibilité”

### e) Métadonnées

Les métadonnées jouent un rôle fondamental dans la gestion de l’information au sein du projet Losse‑en‑Gelaisse. Elles garantissent la traçabilité, l’interopérabilité, la pérennité et la bonne compréhension des jeux de données utilisés dans l’outil web d’accessibilité.  
Conformément au cahier des charges, leur production doit respecter :

* les standards CNIG Accessibilité ;  
* les normes **ISO 19115** (contenu des métadonnées) ;  
* et **ISO 19139** (schéma XML d’encodage).

#### e.1) Choix d’un outil ou plugin pour la gestion des métadonnées

Afin d’assurer une gestion homogène et conforme des métadonnées, il est nécessaire d’utiliser un outil permettant leur création, leur modification, leur exportation et leur documentation selon des standards reconnus. Dans l’environnement QGIS, deux plugins se distinguent particulièrement et méritent une comparaison : PLUME et Geocat Bridge.

* **PLUME (plugin QGIS pour postgreSQL)**

PLUME est une extension développée par le ministère de la Transition écologique. Elle permet de saisir et de consulter les métadonnées directement au sein d’une base PostgreSQL/PostGIS, ce qui facilite la documentation des jeux de données stockés dans la base. Les métadonnées sont enregistrées sous forme de JSON-LD, basé sur le profil européen GeoDCAT-AP, ce qui favorise l’interopérabilité avec les catalogues de données ouverts.

L’outil présente plusieurs avantages. Il est particulièrement adapté aux bases de données PostgreSQL/PostGIS et s’intègre directement dans l’environnement QGIS, ce qui simplifie la manipulation des métadonnées. Son utilisation du vocabulaire DCAT / GeoDCAT-AP facilite également la publication dans des portails open data.

Cependant, PLUME présente certaines limites dans le cadre de ce projet. Il ne repose pas nativement sur les standards ISO 19115 / ISO 19139, qui sont les normes généralement utilisées pour la production de métadonnées institutionnelles. De plus, l’encodage en RDF / JSON-LD diffère des formats attendus dans les référentiels CNIG ou dans les échanges institutionnels. L’outil est donc davantage adapté à une documentation interne des données qu’à la production de métadonnées normées destinées à être diffusées.

* **Geocat Bridge (plugin orienté normes ISO)**

Geocat Bridge est un plugin QGIS spécifiquement conçu pour faciliter la création de métadonnées conformes aux standards ISO 19115 et ISO 19139\. Il permet notamment de générer des métadonnées structurées et de produire directement un fichier XML au format ISO 19139, largement utilisé dans les catalogues de données géographiques.

L’un des principaux avantages de Geocat Bridge est sa conformité avec les normes ISO attendues dans de nombreux projets institutionnels. L’export en XML ISO 19139 constitue également un atout majeur pour répondre aux exigences du CNIG et faciliter le partage des métadonnées entre différents organismes. Le plugin s’intègre par ailleurs relativement simple dans la chaîne de travail basée sur QGIS.

En revanche, Geocat Bridge est moins orienté vers la documentation directe des bases PostgreSQL et vers les logiques de catalogage basées sur DCAT. Il se concentre principalement sur la production de métadonnées normalisées destinées à être diffusées ou échangées.

#### 		e.2) Outil utilisé pour les métadonnées

Malgré les qualités de PLUME, notamment pour la gestion interne des métadonnées dans PostgreSQL, son encodage ne répond pas totalement aux besoins du projet qui exige la production de métadonnées **ISO 19115/19139**.

Au regard des attentes du cahier des charges et de la nécessité d’assurer une interopérabilité institutionnelle (CNIG, collectivités, OpenData), le choix le plus adapté est donc l’utilisation de **Geocat Bridge** comme plugin principal dans QGIS pour la production de métadonnées conformes aux standards ISO.

La gestion des métadonnées reposera ainsi sur plusieurs composants complémentaires :

* **QGIS**, avec **Geocat Bridge** comme plugin principal pour la création et l’édition des métadonnées ;

* **PostgreSQL / PostGIS**, permettant de stocker certains attributs clés (dates de mise à jour, provenance des données, identifiants uniques) ;

* **un catalogue interne**, organisé sous forme d’un dossier structuré regroupant les fichiers XML exportés (ISO 19139), les notices explicatives ainsi que l’historique des versions.

Dans ce dispositif, **PLUME** pourra être utilisé comme outil complémentaire pour la gestion interne des informations dans PostgreSQL, sans constituer la solution principale. Cette organisation garantit que les métadonnées accompagnent les données tout au long de leur cycle de vie, conformément aux exigences définies dans le cahier des charges.

#### 		e.3) Contenu des métadonnées

Chaque jeu de données (CNIG Accessibilité, Travaux, GTFS, Population etc.) doit comporter a minima :

* identifiant,  
* langue,  
* titre,  
* liens,  
* contact,  
* licence.

Ces éléments contribuent à assurer une compréhension immédiate des données, à faciliter leur réutilisation par des tiers, à garantir leur conformité avec le standard CNIG « Accessibilité » et à anticiper leur diffusion future via une API ou une plateforme OpenData.

## V \- Administration et cycle de vie des données

La gestion des données d’accessibilité de Losse‑en‑Gelaisse repose sur deux piliers indissociables :

* un cycle de vie des données garantissant leur qualité, leur actualité et leur cohérence ;  
* une administration rigoureuse de la base PostgreSQL/PostGIS assurant sécurité, maintenance et gouvernance.

Ces deux dimensions forment un système continu et structuré permettant d’alimenter durablement l’outil web d’accessibilité.

### a) Administration de la base de données

L’administration garantit que la base PostgreSQL/PostGIS est stable, sécurisée, performante et exploitable par les utilisateurs internes et les outils.

#### a.1)  Rôles et responsabilités

| Responsabilités | Rôles |
| ----- | ----- |
| Administrateur BDD (SIG) | Création schémas, gestion droits, maintenance, sauvegardes. |
| Référent Accessibilité | Mise à jour CNIG, contrôle qualité PMR. |
| Référent transport (GTFS) | Import régulier GTFS, validation arrêts/lignes. |
| Référent travaux | Intégration des chantiers et gestion de la temporalité. |
| Référent population | Mise à jour population INSEE / Quartiers (carreaux). |
| Consultation | Accès en lecture via QGIS ou l’outil web. |

#### a.2) Gestion des accès et privilèges

Utilisateurs nécessitant un accès à la base de données: Service SIG, Service Voirie, Développeurs de l’outil web, Prestataires. Les types de droits prévus sont les suivants :

* **lecture seule** : outil web, agents non-éditeurs ;  
* **écriture** : référents par thématique (CNIG, Travaux, GTFS, Population) ;  
* **administration** : service SIG

Chaque schéma de la base est associé à des droits spécifiques :

* *accessibilité* \> édition par Référent Accessibilité  
* *travaux* \> édition par Référent Travaux  
* *transport* \> édition par Référent Transport

#### a.3)  Intégration, mise à jour, sécurité

L’intégration et la mise à jour des données sont réalisées de manière contrôlée, notamment via des scripts SQL ou à l’aide de QGIS. L’accès au système est sécurisé grâce à des mécanismes d’authentification, à l’utilisation de mots de passe et, le cas échéant, à des restrictions d’accès par adresse IP ou via VPN. Une surveillance régulière des logs PostgreSQL est également mise en place afin de détecter d’éventuelles anomalies ou tentatives d’accès non autorisées. Par ailleurs, les logiciels PostgreSQL et PostGIS, utilisés avec QGIS, font l’objet de mises à jour régulières afin de garantir la sécurité et la stabilité de l’infrastructure.

### b)  Sauvegardes et versionnement

#### b.1) Sauvegardes quotidiennes

La mise en place d’une stratégie de sauvegarde est indispensable pour garantir la pérennité, la sécurité et la récupération des données en cas d’incident. Dans le cadre du projet Losse‑en‑Gelaisse, trois niveaux de sauvegardes sont recommandés : quotidiennes, hebdomadaires et mensuelles.

Les sauvegardes quotidiennes, lorsque cela est nécessaire, doivent reposer sur l’outil natif de PostgreSQL, *pg\_dump*, qui permet d’extraire la structure et le contenu d’une base de données sous forme de script SQL ou d’archive. Ce fichier contient les commandes nécessaires à la reconstruction de la base dans l’état exact du moment du dump. 

*pg\_dump* produit une **sauvegarde logique**, incluant les tables, les index, les données et les contraintes. Pour exécuter un dump, l’utilisateur doit disposer d’un accès en lecture sur toutes les tables concernées ainsi que du droit *USAGE* sur les schémas correspondants. Ces permissions sont suffisantes, sauf pour certains objets particuliers (exemple: subscriptions), réservés au superutilisateur. 

Avant de restaurer un dump SQL, les rôles et utilisateurs référencés dans ce fichier doivent déjà exister sur l’instance de destination. C’est un prérequis normal des restaurations basées sur un script SQL.

Ci-dessous des exemples de commandes usuelles :

* **Sauvegarde complète d’une base**
```sql
pg_dump dbname > sauvegarde.sql
```
* **Sauvegarde ciblée** (un schéma ou quelques tables)
```sql
pg_dump -n schema_name -t table_name dbname > sauvegarde_partielle.sql
```
La commande *pg\_dump* présente néanmoins les limites suivantes :

* *pg\_dump* ne sauvegarde qu’une seule base de données à la fois ;  
* la commande n’inclut pas les objets globaux du cluster PostgreSQL : rôles, utilisateurs, tablespaces.

C’est pourquoi l’outil pg\_dumpall doit être utilisé pour les sauvegardes complètes mensuelles ou globales du cluster.

#### b.2) Sauvegardes hebdomadaires : sauvegardes disque

Les sauvegardes hebdomadaires doivent porter sur les **fichiers physiques** du serveur PostgreSQL. Elles consistent à copier :

* le répertoire de données PostgreSQL (PGDATA) ;  
* les fichiers de configuration (*postgresql.conf*, *pg\_hba.conf*, *pg\_ident.conf*) ;  
* les répertoires contenant les journaux de transactions (WAL logs, si l’archivage ou la réplication est activé).

Ce type de sauvegarde est important car au niveau du disque il permet de restaurer **tout le serveur PostgreSQL**, et pas seulement une base spécifique. Cela garantit une protection en cas :

* de corruption du système de fichiers,  
* de défaillance matérielle,  
* d’erreur critique ou suppression accidentelle de données internes,  
* ou lorsqu’il faut restaurer l’ensemble du cluster PostgreSQL avec ses paramètres et identifiants.

Elle complète les sauvegardes **logiques** (pg\_dump), qui ne sauvent ni les configurations, ni les rôles, ni les paramètres serveur, ni l’état interne du cluster. Deux approches sont possibles:

* **Sauvegarde à froid** (service arrêté)

- On arrête le service PostgreSQL pour garantir la cohérence des fichiers.

- On copie l’intégralité du répertoire PGDATA via un outil adapté (rsync, robocopy, sauvegarde réseau, snapshot, etc.).  
   \>  Méthode simple et sûre, mais nécessite une interruption de service.

* **Sauvegarde à chaud** (cluster en fonctionnement)

- On active l’archivage WAL (*archive\_mode \= on*, *archive\_command \= ...*).

- On réalise une copie cohérente du répertoire PGDATA ainsi que des WAL archivés, ce qui permet une restauration correcte par *Point-In-Time Recovery (PITR)*.  
  \>  Pas d’interruption de service, mais nécessite une configuration correcte de l’archivage WAL.

La sauvegarde doit être déposée sur un serveur dédié à la sauvegarde ou dans un espace NAS / SAN sécurisé.

#### b.3) Sauvegardes mensuelles : archivage longue durée

Pour garantir une conservation complète et durable du cluster PostgreSQL, il est nécessaire d’utiliser *pg\_dumpall*. Cet outil génère un fichier SQL contenant l’ensemble des bases de données du cluster, ainsi que tous les objets globaux : rôles et utilisateurs, privilèges, tablespaces, et paramètres définis au niveau du cluster.
```sql
pg_dumpall > archive.sql
```
***pg\_dumpall*** permet de sauvegarder des éléments non pris en compte par la commande *pg\_dump* :

- les rôles et utilisateurs,  
- les permissions globales,  
- les tablespaces,  
- les paramètres globaux du cluster.

Les archives mensuelles doivent être :

- compressées (.zip, .gz, .7z, etc.) pour réduire la taille et vérifier l’intégrité,  
- stockées hors du serveur PostgreSQL (NAS, cloud interne, serveur de sauvegarde),  
- conservées sur plusieurs mois, voire plusieurs années selon la politique de rétention établie.

#### b.4) Versionnement

Les différents schémas seront versionnés par année, par exemple *cnig\_2026* ou *gtfs\_2026*, ce qui permet de distinguer les structures de données selon leur millésime et de conserver l’historique des modèles utilisés. En complément, des tables d’archivage suffixées *\_archive* sont mises en place pour conserver les états antérieurs des données. Enfin, chaque jeu de données est accompagné de métadonnées conformes au standard **ISO 19139**, permettant de documenter précisément l’origine, la structure et les conditions d’utilisation des données.

Grâce à cette organisation, la base est :

1. opérationnelle : accessible 24/7,  
2. exploitable : connectée à QGIS et à l’outil web,  
3. sécurisée : droits contrôlés, sauvegardes en place,  
4. pérenne : traçabilité assurée,  
5. conforme : standards CNIG / ISO respectés.

Grâce à la combinaison de *pg\_dump* (sauvegarde logique), des sauvegardes disque (sauvegardes physiques) et de *pg\_dumpall* (archivage complet du cluster), la base de données PostgreSQL de Losse‑en‑Gelaisse bénéficie d’une protection complète contre les pertes de données, les erreurs humaines, les corruptions et les défaillances matérielles, tout en restant rapidement restaurable.

### c) Cycle de vie des données

Le cycle de vie décrit l’ensemble des actions permettant de maintenir une base fiable, conforme aux standards CNIG et exploitable dans l’outil web. Il repose sur un processus itératif comprenant plusieurs phases, depuis la planification de la collecte jusqu’à l’archivage des données.

#### c.1) Planification

La phase de planification consiste à identifier les jeux de données nécessaires au projet et à organiser leur mise à jour. Cela concerne notamment les données issues du standard CNIG, les données de transport au format GTFS, les informations relatives aux travaux de voirie, ainsi que les données démographiques de l’INSEE ou les données altimétriques issues du LiDAR ou de modèles numériques de terrain.

Cette étape permet également de définir la fréquence d’actualisation des données (par exemple une mise à jour mensuelle pour les données GTFS ou annuelle pour certaines données CNIG), de préparer les scripts d’importation et de répartir les responsabilités entre les différents modules du système (accessibilité, transport, travaux et population).

#### c.2) Acquisition

La phase d’acquisition consiste à collecter les différentes sources de données nécessaires au projet. Les données externes, telles que les jeux de données GTFS, les données de l’INSEE ou les modèles LiDAR/MNT, sont téléchargées puis intégrées dans l’environnement de travail.

La base CNIG fournie par la collectivité est également importée, tandis que les données relatives aux travaux sont récupérées auprès du service Voirie. L’ensemble de ces informations est ensuite centralisé dans la base PostgreSQL/PostGIS.

#### c.3) Vérification

Une fois les données intégrées, plusieurs contrôles sont réalisés afin de vérifier leur qualité. Ces vérifications portent notamment sur la validité des géométries (à l’aide d’outil topologique), le respect du système de projection utilisé par la base (RGF93 / Lambert-93 – EPSG:2154), ainsi que sur la détection d’éventuels doublons, valeurs manquantes ou incohérences attributaires.

Des contrôles de cohérence sont également réalisés entre les différentes sources de données, par exemple entre les arrêts de transport issus des données GTFS et les cheminements piétons décrits dans les données CNIG.

#### c.4) Validation

Après la phase de vérification, les anomalies identifiées sont corrigées. Cela peut concerner la correction de géométries invalides, la normalisation des attributs ou encore l’application de contrôles topologiques. Ces contrôles permettent notamment de vérifier la continuité des cheminements accessibles aux personnes à mobilité réduite, par exemple en s’assurant qu’une rampe est correctement connectée au cheminement menant à un arrêt de transport.

Une validation finale est ensuite réalisée par les référents techniques responsables des différentes thématiques (accessibilité, transport et travaux).

#### c.5) Intégration et réutilisation

Une fois validées, les données sont intégrées dans la base de données finale et peuvent être utilisées pour réaliser différentes analyses spatiales. Celles-ci incluent notamment la création de zones tampons de 200 mètres autour des arrêts de transport, l’analyse des intersections entre zones de travaux et itinéraires accessibles, le croisement entre accessibilité et densité de population, ainsi que le calcul des pentes pouvant impacter l’accessibilité des cheminements.

Ces traitements permettent notamment de produire les cartographies thématiques destinées à l’outil web.

#### c.6) Archivage

Les données sont ensuite archivées afin de conserver un historique des versions utilisées. La fréquence d’archivage peut varier selon le type de données (mensuelle ou annuelle). Les informations relatives aux anciens travaux sont également conservées afin de permettre une analyse dans le temps.

Chaque version des données est documentée, en précisant la date, la source et les traitements réalisés.

#### c.7) Retour à la planification

Le cycle de vie des données fonctionne selon un processus continu. Chaque nouvelle mise à jour relance les différentes étapes du cycle, garantissant ainsi l’actualisation régulière et la qualité des données utilisées par la collectivité.

## Annexes 

### Annexe n°1 : Convention de mise à disposition des données

| Convention type de mise à disposition des données d’accessibilité entre l’Agglomération de Losse-en-Gelaisse et le prestataire |
| :---: |

**ENTRE**

L’Agglomération de **Losse-en-Gelaisse**, Autorité Organisatrice de la Mobilité au sens de la Loi d’Orientation des Mobilités, dont le siège est situé 19 rue Vallée Silicone, représentée par Bertrand GERVAIS, en qualité d’expert technique, dûment habilité à cet effet,

**ET**

La société *CALA geom*, dont le siège social est situé 1 All. Maurice Magre, sous le numéro SIRET 999 134 356 00016, représentée par Cloé BARATEAU, en qualité de Présidente Directrice Générale, dûment habilité à cet effet,

Ci-après dénommée **« le Prestataire »**,

**Ci-après désignées collectivement « les Parties »**,

Il a été convenu et arrêté ce qui suit :

**Préambule**

Afin d’améliorer l’information des usagers, de disposer d’une connaissance précise, homogène et actualisée de l’accessibilité de la voirie et des cheminements extérieurs sur son territoire, et de pouvoir cibler plus efficacement les politiques publiques conduites en matière de mobilité inclusive, l’Agglomération de Losse-en-Gelaisse, en sa qualité d’Autorité Organisatrice de la Mobilité au sens de la Loi d’Orientation des Mobilités, a engagé une démarche de collecte et de structuration des données d’accessibilité.

Ces données, conformes au modèle défini par le Conseil National de l’Information Géolocalisée (CNIG), cartographient l’accessibilité de la voirie et des espaces publics situés notamment aux abords des arrêts prioritaires de transport. Elles sont structurées au sein d’une base de données géographiques et ont vocation à être mises à jour régulièrement par les services de la collectivité ou par des prestataires mandatés.

Dans une logique d’amélioration continue, de transparence et d’ouverture des données publiques, la collectivité souhaite mettre à disposition ces données auprès du prestataire retenu afin :

* de concevoir un outil web open source d’analyse territoriale de l’accessibilité ;

* de produire des cartographies thématiques destinées aux services internes et aux associations représentant les personnes en situation de handicap ;

* de mettre en place une méthodologie et des outils de contrôle de la qualité des données collectées.

**Article 1er \- Objet de la convention**

La présente convention a pour objet de définir les conditions de mise à disposition par l’Agglomération de Losse-en-Gelaisse au Prestataire des données géographiques d’accessibilité relatives à l’accessibilité de la voirie et des cheminements extérieurs situés sur le territoire de l’Agglomération, notamment les cheminements piétons, la voirie, les abords d’arrêts de transport prioritaires ainsi que les aménagements et obstacles impactant la mobilité des personnes à mobilité réduite.

**Article 2 \- Fonctionnement de la mise à disposition des données**

Conformément aux dispositions de l’article L141-13 du Code de la voirie routière, et à la Loi n°2019-1428 du 24 décembre 2019 (LOM), l’Agglomération de Losse-en-Gelaisse collecte des données relatives à l’accessibilité des itinéraires piétons situés dans un rayon d’environ 200 mètres autour des points d’arrêt prioritaires du territoire. Ces données sont structurées selon le modèle CNIG et comprennent notamment les entités suivantes : cheminements et tronçons de cheminement, nœuds, obstacles, zones de circulation, traversées piétonnes, rampes, escaliers, escaliers mécaniques, tapis roulants, quais, entrées, passages sélectifs, élévateurs, ascenseurs, stationnements PMR et quartiers.  
Les données sont collectées par des prestataires mandatés et font l’objet d’un premier contrôle portant sur leur intégrité et leur cohérence. Elles seront ensuite mises à disposition du Prestataire.

Les traitements effectués par le Prestataire ont pour objet de compléter ces contrôles, d’identifier d’éventuelles anomalies et de produire des résultats exclusivement destinés à l’exploitation des données et à l’amélioration des services d’accessibilité. Toute utilisation des données à d’autres fins est interdite sans l’accord écrit de la collectivité.

La collectivité définit les conditions d’utilisation et de diffusion des résultats afin de garantir la fiabilité, la sécurité et la confidentialité des informations mises à disposition des services internes, des partenaires et du public.

**Article 3 \- Données mises à disposition du Prestataire**

**3-1- Terminologie**

« Données collectées » : données relatives aux cheminements, voirie, aménagements et équipements extérieurs du territoire, collectées par les services techniques de la collectivité ou par les prestataires mandatés. Il peut s’agir de données brutes ou prétraitées.  
« Données traitées » : données collectées vérifiées et enrichies par le Prestataire, incluant les contrôles de cohérence, de complétude et de conformité au modèle CNIG.  
« Résultats » : analyses, indicateurs et cartographies thématiques produits à partir des données traitées pour l’exploitation dans l’outil web ou pour la planification et le suivi des politiques d’accessibilité.

**3-2- Nature et contenu des données**

Les données mises à disposition comprennent notamment :

* **CHEMINEMENT** et **TRONCON\_CHEMINEMENT** : itinéraires piétons et tronçons élémentaires avec caractéristiques géométriques et physiques (longueur, type, pente, dévers, accessibilité) ;

* **NOEUD** : points géographiques structurants (intersections, extrémités de tronçons) avec informations altimétriques et fonctionnelles (abaissés de trottoir, bandes d’éveil, dispositifs de perception) ;

* **OBSTACLE**, **CIRCULATION**, **TRAVERSEE**, **RAMPE**, **ESCALIER**, **ESCALATOR**, **TAPIS\_ROULANT**, **QUAI**, **ENTREE**, **PASSAGE\_SELECTIF**, **ELEVATEUR**, **ASCENSEUR**, **STATIONNEMENT\_PMR**, **QUARTIER** : détails et attributs techniques correspondant aux caractéristiques d’accessibilité des espaces publics et des équipements extérieurs.

Les données sont fournies dans des formats compatibles SIG et accompagnées de métadonnées détaillant leur origine, leur précision, et leur fréquence de mise à jour.

**3-3- Champ couvert**

Les données mises à disposition concernent :

* les espaces publics extérieurs, les itinéraires piétons et les aménagements situés dans un rayon d’environ 200 mètres autour des points d’arrêt prioritaires au sens de l’article L141-13 du Code de la voirie routière ;  
* les éléments impactant la mobilité des personnes à mobilité réduite, tels que obstacles, traversées piétonnes, rampes, escaliers et dispositifs mécaniques ou d’accessibilité ;  
* l’ensemble des zones et équipements extérieurs pertinents pour le calcul d’itinéraires et la production de cartographies thématiques.

Ne sont pas concernés :

* les cheminements et équipements à l’intérieur des ERP (bâtiments publics, médiathèques, gares).


**Article 4 \- Engagements du Prestataire sur l’utilisation des données**

Le Prestataire s’engage à :

* exploiter les données d’accessibilité mises à disposition par l’Agglomération uniquement dans le cadre défini par la présente convention, notamment pour le développement de l’outil web, la production de cartographies thématiques et la mise en œuvre de contrôles de qualité ;  
* traiter les données collectées, vérifiées et enrichies conformément au modèle CNIG, en garantissant leur intégrité, leur cohérence et leur confidentialité ;  
* respecter la sécurité, la confidentialité et la protection des informations conformément à la réglementation applicable, et ne pas utiliser les données à d’autres fins que celles prévues dans la convention ;  
* signaler à l’Agglomération toute anomalie ou incohérence détectée dans les données et proposer des mesures correctives le cas échéant.

Le Prestataire ne peut transmettre les données ou les résultats obtenus à des tiers sans l’accord écrit préalable de l’Agglomération.

**Article 5 \-  Protection des données, confidentialité et sécurité**

Les données mises à disposition dans le cadre de la présente convention sont utilisées exclusivement aux fins définies à l’article 1er.

Lorsque les données comportent des informations susceptibles d’identifier indirectement des personnes physiques (notamment par croisement avec d’autres jeux de données), leur traitement est réalisé conformément à la réglementation en vigueur relative à la protection des données à caractère personnel, notamment la loi n°78-17 du 6 janvier 1978 modifiée relative à l’informatique, aux fichiers et aux libertés et au Règlement (UE) 2016/679 du Parlement européen et du Conseil du 27 avril 2016 (RGPD).

Le Prestataire s’engage à :

* mettre en œuvre toutes les mesures techniques et organisationnelles nécessaires pour garantir la sécurité, l’intégrité et la confidentialité des données ;  
* limiter l’accès aux données aux seules personnes dûment habilitées dans le cadre de l’exécution du marché ;  
* ne procéder à aucune diffusion, cession ou communication des données à des tiers sans l’accord écrit préalable de l’Agglomération ;  
* ne pas utiliser les données à des fins commerciales ou étrangères à l’objet de la présente convention.

**Article 6 \-  Engagements de l’Agglomération**

L’Agglomération de Losse-en-Gelaisse s’engage à :

* mettre à disposition du Prestataire, sans contrepartie financière distincte de celle prévue au marché public, les données décrites à l’article 3 pendant la durée de la présente convention ;  
* transmettre des données conformes au modèle défini par le Conseil National de l’Information Géolocalisée (CNIG), accompagnées des métadonnées nécessaires à leur exploitation ;  
* permettre l’accès aux données dans des formats compatibles avec les systèmes d’information géographique (SIG) et les outils nécessaires au développement de la solution web ;  
* informer le Prestataire de toute modification substantielle affectant la structure, le périmètre ou les modalités de mise à jour des données ;  
* autoriser le Prestataire à utiliser les données dans le strict cadre défini par la présente convention et le marché public associé.

La mise à disposition des données n’emporte aucun transfert de propriété au profit du Prestataire, lequel ne dispose que d’un droit d’usage limité aux finalités prévues par la convention.

**Article 7 \-  Durée de la convention et conditions de résiliation**

La présente convention est conclue pour une durée correspondant à celle du marché public relatif au développement, à l’hébergement et à la maintenance de l’outil web d’analyse de l’accessibilité, soit une durée prévisionnelle de trente-six mois comprenant :

* douze  mois de conception et de développement ;  
* vingt-quatre mois de maintenance et d’exploitation.

Elle prend effet à compter de la date de notification du marché.

Elle pourra être résiliée de manière anticipée dans les conditions prévues par le marché public ou en cas de manquement grave aux obligations de la présente convention, notamment en matière de confidentialité ou d’usage des données.

À l’issue de la convention ou en cas de résiliation, le Prestataire s’engage à cesser toute utilisation des données et à en restituer ou détruire les copies, sous réserve des obligations légales de conservation.

**Fait à Losse-en-Gelaisse en deux exemplaires originaux, le 12/03/2026**

**Pour l’Agglomération de Losse-en-Gelaisse**

Nom, Prénom  
Fonction du signataire   
Cachet

**Pour le Prestataire**

Nom, Prénom  
Fonction du signataire   
Cachet

### Annexe n°2 : Script SQL de création de la base de donnée

**CREATE** **SCHEMA** **IF** **NOT** **EXISTS** travaux;  
**CREATE** **SCHEMA** **IF** **NOT** **EXISTS** transport;  
**CREATE** **SCHEMA** **IF** **NOT** **EXISTS** accessibilite;

*=======================*  
*GTFS TABLES (transport)*  
*=======================*  
```sql
CREATE TABLE transport.agency (
   agency_id VARCHAR(50) NOT NULL,
   agency_name VARCHAR(50),
   agency_url VARCHAR(50),
   agency_timezone VARCHAR(50),
   agency_lang VARCHAR(50),
   PRIMARY KEY (agency_id)
);
```
```sql
CREATE TABLE transport.route (
   route_id VARCHAR(50) NOT NULL,
   route_short_name VARCHAR(50),
   route_long_name VARCHAR(50),
   route_type INTEGER,
   PRIMARY KEY (route_id)
);
```
```sql
CREATE TABLE transport.stop (
   stop_id VARCHAR(50) NOT NULL,
   stop_name VARCHAR(50),
   stop_lat DOUBLE PRECISION,
   stop_lon DOUBLE PRECISION,
   stop_id_parent VARCHAR(50),
   PRIMARY KEY (stop_id),
   FOREIGN KEY (stop_id_parent) REFERENCES transport.stop(stop_id)
);
```
```sql
CREATE TABLE transport.calendar (
   service_id VARCHAR(50) NOT NULL,
   monday VARCHAR(50),
   tuesday VARCHAR(50),
   wednesday VARCHAR(50),
   thursday VARCHAR(50),
   friday VARCHAR(50),
   saturday VARCHAR(50),
   sunday VARCHAR(50),
   start_date DATE,
   end_date DATE,
   PRIMARY KEY (service_id)
);
```
```sql
CREATE TABLE transport.trip (
   trip_id VARCHAR(50) NOT NULL,
   headsign VARCHAR(50),
   direction_id INTEGER,
   service_id VARCHAR(50) NOT NULL,
   route_id VARCHAR(50) NOT NULL,
   PRIMARY KEY (trip_id),
   FOREIGN KEY (service_id) REFERENCES transport.calendar(service_id),
   FOREIGN KEY (route_id) REFERENCES transport.route(route_id)
);
```
```sql
CREATE TABLE transport.gerer (
   agency_id VARCHAR(50) NOT NULL,
   route_id VARCHAR(50) NOT NULL,
   PRIMARY KEY (agency_id, route_id),
   FOREIGN KEY (agency_id) REFERENCES transport.agency(agency_id),
   FOREIGN KEY (route_id) REFERENCES transport.route(route_id)
);
```
```sql
CREATE TABLE transport.desservir (
   stop_id VARCHAR(50) NOT NULL,
   trip_id VARCHAR(50) NOT NULL,
   stop_sequence VARCHAR(50),
   arrival_time VARCHAR(50),
   departure_time VARCHAR(50),
   PRIMARY KEY (stop_id, trip_id),
   FOREIGN KEY (stop_id) REFERENCES transport.stop(stop_id),
   FOREIGN KEY (trip_id) REFERENCES transport.trip(trip_id)
);
```
*====================================*  
*ACCESSIBILITY TABLES (accessibilite)*  
*====================================*
```sql
CREATE TABLE accessibilite.cheminement (
   idCheminement VARCHAR(255) NOT NULL,
   nom VARCHAR(254),
   PRIMARY KEY (idCheminement)
);
```
```sql
CREATE TABLE accessibilite.obstacle (
   idObstacle VARCHAR(255) NOT NULL,
   typeObstacle VARCHAR(2),
   largeurUtile DOUBLE PRECISION,
   positionObstacle VARCHAR(2),
   longueurObstacle DOUBLE PRECISION,
   rappelObstacle VARCHAR(2),
   reperabiliteVisuelle BOOLEAN,
   largeurObstacle DOUBLE PRECISION,
   hauteurObsPoseSol DOUBLE PRECISION,
   hauteurSousObs DOUBLE PRECISION,
   geom GEOMETRY,
   PRIMARY KEY (idObstacle)
);
```
```sql
CREATE TABLE accessibilite.circulation (
   idCirculation VARCHAR(255) NOT NULL,
   typeSol VARCHAR(2),
   largeurPassageUtile DOUBLE PRECISION,
   etatRevetement VARCHAR(2),
   eclairage VARCHAR(2),
   transition VARCHAR(2),
   typePassage VARCHAR(2),
   repereLineaire VARCHAR(2),
   couvert VARCHAR(50),
   PRIMARY KEY (idCirculation)
);
```
```sql
CREATE TABLE accessibilite.ascenceur (
   idAscenseur VARCHAR(255) NOT NULL,
   largeurUtile DOUBLE PRECISION,
   diamManoeuvreFauteuil DOUBLE PRECISION,
   largeurCabine DOUBLE PRECISION,
   longueurCabine DOUBLE PRECISION,
   boutonsEnRelief VARCHAR(2),
   annonceSonore BOOLEAN,
   signalEtage VARCHAR(2),
   boucleInducMagnet BOOLEAN,
   miroir BOOLEAN,
   eclairage INTEGER,
   voyantAlerte VARCHAR(2),
   typeOuverture VARCHAR(2),
   mainCourante VARCHAR(2),
   hauteurMainCourante DOUBLE PRECISION,
   etatRevetement VARCHAR(2),
   supervision BOOLEAN,
   autrePorteSortie VARCHAR(2),
   PRIMARY KEY (idAscenseur)
);
```
```sql
CREATE TABLE accessibilite.elevateur (
   idElevateur VARCHAR(255) NOT NULL,
   largeurUtile DOUBLE PRECISION,
   boutonsEnRelief VARCHAR(2),
   typeOuverture VARCHAR(2),
   largeurPlateforme DOUBLE PRECISION,
   longueurPlateforme VARCHAR(50),
   utilisableAutonomie BOOLEAN,
   etatRevetement VARCHAR(2),
   supervision BOOLEAN,
   autrePorteSortie VARCHAR(2),
   chargeMaximum INTEGER,
   accompagnateur VARCHAR(2),
   PRIMARY KEY (idElevateur)
);
```
```sql
CREATE TABLE accessibilite.passage_selectif (
   idPassageSelectif VARCHAR(255) NOT NULL,
   passageMecanique BOOLEAN,
   largeurUtile REAL,
   profondeur REAL,
   contrasteVisuel BOOLEAN,
   PRIMARY KEY (idPassageSelectif)
);
```
```sql
CREATE TABLE accessibilite.entree (
   idEntree VARCHAR(255) NOT NULL,
   adresse TEXT,
   type VARCHAR(2),
   rampe VARCHAR(2),
   rampeSonnette BOOLEAN DEFAULT false,
   ascenseur BOOLEAN DEFAULT false,
   escalierNbMarche INTEGER DEFAULT 0,
   escalierMainCourante BOOLEAN DEFAULT false,
   reperabilite BOOLEAN,
   reperageEltsVitres BOOLEAN,
   signaletique BOOLEAN,
   largeurPassage REAL,
   controleAcces VARCHAR(2),
   entreeAccueilVisible BOOLEAN,
   eclairage INTEGER,
   typePorte VARCHAR(2),
   typeOuverture VARCHAR(2),
   espaceManoeuvre VARCHAR(2),
   largManoeuvreExt REAL,
   longManoeuvreExt REAL,
   largManoeuvreInt REAL,
   longManoeuvreInt REAL,
   typePoignee VARCHAR(2),
   effortOuverture INTEGER,
   PRIMARY KEY (idEntree)
);
```
```sql
CREATE TABLE accessibilite.stationnement_pmr (
   idStationnement VARCHAR(255) NOT NULL,
   typeStationnement VARCHAR(2),
   etatRevetement VARCHAR(2),
   largeurStat REAL,
   longueurStat REAL,
   bandLatSecurite BOOLEAN,
   surLongueur REAL,
   signalPMR BOOLEAN,
   marquageSol BOOLEAN,
   pente INTEGER,
   devers INTEGER,
   typeSol VARCHAR(2),
   PRIMARY KEY (idStationnement)
);
```
```sql
CREATE TABLE accessibilite.escalier (
   idEscalier VARCHAR(255) NOT NULL,
   etatRevetement geostandard.enum5,
   mainCourante geostandard.enum5,
   dispositifVigilance geostandard.enum5,
   contrasteVisuel geostandard.enum5,
   largeurUtile REAL,
   mainCouranteContinue geostandard.enum5,
   prolongMainCourante geostandard.enum5,
   nbMarches INTEGER,
   nbVoleeMarches INTEGER,
   hauteurMarche REAL,
   giron REAL,
   PRIMARY KEY (idEscalier)
);
```
```sql
CREATE TABLE accessibilite.quai (
   idQuai VARCHAR(255) NOT NULL,
   etatRevetement VARCHAR(2),
   hauteur REAL,
   largeurPassage REAL,
   signalisationPorte VARCHAR(2),
   dispositifVigilance VARCHAR(2),
   diamZoneManoeuvre REAL,
   PRIMARY KEY (idQuai)
);
```
```sql
CREATE TABLE accessibilite.rampe (
   idRampe VARCHAR(255) NOT NULL,
   etatRevetement VARCHAR(2),
   largeurUtile REAL,
   mainCourante VARCHAR(2),
   distPalierRepos REAL,
   chasseRoue VARCHAR(2),
   aireRotation VARCHAR(2),
   poidsSupporte INTEGER,
   PRIMARY KEY (idRampe)
);
```
```sql
CREATE TABLE accessibilite.tapis_roulant (
   idTapis VARCHAR(255) NOT NULL,
   sens VARCHAR(2),
   dispositifVigilance VARCHAR(2),
   largeurUtile REAL,
   detecteur BOOLEAN,
   PRIMARY KEY (idTapis)
);
```
```sql
CREATE TABLE accessibilite.escalator (
   idEscalator VARCHAR(255) NOT NULL,
   sens geostandard.enum4,
   dispositifVigilance geostandard.enum5,
   largeurUtile REAL,
   detecteur BOOLEAN,
   surpervision BOOLEAN,
   PRIMARY KEY (idEscalator)
);
```
```sql
CREATE TABLE accessibilite.traversee (
   idTraversee VARCHAR(255) NOT NULL,
   etatRevetement VARCHAR(2),
   marquageSol VARCHAR(2),
   eclairage VARCHAR(2),
   feuPietons BOOLEAN,
   aideSonore VARCHAR(2),
   repereLineaire VARCHAR(2),
   presenceIlot BOOLEAN,
   chausseeBombee BOOLEAN,
   covisibilite VARCHAR(2),
   PRIMARY KEY (idTraversee)
);
```
```sql
CREATE TABLE accessibilite.carroyage (
   idCarreau VARCHAR(50) NOT NULL,
   ind NUMERIC(15,2),
   ind_0_3 NUMERIC(15,2),
   ind_4_5 NUMERIC(15,2),
   ind_6_10 NUMERIC(15,2),
   ind_11_17 NUMERIC(15,2),
   ind_18_24 NUMERIC(15,2),
   ind_25_39 NUMERIC(15,2),
   ind_40_54 NUMERIC(15,2),
   ind_55_64 NUMERIC(15,2),
   ind_65_79 NUMERIC(15,2),
   ind_80 NUMERIC(15,2),
   PRIMARY KEY (idCarreau)
);
```
*==================================*  
*TRONCONS ET NOEUDS (accessibilite)*  
*==================================*
```sql
CREATE TABLE accessibilite.troncon_cheminement (
   idTroncon VARCHAR(50) NOT NULL,
   "from" VARCHAR(255),
   "to" VARCHAR(255),
   longueur INTEGER,
   typeTroncon VARCHAR(2),
   statutVoie VARCHAR(2),
   pente INTEGER,
   devers INTEGER,
   accessibiliteGlobale VARCHAR(2),
   geom GEOMETRY NOT NULL,
   idTraversee VARCHAR(255),
   idEscalator VARCHAR(255),
   idTapis VARCHAR(255),
   idRampe VARCHAR(255),
   idQuai VARCHAR(255),
   idEscalier VARCHAR(255),
   idCirculation VARCHAR(255),
   idObstacle VARCHAR(255),
   PRIMARY KEY (idTroncon),
   FOREIGN KEY (idTraversee) REFERENCES accessibilite.traversee(idTraversee),
   FOREIGN KEY (idEscalator) REFERENCES accessibilite.escalator(idEscalator),
   FOREIGN KEY (idTapis) REFERENCES accessibilite.tapis_roulant(idTapis),
   FOREIGN KEY (idRampe) REFERENCES accessibilite.rampe(idRampe),
   FOREIGN KEY (idQuai) REFERENCES accessibilite.quai(idQuai),
   FOREIGN KEY (idEscalier) REFERENCES accessibilite.escalier(idEscalier),
   FOREIGN KEY (idCirculation) REFERENCES accessibilite.circulation(idCirculation),
   FOREIGN KEY (idObstacle) REFERENCES accessibilite.obstacle(idObstacle)
);
```
```sql
CREATE TABLE accessibilite.noeud (
   idNoeud VARCHAR(50) NOT NULL,
   altitude DOUBLE PRECISION,
   bandeEveilVigilance VARCHAR(2),
   hauteurRessaut DOUBLE PRECISION,
   abaissePente INTEGER,
   abaisseTrottoir DOUBLE PRECISION,
   controleBEV VARCHAR(50),
   bandeInterception BOOLEAN,
   geom GEOMETRY NOT NULL,
   idEntree VARCHAR(255) NOT NULL,
   idPassageSelectif VARCHAR(255) NOT NULL,
   idElevateur VARCHAR(255) NOT NULL,
   idAscenseur VARCHAR(255) NOT NULL,
   idCarreau VARCHAR(50) NOT NULL,
   idTroncon VARCHAR(50) NOT NULL,
   PRIMARY KEY (idNoeud),
   UNIQUE (idEntree),
   UNIQUE (idPassageSelectif),
   UNIQUE (idElevateur),
   UNIQUE (idAscenseur),
   FOREIGN KEY (idEntree) REFERENCES accessibilite.entree(idEntree),
   FOREIGN KEY (idPassageSelectif) REFERENCES accessibilite.passage_selectif(idPassageSelectif),
   FOREIGN KEY (idElevateur) REFERENCES accessibilite.elevateur(idElevateur),
   FOREIGN KEY (idAscenseur) REFERENCES accessibilite.ascenceur(idAscenseur),
   FOREIGN KEY (idCarreau) REFERENCES accessibilite.carroyage(idCarreau),
   FOREIGN KEY (idTroncon) REFERENCES accessibilite.troncon_cheminement(idTroncon)
);
```
*=========================*  
*RELATIONS (accessibilite)*  
*=========================*
```sql
CREATE TABLE accessibilite.est_compose_de (
   idTroncon VARCHAR(50) NOT NULL,
   idCheminement VARCHAR(255) NOT NULL,
   PRIMARY KEY (idTroncon, idCheminement),
   FOREIGN KEY (idTroncon) REFERENCES accessibilite.troncon_cheminement(idTroncon),
   FOREIGN KEY (idCheminement) REFERENCES accessibilite.cheminement(idCheminement)
);
```
```sql
CREATE TABLE accessibilite.donne_acces_a (
   idNoeud VARCHAR(50) NOT NULL,
   idStationnement VARCHAR(255) NOT NULL,
   PRIMARY KEY (idNoeud, idStationnement),
   FOREIGN KEY (idNoeud) REFERENCES accessibilite.noeud(idNoeud),
   FOREIGN KEY (idStationnement) REFERENCES accessibilite.stationnement_pmr(idStationnement)
);
```
*========================*  
*TRAVAUX TABLES (travaux)*  
*========================*
```sql
CREATE TABLE travaux.zone (
   id_zone SERIAL,
   nom_zone VARCHAR(255),
   debut DATE,
   fin DATE,
   statut VARCHAR(255),
   libelle VARCHAR(255),
   geom GEOMETRY(POLYGON, 2154),
   PRIMARY KEY (id_zone)
);
```
```sql
CREATE TABLE travaux.impact_accessibilite (
   id_impact_accessibilite SERIAL,
   description VARCHAR(255),
   coupure_totale BOOLEAN,
   recommandation VARCHAR(255),
   id_zone INTEGER NOT NULL,
   PRIMARY KEY (id_impact_accessibilite),
   FOREIGN KEY (id_zone) REFERENCES travaux.zone(id_zone)
);
```
```sql
CREATE TABLE travaux.projet_travaux (
   id_projet_travaux SERIAL,
   nom_chantier VARCHAR(255),
   maitrise_ouvrage VARCHAR(255),
   contact_responsable REAL,
   num_arrete VARCHAR(255),
   id_zone INTEGER NOT NULL,
   PRIMARY KEY (id_projet_travaux),
   FOREIGN KEY (id_zone) REFERENCES travaux.zone(id_zone)
);
```
```sql
CREATE TABLE transport.donner_acces_a (
   stop_id VARCHAR(50) NOT NULL,
   idNoeud VARCHAR(50) NOT NULL,
   PRIMARY KEY (stop_id, idNoeud),
   FOREIGN KEY (stop_id) REFERENCES transport.stop(stop_id),
   FOREIGN KEY (idNoeud) REFERENCES accessibilite.noeud(idNoeud)
);
```
