"""Contrôleur principal de l'application (Contrôleur MVC).

Ce module coordonne l'ensemble des composants du projet :
le scraper Selenium, le téléchargement des images, la persistance SQLite,
l'export CSV et l'affichage des statistiques en console.
"""

from typing import List

from config import (
    CATEGORIES,
    CHEMIN_BDD,
    CHEMIN_CSV,
    DOSSIER_IMAGES,
    PAGES_MAX,
    PAUSE_SECONDES,
    SANS_FENETRE,
)
from models.depot import Depot
from models.produit import Produit
from scraper.driver import DriverSelenium
from scraper.images import TelechargeurImages
from scraper.site_scraper import ScraperSite
from views.export_csv import ExportCsv
from views.vue_console import VueConsole


class ControleurPrincipal:
    """Orchestrateur du flux de données MVC."""

    def __init__(self):
        """Initialise les composants du modèle, des vues et des services."""
        self.depot = Depot(chemin_bdd=CHEMIN_BDD)
        self.vue = VueConsole()
        self.exporteur_csv = ExportCsv(chemin_fichier=CHEMIN_CSV)
        self.telechargeur_images = TelechargeurImages(
            dossier_destination=DOSSIER_IMAGES,
            pause=0.3,
        )

    def executer(self, telecharger_images: bool = True) -> None:
        """Exécute la chaîne complète du traitement de manière automatique."""
        self.vue.afficher_banniere()
        self.vue.afficher_message(
            f"Catégories cibles ({len(CATEGORIES)}) : {', '.join(CATEGORIES.keys())}"
        )
        self.vue.afficher_message(
            f"Paramètres : max {PAGES_MAX} pages/catégorie, pause {PAUSE_SECONDES}s."
        )

        # 1. Étape Scraping avec Selenium
        mode_txt = "arrière-plan (headless)" if SANS_FENETRE else "fenêtre visible (anti-détection Amazon)"
        self.vue.afficher_message(f"Démarrage du navigateur Chrome ({mode_txt})...")
        produits_scrapes: List[Produit] = []

        with DriverSelenium(sans_fenetre=SANS_FENETRE) as driver:
            scraper = ScraperSite(
                driver=driver,
                pause=PAUSE_SECONDES,
                pages_max=PAGES_MAX,
            )
            produits_scrapes = scraper.scraper_tout(CATEGORIES)

        self.vue.afficher_message(
            f"Scraping terminé : {len(produits_scrapes)} produits extraits du web."
        )

        if not produits_scrapes:
            self.vue.afficher_erreur("Aucun produit n'a pu être extrait. Fin du programme.")
            return

        # 2. Étape Téléchargement des images
        if telecharger_images:
            self.vue.afficher_message("Téléchargement des images dans data/images/...")
            self.telechargeur_images.telecharger_images_produits(produits_scrapes)

        # 3. Étape Persistance dans SQLite
        self.vue.afficher_message("Enregistrement des données dans la base SQLite...")
        nouveaux_insérés = self.depot.ajouter_plusieurs(produits_scrapes)
        total_en_base = self.depot.compter()
        self.vue.afficher_message(
            f"Base de données : {nouveaux_insérés} nouveau(x) produit(s) inséré(s) "
            f"({total_en_base} total en base)."
        )

        # Récupération de tous les produits consolidés depuis la base
        tous_les_produits = self.depot.lister()

        # 4. Étape Export CSV
        self.vue.afficher_message(f"Exportation du fichier CSV vers '{CHEMIN_CSV}'...")
        chemin_genere = self.exporteur_csv.exporter(tous_les_produits)
        self.vue.afficher_message(f"Fichier CSV prêt : {chemin_genere}")

        # 5. Étape Affichage et Statistiques
        self.vue.afficher_apercu_produits(tous_les_produits, limite=5)
        self.vue.afficher_statistiques(tous_les_produits)

        self.vue.afficher_message("Traitement terminé avec succès !")
        print(f"-> Base SQLite : {CHEMIN_BDD}")
        print(f"-> Fichier CSV : {CHEMIN_CSV}")
        print(f"-> Dossier Images : {DOSSIER_IMAGES}")
