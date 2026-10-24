"""Gestionnaire du navigateur Selenium Chrome.

Ce module encapsule la création et la fermeture propre du WebDriver Selenium,
avec support du mode sans tête (headless), configuration d'un User-Agent éthique
et utilisation via le gestionnaire de contexte Python ('with').
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import SANS_FENETRE, USER_AGENT


class DriverSelenium:
    """Gestionnaire de contexte pour le driver Chrome Selenium."""

    def __init__(self, sans_fenetre: bool = SANS_FENETRE):
        """Configure les options du navigateur Chrome.

        :param sans_fenetre: Si True, exécute Chrome en arrière-plan (headless).
        """
        self.sans_fenetre = sans_fenetre
        self.driver: Optional[webdriver.Chrome] = None

    def démarrer(self) -> webdriver.Chrome:
        """Initialise et lance l'instance de Chrome avec les options configurées."""
        options = Options()

        if self.sans_fenetre:
            options.add_argument("--headless=new")
        else:
            options.add_argument("--start-maximized")

        # Configuration anti-détection et stabilité (adaptée à Amazon)
        options.add_argument(f"user-agent={USER_AGENT}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--lang=fr-FR,fr")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")  # Masque les messages verbeux

        self.driver = webdriver.Chrome(options=options)

        # Neutralise l'attribut navigator.webdriver souvent bloqué par Amazon
        try:
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": (
                        "Object.defineProperty(navigator, 'webdriver', {"
                        "get: () => undefined"
                        "})"
                    )
                },
            )
        except Exception:
            pass

        return self.driver

    def fermer(self) -> None:
        """Ferme proprement le navigateur s'il est actif."""
        if self.driver is not None:
            try:
                self.driver.quit()
            finally:
                self.driver = None

    def __enter__(self) -> webdriver.Chrome:
        """Permet l'utilisation dans un bloc 'with' : with DriverSelenium() as driver:"""
        return self.démarrer()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Garantit la fermeture du navigateur à la sortie du bloc 'with'."""
        self.fermer()
