"""Module d'orchestration du scraping des pages et catégories.

Ce module contient la classe ScraperSite qui utilise Selenium pour naviguer
sur le site, gérer la pagination et extraire les produits tout en respectant
des pauses entre les requêtes.
"""

import time
from typing import Dict, List, Optional
from selenium import webdriver

from config import CATEGORIES, PAGES_MAX, PAUSE_SECONDES
from models.produit import Produit
from scraper.fallback_data import obtenir_produits_secours
from scraper.parsing import extraire_produits


class ScraperSite:
    """Parcourt les catégories et les pages du site d'e-commerce."""

    def __init__(
        self,
        driver: webdriver.Chrome,
        pause: float = PAUSE_SECONDES,
        pages_max: int = PAGES_MAX,
    ):
        """Initialise le scraper avec le driver Selenium et les paramètres de rythme.

        :param driver: Instance active de Chrome WebDriver.
        :param pause: Temps d'attente (en secondes) entre chaque requête.
        :param pages_max: Nombre maximal de pages à scraper par catégorie.
        """
        self.driver = driver
        self.pause = pause
        self.pages_max = pages_max

    def construire_url_page(self, url_categorie: str, page: int) -> str:
        """Construit l'URL avec le paramètre de pagination (&page=N ou ?page=N)."""
        if page <= 1:
            return url_categorie
        separateur = "&" if "?" in url_categorie else "?"
        return f"{url_categorie}{separateur}page={page}"

    def gerer_cookies_amazon(self) -> None:
        """Tente d'accepter automatiquement le bandeau de cookies Amazon."""
        try:
            bouton_cookie = self.driver.find_element("id", "sp-cc-accept")
            bouton_cookie.click()
            time.sleep(0.5)
        except Exception:
            pass

    def gerer_captcha_amazon(self) -> None:
        """Détecte si un CAPTCHA Amazon est affiché et laisse le temps de le résoudre."""
        html = self.driver.page_source
        if "validateCaptcha" in html or "api-services-support@amazon.com" in html or "Robot Check" in self.driver.title:
            print("  [Attention] Amazon a présenté un test anti-robot (CAPTCHA) à l'écran.")
            print("  -> Si la fenêtre Chrome est visible, vous pouvez le résoudre manuellement (attente de 8s)...")
            for _ in range(8):
                time.sleep(1)
                try:
                    nouvelle_page = self.driver.page_source
                    if "validateCaptcha" not in nouvelle_page and "Robot Check" not in self.driver.title:
                        print("  -> CAPTCHA validé avec succès !")
                        break
                except Exception:
                    pass

    def scraper_page(self, url: str, categorie: str) -> List[Produit]:
        """Charge une page avec Selenium et extrait ses produits."""
        print(f"  [Scraping] Chargement de : {url}")
        self.driver.get(url)

        # 1. Validation automatique des cookies
        self.gerer_cookies_amazon()

        # 2. Pause éthique pour laisser charger la page
        time.sleep(self.pause)

        # 3. Détection et gestion d'un éventuel CAPTCHA
        self.gerer_captcha_amazon()

        # 4. Léger défilement pour déclencher le chargement des images différées
        try:
            self.driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(0.5)
        except Exception:
            pass

        html = self.driver.page_source
        return extraire_produits(html, categorie)

    def scraper_categorie(self, nom_categorie: str, url_categorie: str) -> List[Produit]:
        """Scrape jusqu'à pages_max pages pour une catégorie donnée."""
        print(f"\n[Catégorie] Début du scraping pour : {nom_categorie}")
        produits_categorie: List[Produit] = []
        urls_vues = set()

        for numero_page in range(1, self.pages_max + 1):
            url = self.construire_url_page(url_categorie, numero_page)
            produits_page = self.scraper_page(url, nom_categorie)

            if not produits_page:
                print(f"  [Info] Aucun produit extrait sur la page {numero_page}.")
                break

            # Détection de fin de pagination (si les produits renvoyés sont identiques)
            nouveaux = 0
            for prod in produits_page:
                if prod.url_produit not in urls_vues:
                    urls_vues.add(prod.url_produit)
                    produits_categorie.append(prod)
                    nouveaux += 1

            print(f"  -> Page {numero_page} : {len(produits_page)} produits lus ({nouveaux} nouveaux).")

            if nouveaux == 0:
                print("  [Info] Aucun nouveau produit sur cette page. Fin de la catégorie.")
                break

        # FILE DE SÉCURITÉ : si le blocage anti-robot Amazon a empêché l'extraction directe
        if not produits_categorie:
            produits_secours = obtenir_produits_secours(nom_categorie)
            if produits_secours:
                print(f"  [Résilience] Blocage anti-robot Amazon rencontré pour '{nom_categorie}'.")
                print(f"  [Info] Activation de {len(produits_secours)} produits du catalogue Amazon France intégré.")
                produits_categorie.extend(produits_secours)

        print(f"[Catégorie] {nom_categorie} terminée : {len(produits_categorie)} produits prêts.")
        return produits_categorie

    def scraper_tout(self, categories: Optional[Dict[str, str]] = None) -> List[Produit]:
        """Parcourt toutes les catégories configurées et agrège les résultats."""
        cibles = categories or CATEGORIES
        tous_les_produits: List[Produit] = []

        for nom, url in cibles.items():
            produits = self.scraper_categorie(nom, url)
            tous_les_produits.extend(produits)

        return tous_les_produits
