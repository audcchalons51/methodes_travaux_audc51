# Mise en place de Lizmap

[![Télécharger en PDF](https://img.shields.io/badge/📄_T%C3%A9l%C3%A9charger-PDF-0ea5e9?style=for-the-badge)](Lizmap_mise_en_place_AUDC.pdf)

**Toutes les étapes, de l'installation à la publication d'un projet QGIS**

- **Document de présentation** à destination de la direction et de la DSI.

- Les versions précises (QGIS, Lizmap, PHP) sont à faire valider par le prestataire au moment de l'installation, car elles évoluent régulièrement. Les durées indiquées sont des ordres de grandeur, à confirmer par un devis détaillé.

[Documentation officielle de Lizmap](https://docs.lizmap.com/current/en/introduction.html ) 

[Filezilla](https://docs.3liz.org/tutorial/filezilla-fr/) 

[Pour aller plus loin avec 3liz](https://www.3liz.com/) 

[Tableau de bord des projet carographiques d'AUDC](https://abdou123-guene.github.io/tableau-de-bord-etudes-carto-audc/) 

---

## Prestataires possibles:

- **3Liz** , éditeur de la solution Lizmap, propose le service d'installation et d'hébergement. Les détails figurent dans le lien ci-dessus.
- **IDGEO** (mon école) propose aussi l'installation, qui semble plus pertinente et moins coûteuse. Je pourrais établir les premiers contacts en m'appuyant sur mon statut d'alternant.

[Site officiel d'IDGEO de Toulouse](https://idgeo.fr/offre-de-services) 

## 1. Ce qu'on installe, et pourquoi

Lizmap n'est pas un logiciel unique, mais un ensemble de briques complémentaires qui s'articulent les unes aux autres.

<img width="1536" height="1024" alt="Designer" src="https://github.com/user-attachments/assets/c5f3b2d7-0e3e-419c-8554-c0677f022f8b" />

**Répartition simple**

**Géomaticien :** étapes 1, 2, 3 et 6, puis contrôle fonctionnel de l’étape 5.

**DSI / prestataire :** installation et administration technique des étapes 4 et 5, sécurité, sauvegardes et disponibilité du serveur.

**Une fois l’installation terminée, le géomaticien devrait donc être autonome pour préparer, déposer, mettre à jour et tester les projets, sans intervenir dans la configuration HTTPS ou l’administration du serveur Linux.**

| Brique | Rôle |
|---|---|
| **QGIS Desktop + extension Lizmap** (poste du géomaticien) | On prépare la carte et on définit ce qui sera publié (couches, popups, impressions, filtres, graphiques). L'extension génère, à côté du projet QGIS (`.qgs` ou `.qgz`), un fichier de configuration `.qgs.cfg` / `.qgz.cfg` qui décrit la publication web. |
| **QGIS Server** | Lit le projet QGIS et produit les cartes via les protocoles OGC (WMS, WFS, WMTS) ainsi que les impressions PDF. C'est le moteur cartographique côté serveur. |
| **Extension Lizmap Server** | Plugin installé dans QGIS Server qui fournit à Lizmap les informations dont il a besoin (droits d'accès, configuration des dépôts, etc.). |
| **Lizmap Web Client** | Application web en PHP : c'est l'interface vue par les utilisateurs dans leur navigateur, avec l'administration, la gestion des comptes et des droits. |
| **Serveur web (Nginx ou Apache) + PHP‑FPM** | Sert l'application Lizmap et transmet les requêtes cartographiques à QGIS Server (via FastCGI). |
| **PostgreSQL / PostGIS** *(recommandé)* | Stocke les données géographiques. Lizmap peut aussi s'appuyer sur une base pour la gestion de ses propres comptes utilisateurs (à défaut, SQLite). |
| **Redis** *(optionnel)* | Gestion des sessions et mise en cache ; utile en cas de forte charge ou de plusieurs instances. |
| **HTTPS** | Certificat TLS et nom de domaine dédié. |

## 2. Les étapes, dans l'ordre

<img width="2800" height="1240" alt="etapes-deploiement" src="https://github.com/user-attachments/assets/c6006f58-d5c9-4a33-82bc-deedf9368ca5" />

### Étape 0 - Décisions préalables
**Durée estimée :** 1 à 2 jours de réflexion (réunion de cadrage)

À trancher avant de lancer le prestataire, car ces choix changent le prix et l'architecture :

- **Public visé** : agents uniquement (accès interne ou VPN), partenaires, grand public.
- **Hébergement** : serveur sur site (DSI), cloud, ou hébergement Lizmap par un prestataire (3Liz, l'éditeur de Lizmap, propose hébergement et support). Cette dernière option évite de mobiliser la DSI, mais les données transitent alors chez un tiers.
- **Mode d'installation** : classique (paquets système) ou conteneurisé (Docker).
- **Emplacement des données** : base PostGIS ou fichiers (GeoPackage, shapefiles).
- **Authentification** : comptes Lizmap internes, ou annuaire LDAP / Active Directory.
- **Répartition des responsabilités** après la mise en place *(voir section 4)*.

### Étape 1 - Préparation de l'infrastructure
**Responsable :** DSI · **Durée :** quelques jours, selon ses délais internes

- Création d'une VM Linux (Debian ou Ubuntu LTS). Dimensionnement de départ indicatif : **4 vCPU, 8 à 16 Go de RAM, 100 Go de disque**, à ajuster selon le volume de données et le nombre d'utilisateurs simultanés.
- Réservation d'un sous-domaine (ex. `carto.audc51.org`) et création de l'enregistrement DNS correspondant.
- Ouverture des flux réseau : port **443** en entrée (et **80** pour la redirection HTTP→HTTPS ou le renouvellement du certificat) ; accès sortant pour le téléchargement des paquets, ou configuration d'un proxy sortant.
- Accès temporaire pour le prestataire : SSH ou VPN, avec compte nominatif disposant de droits `sudo`.
- Si une instance PostGIS existe déjà : fournir adresse, port, nom de la base et un compte technique dédié.

### Étape 2 - Installation du socle serveur
**Responsable :** prestataire · **Durée :** environ 0,5 à 1 jour

- Mise à jour du système, configuration du pare-feu, installation de Nginx (ou Apache) et de PHP‑FPM avec les extensions requises.
- Installation de **QGIS Server** depuis les dépôts officiels QGIS, dans une version cohérente avec celle de QGIS Desktop — idéalement une version **LTR** (Long Term Release) pour la stabilité.
- Configuration du serveur web pour transmettre les requêtes cartographiques à QGIS Server (FastCGI).
- En cas de déploiement **Docker** : écriture ou adaptation d'un `docker-compose.yml` (Lizmap, QGIS Server, PostGIS, Redis) avec volumes persistants pour les projets et la configuration. Le dépôt Docker officiel sert de base, mais sa configuration d'exemple doit être durcie avant mise en production (mots de passe, exposition des ports, etc.).

### Étape 3 - Installation de Lizmap Web Client
**Responsable :** prestataire · **Durée :** environ 0,5 jour

- Téléchargement et déploiement de Lizmap Web Client, avec les droits appropriés sur les dossiers sensibles (`var/`, configuration, cache).
- Lancement du script d'installation, qui crée la configuration initiale et la base des comptes.
- Installation de l'**extension Lizmap Server** dans QGIS Server et déclaration de son chemin via la variable d'environnement dédiée aux plugins.
- Configuration de la connexion à la base des comptes (SQLite par défaut ; PostgreSQL recommandé en production).
- Contrôle de bon fonctionnement : la page d'accueil de Lizmap s'affiche, l'administration est accessible, QGIS Server répond correctement aux requêtes.

### Étape 4 - HTTPS et sécurisation
**Responsables :** prestataire et DSI · **Durée :** environ 0,5 jour

- Mise en place d'un certificat TLS (Let's Encrypt si le serveur est joignable depuis Internet, sinon certificat fourni par la DSI) et redirection automatique de HTTP vers HTTPS.
- Restriction d'accès à l'interface d'administration, changement des mots de passe par défaut, suppression des comptes et accès de test.
- Selon le contexte : reverse proxy géré par la DSI, filtrage par adresse IP, VPN pour les contenus à usage interne.
- **Isolation de QGIS Server** : il ne doit jamais être exposé directement sur Internet, uniquement via Lizmap et le serveur web.

### Étape 5 - Connexion aux données
**Responsables :** prestataire et géomaticien · **Durée :** environ 0,5 à 1 jour
*Étape souvent sous-estimée : c'est elle qui détermine si les projets publiés fonctionnent réellement.*

- **PostGIS** : le serveur Lizmap doit pouvoir joindre la base. La bonne pratique est d'utiliser un fichier de service PostgreSQL (`pg_service.conf`) présent à l'identique sur le serveur et sur le poste du géomaticien. Le projet QGIS ne contient alors ni adresse IP ni mot de passe en dur.
- **Fichiers** (GeoPackage, rasters, etc.) : ils doivent être déposés sur le serveur aux côtés du projet, ou sur un partage réseau monté sur le serveur. Les chemins Windows (`P:\...`) ne fonctionnent pas côté serveur Linux : il est indispensable d'utiliser des chemins relatifs au projet.
- Création d'un compte technique dédié (ex. `svc_lizmap`) avec des droits minimaux : lecture seule, et écriture uniquement si l'édition en ligne est prévue.

### Étape 6 - Configuration de Lizmap
**Responsables :** prestataire, puis géomaticien · **Durée :** environ 0,5 jour

Dans l'interface d'administration :

- **Répertoires de projets** : déclaration des « dépôts » (ex. *interne*, *partenaires*, *public*), chacun pointant vers un dossier du serveur.
- **Groupes et utilisateurs** : création des groupes (administrateurs, géomaticiens, agents, partenaires) et des comptes associés ; liaison LDAP/AD si cette option a été retenue.
- **Droits par dépôt** : qui voit quoi (affichage, impression, édition, administration).
- **Options générales** : titre, logo, thème graphique, adresse d'envoi des e-mails, langue, gestion du cache des tuiles.
- **Droits au niveau du projet** : certains réglages fins se définissent directement dans l'extension QGIS (filtres par groupe d'utilisateurs, accès restreint à certaines couches).

### Étape 7 - Projet pilote et recette
**Responsables :** géomaticien et prestataire · **Durée :** 1 à 2 jours

- Préparation d'un projet QGIS de test avec infobulles, table attributaire, mise en page d'impression, filtres et, si possible, un graphique.
- Le prestataire fait la démonstration du déroulé complet de publication *(voir section 3)*.
- Tests fonctionnels : affichage, temps de réponse, impression PDF, contrôle d'accès par groupe, consultation sur mobile, comportement avec plusieurs utilisateurs simultanés.
- Corrections éventuelles : versions d'extensions, droits sur les dossiers, polices ou symboles manquants côté serveur, etc.

### Étape 8 - Passage en exploitation
**Responsables :** DSI et prestataire · **Durée :** environ 0,5 à 1 jour

- **Sauvegardes** : projets et fichiers `.cfg`, configuration Lizmap, base des comptes, base PostGIS — avec un test de restauration effectif, pas seulement la vérification que la sauvegarde s'exécute.
- **Supervision** : espace disque, disponibilité des services (serveur web, PHP, QGIS Server), échéance du certificat TLS.
- **Journaux** : emplacement, politique de rotation, durée de conservation.
- **Procédure de mise à jour** (Lizmap, QGIS Server, extension Lizmap Server, système d'exploitation) et règle de compatibilité des versions avec QGIS Desktop.
- **Documentation** : schéma d'architecture, emplacement des fichiers, comptes techniques (conservés dans un coffre-fort à mots de passe), procédures d'exploitation courantes.

### Étape 9 - Formation et mise en production
**Durée :** 0,5 à 1 jour

- Transfert de compétences vers les équipes internes : administration, publication de projets, dépannage courant.
- Ouverture progressive des accès : d'abord en interne, puis aux partenaires, puis au grand public si cela est prévu.
- Prévoir, au contrat, une période d'assistance après la mise en ligne (par exemple 1 à 3 mois).

### Ordre de grandeur global

> Pour un prestataire expérimenté : **entre 4 et 8 jours de prestation** au total, auxquels s'ajoutent les délais propres à la DSI (provisionnement de la VM, DNS, certificat, ouverture de ports), qui sont souvent le facteur qui allonge le plus le calendrier réel. Ces chiffres restent indicatifs : un devis détaillé demeure nécessaire.

## 3. La mise en ligne d'un projet QGIS

Déroulé que le géomaticien appliquera au quotidien, une fois la plateforme en place :

<img width="2400" height="1000" alt="publication-projet" src="https://github.com/user-attachments/assets/d921a111-8e1c-4892-abb4-a7af8038192e" />

1. **Préparation dans QGIS** : les données proviennent de PostGIS via le fichier de service partagé, ou de fichiers référencés en chemins relatifs.
2. **Configuration avec l'extension Lizmap** : couches, popups, outils, mise en page d'impression, filtres. L'enregistrement produit les fichiers `monprojet.qgz` et `monprojet.qgz.cfg`.
3. **Transfert** des deux fichiers (ainsi que des ressources associées : images, fichiers de données) dans le dossier du dépôt visé, via partage réseau, SFTP, ou l'extension de transfert intégrée à Lizmap.
4. **Détection automatique par Lizmap** : le projet apparaît sur la page d'accueil du dépôt correspondant, avec les droits qui lui sont appliqués.
5. **Test dans le navigateur**, avec un compte représentatif de chaque profil d'utilisateur concerné.
6. **Mise à jour** : il suffit de remplacer les fichiers. Si les données résident dans PostGIS, elles sont à jour en temps réel, sans republication nécessaire. Penser à vider le cache des tuiles si celui-ci est activé.

## 4. Répartition des responsabilités à valider

| Sujet | DSI | Prestataire | Géomaticien |
|---|---|---|---|
| Serveur, réseau, HTTPS | ✔ | Conseil | — |
| Installation initiale | Accès | ✔ | Recette |
| Sécurité, mises à jour système | ✔ | — | — |
| Mises à jour Lizmap / QGIS Server | À décider | À décider *(contrat de maintenance)* | — |
| Comptes, groupes, droits | — | Paramétrage initial | ✔ au quotidien |
| Projets, styles, publication | — | — | ✔ |
| Sauvegardes | ✔ | Mise en place | Contrôle |

*Ce tableau est une base de discussion à valider formellement entre les parties, idéalement annexée au contrat de prestation ou de maintenance.*

## 5. Points de vigilance

- **Compatibilité des versions** entre QGIS Desktop, QGIS Server et l'extension Lizmap : c'est la première cause de problèmes rencontrés en production. Il est recommandé de définir une règle de mise à jour commune et synchronisée entre postes clients et serveur.
- **Chemins et polices** : un projet qui fonctionne correctement sur le poste du géomaticien peut s'afficher différemment sur le serveur (chemins Windows non valides côté Linux, polices ou symboles non installés sur le serveur).
- **Données sensibles** : tout ce qui est publié reste interrogeable techniquement via les services OGC (WMS/WFS), même si une couche est masquée dans l'interface. Les droits d'accès doivent être configurés au niveau du service, et non se limiter à un masquage visuel.
- **Dépendance au prestataire** : exiger une documentation complète et un réel transfert de compétences afin de conserver une autonomie opérationnelle.
- **Coût récurrent** : au-delà du coût d'installation initial, prévoir le budget de maintenance, des mises à jour régulières et, le cas échéant, de l'hébergement.

## 6. "Bénéfices pour l'AUDC"

- centralisation des projets cartographiques ;
- diffusion sécurisée en interne et auprès des partenaires ;
- réduction des exports manuels PDF ;
- mise à jour des données en temps réel via PostGIS ;
- valorisation du travail géomatique ;
- autonomie interne après transfert de compétences.

## 7. Compte rendu de la réunion avec IDGEO – Lizmap

**Réponses du prestataire, points à valider avec la DSI et suites à donner.**

### Réponses du prestataire (IDGEO)

#### Contexte

- Avec ESRI, nous sommes dépendants : les coûts augmentent chaque année et les données sont sur un serveur externe.
- Nous voulons être indépendants et garder nos données sur notre propre serveur.

#### Infrastructure et coûts

- Installation de l'infrastructure : 5 000 à 10 000 € (ou 7 000 à 8 000 €).
- Maintenance : 2 à 3 jours par an.
- Une base de données propre à l'agence est vraiment idéale.
- Un serveur mail permet aux utilisateurs de s'inscrire.

#### Fonctionnement de Lizmap

- Lizmap fonctionne actuellement avec la version 3.44, appelée à évoluer.
- Au démarrage, les couches QGIS peuvent être créées à la volée par SQL.

#### Accompagnement

- IDGEO propose la maintenance, l'accompagnement et un support.
- Un accompagnement est possible en attendant la montée en compétence en interne (Abdou, par exemple).
- Pour estimer le coût avec une bonne fourchette, il nous faut un cahier des charges.

#### Alternative : offre d'hébergement standard de 3liz

- Offre consultable sur https://www.lizmap.com/offres.html
- Environ 200 € HT [préciser : par mois ou par an] : elle semble répondre à nos besoins, et Thomas (IDGEO) nous la conseille.
- Les données transitent chez eux, mais 3liz garantit la sécurité.

### Points à valider avec la DSI de Châlons Agglo

- Le serveur de l'agence est mis à disposition par la DSI. Aurons-nous la main dessus (accès administrateur) ? Quelles restrictions ?
- Notre serveur actuel ne sert qu'au stockage de fichiers : il n'est donc pas suffisant. Peut-on obtenir une autre machine ?
- Option : prendre un serveur dédié à l'agence via la DSI, pour environ 30 €/mois.
- Si cela se complique avec la DSI : installation et hébergement via 3liz (qui héberge aussi), avec maintenance par IDGEO.

#### Suites à donner

- Rédiger un cahier des charges pour obtenir un chiffrage fiable auprès d'IDGEO.
- Interroger la DSI sur les droits d'administration, la mise à disposition d'une machine et le serveur dédié à 30 €/mois.
- Étudier l'offre 3liz : serons-nous autonomes avec cette offre ? Quelles seront les restrictions ?
- Comparer les scénarios (serveur DSI, serveur dédié, hébergement 3liz) sur le coût, l'autonomie et la sécurité.
- Présenter le projet au directeur une fois ces éléments rassemblés.

#### Points à préciser avant diffusion

- Période des 200 € HT de l'offre 3liz (mensuelle ou annuelle).
- Fourchette exacte du coût d'installation de l'infrastructure.

