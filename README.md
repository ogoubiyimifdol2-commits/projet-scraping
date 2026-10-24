# Devoir de Scraping Web - L2 Génie Logiciel

Projet Python d'extraction de données respectueuse et structurée sur **Amazon (amazon.fr)** ciblant automatiquement les objets électroniques (**Téléphones**, **MacBook**, **AirPods**) en architecture **Modèle-Vue-Contrôleur (MVC)**.

---

## 1. Présentation du projet

L'objectif de ce devoir de niveau **Licence 2 (L2) Génie Logiciel** est de développer un programme en **Programmation Orientée Objet (POO)** capable de :
1. Scraper automatiquement les produits électroniques sur Amazon (**Téléphones**, **MacBook**, **AirPods**) avec **Selenium** et **BeautifulSoup** ;
2. Télécharger les visuels des produits en local dans `data/images/` avec **requests** ;
3. Sauvegarder les données dans une base **SQLite** (`data/produits.db`) en gérant l'unicité des fiches ;
4. Exporter les résultats dans un fichier **CSV** (`exports/produits.csv`) au format UTF-8 avec BOM et séparateur `;` ;
5. Calculer et afficher dans la console **trois statistiques clés** :
   - La **moyenne des prix** (globale et par catégorie en €) ;
   - Le **prix maximum** (avec le nom et la catégorie du produit le plus cher) ;
   - Le **nombre de produits par catégorie** (et le total global).

---

## 2. Choix du site cible et respect des règles

### Site cible
- **Plateforme** : Amazon France
- **URL de base** : `https://www.amazon.fr`
- **Catégories électroniques traitées** :
  - **Téléphones** : `/s?k=smartphone`
  - **MacBook** : `/s?k=macbook`
  - **AirPods** : `/s?k=airpods`

### Pourquoi ce site ?
- Amazon est la référence majeure du commerce électronique, offrant un catalogue riche et représentatif pour l'analyse de données (prix en euros, notes clients, volumes d'avis et visuels produits).
- Le projet démontre la capacité à extraire des données réelles complexes tout en adaptant les sélecteurs aux structures dynamiques d'un grand site marchand.

### Résumé du `robots.txt` et éthique du scraping
- **robots.txt** (`https://www.amazon.fr/robots.txt`) :
  - Amazon applique des restrictions strictes sur l'automatisation pour préserver ses serveurs.
  - Dans le cadre de ce devoir académique, les mesures suivantes sont rigoureusement appliquées :
- **Mesures d'éthique et de robustesse** :
  - **User-Agent réaliste** : Transmission d'en-têtes de navigateur récents pour éviter les rejets intempestifs.
  - **Temporisation respectueuse** (`PAUSE_SECONDES = 2.0`) : Délai obligatoire entre chaque requête pour éviter toute surcharge de trafic.
  - **Volume limité** (`PAGES_MAX = 3`) : Bornage strict du nombre de pages par catégorie pour limiter l'empreinte réseau.
  - **Anti-détection et gestion CAPTCHA** : Configuration Chrome masquant les indicateurs d'automatisation (`navigator.webdriver`) et gestion prévenante en cas d'affichage d'un test anti-robot.

---

## 3. Architecture du projet (MVC)

Le code est structuré selon le patron **Modèle-Vue-Contrôleur** pour séparer les responsabilités :

```text
projet_scraping/
│
├── config.py                # Constantes (URLs, limites, User-Agent, chemins)
├── main.py                  # Point d'entrée de l'application
├── requirements.txt         # Dépendances Python installées
├── README.md                # Documentation complète du projet
│
├── models/                  # Modèles de données (M)
│   ├── __init__.py
│   ├── produit.py           # Classe Produit (validation du prix, vers_dict)
│   └── depot.py             # Classe Depot (persistance SQLite, gestion des doublons)
│
├── scraper/                 # Couche d'acquisition et parsing
│   ├── __init__.py
│   ├── driver.py            # Driver Chrome Selenium (anti-détection, User-Agent, context manager)
│   ├── parsing.py           # Parsing BeautifulSoup (convertir_prix, extraire_produits)
│   ├── site_scraper.py      # Classe ScraperSite (navigation, cookies, gestion CAPTCHA)
│   ├── fallback_data.py     # Catalogue Amazon intégré de secours anti-blocage
│   └── images.py            # Téléchargement des photos dans data/images/
│
├── views/                   # Présentation et sorties (V)
│   ├── __init__.py
│   ├── vue_console.py       # Affichage console et calcul des 3 statistiques
│   └── export_csv.py        # Classe ExportCsv (UTF-8-SIG, séparateur ;)
│
├── controllers/             # Orchestration (C)
│   ├── __init__.py
│   └── controleur.py        # Coordonne scraping, images, BDD, export et statistiques
│
├── tests/                   # Tests unitaires
│   ├── __init__.py
│   └── test_parsing.py      # Tests unitaires pour convertir_prix et parsing HTML
│
├── data/                    # Données locales persistées
│   ├── produits.db          # Base SQLite locale
│   └── images/              # Photos téléchargées des produits
│
└── exports/                 # Fichiers exportés
    └── produits.csv         # Export CSV complet
```

---

## 4. Installation et prérequis

### Prérequis
- Python 3.10 ou supérieur
- Google Chrome installé sur la machine
- Environnement virtuel Python activé

### Installation des dépendances
Dans un terminal PowerShell avec l'environnement virtuel activé :

```powershell
pip install -r requirements.txt
```

---

## 5. Utilisation

### Lancer le scraping automatique
Exécutez simplement le point d'entrée principal [main.py](file:///c:/Users/ogoub/Documents/projet_scraping/main.py) :

```powershell
python main.py
```

Le programme s'exécute automatiquement sans nécessiter d'intervention manuelle :
1. Démarre Chrome (avec fenêtre visible configurée dans `config.py` pour éviter le blocage anti-robot d'Amazon).
2. Valide automatiquement les cookies Amazon et parcourt les 3 catégories électroniques (**Téléphones**, **MacBook**, **AirPods**) jusqu'à 3 pages chacune.
3. Télécharge les visuels des produits correspondants dans `data/images/`.
4. Enregistre tous les produits dans la base SQLite `data/produits.db` (en éliminant les doublons).
5. Exporte l'ensemble des données consolidées dans `exports/produits.csv`.
6. Affiche un aperçu des produits et le rapport statistique complet dans la console.

### Lancer les tests unitaires
Pour exécuter la suite de tests unitaires (parsing des prix Amazon, structure HTML et catalogue de secours) :

```powershell
python -m unittest discover -s tests -v
```

---

## 6. Statistiques fournies par l'application

À la fin de l'exécution, le contrôleur génère un rapport statistique complet :
1. **Répartition par catégorie** : Nombre de produits pour chaque catégorie ainsi que le total global.
2. **Moyenne des prix** : Prix moyen par catégorie et moyenne globale sur l'ensemble du catalogue extrait.
3. **Prix maximum** : Le produit le plus cher du catalogue avec son nom, son prix exact et sa catégorie, ainsi que le record par catégorie.
